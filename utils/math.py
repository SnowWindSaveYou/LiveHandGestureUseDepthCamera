import numpy as np

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

def get3DAngle(a,b):
    return (np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))