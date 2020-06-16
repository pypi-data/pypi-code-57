"""A scrollable area.

For more information on the underlying Qt5 object see [QScrollArea](https://doc.qt.io/qt-5/qscrollarea.html).
"""

from .qt import QtGui
from .qt import QtWidgets
from .qt import bind

from .widget import Widget

__all__ = ['ScrollArea']

@bind(QtWidgets.QScrollArea)
class ScrollArea(Widget):
    """A scrollable area."""

    def __init__(self, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setWidgetResizable(True)
        self.qt.setWidget(Widget().qt)
        self.qt.setBackgroundRole(QtGui.QPalette.Base) # fix background
        if layout is not None:
            self.layout = layout

    @property
    def layout(self):
        return self.qt.widget().property(self.QtPropertyKey).layout

    @layout.setter
    def layout(self, value):
        if self.qt.widget():
            self.qt.widget().property(self.QtPropertyKey).layout = value
