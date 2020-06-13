import abc

class TaskListener(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def onTaskUpdate(self, task):
        raise NotImplementedError()

class Task():
    def __init__(self, listener, task_name, task_run_id, task_system='unknown'):
        self.listener = listener

        self.task_name = task_name
        self.task_run_id = task_run_id

        self.task_status = None
        self.task_input = None
        self.task_output = None
        self.task_metadata = None
        self.task_logs = None
        self.task_system = 'unknown'
        self.task_language = 'python'

    def update(self, task_status=None, task_input=None, task_output=None, task_metadata=None, task_system=None, task_logs=None):
        if task_status is not None:
            self.task_status = task_status
        if task_input is not None:
            self.task_input = task_input
        if task_output is not None:
            self.task_output = task_output
        if task_metadata is not None:
            self.task_metadata = task_metadata
        if task_system is not None:
            self.task_system = task_system
        if task_logs is not None:
            self.task_logs = task_logs

        self.listener.onTaskUpdate(self)

        return self
