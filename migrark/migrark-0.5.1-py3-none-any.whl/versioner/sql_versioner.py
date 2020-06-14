from abc import ABC
from typing import Dict, Any, cast
from ..connection import Connection
from .versioner import Versioner


class SqlVersioner(Versioner):
    def __init__(self, context: Dict[str, Any]) -> None:
        self.schema = context.get('schema', '__template__')
        self.table = context.get('table',  '__version__')
        self.connection: Connection = context['connection']
        self.placeholder: str = context.get('placeholder', '${index}')
        self.offset: int = context.get('offset', 1)
        self._setup()

    @property
    def version(self) -> str:
        query = (f"SELECT version FROM {self.schema}.{self.table} "
                 "ORDER BY id DESC LIMIT 1")
        result = self.connection.select(query)
        version_dict: Dict[str, str] = next(iter(result), {})
        version = version_dict.get('version', '')

        return version

    @ version.setter
    def version(self, value: str) -> None:
        index = self.offset
        placeholders = self.placeholder.format(index=index)
        query = (f"INSERT INTO {self.schema}.{self.table} (version) "
                 f"VALUES ({placeholders});")
        self.connection.execute(query, [value])

    def _setup(self) -> None:
        self.connection.execute(
            f"CREATE SCHEMA IF NOT EXISTS {self.schema}; "
            f"CREATE TABLE IF NOT EXISTS {self.schema}.{self.table}("
            "id serial PRIMARY KEY, "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
            "version VARCHAR(255) NOT NULL);")
