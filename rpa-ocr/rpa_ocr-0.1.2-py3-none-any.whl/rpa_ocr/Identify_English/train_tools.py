# -*- coding:utf-8 -*-
# @author :adolf
from rpa_ocr.Identify_English.crnn_model import CRNN
from rpa_ocr.Identify_English.rawdataset import RawDataset
from rpa_ocr.Identify_English.use_alphabet import *

import os
import sys
import time
import random
import json
import requests
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torch.nn.functional as F


class Train(object):
    '''
    :param app_scenes: what scenes this model used
    :param alphabet_mode: which alphabet is used,now is supported "ch","eng","ENG"
    :param data_path: where data storage
    :param model_path: path to save model
    :param short_size: short_size has to be a multiple of 16
    :param verification_length: length of verification; TODO support variable length of verification
    :param device: use cpu or gpu;"cpu" or "cuda"
    :param epochs: how long to train model
    :param lr: learning rate
    :param batch_size: how much data to train on one batch
    :param num_works: how many processes are used to data preprocess
    :param target_acc: The target accuracy
    '''

    def __init__(self,
                 app_scenes,
                 alphabet_mode='eng',
                 data_path=None,
                 model_path='model',
                 short_size=32,
                 verification_length=4,
                 device='cpu',
                 epochs=1200,
                 lr=1e-3,
                 batch_size=256,
                 num_works=0,
                 target_acc=0.95,
                 cloud_service=True):
        # general_config = params['GeneralConfig']
        # train_config = params['TrainConfig']

        if app_scenes is None:
            print('请输入使用场景')
            sys.exit(1)

        # if alphabet_mode is None:
        #     print('请输入使用字母表,"ch"表示中文字符,"eng"表示英文大小写+数字,"ENG"表示英文大写+数字')
        #     sys.exit(1)

        if data_path is None:
            print('请输入存放图片的路径')
            sys.exit(1)

        if model_path is None:
            print('请输入存放模型文件的地址')
            sys.exit(1)

        self.app_scenes = app_scenes

        alphabet = self.read_alphabet(alphabet_mode)
        # print(alphabet)

        self.alphabet_dict = {alphabet[i]: i for i in range(len(alphabet))}
        self.decode_alphabet_dict = {v: k for k, v in self.alphabet_dict.items()}

        self.short_size = short_size
        self.verification_length = verification_length

        self.data_path = data_path
        self.device = device
        self.model_path = model_path
        print(model_path)
        if not os.path.exists(self.model_path):
            os.mkdir(self.model_path)
        self.epochs = epochs
        self.lr = lr
        self.batch_size = batch_size
        self.workers = num_works

        self.cloud_service = cloud_service
        # self.url = "http://192.168.1.135:12020/upload_service/"
        self.url = "https://rpa-vc-upload.ai-indeed.com/"

        # nh:size of the lstm hidden state
        self.model = CRNN(imgH=self.short_size, nc=1, nclass=len(alphabet), nh=256)
        self.model.apply(self.weights_init)

        model = self.model.to(self.device)
        self.criterion = nn.CTCLoss(blank=len(alphabet) - 1, reduction='mean')
        self.optimizer = optim.Adam(model.parameters())  # ,betas=(opt.beta1, 0.999))

        self.train_datasets = None
        self.valid_datasets = None
        self.init_datasets()
        self.train_loader, self.valid_loader = self.data_loaders()

        self.val_best_acc = 0
        self.target_acc = target_acc

        self.patient_epoch = 0

    @staticmethod
    def weights_init(m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            m.weight.data.normal_(0.0, 0.02)
        elif classname.find('BatchNorm') != -1:
            m.weight.data.normal_(1.0, 0.02)
            m.bias.data.fill_(0)

    def init_datasets(self):
        self.train_datasets = RawDataset(file_path=self.data_path,
                                         imgH=self.short_size,
                                         alphabet_dict=self.alphabet_dict,
                                         verification_length=self.verification_length,
                                         is_training=True)
        # valid_datasets = train_datasets
        #
        self.valid_datasets = RawDataset(file_path=self.data_path,
                                         imgH=self.short_size,
                                         alphabet_dict=self.alphabet_dict,
                                         verification_length=self.verification_length,
                                         is_training=False)

    def get_result(self, file_path):
        files = {'file': open(file_path, 'rb')}
        r = requests.post(self.url, files=files)
        res = json.loads(r.text)
        # print(res)
        return res

    @staticmethod
    def read_alphabet(alphabet_mode):
        # res_list = list()
        if alphabet_mode == "eng":
            alphabet = english_alphabet
        elif alphabet_mode == "ENG":
            alphabet = english_alphabet_big
        else:
            # alphabet_str = chinese_alphabet
            alphabet = list(chinese_alphabet)
            alphabet.append('-')
            # print(alphabet)

        return alphabet

    def data_loaders(self):
        loader_train = data.DataLoader(
            self.train_datasets,
            batch_size=self.batch_size,
            shuffle=True,
            drop_last=False,
            num_workers=self.workers,
            pin_memory=False
        )

        loader_valid = data.DataLoader(
            self.valid_datasets,
            batch_size=1,
            drop_last=False,
            num_workers=self.workers,
        )

        return loader_train, loader_valid

    def train_one_epoch(self, epoch):
        self.model.train()
        for batch_idx, (img, label, length) in enumerate(self.train_loader):
            img = img.to(device=self.device, dtype=torch.float)
            label = label.to(device=self.device)
            length = length.to(self.device)
            #         print(img.size())
            output = self.model(img)
            #         print(output.shape)
            log_probs = F.log_softmax(output, dim=2)

            target = label
            target_lengths = length
            input_lengths = torch.full(size=(output.size()[1],), fill_value=output.size()[0], dtype=torch.long)

            loss = self.criterion(log_probs, target, input_lengths, target_lengths)

            self.optimizer.zero_grad()
            loss.backward()

            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 10)
            self.optimizer.step()

            if batch_idx % 10 == 0:
                print('Epoch [{}], Step [{}], Loss: {:.4f}'
                      .format(epoch, batch_idx, loss.item()))

    def val_model(self):
        self.model.eval()
        total = self.valid_loader.dataset.__len__()
        correct = 0
        for img, label, length in self.valid_loader:
            img = img.to(device=self.device, dtype=torch.float)
            label.to(device=self.device)
            length = length.to(self.device)
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
            pred_label, _ = self.valid_datasets.converter_text_to_label(res_str)
            if random.randint(0, 200) == 50:
                print('label:', label)
                print('pred_label', pred_label)
                print('res_str', res_str)
            pred_label_list_a = pred_label.tolist()
            if len(pred_label_list_a) > 4:
                pred_label_list_a = pred_label_list_a[-4:]
            if pred_label_list_a == label.tolist()[0]:
                correct += 1
        acc = correct / total
        return acc

    def main(self):
        for epoch in tqdm(range(self.epochs), total=self.epochs):
            epoch_start_time = time.time()
            self.train_one_epoch(epoch)
            epoch_end_time = time.time()
            print("Epoch [{}] all use time:[{:.2f}]".format(epoch, epoch_end_time - epoch_start_time))
            if epoch > 100 and epoch % 3 == 0:
                val_acc = self.val_model()
                print('valid data accuracy:', val_acc)
                if val_acc > self.val_best_acc:
                    torch.save(self.model.state_dict(),
                               os.path.join(self.model_path,
                                            self.app_scenes + "_verification.pth"))
                    self.patient_epoch = 0
                    self.val_best_acc = val_acc
                else:
                    self.patient_epoch += 1
                if self.val_best_acc > self.target_acc or self.patient_epoch > 30:
                    break

        if self.cloud_service:
            file_path = os.path.join(self.model_path, self.app_scenes + "_verification.pth")
            res = self.get_result(file_path)
            print(res)


