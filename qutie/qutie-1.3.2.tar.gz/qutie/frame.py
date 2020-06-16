from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget

__all__ = ['Frame']

@bind(QtWidgets.QFrame)
class Frame(BaseWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
