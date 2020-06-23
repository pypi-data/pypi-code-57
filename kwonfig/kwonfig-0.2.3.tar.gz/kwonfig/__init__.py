import typing as T
import deepmerge
from collections import OrderedDict
from pathlib import Path
from .constants import PYDANTIC_SUPPORTED
from .handlers import Handlers
from .utils.types import Many
if PYDANTIC_SUPPORTED:
    from pydantic import BaseModel

__version__ = '0.2.1'


def load(base_paths: Many[Path],
         default_data: T.Optional[T.Mapping[str, T.Any]] = None) -> T.Optional[T.Mapping[str, T.Any]]:
    if isinstance(base_paths, Path):
        base_paths = [base_paths]

    out = OrderedDict()
    if default_data is not None:
        out.update(default_data)

    handlers = Handlers()
    for base_path in base_paths:
        data = handlers.load(base_path)
        deepmerge.always_merger.merge(out, data)

    return out


def resolve_base_paths(base_paths: Many[Path], exists=True) -> T.Iterable[Path]:
    if isinstance(base_paths, Path):
        base_paths = [base_paths]

    handlers = Handlers()
    for suffix in handlers.suffixes:
        for base_path in base_paths:
            path = base_path.with_suffix(f'.{suffix}')

            if path.exists() or not exists:
                yield path


if PYDANTIC_SUPPORTED:
    Ty = T.TypeVar('Ty', bound=BaseModel)

    def load_model(base_paths: Many[Path], model_cls: T.Type[Ty],
                   default_data: T.Optional[T.Mapping[str, T.Any]] = None) -> Ty:
        data = load(base_paths, default_data)
        return model_cls.parse_obj(data if data is not None else {})
