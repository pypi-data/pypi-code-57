from pathlib import Path
from typing import Dict, List, Type, Optional, Any, cast
from abc import ABC
from importlib.abc import Loader
from importlib.util import spec_from_file_location, module_from_spec
from ..models import Migration
from .collector import Collector


class DirectoryCollector(Collector):
    def __init__(self, context: Dict[str, Any]) -> None:
        self.context = context
        self.path = self.context['migrations_path']

    def retrieve(self) -> List[Migration]:
        migrations = []
        for migration_file in Path(self.path).rglob('*.py'):
            migration = self._load_migration_file(migration_file)
            if migration:
                migrations.append(migration)

        return sorted(migrations, key=lambda m: m.version)

    def _load_migration_file(self, path: Path) -> Optional[Migration]:
        spec = spec_from_file_location(path.stem, str(path))
        loader = cast(Loader, spec.loader)
        module = module_from_spec(spec)
        loader.exec_module(module)
        if not hasattr(module, 'Migration'):
            return None
        migration: Type[Migration] = getattr(module, 'Migration')
        return migration(self.context)
