import sys
import time

import requests
from progress.bar import Bar
from progress.spinner import Spinner

from .web.urls import TASK_STATUS_URL

import threading

class Task:

    def __init__(self, task_id, callback=None, show=True):
        self.task_id = task_id
        self.task_result = ""
        self.task_type = ""
        self.progress = 0
        self.task_state = "PENDING"
        self.callback = callback
        if self.callback:
            t = threading.Thread(target=self.callback_thread)
            t.start()
        if show:
            self.update()
            print("Started {0}. View status at https://dashboard.neuro-ai.co.uk/tasks/{1}".format(self.task_type.lower(), task_id))

    def wait(self, show_progress=False):
        if show_progress:
            bar = Bar('Training', suffix='%(percent)d%%', stream=sys.stdout)
        else:
            spinner = Spinner('Task in Progress')
        while not self.finished():
            time.sleep(0.1)
            if show_progress:
                bar.goto(self.progress*100)
            else:
                spinner.next()
        if self.task_state == "FAILURE":
            self.update(include_result=True)
            raise Exception("ERROR:" + str(self.task_result))
        if show_progress:
            bar.finish()
        else:
            spinner.finish()

    def callback_thread(self):
        self.get_result()
        self.callback(self.task_result)

    def get_result(self):
        self.wait()
        self.update(include_result=True)
        return self.task_result

    def update(self, include_result=False):
        params = {"include_result": include_result}
        response = requests.get(TASK_STATUS_URL + self.task_id, params=params)
        response = response.json()
        self.task_state = response["state"]
        self.task_type = response["taskType"]
        self.progress = response["progress"]
        if "result" in response:
            self.task_result = response["result"]

    def __str__(self):
        return str(self.get_result())

    def finished(self):
        self.update()
        return self.task_state in ("COMPLETE", "FAILURE")


