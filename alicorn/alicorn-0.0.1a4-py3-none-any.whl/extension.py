#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
from abc import ABC, abstractmethod


class Extension(ABC):
    """An Alicorn extension.

    Pass an instance of the extension to Alicorn before starting the server.

    Example:
        >>> extension = Extension()
        >>> alicorn.add_extension(extension)
    """

    @abstractmethod
    def register(self, app: 'alicorn.Alicorn'):
        """Called by the Alicorn instance when added as an extension"""
        raise NotImplemented()
