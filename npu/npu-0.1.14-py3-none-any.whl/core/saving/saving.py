import glob
import tarfile
import os
from tempfile import TemporaryFile
import numpy as np


def save_model(model, library: str):
    model_path = model
    if not isinstance(model, str):
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        model_path = "tmp/tmp_model"
        if library == "pytorch":
            import torch
            import dill
            model_path += ".pt"
            torch.save(model, model_path, pickle_module=dill)
        elif library == "keras":
            model_path += ".h5"
            import keras
            with keras.backend.get_session().graph.as_default():
                model.save_model(model_path)
        elif library == "mxnet":
            model_path += ".tar"
            model.export(model_path)
            # with tarfile.open(model_path, "w") as tar:
            #     for file in glob.glob(model_path + "dir/*"):
            #         tar.add(file, arcname=os.path.basename(file))
            with tarfile.open(model_path, "w") as tar:
                jsonname = model_path + "-symbol.json"
                paramname = model_path + "-0000.params"
                tar.add(jsonname, arcname=os.path.basename(jsonname))
                tar.add(paramname, arcname=os.path.basename(paramname))
        elif library == "TF":
            model_path += ".tar"
            model.save(model_path + "dir")
            with tarfile.open(model_path, "w") as tar:
                for file in glob.glob(model_path + "dir/*"):
                    tar.add(file, arcname=os.path.basename(file))
        elif library == "TF1":
            model_path += ".pb"
        else:
            raise ValueError("Model type: " + str(library) + " not defined")
    return model_path

    # if model_type is ModelType.ONNX:
    #     onnx.save(model, file_path)
    # elif model_type is ModelType.TF1:
    #     pass
        # tf.saved_model.save(model, "./dd.pb")
        # tf.compat.v1.saved_model.save(model, "tmp")
        # raise ValueError("Tensorflow 1 incompatible. Please use .pb file directly if using Tensorflow 1.")


def save_data(data):
    file = TemporaryFile()
    if isinstance(data, (tuple, list)):
        if not all([isinstance(x, np.ndarray) for x in data]):
            raise TypeError("Either train or validation data is not in numpy array format.")
        dict_data = {str(i): data[i] for i in range(0, len(data))}
        np.savez_compressed(file, **dict_data)
    else:
        if not isinstance(data, np.ndarray):
            raise TypeError("Data is not in numpy array format.")
        np.savez_compressed(file, data)
    file.seek(0)
    return file


def determine_model(model):
    try:
        from torch import nn
        if isinstance(model, nn.Module):
            return "pytorch"
    finally:
        pass
    try:
        from tensorflow.keras import Model
        if isinstance(model, Model):
            return "TF"
    finally:
        pass
    try:
        import mxnet
        if isinstance(model, mxnet.gluon.nn.Block):
            return "mxnet"
    finally:
        return ""
