import json
import sklearn.metrics
import time
import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import DataLoader


def generate_batch(batch):
    feature = torch.tensor([entry[0] for entry in batch], dtype=torch.float32)
    label = torch.tensor([entry[1] for entry in batch], dtype=torch.float32)
    label = label.unsqueeze(1)
    return feature, label


class Trainer():
    def __init__(self, model, train_data, dev_data):
        self.train_data = train_data
        self.dev_data = dev_data
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.criterion = model.criterion()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=1.0)
        self.scheduler = torch.optim.lr_scheduler.StepLR(self.optimizer, 1, gamma=0.9)

    def train(self, batch_size=128):
        # Train the model
        train_loss = 0
        train_acc = 0
        data = DataLoader(self.train_data, batch_size=batch_size, shuffle=True, collate_fn=generate_batch)
        for i, (inputs, cls) in enumerate(data):
            self.optimizer.zero_grad()
            inputs, cls = inputs.to(self.device), cls.to(self.device)
            output = self.model(inputs)
            self.loss = self.criterion(output, cls)
            self.loss.backward()
            self.optimizer.step()

            train_loss += self.loss.item()
            train_acc += ((output > 0.5) == cls).sum().item()

        # Adjust the learning rate
        self.scheduler.step()

        train_len = len(self.train_data)
        return train_loss / train_len, train_acc / train_len

    def dev(self, batch_size=128):
        loss = 0
        acc = 0
        data = DataLoader(self.dev_data, batch_size=batch_size, collate_fn=generate_batch)
        y = []
        pred = []
        for inputs, cls in data:
            y.extend(cls.tolist())
            inputs, cls = inputs.to(self.device), cls.to(self.device)

            with torch.no_grad():
                output = self.model(inputs)
                loss = self.criterion(output, cls)
                loss += loss.item()
                acc += ((output > 0.5) == cls).sum().item()
                pred.extend(output.cpu().tolist())

        auc_roc = sklearn.metrics.roc_auc_score(y, pred)
        dev_len = len(self.dev_data)
        return loss / dev_len, acc / dev_len, auc_roc

    def predict(self, infer_data, batch_size=128):
        data = DataLoader(infer_data, batch_size=batch_size, collate_fn=generate_batch)
        pred = []
        for inputs, _ in data:
            inputs = inputs.to(self.device)
            with torch.no_grad():
                output = self.model(inputs)
                pred.extend(output.cpu().tolist())

        return pred

    def train_loop(self, batch_size=128, n_epochs=50):
        min_valid_loss = float('inf')
        for epoch in range(n_epochs):
            start_time = time.time()
            train_loss, train_acc = self.train(batch_size)
            valid_loss, valid_acc, valid_aucroc = self.dev(batch_size)
            secs = int(time.time() - start_time)
            mins = secs / 60
            secs = secs % 60

            print('Epoch: %d, | time in {%d} minutes, {%d} seconds.' % (epoch + 1, mins, secs))
            print('\tLoss: %.4f(train)\t|\tAcc: %.1f%%(train)' % (train_loss, train_acc * 100))
            print('\tLoss: %.4f(test)\t|\tAcc: %.1f%%(test)|\tAuc: %.1f%%(test)' % (valid_loss, valid_acc * 100, valid_aucroc * 100))

    
