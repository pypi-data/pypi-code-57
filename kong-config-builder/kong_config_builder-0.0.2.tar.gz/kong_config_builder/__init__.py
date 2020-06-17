from yaml import dump
from typing import List
from dataclasses import dataclass
from kong_config_builder.base import BaseYamlObject
from kong_config_builder.utils import no_empty, noop
from kong_config_builder.consumer import Consumer
from kong_config_builder.plugin import Plugin, KeyauthCredential
from kong_config_builder.service import Service, Route
from kong_config_builder.upstream import (
    Upstream, Target, Healthcheck, HealthcheckActive,
    HealthcheckHealthy, HealthcheckUnhealthy)


@dataclass
class Kong(BaseYamlObject):
    services: List[Service]
    upstreams: List[Upstream]
    plugins: List[Plugin]
    consumers: List[Consumer]
    keyauth_credentials: List[KeyauthCredential]
    _format_version: str = "1.1"

    def save(self, filename="kong.yml"):
        with open(filename, "w") as f:
            dump(self, f)


Kong.yaml_dumper.add_representer(Kong, no_empty)
Kong.yaml_dumper.process_tag = noop

__all__ = [
    "Consumer",
    "Plugin",
    "KeyauthCredential",
    "Service",
    "Route",
    "Upstream",
    "Target",
    "Healthcheck",
    "HealthcheckActive",
    "HealthcheckHealthy",
    "HealthcheckUnhealthy",
    "Kong"
]
