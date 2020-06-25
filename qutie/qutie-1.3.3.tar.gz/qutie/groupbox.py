from .qt import QtWidgets
from .qt import bind

from .widget import Widget

__all__ = ['GroupBox']

@bind(QtWidgets.QGroupBox)
class GroupBox(Widget):

    def __init__(self, title=None, *, checkable=None, checked=None, flat=None,
                 clicked=None, toggled=None, **kwargs):
        super().__init__(**kwargs)
        if title is not None:
            self.title = title
        if checkable is not None:
            self.checkable = checkable
        if checked is not None:
            self.checked = checked
        if flat is not None:
            self.flat = flat
        self.clicked = clicked
        self.toggled = toggled
        # Connect signals
        self.qt.clicked.connect(self.__handle_clicked)
        self.qt.toggled.connect(self.__handle_toggled)

    @property
    def title(self):
        return self.qt.title()

    @title.setter
    def title(self, value):
        self.qt.setTitle(value)

    @property
    def checkable(self):
        return self.qt.isCheckable()

    @checkable.setter
    def checkable(self, value):
        self.qt.setCheckable(value)

    @property
    def checked(self):
        return self.qt.isChecked()

    @checked.setter
    def checked(self, value):
        self.qt.setChecked(value)

    @property
    def flat(self):
        return self.qt.isFlat()

    @flat.setter
    def flat(self, value):
        self.qt.setFlat(value)

    @property
    def clicked(self):
        return self.__clicked

    @clicked.setter
    def clicked(self, value):
        self.__clicked = value

    def __handle_clicked(self, _):
        if callable(self.clicked):
            self.clicked()

    @property
    def toggled(self):
        return self.__toggled

    @toggled.setter
    def toggled(self, value):
        self.__toggled = value

    def __handle_toggled(self, checked):
        if callable(self.toggled):
            self.toggled(checked)
