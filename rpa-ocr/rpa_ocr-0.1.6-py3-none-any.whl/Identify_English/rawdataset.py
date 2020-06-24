# -*- coding:utf-8 -*-
# @author :adolf
import cv2
import torch.utils.data as data
import torch
import torchvision.transforms as transforms
import random
import os
from tqdm import tqdm


class RawDataset(data.Dataset):
    def __init__(self, file_path, imgH, alphabet_dict, verification_length, is_training):
        # for png_name in data_list:
        #     img = cv2.imread(file_path + png_name)
        #     assert img.shape[2] == 3, "请读入3通道图片"
        #     img = cv2.resize(img, (imgW, imgH))
        #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #     label = png_name.split('.')[0]
        #     all_data_list.append((img, label))
        # self.img_input = all_data_list
        self.root = file_path
        self.imgH = imgH
        self.imgW = None
        self.is_training = is_training

        self.patients = list(sorted(os.listdir(self.root)))
        validation_cases = int(0.1 * len(self.patients))

        validation_patients = random.sample(self.patients, k=validation_cases)
        # validation_patients = ['img_363.jpg']

        if not is_training:
            self.patients = validation_patients
        else:
            self.patients = sorted(
                list(set(self.patients).difference(validation_patients))
            )
        self.img_input = list()

        for img_name in tqdm(self.patients):
            img_path = os.path.join(self.root, img_name)
            img = cv2.imread(img_path)
            self.imgW = int(img.shape[1] * self.imgH / img.shape[0])
            assert img.shape[2] == 3, "请读入3通道图片"
            img = cv2.resize(img, (self.imgW, self.imgH))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            label = img_name.split('.')[0][:verification_length]
            self.img_input.append((img, label))

        self.alphabet_dict = alphabet_dict
        self.transform = transforms.Compose([transforms.ToTensor()])
        self.target_transform = self.converter_text_to_label

    def __len__(self):
        return len(self.img_input)

    def __getitem__(self, index):
        img, label = self.img_input[index]
        img = self.transform(img)
        label, length = self.target_transform(label)
        return img, label, length

    def converter_text_to_label(self, label_str):
        # print(label_str)
        # print(self.alphabet_dict)
        label = [self.alphabet_dict[char] for char in label_str]
        length = [len(label)]
        return torch.IntTensor(label), torch.IntTensor(length)
