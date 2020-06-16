import math

import torch
from torch import nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np


class BCEFocalLoss(nn.Module):
    def __init__(self, gamma=2):
        super(BCEFocalLoss, self).__init__()
        self.gamma = gamma

    def forward(self, input, target):
        BCE_loss = F.binary_cross_entropy_with_logits(input, target, reduction='none')
        pt = torch.exp(-BCE_loss)  # prevents nans when probability 0
        focal_loss = (1 - pt) ** self.gamma * BCE_loss
        return focal_loss.mean()


class BCEGWLoss(nn.Module):
    def __init__(self):
        super(BCEGWLoss, self).__init__()

    def gaussian(self, x, mean=0.5, variance=0.25):
        for i, v in enumerate(x.data):
            x.data[i] = math.exp(-(v - mean) ** 2 / (2.0 * variance ** 2))
        return x

    def forward(self, input, target):
        BCE_loss = F.binary_cross_entropy_with_logits(input, target, reduction='none')
        BCE_loss = BCE_loss.view(-1)
        pt = sigmoid(BCE_loss)  # prevents nans when probability 0
        loss = (self.gaussian(pt, variance=0.1 * math.exp(1), mean=0.5) - 0.1 * pt) * BCE_loss
        return loss.mean()


class FocalLoss(nn.Module):
    def __init__(self, gamma=2):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.softmax = nn.Softmax(dim=1)
        self.nll = nn.NLLLoss(ignore_index=-1)

    def forward(self, input, target):
        softmax = self.softmax(input)
        logpt = torch.log(softmax)
        pt = Variable(logpt.data.exp())
        return self.nll((1 - pt) ** self.gamma * logpt, target)


class DiceLoss(nn.Module):
    """DiceLoss implemented from 'Dice Loss for Data-imbalanced NLP Tasks'
    Useful in dealing with unbalanced data
    Add softmax automatically
    """

    def __init__(self):
        super(DiceLoss, self).__init__()

    def forward(self, y_pred, y_true):
        y_pred = torch.softmax(y_pred, dim=1)
        pred_prob = torch.gather(y_pred, dim=1, index=y_true.unsqueeze(1))
        dsc_i = 1 - ((1 - pred_prob) * pred_prob) / ((1 - pred_prob) * pred_prob + 1)
        dice_loss = dsc_i.mean()
        return dice_loss


class NegativeCElLoss(nn.Module):
    def __init__(self, ignore_index=-1, reduction='mean'):
        super(NegativeCElLoss, self).__init__()
        self.softmax = nn.Softmax(dim=1)
        self.alpha = 1
        self.nll = nn.NLLLoss(ignore_index=ignore_index, reduction=reduction)

    def forward(self, input, target):
        nsoftmax = self.softmax(input)
        nsoftmax = torch.clamp((1.0 - nsoftmax), min=1e-32)
        return self.nll(torch.log(nsoftmax) * self.alpha, target)


class LabelSmoothingLoss(nn.Module):
    def __init__(self, classes, smoothing=0.1, dim=-1):
        super(LabelSmoothingLoss, self).__init__()
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.cls = classes
        self.dim = dim

    def forward(self, pred, target):
        pred = pred.log_softmax(dim=self.dim)
        with torch.no_grad():
            # true_dist = pred.data.clone()
            true_dist = torch.zeros_like(pred)
            true_dist.fill_(self.smoothing / (self.cls - 1))
            true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)
        return torch.mean(torch.sum(-true_dist * pred, dim=self.dim))


class LossDropper(nn.Module):
    """DiceLoss implemented from 'Improved Natural Language Generation via Loss Truncation'
        Useful in dealing with text generate
        """

    def __init__(
            self,
            dropc=0.4,
            min_count=10000,
            recompute=10000,
            verbose=True
    ):
        super().__init__()
        self.keepc = 1. - dropc
        self.count = 0
        self.min_count = min_count

        self.recompute = recompute
        self.last_computed = 0
        self.percentile_val = 100000000.
        self.cur_idx = 0

        self.verbose = verbose

        self.vals = np.zeros(self.recompute, dtype=np.float32)

    def forward(self, loss):
        if loss is None:
            return loss

        self.last_computed += loss.numel()
        self.count += loss.numel()
        if self.count < len(self.vals):
            self.vals[self.count - loss.numel():self.count] = loss.detach().cpu().numpy().flatten()
            self.cur_idx += loss.numel()
            return (loss < np.inf).type(loss.dtype)
        else:
            for idx, item in enumerate(loss):
                self.vals[self.cur_idx] = item
                self.cur_idx += 1
                if self.cur_idx >= len(self.vals):
                    self.cur_idx = 0
        if self.count < self.min_count:
            return (loss < np.inf).type(loss.dtype)

        if self.last_computed > self.recompute:
            self.percentile_val = np.percentile(self.vals, self.keepc * 100)
            if self.verbose:
                print('Using cutoff', self.percentile_val)
            self.last_computed = 0

        mask = (loss < self.percentile_val).type(loss.dtype)
        return mask
