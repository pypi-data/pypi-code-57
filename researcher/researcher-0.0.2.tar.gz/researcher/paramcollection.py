
from researcher.starters import *

class ParamCollection():
    def __init__(self):
        self.TF_CALLBACKS = {}
        self.TORCH_CALLBACKS = {}
        self.TF_LOSSES = {}
        self.TORCH_LOSSES = {}
        self.LOSS_LOGGER_MAKERS = {}
        self.TF_MODELS = {}