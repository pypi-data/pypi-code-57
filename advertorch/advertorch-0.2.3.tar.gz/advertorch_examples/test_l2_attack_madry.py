from advertorch.attacks import L2PGDAttack
from advertorch.attacks import LinfPGDAttack
from advertorch_examples.utils import TRAINED_MODEL_PATH
import os
import torch
import torch.nn as nn

from advertorch.utils import predict_from_logits
from advertorch_examples.utils import get_mnist_test_loader


class LeNet5(nn.Module):

    def __init__(self, offset=0., minus_max=False):
        super(LeNet5, self).__init__()
        self.offset = offset
        self.minus_max = minus_max
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1, stride=1)
        self.relu1 = nn.ReLU(inplace=True)
        self.maxpool1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1, stride=1)
        self.relu2 = nn.ReLU(inplace=True)
        self.maxpool2 = nn.MaxPool2d(2)
        self.linear1 = nn.Linear(7 * 7 * 64, 200)
        self.relu3 = nn.ReLU(inplace=True)
        self.linear2 = nn.Linear(200, 10)

    def forward(self, x):
        out = self.maxpool1(self.relu1(self.conv1(x)))
        out = self.maxpool2(self.relu2(self.conv2(out)))
        out = out.view(out.size(0), -1)
        out = self.relu3(self.linear1(out))
        out = self.linear2(out)
        # out = out / 2.
        out = out + self.offset
        if self.minus_max:
            out = out - torch.max(out, dim=1, keepdim=True)[0]
        return out


if __name__ == '__main__':
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    filename = "mnist_lenet5_advtrained.pt"
    model = LeNet5(minus_max=True)
    model.load_state_dict(
        torch.load(os.path.join(TRAINED_MODEL_PATH, filename)))
    model.to(device)
    model.eval()


    batch_size = 100
    loader = get_mnist_test_loader(batch_size=batch_size)
    for cln_data, true_label in loader:
        break
    cln_data, true_label = cln_data.to(device), true_label.to(device)

    eps = 2.
    eps_iter = eps / 4
    nb_iter = 1000
    adversary = L2PGDAttack(
        model, loss_fn=nn.CrossEntropyLoss(reduction="sum"), eps=eps,
        nb_iter=nb_iter, eps_iter=eps_iter,
        rand_init=False, clip_min=0.0, clip_max=1.0,
        targeted=False)


    adv = adversary.perturb(cln_data, true_label)

    model.offset = 0.
    model.minus_max = False
    advpred = predict_from_logits(model(adv))
    print((advpred == true_label).float().mean().item())
