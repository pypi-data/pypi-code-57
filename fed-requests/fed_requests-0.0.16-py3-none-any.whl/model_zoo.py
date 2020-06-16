from torch import nn as nn
from torch import optim as optim


class LinearRegression(nn.Module):
    def __init__(self, in_dim, out_dim):
        super(LinearRegression, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(in_dim, out_dim),
            nn.Sigmoid()
        )

        self.loss_function = nn.NLLLoss()

    def forward(self, x):
        return self.fc(x)


class ModelPipeline(nn.Module):
    def __init__(self, in_dim, out_dim, model_name='linear_regression'):
        super(ModelPipeline, self).__init__()

        self.model = self.get_model(in_dim, out_dim, model_name)
        self.optimizer = optim.Adam(self.model.parameters())

        # Historic
        self.train_loss = []

    def get_model(self, in_dim, out_dim, model_name):
        model_name = model_name.lower()  # A bit of robustness
        if model_name == 'linear_regression':
            return LinearRegression(in_dim=in_dim, out_dim=out_dim)
        else:
            raise NotImplementedError(f'Model {model_name} is not implemented in this version.')

    def log_loss(self, loss):
        self.train_loss.append(loss.item())

    def forward(self, x):
        return self.model(x)

    def fit(self, data_loader, epochs):
        for epoch in range(epochs):
            for data, target in data_loader:
                self.optimizer.zero_grad()

                pred = self.model(data)
                loss = self.model.loss_function(pred, target)
                loss.backward()

                self.log_loss(loss)
                self.optimizer.step()
