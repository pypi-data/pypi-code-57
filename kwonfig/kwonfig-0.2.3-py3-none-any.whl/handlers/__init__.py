import abc
import typing as T
from pathlib import Path
from kwonfig.plugin import Plugins, plugins, hookspec
from kwonfig.utils.types import Many


class Handler(abc.ABC):
    Data = T.Mapping[str, T.Any]

    enabled: bool = True

    suffix: Many[str]

    @classmethod
    @abc.abstractmethod
    def load(cls, fp: T.IO[T.AnyStr]) -> 'Handler.Data':
        pass


@Plugins.register_specs
class Handlers:
    _handlers: T.Dict[str, T.Type[Handler]] = {}

    def __init__(self):
        # Load additional handlers
        handlers: T.List[T.Type[Handler]] = plugins.hook.add_handler()
        for handler in handlers:
            self.register_handler(handler)

    def get_handler(self, path: Path) -> T.Optional[T.Type[Handler]]:
        return self._handlers.get(path.suffix, None)

    def find_handler(self, base_path: Path) -> T.Optional[T.Tuple[Path, T.Type[Handler]]]:
        for (ext, handler) in self._handlers.items():
            path = base_path.with_suffix(f'.{ext}')
            if path.exists():
                return (path, handler)  # noqa

        return None

    def load(self, base_path: Path) -> T.Optional[Handler.Data]:
        result = self.find_handler(base_path)
        if result is None:
            return None

        (path, handler) = result
        with path.open() as f:
            return handler.load(f)

    @property
    def handlers(self) -> T.Iterator[T.Type[Handler]]:
        yield from self._handlers.values()

    @property
    def suffixes(self) -> T.Iterator[str]:
        for suffix in self._handlers.keys():
            yield suffix

    @hookspec
    def add_handler(self):
        pass

    @classmethod
    def register_handlers(cls):
        from .hjson import HJsonHandler
        from .ini import IniHandler
        from .json import JsonHandler
        from .json5 import Json5Handler
        from .python import PythonHandler
        from .toml import TomlHandler
        from .yaml import YamlHandler

        cls.register_handler(HJsonHandler)
        cls.register_handler(IniHandler)
        cls.register_handler(JsonHandler)
        cls.register_handler(Json5Handler)
        cls.register_handler(PythonHandler)
        cls.register_handler(TomlHandler)
        cls.register_handler(YamlHandler)

    @classmethod
    def register_handler(cls, handler_cls: T.Type[Handler]):
        if not handler_cls.enabled:
            return

        suffixes = handler_cls.suffix
        if isinstance(handler_cls.suffix, str):
            suffixes = [suffixes]

        for suffix in suffixes:
            cls._handlers[suffix] = handler_cls


Handlers.register_handlers()
