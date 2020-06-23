import typing as T
from types import (
    MethodType,
)
from loguru import logger
from pluggy import (
    PluginManager,
    HookspecMarker,
    HookimplMarker,
)
from pluggy.hooks import HookImpl
from .utils.lazy import lazy

PROJECT_NAME = 'kwconfig'

hookspec = HookspecMarker(PROJECT_NAME)
hookimpl = HookimplMarker(PROJECT_NAME)


class Plugin:
    class Hook:
        def __init__(self, name: str, method: MethodType):
            self.name = name
            self.method = method

        def __call__(self, *args, **kwargs):
            return self.method(*args, **kwargs)

    @staticmethod
    def hook(name: str):
        def wrapper(f):
            if not isinstance(f, MethodType):
                logger.warning(f'{f} is not a valid hooked method')
                return f

            return Plugin.Hook(name, f)
        return wrapper


class Plugins(PluginManager):
    specs: T.List[T.Type] = []

    def __init__(self):
        super().__init__(PROJECT_NAME)

        self.load_setuptools_entrypoints(f'{PROJECT_NAME}.exts')

        for cls in self.specs:
            self.add_hookspecs(cls)

    def register(self, plugin: T.Union[T.Any, T.Type[Plugin]], name=None):
        if name is None:
            name = self.get_canonical_name(plugin)

        if not issubclass(plugin, Plugin):
            return super().register(plugin, name=name)

        plugin_cls: T.Type[Plugin] = plugin

        plugin = plugin_cls()
        self._name2plugin[name] = plugin
        self._plugin2hookcallers[plugin] = hookcallers = []

        for item in plugin.__dict__.values():
            if not isinstance(item, Plugin.Hook):
                continue

            if not hasattr(self.hook, item.name):
                logger.warning(f'Non-existent hook: {item.name}')
                continue

            hook = getattr(self.hook, item.name)

            hook_impl_opts = self.parse_hookimpl_opts(plugin, item.name)
            _hookimpl = HookImpl(plugin, name, item.method, hook_impl_opts)

            hook._add_hookimpl(_hookimpl)
            hookcallers.append(hook)

    @classmethod
    def register_specs(cls, klass):
        cls.specs.append(klass)
        return klass


plugins = lazy(Plugins)
