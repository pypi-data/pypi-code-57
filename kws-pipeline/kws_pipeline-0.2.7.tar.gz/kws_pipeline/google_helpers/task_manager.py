import pickle
from urllib.parse import urljoin

from ..queue.abc import TaskManagerABC

from google.cloud import tasks_v2


class GoogleTaskManager(TaskManagerABC):
    def __init__(self, project_id, location, queue, worker_url=""):
        self.task_client = tasks_v2.CloudTasksClient()
        self.parent = self.task_client.queue_path(project_id, location, queue)
        self.worker_url = worker_url

    def _create_task(self, binary_data, handler_uri):
        if not self.worker_url:
            task = {
                "app_engine_http_request": {
                    "http_method": "POST",
                    "relative_uri": handler_uri,
                    "body": binary_data,
                }
            }

        else:
            task = {
                "http_request": {
                    "url": urljoin(self.worker_url, handler_uri),
                    "http_method": "POST",
                    "body": binary_data,
                }
            }

        return task

    def _enqueue(self, task):
        return self.task_client.create_task(self.parent, task)
