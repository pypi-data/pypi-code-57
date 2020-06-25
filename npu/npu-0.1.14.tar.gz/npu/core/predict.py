# @wait_task
import requests

from .common import getToken, checkData, sliceData
from .Task import Task
from .web.urls import PREDICT_URL
from .Dataset import Dataset
from .Model import Model


def predict(model, data, asynchronous=False, callback=None):
    inference_data = checkData(data)
    task_id = model.task_id if isinstance(model, Task) else ""
    resp = predictApi(model, inference_data, task_id)
    task = Task(resp.json(), callback)
    if not asynchronous:
        task.wait()
    return task


def predictApi(model, data_id, task_id):
    x = y = None
    data_name = ""
    if isinstance(data_id, dict):
        data_id, x, y = sliceData(data_id)
    if isinstance(data_id, Dataset):
        data_name = data_id.id
        data_id = ""
    params = {"dataId": data_id, "token": getToken(), "task_id": task_id, "x": x, "y": y, "data_name": data_name}
    if isinstance(model, Model):
        params["model_name"] = model.name
    elif model != "" and not isinstance(model, Task):
        params["modelId"] = model
    response = requests.get(PREDICT_URL, params=params)
    if response.status_code != 200:
        raise ValueError(response.text)
    return response


