import copy
import torch
import numpy as np


def mip_x(self):
    new = copy.deepcopy(self)
    if isinstance(self._data, torch.Tensor):
        tmp = torch.max(self._data, dim=1, keepdim=True).values.permute(0, 2, 1)
        new.data_(tmp)
    elif isinstance(self._data, np.ndarray):
        tmp = np.transpose(np.amax(self._data, axis=1, keepdims=True), [0, 2, 1])
        new.data_(tmp)
    else:
        raise ValueError("Check type of stack")

    return new

def mip_y(self):
    new = copy.deepcopy(self)
    if isinstance(self._data, torch.Tensor):
        tmp = torch.max(self._data, dim=0, keepdim=True).values.permute(0, 2, 1)
        new.data_(tmp)
    elif isinstance(self._data, np.ndarray):
        tmp = np.transpose(np.amax(self._data, axis=0, keepdims=True), [2, 1, 0])
        new.data_(tmp)
    else:
        raise ValueError("Check type of stack")

    return new

def mip_z(self):
    new = copy.deepcopy(self)
    if isinstance(self._data, torch.Tensor):
        tmp = torch.max(self._data, dim=2, keepdim=True).values
        new.data_(tmp)
    elif isinstance(self._data, np.ndarray):
        tmp = np.amax(self._data, axis=2, keepdims=True)
        new.data_(tmp)
    else:
        raise ValueError("Check type of stack")

    return new
