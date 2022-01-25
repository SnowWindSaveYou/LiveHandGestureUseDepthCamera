import grpc
import enum
# from ..utils import commonSetting

# from .py_proto import hand_pb2
# from .py_proto import hand_pb2_grpc

import py_proto.hand_pb2 as hand_pb2
import py_proto.hand_pb2_grpc as hand_pb2_grpc

class MPHandLandmark(enum.IntEnum):
    Wrist = 0
    # 拇指
    ThumbCMC = 1
    ThumbMCP = 2
    ThumbDIP = 3
    ThumbTIP = 4
    #食指
    IndexMCP = 5
    IndexPIP = 6
    IndexDIP = 7
    IndexTIP = 8
    #中指
    MiddleMCP = 9
    MiddlePIP = 10
    MiddleDIP = 11
    MiddleTIP = 12
    #无名指
    RingMCP = 13
    RingPIP = 14
    RingDIP = 15
    RingTIP = 16
    #小拇指
    PinkyMCP = 17
    PinkyPIP = 18
    PinkyDIP = 19
    PinkyTIP = 20
    
class HandExcutor:
    def __init__(self,host="localhost",port=2333):
        self.connection  = grpc.insecure_channel("%s:%d"%(host,port))
        self.client = hand_pb2_grpc.HandServiceStub(channel=self.connection)
    
    def pushHand(self,mpHand,commandId):
        if mpHand==None or len(mpHand)==0:
            return
        protoRequest = hand_pb2.ProtoHandRequest()
        protoRequest.command = commandId

        handsReq = protoRequest.hands.add()
        self.setProtoPoint3(handsReq.WRIST,mpHand[0])
        for i in range(1,21):
            mark = MPHandLandmark(i)
            self.setProtoPoint3(getattr(handsReq,mark.name),mpHand[i])
        self.client.PushHand(protoRequest)
        pass
    
    
    @staticmethod
    def setProtoPoint3(proto,point3):
        proto.x = point3[0]
        proto.y = point3[1]
        proto.z = point3[2]