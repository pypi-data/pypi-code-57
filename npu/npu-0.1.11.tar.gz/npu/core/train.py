# @wait_task
import requests

from .Dataset import Dataset
from .common import getToken, checkData, sliceData
from .Task import Task
from .web.urls import TRAIN_URL
from .Model import Model


def train(model, training_data, test_data, batch_size, epochs, optimiser, loss, asynchronous, callback):
    training_data = checkData(training_data)
    test_data = checkData(test_data)
    task_id = model.task_id if isinstance(model, Task) else ""
    task = Task(trainApi(model, training_data, test_data, optimiser, loss, batch_size, epochs, task_id).json(),
                callback)
    if not asynchronous:
        task.wait(show_progress=True)
        print("Model finished training")
    return task


def trainApi(model_id, train_id, test_id, optimiser, loss, batch_size, epochs, task_id=""):
    train_x = train_y = test_x = test_y = None
    train_name = ""
    test_name = ""
    if isinstance(train_id, dict):
        train_id, train_x, train_y = sliceData(train_id)
    if isinstance(test_id, dict):
        test_id, test_x, test_y = sliceData(test_id)
    if isinstance(train_id, Dataset):
        train_name = train_id.id
        train_id = ""
    if isinstance(test_id, Dataset):
        test_name = test_id.id
        test_id = ""
    params = {"trainId": train_id, "testId": test_id, "loss": loss,
              "token": getToken(), "batch_size": batch_size, "epochs": epochs, "task_id": task_id, "train_x": train_x,
              "train_y": train_y, "test_x": test_x, "test_y": test_y, "train_name": train_name, "test_name": test_name}

    if isinstance(model_id, Model):
        params["model_name"] = model_id.name
    elif model_id != "" and not isinstance(model_id, Task):
        params["modelId"] = model_id
    response = requests.get(TRAIN_URL, params=params, json=optimiser)
    if response.status_code != 200:
        raise ValueError(response.text)
    return response
