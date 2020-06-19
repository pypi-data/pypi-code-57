import os
import json
import binascii

import tensorflow as tf
import numpy as np
import torch
import hashlib

from researcher.logging import *
from researcher.assist import *
from researcher.torch_train import *

class MetricEarlyStopping(tf.keras.callbacks.Callback):
    """Stop training when the metric is at its min, i.e. the loss stops decreasing.

    Arguments:
        patience: Number of epochs to wait after min has been hit. After this
        number of no improvement, training stops.
        metric: The name of the metric to track. It is expected that this 
        metric will be recorded in the logs dictionary.
    """

    def __init__(self, metric, patience=0):
        super(MetricEarlyStopping, self).__init__()
        self.patience = patience
        self.best_weights = None
        self.metric = metric

    def on_train_begin(self, logs=None):
        self.wait = 0
        self.stopped_epoch = 0
        self.best = np.Inf

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.metric)
        if np.less(current, self.best):
            self.best = current
            self.wait = 0
            self.best_weights = self.model.get_weights()
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = epoch
                self.model.stop_training = True
                print('\nRestoring model weights from the end of epoch ')
                self.model.set_weights(self.best_weights)

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            print('\nEarly stopping occured at epoch: %05d' % (self.stopped_epoch + 1))


class LinearDecay(tf.keras.optimizers.schedules.LearningRateSchedule):
    def __init__(self, points):
        super(LinearDecay, self).__init__()
        
        assert points[0][0] == 0
        for i, p in enumerate(points):
            assert p[1] > 0
            
            if i < len(p) - 1:
                assert p[0] < points[i+1][0]
        
        self.points = points
    
    @tf.function
    def __call__(self, step):
        value = self.points[-1][1]
        for i, next_p in enumerate(self.points):
            if next_p[0] > step:
                prev_p = self.points[i-1]
                x_distance = next_p[0] - prev_p[0]
                y_distance = next_p[1] - prev_p[1]
                
                weight = y_distance / x_distance
                
                offset = weight * (step - prev_p[0]) 
                
                value = prev_p[1] + offset
        
        return value
                
    def get_config(self, step):
        return None
        

class Al(tf.keras.optimizers.schedules.LearningRateSchedule):
    def __init__(self, lr, steps_per_epoch):
        super(Al, self).__init__()

        self.lr = lr
        self.steps_per_epoch = steps_per_epoch
    
    @tf.function
    def __call__(self, step):
        return self.lr * (0.2 ** tf.math.floor(1 + step / self.steps_per_epoch))
                
    def get_config(self, step):
        return None

def get_torch_optimizer_maker(id, max_lr, steps):
    if id == "adam":
        return lambda model_parameters: torch.optim.Adam(model_parameters, lr=max_lr)
    if id == "adamw":
        def make_adam_optimizer(parameters):
            no_decay = [
                "bias",
                "LayerNorm.bias",
                "LayerNorm.weight"
            ]
            parameter_weights = [
                {
                    'params': [
                        p for n, p in parameters if not any(nd in n for nd in no_decay)
                    ], 
                    'weight_decay': 0.001
                },
                {
                    'params': [
                        p for n, p in parameters if any(nd in n for nd in no_decay)
                    ], 
                    'weight_decay': 0.0
                },
            ]
            optimizer = torch.optim.AdamW(parameter_weights, lr=max_lr)

            return optimizer

        return make_adam_optimizer

    ValueError("unrecognized id for torch optimizer: " + id)

def save_experiment(path, name, parameters, results):
    parameters["results"] = results
    file_name = path + name + ".json"
    with open(file_name, "w") as f:
        f.write(json.dumps(parameters, indent=4))

    os.chmod(file_name, 0o777)

def load_experiment(path, name):
    file_name = path + name + ".json"
    if os.path.isfile(file_name): 
        with open(file_name, "r") as f:
            params = json.load(f)
        return params

    return None

def tf_model_maker(superset, params):
    return make_tf_model(
        params["max_len"],
        params["dropout"],
        params["activation"],
        superset.TF_MODELS[params["model_fn"]],
        superset.TF_LOSSES[params["loss_fn"]],
        params["batch_size"],
        superset.get_tf_optimizer_maker(
            params["optimizer_id"],
            params["max_lr"],
            params["epochs"],
            params["steps_per_epoch"],
            params["min_lr"],
        ),
        params["loss_weights"],
        params["custom"],
    )

def make_tf_model(
    max_len, 
    dropout, 
    activation, 
    model_fn, 
    loss_fn, 
    batch_size, 
    optimizer_maker,
    loss_weights=None,
):
    def make():
        model, _ = model_fn(max_len, dropout=dropout, activation=activation)
        
        model.compile(loss=loss_fn, optimizer=optimizer_maker(), loss_weights=loss_weights)
        return model
    
    return make

def torch_model_maker(superset, params):
    return make_torch_model(
        superset.TORCH_MODELS[params["model_fn"]],
        superset.TORCH_LOSSES[params["loss_fn"]],
        get_torch_optimizer_maker(
            params["optimizer_id"],
            params["max_lr"],
            params["epochs"] * params["steps_per_epoch"],
        ),
    )

def make_torch_model(model_maker, loss_maker, optimizer_maker):
    assert torch.cuda.is_available()
    device = torch.device("cuda:0")

    def make():
        model = model_maker()
        model.to(device)

        return model, optimizer_maker(model.named_parameters()), loss_maker()

    return make

def get_hash(params):
    return hex(int(binascii.hexlify(hashlib.md5(json.dumps(params).encode("utf-8")).digest()), 16))[2:]