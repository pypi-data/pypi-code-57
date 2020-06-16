from typing import TypeVar

from zope.interface import implementer

from moksh_orchestrator.framework.apis.execution_context import ExecutionContext
from moksh_orchestrator.framework.apis.dataset import Dataset
from moksh_orchestrator.logging.moksh_logger import MokshLogger

T = TypeVar('T')


@implementer(Dataset)
class DatasetImpl:

    def __init__(self):
        self.cnt = 0;

    def execute(self, execution_context: ExecutionContext) -> ExecutionContext:
        self.cnt = self.cnt + 1
        MokshLogger.moksh_log_debug(
            'Called {} with execution_context {}'.format(self.__class__.__name__, execution_context))
        MokshLogger.moksh_log_debug('Dataset called {}'.format(self.cnt))
