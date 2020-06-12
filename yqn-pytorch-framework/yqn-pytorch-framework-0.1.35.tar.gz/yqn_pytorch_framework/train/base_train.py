import os
import shutil
from abc import abstractmethod

import torch
from torch.backends import cudnn
from torch.utils.data.dataloader import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import optim

from yqn_config.base_config import BaseConfig
from yqn_pytorch_framework.device import get_cpu_device, tensor_load_device
from yqn_pytorch_framework.train.base_engine import BaseModelEngine


class BaseModelTrain:

    def __init__(self, engine: BaseModelEngine):
        self.engine = engine
        super(BaseModelTrain, self).__init__()

    @abstractmethod
    def load_model(self, model_config: BaseConfig):
        """
        :param model_config:
        :return:  nn model
        """
        pass

    @abstractmethod
    def load_data(self, config: BaseConfig, data_flag='train'):
        """
        加载训练数据
        :param config:
        :param data_flag
        :return:
        """
        pass

    @staticmethod
    def get_resume_file(config: BaseConfig):
        """
        获取继续训练的模型位置
        :param config:
        :return:
        """
        directory = config.get_train_model_out_dir(config.split_date)
        resume_file = os.path.join(directory, 'model_last.pth')
        return resume_file

    @staticmethod
    def get_optimizer(model, config: BaseConfig):
        """
        获取loss Optimizer 方法
        :param self:
        :param model:
        :param config:
        :return:
        """
        if config.optimizer in ["sdg", "adam"]:
            if config.optimizer == "sdg":
                return torch.optim.SGD(model.parameters(), lr=config.learning_rate)
            else:
                return torch.optim.Adam(model.parameters(), lr=config.learning_rate)
        else:
            return torch.optim.Adam(model.parameters(), lr=config.learning_rate)

    def start_train(self, model, config: BaseConfig):
        train_data = self.load_data(config, 'train')
        train_loader = DataLoader(dataset=train_data,
                                  batch_size=config.batch_size,
                                  shuffle=config.shuffle_batch,
                                  # num_workers=8,
                                  pin_memory=True)
        writer = SummaryWriter(config.get_train_log_dir())
        model = tensor_load_device(model, config.device)
        dummy_input = model.get_default_input()
        writer.add_graph(model, input_to_model=dummy_input)
        writer.flush()
        # optimizer = self.get_optimizer(model=model, config=config)
        optimizer = optim.Adam(model.parameters(), lr=config.learning_rate, amsgrad=True,
                               weight_decay=config.lr_rate_decay)
        for group in optimizer.param_groups:
            group.setdefault('initial_lr', group['lr'])

        lr_scheduler = None
        best_acc = None
        last_epoch = 0
        global_step = 0
        if not config.retrain:
            resume_file = self.get_resume_file(config)
            if os.path.exists(resume_file):
                print("=> loading checkpoint '{}'".format(resume_file))
                checkpoint = torch.load(resume_file, map_location=device)
                last_epoch = checkpoint['epoch']
                global_step = checkpoint['step']
                if 'best_acc_list' in checkpoint:
                    best_acc = checkpoint['best_acc_list']
                model.load_state_dict(checkpoint['state_dict'])
                print("=> loaded checkpoint '{}' (epoch {} global step {})".format(resume_file,
                                                                                   checkpoint['epoch'],
                                                                                   checkpoint['step']))
        else:
            directory = config.get_train_model_out_dir(config.split_date)
            shutil.rmtree(directory)
        if lr_scheduler:
            lr_scheduler.step(epoch=global_step)
        for epoch in range(last_epoch, last_epoch + config.num_epochs):
            best_acc, global_step = self.engine.train_one_epoch(model,
                                                                optimizer=optimizer,
                                                                data_loader=train_loader,
                                                                device=config.device,
                                                                epoch=epoch,
                                                                lr_scheduler=lr_scheduler,
                                                                step=global_step,
                                                                last_best_acc=best_acc,
                                                                writer=writer)

    def train(self, config):
        model = self.load_model(model_config=config)
        model = tensor_load_device(model, config.device)
        print(model)
        self.start_train(model, config)
