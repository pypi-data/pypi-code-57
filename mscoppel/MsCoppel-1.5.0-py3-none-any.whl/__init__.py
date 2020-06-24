from .microservices import Microservices
from .ms_base import KafkaBase
from .loggs import Loggs
from .types import Types, TypesActions, Actions
from .options import Options
from .ErrorMs import ErrorMs
from .version_framework import version

name = 'MsCoppel'

__all__ = [
    'Microservices' ,
    'KafkaBase',
    'Loggs',
    'Types',
    'Options',
    'MsManager',
    'TypesActions',
    'ErrorMs',
    'Actions'
]

__version__ = version