import pyrealsense2 as rs
import cv2
import numpy as np
import keyboard
import os
import models
from models.simpleClassifer import enums
from utils.handDetector import HandDetector
import utils
# 
windowName = "RealSense Hand Detect"
count = 0
landmark = None


# region gesture configs
gestureButtons = {
    "0":enums.GestureEnum.NONE,
    "1":enums.GestureEnum.ONE,
    "2":enums.GestureEnum.TWO,
    "3":enums.GestureEnum.THREE,
    "4":enums.GestureEnum.FOUR,
    "5":enums.GestureEnum.FIVE,
    "6":enums.GestureEnum.PALM,
    "7":enums.GestureEnum.PINCH,
    "8":enums.GestureEnum.FIST,
    "9":enums.GestureEnum.PINCH_THREE,
    "q":enums.GestureEnum.THUMB,
    "w":enums.GestureEnum.TWO_CLOSE,
}
textNotice = [ k +":"+ gestureButtons[k].name for k in gestureButtons]
save_dir = "./models/simpleClassifer/data/nyu/"
saveDict = {}

def loadData():
    for key in gestureButtons:
        name = gestureButtons[key].name
        saveDict[name] = []
        if os.path.exists(save_dir+name+".npy"):
            saveDict[name] = np.load(save_dir+name+".npy").tolist()
def save():
    for key in gestureButtons:
        name = gestureButtons[key].name
        np.save(save_dir+name+".npy",np.array(saveDict[name]))
        print("save "+name+" ok")
        
def registerKey(key):
    def onKeyPress():
        name = gestureButtons[key].name
        if landmark is None:
            print(key, "Failed to saving "+ name, len(saveDict[name]))
            return
        saveDict[name].append(landmark)
        print(key, "saving "+ name, len(saveDict[name]))
    keyboard.add_hotkey(key, onKeyPress)

loadData()
for key in gestureButtons:
    registerKey(key)
#endregion

# region sr300 parms
fx = 475.065948
fy = 475.065857
ux = 315.944855
uy = 245.287079
max_depth = 500
depth_scale = 0.00012498664727900177 

# endregion

# region a2j params
keypointsNumber = 14
cropWidth = 176
cropHeight = 176
worldBoxSize = 240
depthSize = 300
hand_mean = -0.66877532422628
hand_std = 28.329582076876047
model_dir="./models/a2j/model/NYU.pth"
colorMap = utils.colorMap.FINGER_COLORS_NYU
# endregion




# init
jointDetector = models.a2j.JointDetector(model_dir=model_dir,keypointsNumber=keypointsNumber, useCuda=True)
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# try:
pipe_profile = pipeline.start(config)



while True:
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()
    if not depth: continue
    depth_img = np.asanyarray(depth.get_data())*depth_scale*1000
    display_img = utils.display.matToImg(depth_img)
    #
    hand = HandDetector(depth_img,fx, fy,ux,uy,max_depth)
    handCrop,com,mat = hand.detect(worldBoxSize=worldBoxSize,depthSize=depthSize)
    if handCrop is not None:
        test_topRight_pixel, test_bottomLeft_pixel = hand.comToBounds(com,worldBoxSize/2,True)
        result = jointDetector.forward(utils.math.scaleImg(handCrop,hand_mean,hand_std))
        if result is not None:
            landmark = (result[:,[1,0,2]]/(cropHeight,cropWidth,depthSize))-(0.5,0.5,0)
            display_img = utils.display.drawResult((landmark+1)*50,display_img)
            
            
            result = utils.math.applyTrans(result,mat)
            # result = jointDetector.convertHand2017ToMpOrder(result)
            display_img = utils.display.drawResult(result[:,[1,0,2]],display_img,colorMap)
            
        display_img = cv2.rectangle(display_img,
                                    (int(test_topRight_pixel[0]),int(test_topRight_pixel[1])), 
                                    (int(test_bottomLeft_pixel[0]),int(test_bottomLeft_pixel[1])),
                                    (255,0,0),5)
    display_img =utils.display.drawTexts(textNotice,display_img)
    cv2.imshow(windowName,display_img)
    
    key = cv2.waitKey(20)
    if key == 13: # take photo
        np.save("./data/depth"+str(count)+".npy",depth_img)
        count+=1
    if key == 27: # exit
        break
pipeline.stop()
save()
exit(0)
# except Exception as e:
#     print(e)
#     pass