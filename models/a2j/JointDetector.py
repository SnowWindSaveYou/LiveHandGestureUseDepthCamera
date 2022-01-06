import torch
import torch.utils.data
import numpy as np

from . import src

class JointDetector:
    def __init__(self,model_dir="./models/a2j/model/HANDS2017.pth",keypointsNumber=21,cropWidth=176,cropHeight=176, useCuda=False):
        self.useCuda = useCuda
        self.inputShape = (1,1,cropHeight,cropWidth)
        self.a2jnet = src.model.A2J_model(keypointsNumber)
        self.post_precess = src.anchor.post_process(shape=[cropHeight//16,cropWidth//16],stride=16,P_h=None, P_w=None,useCuda=useCuda)
        
        if useCuda:
            self.a2jnet.load_state_dict(torch.load(model_dir)) 
            self.a2jnet.cuda()
        else:
            self.a2jnet.load_state_dict(torch.load(model_dir,map_location=torch.device('cpu') )) 
        self.a2jnet.eval()
        
    def forward(self,img):
        if img is None:
            return None
        inputHand_tensor = torch.from_numpy(np.array(img.reshape(self.inputShape),dtype=np.float32))
        
        if self.useCuda==True:
            inputHand_tensor = inputHand_tensor.cuda()
            
        with torch.no_grad():
            head = self.a2jnet(inputHand_tensor)
            pred_keypoints = self.post_precess(head,voting=False)
            result = pred_keypoints.data.cpu().numpy()
            return result[0]
    @staticmethod
    def convertHand2017ToMpOrder(result):
        mpJoint = np.zeros((21,3))
        mpJoint[0] = result[0]
        for i in range(5):
            mpStart = i*4+1
            rsStart = i*3+5
            mpJoint[mpStart] = result[i+1]
            for j in range(1,4):
                mpJoint[mpStart+j] = result[rsStart+j]
        return mpJoint[:,[1,0,2]]