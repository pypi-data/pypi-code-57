import importlib


class Config:
    def __init__(self, config, env):
        self._config = importlib.import_module(f"{config}.{env}")

    def __getattr__(self, name):
        return getattr(self._config, name, None)

    def get(self, name, default=None):
        return getattr(self, name, default)
