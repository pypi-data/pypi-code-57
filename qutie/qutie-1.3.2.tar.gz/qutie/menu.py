from .qt import QtWidgets
from .qt import bind

from .action import Action
from .widget import BaseWidget

__all__ = ['Menu']

@bind(QtWidgets.QMenu)
class Menu(BaseWidget):

    def __init__(self, *items, text=None, **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.append(item)
        if text is not None:
            self.text = text

    @property
    def text(self):
        return self.qt.title()

    @text.setter
    def text(self, value):
        self.qt.setTitle(value)

    def append(self, item):
        if isinstance(item, Action):
            self.qt.addAction(item.qt)
        elif isinstance(item, Menu):
            self.qt.addMenu(item.qt)
        elif isinstance(item, str):
            item = Action(item)
            self.qt.addAction(item.qt)
        else:
            raise ValueError(item)
        return item

    def insert(self, before, item):
        if isinstance(item, Action):
            if isinstance(before, Menu):
                self.qt.insertAction(before.qt.menuAction(), item.qt)
            else:
                self.qt.insertAction(before.qt, item.qt)
        elif isinstance(item, Menu):
            if isinstance(before, Menu):
                self.qt.insertMenu(before.qt.menuAction(), item.qt)
            else:
                self.qt.insertMenu(before.qt, item.qt)
        elif isinstance(item, str):
            item = Action(item)
            if isinstance(before, Menu):
                self.qt.insertAction(before.qt.menuAction(), item.qt)
            else:
                self.qt.insertAction(before.qt, item.qt)
        else:
            raise ValueError(item)
        return item

    def index(self, item):
        return self.qt.actions().index(item)

    def __getitem__(self, index):
        item = self.qt.actions()[index]
        return item.property(self.QtPropertyKey)

    def __iter__(self):
        return iter(item.property(self.QtPropertyKey) for item in self.qt.actions())

    def __len__(self):
        return len(self.qt.actions())
