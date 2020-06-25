from os import environ
from pathlib import Path

from pydantic import BaseModel


class ApeironConfig(BaseModel):
    sources_dir: Path = "~/apeiron/sources"
    packages_dir: Path = "~/apeiron/packages"
    modpack_index: str = "index.json"
    parallelism: int = 4
    debug: bool = False


_defaults = ApeironConfig()


cfg = ApeironConfig(
    sources_dir=Path(environ.get("APEIRON_SOURCES_DIR", _defaults.sources_dir)).expanduser().as_posix(),
    packages_dir=Path(environ.get("APEIRON_PACKAGES_DIR", _defaults.packages_dir)).expanduser().as_posix(),
    modpack_index=environ.get("APEIRON_MODPACK_INDEX", _defaults.modpack_index),
    parallelism=int(environ.get("APEIRON_PARALLELISM", _defaults.parallelism)),
    debug=("APEIRON_DEBUG" in environ),
)
