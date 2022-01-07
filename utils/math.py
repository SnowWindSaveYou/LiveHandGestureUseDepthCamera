import numpy as np
from .commonSetting import *

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

def scaleImg(img,meam,std):
    return (img - meam) / std

def applyTrans(vecs,mat):
    # 转为齐次坐标
    shape = vecs.shape 
    a = np.eye(shape[1]+1,shape[0]+1)
    a[:-1,:-1] = vecs.T
    a[-1]=1
    return np.matmul(mat, a).T[:-1,:-1] 

def getCoord(a,b,c):
    ab = b-a
    ac = c-a
    yd = np.cross(ab,ac)
    y = yd/np.linalg.norm(yd)
    x = ab/np.linalg.norm(ab)
    zd = np.cross(x,y)
    z = zd/np.linalg.norm(zd)
    return np.array([x,y,z])

def linear_regression(x,y):
    N = len(x)
    sumx = sum(x)
    sumy = sum(y)
    sumx2 = sum(x**2)
    sumxy = sum(x*y)
    A = np.mat([[N,sumx],[sumx,sumx2]])
    b = np.array([sumy,sumxy])
    bias,grad = np.linalg.solve(A,b)
    return grad, bias


def get3DCosAngle(a,b):
    return np.arccos((np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))))

def get3DAngleDeg(a:np.ndarray,b:np.ndarray,axis:np.ndarray=None):
    angle = np.rad2deg(get3DCosAngle(a,b))
    if axis is not None:
        axb = np.cross(a,b)
        axb /= np.linalg.norm(axb)
        dirc = np.dot(axis,axb)
        if dirc<0:
            angle = -angle
    return float(angle)

def get3DAngleDegByPlane(vec:np.ndarray,pa:np.ndarray,pb:np.ndarray):
    pab = np.cross(pa,pb) 
    angle = 90-np.rad2deg(get3DCosAngle(vec,pab))
    if np.dot(vec,pab)<0:
        angle = -angle
    return angle
def getFlexionExtensionAngleList(landmark):
    angle_list = [None]*5
    thumbAxis =  landmark[1]-landmark[5] 
    thumbAxis/= np.linalg.norm(thumbAxis)
    thumb = FINGERS[0]
    vecList = landmark[thumb[1:]]-landmark[thumb[:4]]
    thumbCMC =  get3DAngleDegByPlane(vecList[1],landmark[5]-landmark[0],vecList[0]) 
    thumbMCP = get3DAngleDeg(vecList[1],vecList[2],thumbAxis)
    thumbIP = get3DAngleDeg(vecList[2],vecList[3],thumbAxis)
    angle_list[0] =[thumbCMC,thumbMCP,thumbIP]
    
    handAxis =  landmark[5]-landmark[17]
    handAxis/= np.linalg.norm(handAxis)
    for i in range(1,5):
        finger = FINGERS[i]
        vecList = landmark[finger[1:]]-landmark[finger[:4]]
        for v in range(3):
            vecList[v]/= np.linalg.norm(vecList[v])
        angleMCP = get3DAngleDeg(vecList[0],vecList[1],handAxis)
        anglePIP = get3DAngleDeg(vecList[1],vecList[2],handAxis)
        angleDIP = get3DAngleDeg(vecList[2],vecList[3],handAxis)
        angle_list[i] = [angleMCP,anglePIP,angleDIP]
    return angle_list

def getAbductionAdductionAngleList(landmark):
    angle_list = [None]*5
    axis = np.cross(landmark[5]-landmark[0],landmark[17]-landmark[0])
    axis/= np.linalg.norm(axis)
    for i in range(4):
        finger1 = FINGERS[i]
        finger2 = FINGERS[i+1]
        vec1 = landmark[finger1[1]]-landmark[0]
        vec2 = landmark[finger2[1]]-landmark[0]
        angle_list[i] = get3DAngleDeg(vec1,vec2,axis)
    
    v1 = landmark[2]-landmark[1]
    v2 = landmark[5]-landmark[1]
    axis = np.cross(v1,v2)
    angle_list[4] = get3DAngleDeg(v1,v2,axis)
    
    return angle_list