from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

__all__ = [
    'QtCore',
    'QtGui',
    'QtWidgets',
    'bind'
]

def bind(qt):
    """Decorator used to bind custom events on a Qt base class."""
    def bind(cls):
        class QtClass(qt):
            eventEmitted = QtCore.pyqtSignal(str, object, object)
        cls.QtClass = QtClass
        return cls
    return bind
