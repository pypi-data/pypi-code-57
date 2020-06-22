from dataclasses import dataclass
from kong_config_builder.base import BaseYamlObject


@dataclass
class Consumer(BaseYamlObject):
    username: str
