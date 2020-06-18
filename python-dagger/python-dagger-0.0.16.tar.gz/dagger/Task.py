import abc

from dagger.logger import logger

class TaskListener(metaclass=abc.ABCMeta):
    """
    TODO: Is it actually valuable to use a change listener for this?

    Args:
        metaclass ([type], optional): [description]. Defaults to abc.ABCMeta.

    Raises:
        NotImplementedError: [description]
    """
    @abc.abstractmethod
    def onTaskUpdate(self, task):
        raise NotImplementedError()

class Task():
    def __init__(self, task_name, task_run_id, task_system='unknown', listener=None):
        self.listener = listener

        self.task_name = task_name
        self.task_run_id = task_run_id

        self.task_status = None
        self.task_input = {}
        self.task_output = {}
        self.task_metadata = {}
        self.task_logs = {}
        self.task_system = 'unknown'
        self.task_language = 'python'

    def setListener(self, listener):
        self.listener = listener

    def notifyListener(self):
        if self.listener is not None:
            self.listener.onTaskUpdate(self)

    def update(self, task_status=None, task_input=None, task_output=None, task_metadata=None, task_system=None, task_logs=None, **other_kwargs):
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
        if other_kwargs is not None:
            logger.info('Task.update got unknown kwargs %s', other_kwargs)

        self.notifyListener()

        return self
