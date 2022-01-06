
import torch
import torch.nn.functional as F   

class SimpleNet(torch.nn.Module):    
    def __init__(self, n_output):
        super(SimpleNet, self).__init__()    
        n_feature = 63
        self.hidden = torch.nn.Linear(n_feature, 128)  
        self.hidden2 = torch.nn.Linear(128, 32)  
        self.out = torch.nn.Linear(32, n_output)   

    def forward(self, x):
        x = F.relu(self.hidden(x))    
        x = F.relu(self.hidden2(x))      
        # x = F.softmax(self.out(x),1 )    
        x = self.out(x)            
        return x