from ...application.domain.models import Link
from ...application.domain.common import QueryParser
from ...application.domain.repositories import LinkRepository
from .rst_repository import RstRepository, RstLoader


class RstLinkRepository(RstRepository[Link], LinkRepository):
    """Restructuredtext Link Repository"""

    def __init__(self, parser: QueryParser,
                 loader: RstLoader) -> None:
        super().__init__(parser=parser, loader=loader, item_class=Link)
        self.counter = 0

    def load(self):
        nodes = self.loader.nodes

        previous = ''
        for value in nodes:
            if value.get('summary'):
                continue

            target = value.get('id')
            predecessors = value.get('predecessors', [])

            if not predecessors:
                predecessors.append(previous)
            elif not isinstance(predecessors, list):
                predecessors = [predecessors]

            for source in predecessors:
                self.counter += 1
                item = self.item_class(
                    id=self.counter, source=source, target=target)
                self.data[self._location][
                    str(self.counter)] = item # type: ignore

            previous = target
