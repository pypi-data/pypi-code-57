from abc import ABC, abstractmethod
from ..domain.repositories import (
    TaskRepository, LinkRepository, ClassifierRepository,
    ScheduleRepository, SlotRepository)
from ..domain.common import QueryDomain, RecordList


class EstimarkInformer(ABC):

    @abstractmethod
    async def search(self,
                     model: str,
                     domain: QueryDomain = None,
                     limit: int = 0,
                     offset: int = 0) -> RecordList:
        """Returns a list of <<model>> dictionaries matching the domain"""


class StandardEstimarkInformer(EstimarkInformer):
    def __init__(self, task_repository: TaskRepository,
                 link_repository: LinkRepository,
                 classifier_repository: ClassifierRepository,
                 schedule_repository: ScheduleRepository,
                 slot_repository: SlotRepository) -> None:
        self.task_repository = task_repository
        self.link_repository = link_repository
        self.classifier_repository = classifier_repository
        self.schedule_repository = schedule_repository
        self.slot_repository = slot_repository

    def search(self,
               model: str,
               domain: QueryDomain = None,
               limit: int = 1000,
               offset: int = 0) -> RecordList:
        repository = getattr(self, f'{model}_repository')
        return [vars(entity) for entity in
                repository.search(
                    domain or [], limit=limit, offset=offset)]
