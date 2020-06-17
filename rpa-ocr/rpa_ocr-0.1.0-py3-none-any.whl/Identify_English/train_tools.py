# -*- coding:utf-8 -*-
# @author :adolf
from Identify_English.crnn_model import CRNN
from Identify_English.rawdataset import RawDataset

import os
import time
import random
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torch.nn.functional as F


class Train(object):
    def __init__(self, params):
        general_config = params['GeneralConfig']
        train_config = params['TrainConfig']

        self.app_scenes = general_config['app_scenes']

        alphabet = general_config['alphabet']
        self.alphabet_dict = {alphabet[i]: i for i in range(len(alphabet))}
        self.decode_alphabet_dict = {v: k for k, v in self.alphabet_dict.items()}

        self.short_size = general_config['short_size']
        self.verification_length = general_config['length']

        self.data_path = train_config['train_data_path']
        self.device = train_config['Device']
        self.model_path = train_config['model_path']
        if not os.path.exists(self.model_path):
            os.mkdir(self.model_path)
        self.epochs = train_config['epochs']
        self.lr = train_config['lr']
        self.batch_size = train_config['batch_size']
        self.workers = train_config['num_works']

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
                      .format(epoch + 1, batch_idx + 1, loss.item()))

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


if __name__ == '__main__':
    import yaml

    # os.environ["CUDA_VISIBLE_DEVICES"] = "3"

    with open('Identify_English/Identify_English.yaml', 'r') as fp:
        config = yaml.load(fp.read(), Loader=yaml.FullLoader)

    trainer = Train(params=config)
    trainer.main()
