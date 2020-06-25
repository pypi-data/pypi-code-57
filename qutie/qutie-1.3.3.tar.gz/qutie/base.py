__all__ = [
    'Base',
]

class Base:
    """Base class used for abstracting Qt5 classes."""

    QtClass = NotImplemented
    """Underlying Qt5 class."""

    def __init__(self, *args):
        self.__qt = self.QtClass(*args)

    @property
    def qt(self):
        """Access underlying Qt5 instance."""
        return self.__qt
