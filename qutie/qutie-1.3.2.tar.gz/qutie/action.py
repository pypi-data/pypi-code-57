from .qt import QtGui
from .qt import QtWidgets
from .qt import bind

from .object import Object

__all__ = ['Action']

@bind(QtWidgets.QAction)
class Action(Object):

    def __init__(self, text=None, *, checkable=None, checked=False, tool_tip=None,
                 status_tip=None, shortcut=None, separator=None, triggered=None,
                 toggled=None, **kwargs):
        super().__init__(**kwargs)
        if text is not None:
            self.text = text
        if checkable is not None:
            self.checkable = checkable
        self.checked = checked
        if tool_tip is not None:
            self.tool_tip = tool_tip
        if status_tip is not None:
            self.status_tip = status_tip
        if shortcut is not None:
            self.shortcut = shortcut
        if separator is not None:
            self.separator = separator
        self.triggered = triggered
        self.toggled = toggled
        # Connect signals
        self.qt.triggered.connect(self.__handle_triggered)
        self.qt.toggled.connect(self.__handle_toggled)

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, value):
        self.qt.setText(value)

    @property
    def checked(self):
        return self.qt.isChecked()

    @checked.setter
    def checked(self, value):
        self.qt.setChecked(value)

    @property
    def checkable(self):
        return self.qt.isCheckable()

    @checkable.setter
    def checkable(self, value):
        self.qt.setCheckable(value)

    @property
    def tool_tip(self):
        return self.qt.toolTip()

    @tool_tip.setter
    def tool_tip(self, value):
        self.qt.setToolTip(value)

    @property
    def status_tip(self):
        return self.qt.statusTip()

    @status_tip.setter
    def status_tip(self, value):
        self.qt.setStatusTip(value)

    @property
    def shortcut(self):
        return self.qt.shortcut().toString() or None

    @shortcut.setter
    def shortcut(self, value):
        if value is None:
            self.qt.setShortcut(QtGui.QKeySequence())
        else:
            self.qt.setShortcut(QtGui.QKeySequence(value))

    @property
    def separator(self):
        return self.qt.isSeparator()

    @separator.setter
    def separator(self, value):
        self.qt.setSeparator(value)

    @property
    def triggered(self):
        return self.__triggered

    @triggered.setter
    def triggered(self, value):
        self.__triggered = value

    def __handle_triggered(self):
        if callable(self.triggered):
            self.triggered()

    @property
    def toggled(self):
        return self.__toggled

    @toggled.setter
    def toggled(self, value):
        self.__toggled = value

    def __handle_toggled(self, checked):
        if callable(self.toggled):
            self.toggled(checked)

    def trigger(self):
        self.qt.trigger()

    def toggle(self):
        self.qt.toggle()
