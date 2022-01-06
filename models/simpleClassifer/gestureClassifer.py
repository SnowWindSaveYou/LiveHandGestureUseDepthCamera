import torch
import torch.nn.functional as F     
import numpy as np
from .enums import *
from .src.model import SimpleNet 

    
class GestureClassifier:
    def __init__(self,model_path):
        self.model = SimpleNet(len(GestureEnum))
        self.model.load_state_dict(torch.load(model_path))
        self.model = self.model.eval()
        
    def formater(self,landmark):
        coord = self.getCoord(landmark[0],landmark[5],landmark[17])
        invCoord = np.linalg.inv(coord)
        landmarkHandCoord = np.matmul(landmark,invCoord)
        
        return torch.from_numpy(np.array(landmarkHandCoord,dtype=np.float32).reshape(1,63))
    
    def getCoord(self,a,b,c):
        ab = b-a
        ac = c-a
        yd = np.cross(ab,ac)
        y = yd/np.linalg.norm(yd)
        x = ab/np.linalg.norm(ab)
        zd = np.cross(x,y)
        z = zd/np.linalg.norm(zd)
        return np.array([x,y,z])
    
    def calc(self,landmarks):
        landmark = self.formater(landmarks)
        res = self.model(landmark)
        resGesture = GestureEnum(int(res.argmax(dim=1)[0]))
        return resGesture
        