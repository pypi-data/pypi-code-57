from typing import Dict, Any
from .connection import Connection
from .collector import DirectoryCollector
from .versioner import SqlVersioner
from .migrator import Migrator


def sql_migrate(connection: Connection, migrations_path: str,
                schema: str = None, context: Dict[str, Any] = {},
                target_version: str = None):
    schema = schema or '__template__'
    target_version = target_version or '999999'

    connection.open()

    migration_context = {
        'migrations_path': migrations_path,
        'connection': connection,
        'schema': schema
    }
    migration_context.update(context)

    collector = DirectoryCollector(migration_context)
    versioner = SqlVersioner(migration_context)
    migrator = Migrator(versioner, collector)

    migrator.migrate(target_version)

    connection.close()
