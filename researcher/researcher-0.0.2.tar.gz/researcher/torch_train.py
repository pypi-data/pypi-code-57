import datetime

import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from researcher.logging import *

def run_torch_model(model, optimizer, loss_fn, loader, epoch, train, device, loggers, steps_per_epoch=None):
    n_steps = steps_per_epoch or len(loader)
    
    if train:
        model.train()
    else:
        model.eval()
        torch.set_grad_enabled(False)
    
    for i, data in enumerate(loader, 0):
        step = epoch * n_steps + i

        if steps_per_epoch and i > steps_per_epoch:
            break

        text_ids = data[:, 0].to(device, dtype=torch.long)
        attention_mask = data[:, 1].to(device, dtype=torch.long)
        token_type_ids = data[:, 2].to(device, dtype=torch.long)
        
        start_ids = data[:, 3].to(device, dtype=torch.float32)
        end_ids = data[:, 4].to(device, dtype=torch.float32)
        
        if train:
            optimizer.zero_grad()
        
        start_preds, end_preds = model(text_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        loss = loss_fn(start_preds, torch.argmax(start_ids, axis=1)) + loss_fn(end_preds, torch.argmax(end_ids, axis=1))
        
        if train:
            loss.backward()
            optimizer.step()

        with torch.no_grad():
            pred_values = [start_preds.cpu().numpy(), end_preds.cpu().numpy()]
            target_values = [start_ids.cpu().numpy(), end_ids.cpu().numpy()]
            losses = [loss.cpu().numpy()]
            for logger in loggers:
                logger.collect(pred_values, target_values, losses, step)
    
    with torch.no_grad():
        for logger in loggers:
            logger.write(epoch)
        
    if not train:
        torch.set_grad_enabled(True)


class LossMetric():
    def __init__(self, loggers, write_fn):
        super().__init__()

        self.loggers = loggers
        self.write_fn = write_fn

        self.__reset()
    
    def __reset(self):
        self.metrics = [0 for i in range(len(self.loggers))]
        self.step_count = 0

    def collect(self, preds, targets, losses, step):
        for i, logger in enumerate(self.loggers):
            metric = logger.fn(preds, targets, losses)
            self.metrics[i] += metric

            self.write_fn("batch_" + logger.name, metric, step)
        
        self.step_count += 1
    
    def write(self, epoch):
        for i, logger in enumerate(self.loggers):
            value = self.metrics[i] / self.step_count
            self.write_fn(logger.name, value, epoch)
            print("{}: {}".format(logger.name, value), end=' ')
    
        self.__reset()

class ComplexMetric():
    def __init__(self, loggers, write_fn, df, batch_size):
        super().__init__()

        self.loggers = loggers
        self.write_fn = write_fn
        self.df = df
        self.batch = False
        self.batch_size = batch_size
    
        self.__reset()

    def __reset(self):
        self.metrics = [0 for i in range(len(self.loggers))]
        self.step_count = 0

    def collect(self, preds, targets, losses, step):
        preds_numpy = (preds[0], preds[1])
        pred_count = preds_numpy[0].shape[0]
        index = self.step_count*self.batch_size
        df = self.df[index:index+pred_count].reset_index()

        for i, logger in enumerate(self.loggers):
            metric = 0
            for j in range(pred_count):
                metric += logger.fn(df, preds_numpy, j)
            self.metrics[i] += metric / pred_count
        
        self.step_count += 1

    def write(self, epoch):
        for i, logger in enumerate(self.loggers):
            value = self.metrics[i] / self.step_count
            self.write_fn(logger.name, value, epoch)

        self.__reset()

class TorchMetricEarlyStopping():
    def __init__(self, metric, patience=0, filename="models/early_stopping/checkpoint"):
        self.patience = patience
        self.metric = metric
        self.filename = filename

        self.wait = 0
        self.stopped_epoch = 0
        self.lowest_loss = np.Inf

    def make_assessment(self, model, epoch, history):
        current_loss = history[self.metric][epoch]

        if np.less(current_loss, self.lowest_loss):
            self.lowest_loss = current_loss
            self.wait = 0
            self.stopped_epoch = epoch
            self.__save_checkpoint({
                'epoch': epoch,
                'state_dict': model.state_dict(),
            })
        else:
            self.wait += 1
            if self.wait >= self.patience:
                checkpoint = torch.load(self.filename)
                model.load_state_dict(checkpoint['state_dict'])
                print('\nPatience exceeded on epoch {}, restoring model weights from the end of epoch {}'.format(epoch, self.stopped_epoch))
                return False
        
        return True

    def __save_checkpoint(self, state):
        torch.save(state, self.filename)