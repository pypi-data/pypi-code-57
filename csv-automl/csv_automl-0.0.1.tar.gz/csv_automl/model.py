import json
import sklearn.metrics
import torch
import torch.nn as nn
import torch.nn.functional as F

class DenseLogisticRegression(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 50)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(50, 20)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(20, 1)        
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.fc1.weight.data.uniform_(-initrange, initrange)
        self.fc1.bias.data.zero_()
        self.fc2.weight.data.uniform_(-initrange, initrange)
        self.fc2.bias.data.zero_()
        self.fc3.weight.data.uniform_(-initrange, initrange)
        self.fc3.bias.data.zero_()

    def forward(self, inputs):
        fc1 = self.fc1(inputs)
        fc2 = self.fc2(self.relu1(fc1))
        fc3 = self.fc3(self.relu2(fc2))
        return torch.sigmoid(fc3)

    @classmethod
    def criterion(cls):
        return torch.nn.BCELoss(size_average=True)

    
