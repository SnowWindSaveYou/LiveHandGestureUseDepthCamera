import numpy as np
import cv2

class HandKalmanFilter:
    def __init__(self):
        # 平滑手运动
        self.kalman = cv2.KalmanFilter(126,63,0,cv2.CV_64F) #int dynam_params, int measure_params, int control_params=0 
        self.kalman.measurementMatrix = np.array(np.eye(63,126), np.float64)  # 测量矩阵    H
        self.kalman.measurementNoiseCov = np.array(np.eye(63,63), np.float64) * 0.03 # 测量噪声    R
        transitionMatrix = np.array(np.eye(126,126), np.float64)
        transitionMatrix[:63]+=transitionMatrix[63:] # 测量矩阵    H
        self.kalman.transitionMatrix = transitionMatrix  # 转移矩阵 A
        self.kalman.processNoiseCov = np.array(np.eye(126,126), np.float64) * 0.003  # 过程噪声 Q
        # kalman.errorCovPost = np.array(np.eye(126,63), np.float64)  # 最小均方误差 P
        pass
    def calc(self,landmark):
        try:
            self.kalman.correct(landmark.reshape(63,1))
            return self.kalman.predict()[:63].reshape(21,3)
        except:
            print("calc hand kalman failed:",landmark)


class Point3KalmanFilter:
    def __init__(self):
        self.kalman = cv2.KalmanFilter(6,3,0,cv2.CV_64F) #int dynam_params, int measure_params, int control_params=0 
        self.kalman.measurementMatrix = np.array(np.eye(3,6), np.float64)  # 测量矩阵    H
        self.kalman.measurementNoiseCov = np.array(np.eye(3,3), np.float64) * 0.08 # 测量噪声    R
        transitionMatrix = np.array(np.eye(6,6), np.float64)
        transitionMatrix[:3]+=transitionMatrix[3:] # 测量矩阵    H
        self.kalman.transitionMatrix = transitionMatrix  # 转移矩阵 A
        self.kalman.processNoiseCov = np.array(np.eye(6,6), np.float64) * 0.03  # 过程噪声 Q
        # self.kalman.errorCovPost = np.array(np.eye(6,6) , np.float64)*0.01  # 最小均方误差 P
        pass
    def calc(self,point3):
        self.kalman.correct(point3.reshape(3,1))
        return self.kalman.predict()[:3].reshape(3,)