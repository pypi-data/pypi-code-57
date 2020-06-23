# -*- coding:utf-8 -*-
# @author :adolf
import base64
import cv2
import numpy as np
import os
import torch
import torchvision.transforms as transforms
from torch import nn
from Identify_English.crnn_model import CRNN


class CRNNInference(object):
    def __init__(self, params):
        general_config = params['GeneralConfig']
        infer_config = params['InferenceConfig']

        self.app_scenes = general_config['app_scenes']

        alphabet = general_config['alphabet']
        self.alphabet_dict = {alphabet[i]: i for i in range(len(alphabet))}
        self.decode_alphabet_dict = {v: k for k, v in self.alphabet_dict.items()}

        self.short_size = general_config['short_size']
        self.verification_length = general_config['length']

        self.device = infer_config['Device']
        self.model_path = os.path.join(infer_config['model_path'],
                                       self.app_scenes + "_verification.pth")

        self.transform = transforms.Compose([transforms.ToTensor()])

        self.model = CRNN(imgH=self.short_size, nc=1, nclass=len(alphabet), nh=256)
        self.init_torch_tensor()
        self.resume()
        self.model.eval()

    def init_torch_tensor(self):
        torch.set_default_tensor_type('torch.FloatTensor')
        if self.device != "cpu":
            torch.set_default_tensor_type('torch.cuda.FloatTensor')

    def resume(self):
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device), strict=True)
        self.model.to(self.device)

    @staticmethod
    def base64_to_opencv(image_base64):
        img = base64.b64decode(image_base64)
        img_array = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img

    def predict(self, image_base64):
        img = self.base64_to_opencv(image_base64)

        imgW = int(img.shape[1] * self.short_size / img.shape[0])
        img = cv2.resize(img, (imgW, self.short_size))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img[:, :, np.newaxis]
        img = self.transform(img)

        img = img.unsqueeze(0)
        with torch.no_grad():
            output = self.model(img)

        output = output.squeeze()

        _, preds = output.max(1)
        preds_list = preds.tolist()

        preds_decode_list = [self.decode_alphabet_dict[i] for i in preds_list]
        res_str = ""

        for i in range(len(preds_decode_list)):
            if i == 0 and preds_decode_list[i] != '-':
                res_str += preds_decode_list[i]
            if preds_decode_list[i] != preds_decode_list[i - 1] and preds_decode_list[i] != '-':
                res_str += preds_decode_list[i]

        if len(res_str) > self.verification_length:
            res_str = res_str[-self.verification_length:]
        return res_str
