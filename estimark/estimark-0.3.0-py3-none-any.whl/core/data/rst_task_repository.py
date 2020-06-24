from ...application.domain.models import Task
from ...application.domain.common import QueryParser
from ...application.domain.repositories import TaskRepository
from .rst_repository import RstRepository, RstLoader


class RstTaskRepository(RstRepository[Task], TaskRepository):
    """Restructuredtext Task Repository"""

    def __init__(self, parser: QueryParser,
                 loader: RstLoader) -> None:
        super().__init__(parser=parser, loader=loader, item_class=Task)
