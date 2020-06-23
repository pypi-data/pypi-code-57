from typing import List
from dataclasses import dataclass
from kong_config_builder.base import BaseYamlObject


@dataclass
class HealthcheckUnhealthy(BaseYamlObject):
    interval: int
    timeouts: int
    http_failures: int


@dataclass
class HealthcheckHealthy(BaseYamlObject):
    interval: int
    successes: int
    http_statuses: List[int]


@dataclass
class HealthcheckActive(BaseYamlObject):
    type: str
    http_path: str
    timeout: float
    concurrency: int
    healthy: HealthcheckHealthy
    unhealthy: HealthcheckUnhealthy


@dataclass
class Healthcheck(BaseYamlObject):
    active: HealthcheckActive


@dataclass
class Target(BaseYamlObject):
    target: str


@dataclass
class Upstream(BaseYamlObject):
    name: str
    targets: List[Target]
    healthchecks: Healthcheck
