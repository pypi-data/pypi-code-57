import json
from worker import API
from worker.framework.mixins import LoggingMixin, RollbarMixin
from worker.data.enums import LambdaStates


class TaskHandler(LoggingMixin, RollbarMixin):
    def __init__(self, *args, **kwargs) -> None:
        self._api = kwargs.pop("api", API())
        super().__init__(*args, **kwargs)
        self.event = {}
        self.task_id = ""
        self.task = {}

    def process(self, *args, **kwargs):
        """
        Provides a placeholder for actual logic code for each app.
        e.g. Instantiate the app and run it
        This method must be overriden by each app
        :return:
        """
        raise NotImplementedError("process method must be defined before instantiating this class")

    def run_process(self, event: dict, *args, **kwargs):
        """
        Runs the task handler workflow.
        This method would be called after instantiation of the TaskHandler class
        :param event:
        :return:
        """
        self.event = event
        self.task_id = self.event.get("task_id")
        self.get_task(self.task_id)

        try:
            data = self.process(self.event, *args, **kwargs)
            request_body = {
                "task": {
                    "payload": {
                        "data": data,
                        "message": LambdaStates.SUCCEEDED.value
                    }
                }
            }
            self.update_task(self.task_id, "success", request_body)
            return data

        except Exception as exception:
            request_body = {
                "task": {
                    "fail_reason": f"Message: {LambdaStates.FAILED.value}, Exception: {exception}"
                }
            }
            self.update_task(self.task_id, "fail", request_body)
            raise exception

    def get_task(self, task_id: str) -> None:
        """
        Gets the task from API endpoint for the given task_id
        :param task_id:
        :return:
        """
        path = "/v2/tasks/{0}".format(task_id)
        self.task = self._api.get(path).data

    def update_task(self, task_id: str, status: str, request_body: dict) -> None:
        """
        Updates the task status on the API endpoint in case of success or failure
        :param task_id:
        :param status: [success, fail]
        :param request_body:
        :return:
        """
        path = "/v2/tasks/{0}/{1}".format(task_id, status)
        self.task = self._api.put(path, data=json.dumps(request_body)).data
