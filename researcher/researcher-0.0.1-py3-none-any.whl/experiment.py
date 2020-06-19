import datetime
import os
import time
import gc

import json
import tensorflow as tf
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter

from researcher.logging import *
from researcher.assist import *
from researcher.starters import *
from researcher.kfold import *
from researcher.torch_train import *

def write_history(histories, write_fn):
    n_histories = len(histories)
    for k in histories[0]:
        for i in range(len(histories[0][k])):
            s = 0
            value_count = 0
            for h in histories:
                if i < len(h[k]):
                    s += h[k][i]
                    value_count += 1
            
            write_fn(k, s/value_count, i)

def log_histories(history, writer, val_writer):
    train_histories = []
    val_histories = []

    for h in history:
        train_history = {}
        val_history = {}
        for k in h:
            if k[:4] == "val_":
                val_history[k[4:]] = h[k]
            else:
                train_history[k] = h[k]
        train_histories.append(train_history)
        val_histories.append(val_history)

    write_history(train_histories, writer)
    write_history(val_histories, val_writer)   

def kfold_tf_experiment(name, make_model, train_gens, epochs,steps_per_epoch, batch_size,
                    n_folds, callback_makers, val_gens, workers,
                    save, model_save_path, log_path):

    assert val_gens is None or len(train_gens) == len(val_gens)
  
    tf.keras.backend.clear_session()
    val_gens = val_gens or [None for i in train_gens]

    start_time = datetime.datetime.now()
    log_dir = "{}/{}_{}".format(log_path, name, start_time.strftime("%Y%m%d-%H%M%S"))
    
    tb_writer = tf.summary.create_file_writer(log_dir + "_train")
    tb_writer.set_as_default()
    val_tb_writer = tf.summary.create_file_writer(log_dir + "_val")
    val_tb_writer.set_as_default()

    histories = []

    for fold, gen in enumerate(train_gens):
        print("\n\n========== Starting Fold {} =========".format(fold))
        
        # Logging callbacks
        val_history = {}
        batch_history = {}
        batch_losses = BatchWriter(make_dict_writer(batch_history), batch_metrics=["loss"])
        callbacks = [batch_losses] + [make() for make in callback_makers]

        model = make_model()

        model.fit(
            gen, 
            batch_size=batch_size,
            epochs=epochs,
            steps_per_epoch=steps_per_epoch,
            verbose=1,
            callbacks=callbacks,
            validation_data=val_gens[fold]
        )
        
        histories.append({**model.history.history, **batch_history})
        
        if save:
            model.save_weights(model_weights_file(model_save_path, name, fold=fold))
        
        del model
        gc.collect()
        tf.keras.backend.clear_session()
    
    log_histories(histories, make_write_to_tb(tb_writer), make_write_to_tb(val_tb_writer))

    return histories


# ---------------------------------------------------------------------------------------------------------
#
#                                       PARAMETER EXPERIMENTING 
#
# ---------------------------------------------------------------------------------------------------------

def get_experiment_methods(superset, params):
    assert not (params["model_fn"] in superset.TF_MODELS and params["model_fn"] in superset.TORCH_MODELS)

    if params["model_fn"] in superset.TF_MODELS:
        return tf_model_maker(params), kfold_tf_experiment, superset.TF_CALLBACKS
    
    raise NotImplementedError
    return torch_model_maker(params), None , superset.TORCH_CALLBACKS

def process_params(superset, params):
    param_hash = get_hash(params)

    model_fn, experiment_fn, callback_map = get_experiment_methods(params)   

    return param_hash, model_fn, experiment_fn, callback_map

def run_param_kfold_experiment(superset, params,  model_save_path, log_path, workers=1, save=False, test=False):
    param_hash, model_fn, experiment_fn, callback_map = process_params(params)

    print("running experiment: {} {}".format(params["description"], param_hash))
    
    if test:
        params["log_to"] = "test"
        params["epochs"] = 2
        params["save"] = False

    results = experiment_fn(
        "{}___{}".format(params["description"],param_hash[:8]),
        model_fn,
        params["train_gens"],
        params["epochs"],
        params["steps_per_epoch"],
        params["batch_size"],
        [callback_map[i](**params["callback_args"]) for i in params["callback_makers"]],
        params["val_gens"],
        workers,
        save,
        model_save_path,
        log_path,
    )

    if not test:
        save_experiment("{}_{}".format(params["description"],param_hash), parameters=params, results=results)
    else:
        save_experiment("test", parameters=params, results=results)
    
