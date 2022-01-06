import pyrealsense2 as rs
import cv2
import numpy as np


import models
from utils.handDetector import HandDetector
import utils
# 
windowName = "RealSense Hand Detect"
count = 0

# sr300 parm
fx = 475.065948
fy = 475.065857
ux = 315.944855
uy = 245.287079
max_depth = 500
depth_scale = 0.00012498664727900177 
hand_mean = -6.39239157
hand_std = 25.00686072

# a2j param
keypointsNumber = 21
cropWidth = 176
cropHeight = 176
worldBoxSize = 240
depth_thres = 150
model_dir="./models/a2j/model/HANDS2017.pth"

# init

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipe_profile = pipeline.start(config)

while True:
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()
    if not depth: continue
    depth_img = np.asanyarray(depth.get_data())*depth_scale*1000
    
    #
    hand = HandDetector(depth_img,fx, fy,ux,uy,max_depth)
    handCrop,com,_ = hand.detect(worldBoxSize=worldBoxSize)
    if handCrop is None:
        continue
    
    test_lefttop_pixel, test_rightbottom_pixel = hand.comToBounds(com,worldBoxSize/2,True)
    blank_image = utils.display.matToImg(depth_img)
    
    print("----------",com,test_lefttop_pixel,test_rightbottom_pixel)
    display_img = cv2.rectangle(blank_image,
                                (int(test_lefttop_pixel[0]),int(test_lefttop_pixel[1])), 
                                (int(test_rightbottom_pixel[0]),int(test_rightbottom_pixel[1])),
                                (255,0,0),5)
    
    cv2.imshow(windowName,display_img)
    key = cv2.waitKey(20)
    if key == 13: # take photo
        np.save("./data/depth"+str(count)+".npy",depth_img)
        count+=1
    if key == 27: # exit
        break
pipeline.stop()
exit(0)
# except Exception as e:
#     print(e)
#     pass