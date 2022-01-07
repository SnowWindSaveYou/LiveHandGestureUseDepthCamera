import numpy as np
import cv2
from scipy import stats, ndimage


class HandDetector(object):
    
    def __init__(self, img, fx, fy,ux,uy, maxDepth = 1500, minDepth = 10):
        self.img = img.copy()
        self.max_depth = min(maxDepth, img.max())
        self.min_depth = max(minDepth, img.min())
        self.img[self.img > self.max_depth] = 0.
        self.img[self.img < self.min_depth] = 0.
        self.fx = fx
        self.fy = fy
        self.ux = ux
        self.uy = uy

    def calculateCoM(self,depthRange=150):
        # 假设最近的最大物体为手
        dc = self.img.copy()
        nozero = dc[dc>0]
        num = len(nozero)
        if num>0:
            shift = nozero.min()-1
            dc[dc>0] -= shift
            dc[dc>depthRange] =0  
            binary = np.array(dc,dtype=np.int8)
            binary[binary>0] =1
            _, labels, stats, centers = cv2.connectedComponentsWithStats(binary)
            maxRegion = 1
            for i in range(1,len(stats)): #跳过背景
                if stats[i][4]>stats[maxRegion][4]:
                    maxRegion = i
            dc = self.img[labels==maxRegion]
            cc = centers[maxRegion]
            num = np.count_nonzero(dc)
            com = np.array((cc[0]*num, cc[1]*num, dc.sum()), np.float32)
            # cc = ndimage.measurements.center_of_mass(dc > 0)
            # dc[dc>0]+= shift
            # com = np.array((cc[1]*num, cc[0]*num, dc.sum()), np.float32)
            return com/num
        return np.array((0, 0, 0), np.float32)
        
    def comToBounds(self,com,xy_thres = 100,restrict=False):
        center_world = self.pixel2world(com.copy())
        topRight_world =       [center_world[0]-xy_thres, center_world[1]+xy_thres,center_world[2]]
        bottomLeft_world =   [center_world[0]+xy_thres, center_world[1]-xy_thres,center_world[2]]
        topRight_pixel = self.world2pixel(topRight_world)
        bottomLeft_pixel = self.world2pixel(bottomLeft_world)
        if restrict:
            topRight_pixel[0] = max(topRight_pixel[0], 0)
            topRight_pixel[1] = min(topRight_pixel[1], self.img.shape[0] - 1)
            bottomLeft_pixel[1] = max(bottomLeft_pixel[1], 0)  
            bottomLeft_pixel[0] = min(bottomLeft_pixel[0], self.img.shape[1] - 1)
        return topRight_pixel, bottomLeft_pixel
    
    def crop2d(self, topRight, bottomLeft):
        new_Xmin = max(topRight[0], 0)
        new_Ymin = max(bottomLeft[1], 0)  
        new_Xmax = min(bottomLeft[0], self.img.shape[1] - 1)
        new_Ymax = min(topRight[1], self.img.shape[0] - 1)
        imCrop = self.img.copy()[int(new_Ymin):int(new_Ymax), int(new_Xmin):int(new_Xmax)]
        return imCrop
    
    def crop3d(self, com, topRight, bottomLeft, depth_thres=150):
        # 返回以com为中心的区域
        imCrop = self.crop2d(topRight, bottomLeft)
        imCrop[np.where(imCrop >= com[2] + depth_thres)] = com[2] 
        imCrop[np.where(imCrop <= com[2] - depth_thres)] = com[2] 
        imCrop = (imCrop - com[2])
        return imCrop
        
    def detect(self, com=None, worldBoxSize=300, depthSize=300, img_size=(176, 176)):
        if com is None:
            com = self.calculateCoM()
        if np.count_nonzero(com)==0:
            return None, com, None
            
        topRight_pixel, bottomLeft_pixel = self.comToBounds(com,worldBoxSize/2,True)
        imCrop = self.crop3d(com,  topRight_pixel, bottomLeft_pixel, depthSize/2)
        
        imgResize = cv2.resize(imCrop, img_size, interpolation=cv2.INTER_NEAREST)
        crop2imgmat = self.getTransMat(com,topRight_pixel, bottomLeft_pixel ,img_size)
        return np.asarray(imgResize,dtype = 'float32') ,com, crop2imgmat

    def pixel2world(self,x):
        x[ 0] = (x[ 0] - self.ux) * x[ 2] / self.fx
        x[ 1] = (x[ 1] - self.uy) * x[ 2] / self.fy
        return x
    def world2pixel(self,x):
        x[0] = x[0] * self.fx / x[ 2] + self.ux
        x[1] = x[1] * self.fy / x[2] + self.uy
        return x
            
    def getTransMat(self,com, topRight, bottomLeft, imgSize=(176,176)):
        height_crop = bottomLeft[0]- topRight[0]
        width_crop =  topRight[1]-bottomLeft[1]
        
        # 位移变换
        trans = np.array([
            [1,0,0,bottomLeft[1]],
            [0,1,0,topRight[0]],
            [0,0,1,com[2]],
            [0,0,0,1],
        ])
        # 缩放变换
        scale = np.array([
            [height_crop/imgSize[0],0,0,0],
            [0,width_crop/imgSize[1],0,0],
            [0,0,1,0],
            [0,0,0,1],
        ])
        mat = np.matmul(trans,scale)
        return mat