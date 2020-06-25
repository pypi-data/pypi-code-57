from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget

__all__ = ['ComboBox']

@bind(QtWidgets.QComboBox)
class ComboBox(BaseWidget):

    def __init__(self, items=None, *, current=None, editable=False,
                 changed=None, **kwargs):
        super().__init__(**kwargs)
        if items is not None:
            self.items = items
        if current is not None:
            self.current = current
        self.editable = editable
        self.changed = changed
        # Connect signals
        self.qt.currentIndexChanged.connect(self.__handle_changed)

    @property
    def items(self):
        return list(self)

    @items.setter
    def items(self, items):
        self.clear()
        for item in items:
            self.append(item)

    def clear(self):
        self.qt.clear()

    def append(self, value):
        self.qt.addItem(format(value), value)

    def insert(self, index, value):
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.insertItem(index, format(value), value)

    def remove(self, value):
        self.qt.removeItem(self.qt.findData(value))

    @property
    def current(self):
        return self.qt.itemData(self.qt.currentIndex())

    @current.setter
    def current(self, item):
        index = self.qt.findData(item)
        self.qt.setCurrentIndex(index)

    def index(self, item):
        index = self.qt.findData(item)
        if index < 0:
            raise ValueError("item not in list")
        return index

    @property
    def editable(self):
        return self.qt.isEditable()

    @editable.setter
    def editable(self, value):
        self.qt.setEditable(value)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, changed):
        self.__changed = changed

    def __handle_changed(self, index):
        if callable(self.changed):
            value = self.items[index]
            self.changed(value)

    def __getitem__(self, key):
        return self.qt.itemData(key)

    def __setitem__(self, key, value):
        self.qt.setItemText(key, format(value))
        self.qt.setItemData(key, value)

    def __delitem__(self, key):
        self.qt.removeItem(key)

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        return (self[row] for row in range(len(self)))
