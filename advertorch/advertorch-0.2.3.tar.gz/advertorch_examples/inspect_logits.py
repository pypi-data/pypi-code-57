import torch
import torch.nn as nn
from test_softmax_stability import ConvNet


loss_fn = nn.CrossEntropyLoss(reduction="sum")


def generate_logits_grad(logits, label):
    logits = logits.detach().clone().requires_grad_()
    loss_fn(logits, label).backward()
    return logits.grad


def generate_input_grad(data, label, model):
    data = data.detach().clone().requires_grad_()
    loss_fn(model(data), label).backward()
    return data.grad


if __name__ == '__main__':
    model, data, label, logits = torch.load("logits.pt")
    batch_size = len(label)




    # print(torch.max(logits, dim=1)[0] - torch.min(logits, dim=1)[0])

    grad0 = generate_logits_grad(logits, label)
    grad1 = generate_logits_grad(
        logits - torch.max(logits, dim=1, keepdim=True)[0], label)


    neq_mask = grad1 != grad0

    print(grad0[neq_mask])
    print(grad1[neq_mask])


    signneq_mask = grad1.sign() != grad0.sign()
    print(signneq_mask.sum().item() / signneq_mask.nelement())


    model.minus_max = False
    grad0 = generate_input_grad(data, label, model)
    model.minus_max = True
    grad1 = generate_input_grad(data, label, model)

    signneq_mask = grad1.sign() != grad0.sign()
    print(signneq_mask.sum().item() / signneq_mask.nelement())


    diff_ratio = signneq_mask.view(batch_size, -1).sum(dim=1).float() / 784.
    logit_range = torch.max(logits, dim=1)[0] - torch.min(logits, dim=1)[0]


    cos = (diff_ratio * logit_range).sum() \
        / (torch.norm(diff_ratio) * torch.norm(logit_range))

    # max_sum = 0
    # for ii in range(100):
    #     for jj in range(100):
    #         val = ((logit_range > ii) == (diff_ratio > jj / 100.)).sum()
    #         if val > max_sum:
    #             max_sum, ii_max, jj_max = val, ii, jj

    # print(ii, jj / 100., max_sum)


    # TODO:
    # only from the gradient on the logit, it seems to be OK
    # So it should also have something to do with

    # print(neq_mask)

    # print(grad1 - grad0)


    # logits = logits - torch.max(logits, dim=1, keepdim=True)[0]



    # label_mask = torch.zeros_like(logits).byte()
    # label_mask[torch.arange(len(label)), label] = 1

    # nonlabel_mask = 1 - label_mask

    # # print(logits.grad)
    # print(logits.grad[label_mask].abs().mean().item())
    # print(logits.grad[nonlabel_mask].abs().mean().item())
