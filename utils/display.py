import numpy as np
import cv2
from . import math
from .colorMap import FINGER_COLORS_MP


def drawResult(landmark,image=None,colorMap=FINGER_COLORS_MP):
    if image is None:
        image = np.zeros((int(landmark[:,1].max()),int(landmark[:,0].max()),3), np.uint8)
    i = 0
    for p in landmark:
        p = p.tolist()
        x = int(p[0]) 
        y = int(p[1])
        color = colorMap[i]
        cv2.circle(image,(x,y),1,color,2)
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

