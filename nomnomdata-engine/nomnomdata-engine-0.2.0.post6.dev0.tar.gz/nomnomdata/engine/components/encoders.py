from json import JSONEncoder
from pathlib import PosixPath

from .base import Help, ParameterGroup, ParameterType


class ModelEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Help):
            return o.serialize()
        if isinstance(o, PosixPath):
            return str(o)
        if isinstance(o, ParameterGroup):
            return o.serialize()
        elif isinstance(o, ParameterType):
            return o.serialize()
        else:
            return super().default(o)
