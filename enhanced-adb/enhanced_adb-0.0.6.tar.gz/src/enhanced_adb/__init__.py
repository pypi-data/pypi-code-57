import os
import yaml
from pathlib import Path

from ._utils import SingletonMetaClass
from pkg_resources import resource_filename

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

user_root = Path(Path.home().joinpath(".eadb"))
user_config_file = user_root.joinpath("user.yml")
user_local = user_root.joinpath("local")

user_config = None

if os.path.isfile(user_config_file):
    with open(user_config_file, encoding="utf-8") as file:
        user_config = yaml.load(file, Loader=Loader)

with open(os.path.join(resource_filename("enhanced_adb", "res"), "user.yml"), encoding="utf-8") as file:
    user_config_default = yaml.load(file, Loader=Loader)


class UserConfig(object):
    __metaclass__ = SingletonMetaClass

    def __init__(self):
        self._default = user_config_default
        if user_config is None:
            self._user = user_config_default
        else:
            self._user = user_config

    def get(self, key):
        return self._user.get(key, self._default[key])

