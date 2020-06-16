"""Stack widget.

For more information on the underlying Qt5 object see [QStackedWidget](https://doc.qt.io/qt-5/qstackedwidget.html).
"""

from .qt import QtCore
from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget

__all__ = ['Stack']

@bind(QtWidgets.QStackedWidget)
class Stack(BaseWidget):

    def __init__(self, *items, changed=None, **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.append(item)
        self.changed = changed
        # Connect signals
        self.qt.currentChanged.connect(self.__handle_changed)

    @property
    def items(self):
        return list(self)

    def append(self, item):
        self.qt.addWidget(item.qt)

    def insert(self, index, item):
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.insertWidget(index, item.qt)

    def remove(self, item):
        self.qt.removeWidget(item.qt)

    @property
    def current(self):
        item = self.qt.currentIndex()
        if item is not None:
            return item.property(self.QtPropertyKey)
        return item

    @current.setter
    def current(self, item):
        index = self.qt.indexOf(item.qt)
        self.qt.setCurrentIndex(index)

    def index(self, item):
        index = self.qt.indexOf(item.qt)
        if index < 0:
            raise ValueError("item not in stack")
        return index

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, changed):
        self.__changed = changed

    def __handle_changed(self, index):
        if callable(self.changed):
            self.changed(index)

    def __getitem__(self, key):
        item = self.qt.widget(key)
        if not item:
            raise KeyError(key)
        return item.property(self.QtPropertyKey)

    def __setitem__(self, key, value):
        del self[key]
        self.insert(key, value)

    def __delitem__(self, key):
        item = self[key]
        self.qt.removeWidget(item)

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        return (self[index] for index in range(len(self)))