if __name__ == '__main__':
    # import yaml

    # os.environ["CUDA_VISIBLE_DEVICES"] = "3"

    # with open('Identify_English/Identify_English.yaml', 'r') as fp:
    #     config = yaml.load(fp.read(), Loader=yaml.FullLoader)
    import argparse

    # test command:
    # python -m rpa_ocr.Identify_English.train_tools -sc jindie -a eng
    # -data /home/shizai/adolf/data/jindie -m /home/shizai/adolf/model/

    parser = argparse.ArgumentParser(description="Params to use fro train algorithm")
    parser.add_argument("--app_scenes", "-sc", type=str,
                        default=argparse.SUPPRESS, nargs='?', help="what scenes this model used")
    parser.add_argument("--alphabet_mode", "-a", type=str,
                        default="eng", nargs='?', help="alphabet what is used,'eng','ch','ENG'")
    parser.add_argument("--data_path", "-data", type=str,
                        default=argparse.SUPPRESS, nargs='?', help="where data storage")
    parser.add_argument("--model_path", "-m", type=str,
                        default=argparse.SUPPRESS, nargs='?', help="path to save model")
    parser.add_argument("--short_size", "-sh", type=int,
                        default=32, nargs='?', help="short_size has to be a multiple of 16")
    parser.add_argument("--verification_length", "-v", type=int, const=True,
                        default=4, nargs='?', help="length of verification")
    parser.add_argument("--device", "-dev", type=str,
                        default="cpu", nargs='?', help="use cpu or gpu;'cpu' or 'cuda'")
    parser.add_argument("--epochs", "-e", type=int,
                        default=1200, nargs='?', help="if you don't know what meaning,using default")
    parser.add_argument("--lr", "-l", type=float,
                        default=1e-3, nargs='?', help="if you don't know what meaning,using default")
    parser.add_argument("--batch_size", "-b", type=int,
                        default=256, nargs='?', help="if you don't know what meaning,using default")
    parser.add_argument("--num_works", "-n", type=int,
                        default=0, nargs='?', help="how many processes are used to data")
    parser.add_argument("--target_acc", "-t", type=float,
                        default=0.95, nargs='?', help="The target accuracy")
    args = parser.parse_args()

    args.app_scenes = 'jindie'
    args.data_path = '/home/shizai/adolf/data/jindie/'
    args.model_path = '/home/shizai/adolf/model/'

    trainer = Train(app_scenes=args.app_scenes,
                    alphabet_mode=args.alphabet_mode,
                    data_path=args.data_path,
                    model_path=args.model_path,
                    short_size=args.short_size,
                    verification_length=args.verification_length,
                    device=args.device,
                    epochs=args.epochs,
                    lr=args.lr,
                    batch_size=args.batch_size,
                    num_works=args.num_works,
                    target_acc=args.target_acc)

    # trainer.main()
    trainer.read_alphabet("ch")
