import torch

class AverageBinaryAccuracyTorch:
    def __init__(self):
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, y_pred, y_test):

        y_pred_tag = torch.round(torch.sigmoid(y_pred))
        correct_results_sum = (y_pred_tag == y_test).sum().float()
        acc = correct_results_sum/y_test.shape[0]
        acc = torch.round(acc * 100)

        self.sum += acc * y_test.shape[0]
        self.count += y_test.shape[0]
        self.avg = self.sum / self.count
    