from typing import Optional
from dataclasses import dataclass
from kong_config_builder.base import BaseYamlObject


@dataclass
class KeyauthCredential(BaseYamlObject):
    consumer: str
    key: str


@dataclass
class Plugin(BaseYamlObject):
    name: str
    enabled: bool = True
    service: Optional[str] = None
    route: Optional[str] = None
    config: Optional[dict] = None
