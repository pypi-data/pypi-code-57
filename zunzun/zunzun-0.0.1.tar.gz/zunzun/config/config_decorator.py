import inspect
from injector import Scope, InstanceProvider, Injector, ScopeDecorator
from .config import Config


class ConfigScope(Scope):
    def __init__(self, injector: Injector):
        super().__init__(injector)

    def get(self, key, provider):
        args_spec = inspect.getfullargspec(key)
        additional_kwargs = dict()
        for field, _type in args_spec.annotations.items():
            config = self.injector.get(Config)
            config_value = getattr(config, field, None)
            if config_value and type(config_value) == _type:
                additional_kwargs[field] = config_value
        instance = self.injector.create_object(key, additional_kwargs)
        provider = InstanceProvider(instance)
        return provider


def create_config_scope():
    return ScopeDecorator(ConfigScope)
