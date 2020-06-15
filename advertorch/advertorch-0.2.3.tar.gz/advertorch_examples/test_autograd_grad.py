import torch



x = torch.tensor([1., 2.])
x.requires_grad_()
y = x ** 2

# print(torch.autograd.grad(y, x, torch.tensor([1., 0.]), retain_graph=True))
# print(torch.autograd.grad(y, x, torch.tensor([0., 1.]), retain_graph=True))
