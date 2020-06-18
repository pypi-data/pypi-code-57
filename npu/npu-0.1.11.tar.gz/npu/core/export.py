# @wait_task
import os
import re

import requests

from .common import getToken
from .Task import Task
from .web.urls import EXPORT_URL
from .Model import Model


def export(model, path):
    if isinstance(model, Task):
        task = Task(model.task_id, show=False)
        task.wait()
        model = task.get_result()
    return exportApi(model, path)


def exportApi(model, path):
    params = {"token": getToken()}
    if isinstance(model, Model):
        params["model_name"] = model.name
    elif model != "":
        params["modelId"] = model
    response = requests.get(EXPORT_URL, params=params, stream=True)
    if response.status_code == 200:
        d = response.headers['content-disposition']
        filename = re.findall("filename=(.+)", d)[0]
        print(filename)
        with open(os.path.join(path, filename), "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                # writing one chunk at a time to file
                if chunk:
                    file.write(chunk)
        print("Model exported.")
    else:
        raise Exception("{}".format(response.content))
    return True


