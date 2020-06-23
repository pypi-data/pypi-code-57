from typing import List
from dataclasses import dataclass
from kong_config_builder.base import BaseYamlObject


@dataclass
class Route(BaseYamlObject):
    name: str
    paths: List[str]
    strip_path: bool = False


@dataclass
class Service(BaseYamlObject):
    name: str
    host: str
    routes: List[Route]
