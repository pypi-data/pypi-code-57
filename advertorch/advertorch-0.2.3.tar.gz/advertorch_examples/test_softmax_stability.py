from advertorch.attacks import L2PGDAttack
from advertorch.attacks import LinfPGDAttack
from advertorch_examples.utils import TRAINED_MODEL_PATH
import os
import torch
import torch.nn as nn

from advertorch.utils import predict_from_logits
from advertorch.loss import SoftLogitMarginLoss
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
        out = out * 5
        out = out + self.offset
        if self.minus_max:
            out = out - torch.max(out, dim=1, keepdim=True)[0]
        return out


class ConvNet(nn.Module):
    def __init__(
            self, num_classes=10, return_intermediate=False,
            offset=0., minus_max=False):
        super(ConvNet, self).__init__()
        self.return_intermediate = return_intermediate
        self.minus_max = minus_max
        self.offset = offset

        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d((2, 2))
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.layer3 = nn.Sequential(
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
        )

        self.layer4 = nn.Sequential(
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Dropout(0.5)
        )

        self.layer5 = nn.Sequential(
            nn.Linear(256, num_classes)
        )

        self.layers = [self.layer1, self.layer2, self.layer3, self.layer4]

    def forward(self, x):
        relus = list()

        output = self.layer1(x)
        relus.append(output)

        output = self.layer2(output)
        output = output.view(-1, 128 * 4 * 4)
        relus.append(output)

        output = self.layer3(output)
        relus.append(output)

        output = self.layer4(output)
        relus.append(output)

        logits = self.layer5(output)

        # import ipdb
        # ipdb.set_trace()

        # logits = logits / 5.
        # print(torch.max(torch.max(logits, dim=1)[0]
        #                 - torch.min(logits, dim=1)[0]))

        logits = logits + self.offset

        if self.minus_max:
            logits = logits - torch.max(logits, dim=1, keepdim=True)[0]

        if self.return_intermediate:
            return logits, relus
        else:
            return logits


if __name__ == '__main__':
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    # loss_fn = nn.CrossEntropyLoss(reduction="sum")
    loss_fn = SoftLogitMarginLoss(reduction="sum")


    filename = "mnist_lenet5_clntrained.pt"
    model = LeNet5()
    model.load_state_dict(
        torch.load(os.path.join(TRAINED_MODEL_PATH, filename)))
    model.to(device)
    model.eval()

    # filename = "model_best.pth.tar"
    # model = ConvNet()
    # model.load_state_dict(torch.load(filename)['state_dict'])
    # model.to(device)
    # model.eval()

    situations = [
        (-1000000000000, False),
        (-10000000000, False),
        (-100000000, False),
        (-1000000, False),
        (-1000, False),
        (-40, False),
        (0, False),
        (40, False),
        (1000, False),
        (1000000, False),
        (100000000, False),
        (10000000000, False),
        (1000000000000, False),
        (-1000000000000, True),
        (-10000000000, True),
        (-100000000, True),
        (-1000000, True),
        (-1000, True),
        (-40, True),
        (0, True),
        (40, True),
        (1000, True),
        (1000000, True),
        (100000000, True),
        (10000000000, True),
        (1000000000000, True),
    ]


    batch_size = 100
    loader = get_mnist_test_loader(batch_size=batch_size)
    for cln_data, true_label in loader:
        break
    cln_data, true_label = cln_data.to(device), true_label.to(device)


    logits = model(cln_data)
    torch.save((model, cln_data, true_label, logits), "logits.pt")

    # raise


    # for eps in [0.1, 0.2, 0.3]:
    for eps in [0.3]:
        # eps_iter = eps / 4
        # nb_iter = 100
        eps_iter = eps
        nb_iter = 1
        adversary = LinfPGDAttack(
            model, loss_fn=loss_fn, eps=eps,
            nb_iter=nb_iter, eps_iter=eps_iter,
            rand_init=False, clip_min=0.0, clip_max=1.0,
            targeted=False)

        for offset, minus_max in situations:
            model.offset = offset
            model.minus_max = minus_max
            adv = adversary.perturb(cln_data, true_label)

            # print(torch.norm(adv - cln_data))
            # print((adv != cln_data).sum().item())

            model.offset = 0.
            model.minus_max = False
            advpred = predict_from_logits(model(adv))
            print(
                "eps: {}, offset: {}, minus_max: {}, acc: {:.2f}".format(
                    eps, offset, minus_max,
                    (advpred == true_label).float().mean().item()
                ))


    # eps = 2.
    # eps_iter = eps / 4
    # nb_iter = 100
    # adversary = L2PGDAttack(
    #     model, loss_fn=nn.CrossEntropyLoss(reduction="sum"), eps=eps,
    #     nb_iter=nb_iter, eps_iter=eps_iter,
    #     rand_init=False, clip_min=0.0, clip_max=1.0,
    #     targeted=False)



# https://www.google.com/search?q=pytorch+numerically+stable&oq=pytorch+numerically+stable&aqs=chrome..69i57.6799j0j7&sourceid=chrome&ie=UTF-8

# https://github.com/pytorch/pytorch/issues/1546

# https://discuss.pytorch.org/t/branching-for-numerical-stability/15763

# https://github.com/kleincup/DEEPSEC/issues/3

# https://github.com/BorealisAI/advertorch/issues/63
