from .qt import QtWidgets
from .qt import bind

from .menu import Menu
from .widget import BaseWidget

__all__ = ['MainWindow']

@bind(QtWidgets.QMenuBar)
class MenuBar(BaseWidget):

    def __init__(self, *items, **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.append(item)

    def append(self, item):
        if isinstance(item, str):
            item = Menu(text=item)
        self.qt.addMenu(item.qt)
        return item

    def insert(self, before, item):
        if isinstance(item, str):
            item = Menu(text=item)
        if isinstance(before, Menu):
            self.qt.insertMenu(before.qt.menuAction(), item.qt)
        else:
            self.qt.insertMenu(before.qt, item.qt)
        return item

    def __getitem__(self, index):
        item = self.qt.actions()[index]
        return item.property(self.QtPropertyKey)

    def __iter__(self):
        return iter(item.property(self.QtPropertyKey) for item in self.qt.actions())

    def __len__(self):
        return len(self.qt.actions())

@bind(QtWidgets.QStatusBar)
class StatusBar(BaseWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def append(self, widget):
        self.qt.addPermanentWidget(widget.qt)
        return widget

@bind(QtWidgets.QMainWindow)
class MainWindow(BaseWidget):

    def __init__(self, *, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setMenuBar(MenuBar().qt)
        self.qt.setStatusBar(StatusBar().qt)
        self.layout = layout

    @property
    def layout(self):
        widget = self.qt.centralWidget()
        if widget is not None:
            return widget.property(self.QtPropertyKey)
        return None

    @layout.setter
    def layout(self, value):
        if value is None:
            self.qt.setCentralWidget(None)
        else:
            if not isinstance(value, BaseWidget):
                raise ValueError(value)
            self.qt.setCentralWidget(value.qt)

    @property
    def menubar(self):
        return self.qt.menuBar().property(self.QtPropertyKey)

    @property
    def statusbar(self):
        return self.qt.statusBar().property(self.QtPropertyKey)
