from typing import Optional
from ..connection import Connection
from typing import Dict, Any


class Migration:
    def __init__(self, context: Dict[str, Any]) -> None:
        self._version = context.get('version', '')
        self._connection = context.get('connection')
        self._schema_up = False
        self._schema_down = False

    @property
    def version(self) -> str:
        return self._version

    @property
    def connection(self) -> Optional[Connection]:
        return self._connection

    def schema_up(self) -> None:
        self._schema_up = True

    def schema_down(self) -> None:
        self._schema_down = True
