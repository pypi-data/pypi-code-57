from injectark import Factory
from ..core.common import Config
from ..application.domain.common import QueryParser
from ..application.domain.repositories import (
    TaskRepository, MemoryTaskRepository,
    LinkRepository, MemoryLinkRepository,
    ClassifierRepository, MemoryClassifierRepository,
    ClassificationRepository, MemoryClassificationRepository,
    ScheduleRepository, MemoryScheduleRepository,
    SlotRepository, MemorySlotRepository)
from ..application.domain.services import PlotService, MemoryPlotService
from ..application.managers import EstimationManager
from ..application.informers import StandardEstimarkInformer



class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = config

    def query_parser(self) -> QueryParser:
        return QueryParser()

    def memory_task_repository(
            self, query_parser: QueryParser
    ) -> MemoryTaskRepository:
        return MemoryTaskRepository(query_parser)

    def memory_link_repository(
            self, query_parser: QueryParser
    ) -> MemoryLinkRepository:
        return MemoryLinkRepository(query_parser)

    def memory_classifier_repository(
            self, query_parser: QueryParser
    ) -> MemoryClassifierRepository:
        return MemoryClassifierRepository(query_parser)

    def memory_classification_repository(
            self, query_parser: QueryParser
    ) -> MemoryClassificationRepository:
        return MemoryClassificationRepository(query_parser)

    def memory_schedule_repository(
            self, query_parser: QueryParser
    ) -> MemoryScheduleRepository:
        return MemoryScheduleRepository(query_parser)

    def memory_slot_repository(
            self, query_parser: QueryParser
    ) -> MemorySlotRepository:
        return MemorySlotRepository(query_parser)

    def memory_plot_service(self) -> MemoryPlotService:
        return MemoryPlotService()

    def estimation_manager(
            self, task_repository: TaskRepository,
            classifier_repository: ClassifierRepository,
            classification_repository: ClassificationRepository,
            link_repository: LinkRepository,
            schedule_repository: ScheduleRepository,
            slot_repository: SlotRepository,
            plot_service: PlotService
    ) -> EstimationManager:
        return EstimationManager(
            task_repository, classifier_repository,
            classification_repository, link_repository,
            schedule_repository, slot_repository, plot_service)

    def standard_estimark_informer(
            self, task_repository: TaskRepository,
            link_repository: LinkRepository,
            classifier_repository: ClassifierRepository,
            schedule_repository: ScheduleRepository,
            slot_repository: SlotRepository
    ) -> StandardEstimarkInformer:
        return StandardEstimarkInformer(
            task_repository, link_repository, classifier_repository,
            schedule_repository, slot_repository)
