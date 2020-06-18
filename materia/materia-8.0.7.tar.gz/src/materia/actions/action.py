import abc

__all__ = ["Action", "ActionSignal"]


class Action(abc.ABC):
    @abc.abstractmethod
    def run(self, node, tasks, links, done):
        pass


class ActionSignal(Exception):
    def __init__(self, message=None, result=None, actions=None):
        # result and actions have default values only so they can come after message which has a default value
        super().__init__(message)
        self.result = result
        self.actions = actions
