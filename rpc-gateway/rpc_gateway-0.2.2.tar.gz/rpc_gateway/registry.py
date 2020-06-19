from typing import Any, Dict, Callable, Optional, Union, List, Tuple
from inspect import isclass
import json

FactoryType = Callable[..., Any]
ConfigurationType = Dict[str, Union[List, Dict[str, Any]]]
GetItemType = Union[str, FactoryType]


def configure(config: Union[str, ConfigurationType]):
    Registry.default_registry().configure(config)


def get(item: GetItemType, *args: Any, **kwargs: Any) -> Any:
    return Registry.default_registry().get(item, *args, **kwargs)


def register(factory: FactoryType, name: Optional[str] = None):
    Registry.default_registry().register(factory, name)


def default_registry() -> 'Registry':
    return Registry.default_registry()


class Registry:
    CONFIG_META_PREFIX = '@'
    ARGS_KEY = '@args'
    _default_registry: Optional['Registry'] = None

    @staticmethod
    def reset():
        Registry._default_registry = None

    @staticmethod
    def default_registry() -> 'Registry':
        if Registry._default_registry is None:
            Registry._default_registry = Registry()

        return Registry._default_registry

    def __init__(self,
                 config_path: Optional[str] = None,
                 configuration: Optional[ConfigurationType] = None,
                 factories: Optional[Dict[str, FactoryType]] = None,
                 objects: Optional[Dict[str, Any]] = None,
                 set_default: bool = True):
        self.config_path = config_path
        self.configuration = configuration or {}
        self.factories = factories or {}
        self.factory_types = {val: key for key, val in self.factories.items()}
        self.objects = objects or {}

        if set_default and Registry._default_registry is None:
            Registry._default_registry = self

        if self.config_path is not None:
            self.load_configuration()

    def reset_object(self, object_name: str):
        self.objects.pop(object_name)

    def configure(self, config: Union[str, ConfigurationType]):
        if isinstance(config, dict):
            self.configuration = config
        else:
            self.load_configuration(config)

    def load_configuration(self, config_path: Optional[str] = None):
        with open(config_path or self.config_path) as config_file:
            self.configuration = json.load(config_file)

    def get_object_meta_configuration(self, object_name: str) -> Dict[str, Any]:
        if object_name not in self.configuration:
            return {}

        config = self.configuration[object_name]
        # remove any keys that don't start with @ (and aren't @args) and remove the @ from the keys
        return {k[1:]: v for k, v in config.items() if k.startswith(self.CONFIG_META_PREFIX) and k != self.ARGS_KEY}

    def get_object_configuration(self, object_name: str, *args: Any, **kwargs: Any) -> Tuple[List, Dict]:
        if object_name not in self.configuration:
            return [], {}

        config = self.configuration[object_name]

        if isinstance(config, list):
            return [*config, *args], kwargs

        config_args = config.get(self.ARGS_KEY, [])
        config_kwargs = {k: v for k, v in config.items() if not k.startswith(self.CONFIG_META_PREFIX)}
        return [*config_args, *args], {**config_kwargs, **kwargs}

    def register(self, factory: FactoryType, name: Optional[str] = None):
        if name is None:
            if not isclass(factory):
                raise RegistryError(f'Only classes can be registered without a name')

            name = factory.__name__

        if name in self.factories:
            raise RegistryFactoryExists(f'Factory with name "{name}" already registered')

        self.factories[name] = factory
        self.factory_types[factory] = self.factory_types.get(factory, []) + [name]

    def create_object(self, object_name: str, *args: Any, **kwargs: Any):
        if object_name not in self.factories:
            raise RegistryFactoryNotFoundError(f'Unable to find a factory for object: {object_name}')

        object_args, object_kwargs = self.get_object_configuration(object_name, *args, **kwargs)

        return self.factories[object_name](*object_args, **object_kwargs)

    def get_by_name(self, object_name: str, *args: Any, **kwargs: Any):
        if object_name in self.objects:
            return self.objects[object_name]

        self.objects[object_name] = self.create_object(object_name, *args, **kwargs)
        return self.objects[object_name]

    def get_by_type(self, factory: FactoryType, *args: Any, **kwargs: Any) -> Any:
        if factory not in self.factory_types:
            raise RegistryFactoryNotFoundError(f'Unable to find factory: {factory}')

        if not isclass(factory):
            raise RegistryFactoryIsNotClassError(f'Cannot get default object, factory must be a class: {factory}')

        object_names = self.factory_types[factory]
        object_name = factory.__name__

        if object_name not in object_names:
            raise RegistryFactoryDefaultNotFoundError(f'Unable to find a default object for factory: {factory}')

        return self.get_by_name(object_name, *args, **kwargs)

    def get(self, item: GetItemType, *args: Any, **kwargs: Any) -> Any:
        if isinstance(item, str):
            return self.get_by_name(item, *args, **kwargs)

        return self.get_by_type(item, *args, **kwargs)


class RegistryError(Exception):
    pass


class RegistryFactoryNotFoundError(RegistryError):
    pass


class RegistryFactoryDefaultNotFoundError(RegistryError):
    pass


class RegistryFactoryExists(RegistryError):
    pass


class RegistryFactoryIsNotClassError(RegistryError):
    pass
