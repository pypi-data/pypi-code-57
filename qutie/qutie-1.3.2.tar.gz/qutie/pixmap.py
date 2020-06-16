from .qt import QtGui
from .qt import bind

from .base import Base

__all__ = ['Pixmap']

@bind(QtGui.QPixmap)
class Pixmap(Base):

    def __init__(self, filename=None, *, qt=None):
        if qt is None:
            super().__init__()
        else:
            super().__init__(qt)
        if filename is not None:
            self.load(filename)

    @property
    def width(self):
        return self.qt.width()

    @property
    def height(self):
        return self.qt.height()

    @property
    def size(self):
        return self.width, self.height

    def load(self, filename):
        """Loa pixmap from file."""
        return self.qt.load(filename)

    def save(self, filename, quality=-1):
        """Save pixmap to file."""
        return self.qt.save(filename, quality)

    def fill(self, color):
        """Fill pixmap with color."""
        self.qt.fill(QtGui.QColor(color))

    @classmethod
    def create(cls, width, height, color=None):
        """Return new pixmap instance, with optional fill color."""
        pixmap = Pixmap(qt=cls.QtClass(width, height))
        if color is not None:
            pixmap.fill(color)
        return pixmap
