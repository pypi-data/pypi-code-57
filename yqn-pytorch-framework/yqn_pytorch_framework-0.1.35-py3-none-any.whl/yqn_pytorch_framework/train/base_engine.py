import math
import os
import pathlib
import shutil
import sys
from abc import abstractmethod

import torch
import torchvision

from yqn_common import metric_logger as utils
from yqn_config.base_config import BaseConfig
from yqn_pytorch_framework.device import tensor_load_device


def save_checkpoint(state, is_best, directory, filename='checkpoint.pth'):
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    torch.save(state, os.path.join(directory, filename))
    shutil.copyfile(os.path.join(directory, filename), os.path.join(directory, 'model_last.pth'))
    if is_best:
        shutil.copyfile(os.path.join(directory, filename), os.path.join(directory, 'model_best.pth'))


class BaseModelEngine:
    def __init__(self, config: BaseConfig):
        super(BaseModelEngine, self).__init__()
        self.config = config

    @abstractmethod
    def criterion(self, outputs, labels):
        pass

    @abstractmethod
    def accuracy(self, outputs, labels):
        pass

    @abstractmethod
    def load_inputs(self, dataset):
        pass

    @abstractmethod
    def load_labels(self, dataset):
        pass

    @staticmethod
    def check_best(last_best_acc, focal_acc):
        is_best = True
        if last_best_acc is None:
            return is_best
        else:
            for index in range(len(focal_acc)):
                is_best = is_best & torch.gt(focal_acc[index], last_best_acc[index]).item()
            return is_best

    @staticmethod
    def get_save_info_per_epoch(epoch, step, model, optimizer, acc_list):
        return {
            'epoch': epoch + 1,
            'step': step,
            'state_dict': model.state_dict(),
            'acc_list': acc_list,
            'optimizer': optimizer.state_dict(),
        }

    def write_scalar(self, writer, focal_loss, focal_acc, step, epoch_index):
        if (epoch_index + 1) % self.config.summary_freq == 0:
            if focal_loss:
                for index, loss_value in enumerate(focal_loss):
                    writer.add_scalar('Train/loss_' + str(index),
                                      loss_value,
                                      step)
            if focal_acc:
                for index, acc_value in enumerate(focal_acc):
                    writer.add_scalar('Train/acc_' + str(index),
                                      acc_value,
                                      step)

    def write_image(self, writer, labels, predicts, step, epoch_index):
        if (epoch_index + 1) % self.config.summary_freq == 0:
            targets_img_grid = torchvision.utils.make_grid(labels[0, :, :], nrow=2)
            writer.add_image('Image_Label/targets_images', targets_img_grid, step)
            predicts_img_grid = torchvision.utils.make_grid(predicts[0, :, :], nrow=2)
            writer.add_image('Image_Pred/predicts_images', predicts_img_grid, step)

    def save_model(self, epoch, is_best, focal_acc, model, optimizer, step):
        if step % self.config.save_freq == 0:
            save_info = self.get_save_info_per_epoch(epoch, step, model, optimizer, focal_acc)
            save_checkpoint(save_info,
                            is_best,
                            self.config.get_train_model_out_dir(self.config.split_date),
                            filename='checkpoint_%d.pth' % step)

    def train_one_epoch(self,
                        model,
                        optimizer,
                        data_loader,
                        device,
                        epoch,
                        lr_scheduler=None,
                        last_best_acc=None,
                        step=0,
                        writer=None):
        current_acc = None
        try:
            metric_logger = utils.MetricLogger(delimiter="  ")
            metric_logger.add_meter('lr', utils.SmoothedValue(window_size=1, fmt='{value:.6f}'))
            header = 'Epoch: [{}]'.format(epoch)
            model.train()
            for dataset, index in metric_logger.log_every(data_loader, self.config.progress_freq, header):
                inputs_dataset = self.load_inputs(dataset)
                labels_dataset = self.load_labels(dataset)
                input_features = []
                labels = []
                if type(inputs_dataset) is list or type(inputs_dataset) is tuple:
                    for input_dataset in inputs_dataset:
                        input_features.append(tensor_load_device(input_dataset, device))
                else:
                    input_features = tensor_load_device(inputs_dataset, device)
                if type(labels_dataset) is list or type(labels_dataset) is tuple:
                    for label_dataset in labels_dataset:
                        labels.append(tensor_load_device(label_dataset, device))
                else:
                    labels = tensor_load_device(labels_dataset, device)
                outputs = model(*input_features)
                if len(outputs) == 1:
                    outputs = outputs[0]
                focal_loss = self.criterion(outputs=outputs, labels=labels)
                focal_acc = self.accuracy(outputs=outputs, labels=labels)
                # focal_loss = self.criterion(outputs=tuple(outputs), labels=tuple(labels))
                # focal_acc = self.accuracy(outputs=tuple(outputs), labels=tuple(labels))
                current_acc = focal_acc
                if not math.isfinite(focal_loss[0]):
                    print("Loss is {}, stopping training".format(focal_loss[0]))
                    sys.exit(1)

                optimizer.zero_grad()
                focal_loss[0].backward()
                optimizer.step()
                if lr_scheduler:
                    lr_scheduler.step()
                step += 1

                is_best = self.check_best(last_best_acc, focal_acc)
                if is_best:
                    last_best_acc = focal_acc
                self.save_model(epoch, is_best, focal_acc, model, optimizer, step)
                if writer is not None:
                    if self.config.write_scalar:
                        self.write_scalar(writer, focal_loss, focal_acc, step, index)
                    if self.config.write_image:
                        self.write_image(writer, labels, outputs, step, index)
                    writer.flush()
                metric_logger.update(loss=focal_loss[0], lr=optimizer.param_groups[0]["lr"])
        except KeyboardInterrupt:
            pass
            # save_info = self.get_save_info_per_epoch(epoch, step, model, optimizer, current_acc)
            # torch.save(save_info,
            #            os.path.join(self.config.get_train_model_out_dir(self.config.split_date), 'model_last.pth'))

        return last_best_acc, step
