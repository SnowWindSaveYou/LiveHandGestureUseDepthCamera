import numpy as np
import cv2
from . import math
from .colorMap import FINGER_COLORS_MP

from .commonSetting import *

def drawAngle(image,landmark, feangleList,AbductionAdductionAngleList=None):
    for i in range(5):
        for j in range(3):
            pos = landmark[FINGERS[i][j+1]]
            cv2.putText(image,str(np.round(feangleList[i][j],2)),np.int32(pos[:2]),0,0.3,(255,255,255),1)
    if AbductionAdductionAngleList is not None:
        cv2.putText(image,str(np.round(AbductionAdductionAngleList[0],2)),np.int32(landmark[1][:2]+(0,-20)),0,0.3,(255,0,0),1)
        cv2.putText(image,str(np.round(AbductionAdductionAngleList[1],2)),np.int32(landmark[5][:2]+(0,-20)),0,0.3,(255,0,0),1)
        cv2.putText(image,str(np.round(AbductionAdductionAngleList[2],2)),np.int32(landmark[9][:2]+(0,-20)),0,0.3,(255,0,0),1)
        cv2.putText(image,str(np.round(AbductionAdductionAngleList[3],2)),np.int32(landmark[13][:2]+(0,-20)),0,0.3,(255,0,0),1)
        cv2.putText(image,str(np.round(AbductionAdductionAngleList[4],2)),np.int32(landmark[2][:2]+(0,-20)),0,0.3,(255,0,0),1)
    return image

def drawResult(landmark,image=None,colorMap=FINGER_COLORS_MP,zType=0,showLabel=False):
    if image is None:
        image = np.zeros((int(landmark[:,1].max()),int(landmark[:,0].max()),3), np.uint8)
    i = 0
    for p in landmark:
        p = p.tolist()
        x = int(p[0]) 
        y = int(p[1])
        color = colorMap[i]
        z = 2
        if zType == 1:
            if p[2]<200:
                z = 5
            elif p[2]<300:
                z = 4
            elif p[2]<500:
                z = 3
            elif p[2]<700:
                z = 2
            else:
                z = 1  
        if showLabel:
            cv2.putText(image,str(np.round(p,2)),(x,y+10),0,0.3,(255,255,255),1)
        cv2.circle(image,(x,y),1,color,z)
        i+=1
    return image

def drawTexts(textlist,image):
    i = 0
    for t in textlist:
        cv2.putText(image,t,(5,10+i*20),0,0.3,(255,255,255),1)
        i+=1
    return image

def matToImg(mat):
    blank_image = np.zeros((mat.shape[0],mat.shape[1],3), np.uint8)
    mat_ = math.normalization(mat.copy())*255
    blank_image[:,:,0] = mat_
    blank_image[:,:,1] = mat_
    blank_image[:,:,2] = mat_
    return blank_image

def drawCoord(img,origin, coord,scale=10):
    coordEx = coord*scale
    cv2.line(img,origin,coordEx[0]+origin,(255,0,0),2)
    cv2.line(img,origin,coordEx[1]+origin,(0,255,0),2)
    cv2.line(img,origin,coordEx[2]+origin,(0,0,255),2)
    return img

