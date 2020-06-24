from ..core.common import Config
from ..application.domain.models import Task
from ..application.domain.common import QueryParser
from ..application.domain.repositories import MemoryTaskRepository
from .base_factory import BaseFactory


class CheckFactory(BaseFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = config

    # Repositories
    def memory_task_repository(
            self, query_parser: QueryParser
    ) -> MemoryTaskRepository:

        memory_task_repository = super().memory_task_repository(
            query_parser)

        memory_task_repository.load({'default': {
            "1": Task(id='1', name='Define WBS'),
            "2": Task(id='2', name='Deploy Servers'),
            "3": Task(id='3', name='Design Website')
        }})
        return memory_task_repository
