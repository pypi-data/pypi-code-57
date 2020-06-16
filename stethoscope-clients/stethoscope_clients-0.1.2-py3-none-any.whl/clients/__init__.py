from clients.runner import (
    start_instance, stop_instance
)

from clients.types import (
    ENR, InstanceConfig
)

from clients.rumor import (
    connect_rumor
)

# TODO: just for testing. remove later
import pkg_resources
n = __name__
s = pkg_resources.resource_string(__name__, 'bin/lighthouse/start')

__all__ = [
    'start_instance',
    'stop_instance',
    'ENR',
    'InstanceConfig',
    'connect_rumor'
]
