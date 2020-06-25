from .qt import QtCore

__all__ = ['OrientationMixin']

class OrientationMixin:

    horizontal = 'horizontal'
    vertical = 'vertical'

    @property
    def orientation(self):
        return {
            QtCore.Qt.Horizontal: OrientationMixin.horizontal,
            QtCore.Qt.Vertical: OrientationMixin.vertical
        }[self.qt.orientation()]

    @orientation.setter
    def orientation(self, value):
        self.qt.setOrientation({
            OrientationMixin.horizontal: QtCore.Qt.Horizontal,
            OrientationMixin.vertical: QtCore.Qt.Vertical
        }[value])
