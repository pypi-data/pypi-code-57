from ..models import (
    Classification, Classifier, Link, Schedule, Slot, Task)
from .repository import Repository
from .memory_repository import MemoryRepository


class ClassificationRepository(Repository[Classification]):
    """Classification Repository"""


class MemoryClassificationRepository(
        MemoryRepository[Classification], ClassificationRepository):
    """Memory Classification Repository"""


class ClassifierRepository(Repository[Classifier]):
    """Classifier Repository"""


class MemoryClassifierRepository(
        MemoryRepository[Classifier], ClassifierRepository):
    """Memory Classifier Repository"""


class LinkRepository(Repository[Link]):
    """Link Repository"""


class MemoryLinkRepository(
        MemoryRepository[Link], LinkRepository):
    """Memory Link Repository"""


class ScheduleRepository(Repository[Schedule]):
    """Schedule Repository"""


class MemoryScheduleRepository(
        MemoryRepository[Schedule], ScheduleRepository):
    """Memory Schedule Repository"""


class SlotRepository(Repository[Slot]):
    """Slot Repository"""


class MemorySlotRepository(
        MemoryRepository[Slot], SlotRepository):
    """Memory Slot Repository"""


class TaskRepository(Repository[Task]):
    """Task Repository"""


class MemoryTaskRepository(
        MemoryRepository[Task], TaskRepository):
    """Memory Task Repository"""
