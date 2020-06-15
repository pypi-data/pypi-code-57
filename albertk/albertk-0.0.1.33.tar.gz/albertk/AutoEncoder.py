import numpy as np
import torch
import tkitFile
from tqdm import tqdm
import tkitFile
from harvesttext import HarvestText
import numpy as np
 
import matplotlib.pyplot as plt

import torch
import torch.nn.functional as F     # 激励函数都在这


class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()

        # 压缩
        self.encoder = nn.Sequential(
            nn.Linear(28*28, 128),
            nn.Tanh(),
            nn.Linear(128, 64),
            nn.Tanh(),
            nn.Linear(64, 12),
            nn.Tanh(),
            nn.Linear(12, 3),   # 压缩成3个特征, 进行 3D 图像可视化
        )
        # 解压
        self.decoder = nn.Sequential(
            nn.Linear(3, 12),
            nn.Tanh(),
            nn.Linear(12, 64),
            nn.Tanh(),
            nn.Linear(64, 128),
            nn.Tanh(),
            nn.Linear(128, 28*28),
            nn.Sigmoid(),       # 激励函数让输出值在 (0, 1)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded

# autoencoder = AutoEncoder()
# 训练 