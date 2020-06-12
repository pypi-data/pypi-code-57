import time

import torch

from yqn_pytorch_framework.device import tensor_load_device


def model_time_estimate(device, get_model, loop=100):
    model = tensor_load_device(get_model(), device).eval()
    torch.cuda.synchronize(device)
    start = time.time()
    with torch.no_grad():
        for i in range(loop):
            result = model(model.get_default_input())
    torch.cuda.synchronize(device)
    end = time.time()
    print(f"{model._get_name()} GPU PerLoop Cost {(end - start) * 1000 / loop:<5.2f}ms")
