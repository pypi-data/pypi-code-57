#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
from grpc import ServicerContext


class AlicornContext:
    """The alicorn context"""

    def __init__(self, app):
        self.app = app
        self.original_handler = None

    def _add(self, data):
        """Add data into this context"""
        self.__dict__.update(data)


class GrpcContext(ServicerContext):
    """A grpc Context with an alicorn context attached"""

    alicorn: AlicornContext
