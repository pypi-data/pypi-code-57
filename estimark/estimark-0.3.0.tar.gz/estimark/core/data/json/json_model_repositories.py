from estimark.application.domain.models import (
    Classification, Classifier, Link, Schedule, Slot, Task)
from estimark.application.domain.common import QueryParser
from estimark.application.domain.repositories import (
    ClassificationRepository,  ClassifierRepository, LinkRepository,
    ScheduleRepository, SlotRepository, TaskRepository)
from estimark.core.data.json import JsonRepository


class JsonClassificationRepository(
        JsonRepository[Classification], ClassificationRepository):
    """Json Classification Repository"""

    def __init__(self, file_path: str, parser: QueryParser,
                 collection_name: str='classifications',
                 file_suffix: str='') -> None:
        super().__init__(file_path, parser, collection_name,
                         Classification, file_suffix)


class JsonClassifierRepository(
        JsonRepository[Classifier], ClassifierRepository):
    """Json Classifier Repository"""

    def __init__(self, file_path: str, parser: QueryParser,
                 collection_name: str='classifiers',
                 file_suffix: str='') -> None:
        super().__init__(file_path, parser, collection_name,
                         Classifier, file_suffix)


class JsonLinkRepository(
        JsonRepository[Link], LinkRepository):
    """Json Link Repository"""

    def __init__(self, file_path: str, parser: QueryParser,
                 collection_name: str='links',
                 file_suffix: str='') -> None:
        super().__init__(file_path, parser, collection_name,
                         Link, file_suffix)


class JsonScheduleRepository(
        JsonRepository[Schedule], ScheduleRepository):
    """Json Schedule Repository"""

    def __init__(self, file_path: str, parser: QueryParser,
                 collection_name: str='schedules',
                 file_suffix: str='') -> None:
        super().__init__(file_path, parser, collection_name,
                         Schedule, file_suffix)


class JsonSlotRepository(
        JsonRepository[Slot], SlotRepository):
    """Json Slot Repository"""

    def __init__(self, file_path: str, parser: QueryParser,
                 collection_name: str='slots',
                 file_suffix: str='') -> None:
        super().__init__(file_path, parser, collection_name,
                         Slot, file_suffix)


class JsonTaskRepository(
        JsonRepository[Task], TaskRepository):
    """Json Task Repository"""

    def __init__(self, file_path: str, parser: QueryParser,
                 collection_name: str='tasks',
                 file_suffix: str='') -> None:
        super().__init__(file_path, parser, collection_name,
                         Task, file_suffix)
