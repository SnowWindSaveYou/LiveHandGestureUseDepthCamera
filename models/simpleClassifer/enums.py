import enum

class GestureEnum(enum.IntEnum):
    ANY = 999,
    NONE = 0,
    ONE = 1, 
    TWO = 2, 
    THREE = 3, 
    FOUR = 4, 
    FIVE = 5, 
    PALM = 6, 
    PINCH = 7,
    FIST = 8,
    PINCH_THREE = 9,#三指捏住
    THUMB = 10,
    TWO_CLOSE = 11, 

class HandLandmark(enum.IntEnum):
    WRIST = 0
    # 拇指
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_DIP = 3
    THUMB_TIP = 4
    #食指
    INDEX_FINGER_MCP = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    #中指
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    #无名指
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    #小拇指
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20

FINGER_THUMB  = [0,1,2,3,4]
FINGER_INDEX  = [0,5,6,7,8]
FINGER_MIDDLE = [0,9,10,11,12]
FINGER_RING   = [0,13,14,15,16]
FINGER_PINKY  = [0,17,18,19,20]
FINGERS = [FINGER_THUMB,FINGER_INDEX, FINGER_MIDDLE, FINGER_RING,FINGER_PINKY ]

class CURL_STATE(enum.IntEnum):
    NO=0
    HALF=1
    CURL=2
    FULLCURL =3
    
class HotKeyEnum(enum.IntEnum):
    ctrl = 0
    shift = 1
    z = 2
    x = 3
    c = 4
    
