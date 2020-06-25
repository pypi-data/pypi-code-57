from .qt import QtGui
from .qt import QtWidgets
from .qt import bind

from .icon import Icon
from .widget import Widget

__all__ = ['Button', 'RadioButton']

@bind(QtWidgets.QAbstractButton)
class BaseButton(Widget):

    def __init__(self, text=None, *, checkable=None, checked=None, icon=None,
                 clicked=None, toggled=None, pressed=None, released=None,
                 **kwargs):
        super().__init__(**kwargs)
        if text is not None:
            self.text = text
        if checkable is not None:
            self.checkable = checkable
        if checked is not None:
            self.checked = checked
        if icon is not None:
            self.icon = icon
        self.clicked = clicked
        self.pressed = pressed
        self.released = released
        self.toggled = toggled
        # Connect signals
        self.qt.clicked.connect(self.__handle_clicked)
        self.qt.pressed.connect(self.__handle_pressed)
        self.qt.released.connect(self.__handle_released)
        self.qt.toggled.connect(self.__handle_toggled)

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, value):
        self.qt.setText(value)

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
    def icon(self):
        icon = self.qt.icon()
        if icon.isNull():
            return None
        return Icon(qt=icon)

    @icon.setter
    def icon(self, value):
        if value is None:
            self.qt.setIcon(QtGui.QIcon())
        else:
            if not isinstance(value, Icon):
                value = Icon(value)
            self.qt.setIcon(value.qt)

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
    def pressed(self):
        return self.__pressed

    @pressed.setter
    def pressed(self, value):
        self.__pressed = value

    def __handle_pressed(self):
        if callable(self.pressed):
            self.pressed()

    @property
    def released(self):
        return self.__released

    @released.setter
    def released(self, value):
        self.__released = value

    def __handle_released(self):
        if callable(self.released):
            self.released()

    @property
    def toggled(self):
        return self.__toggled

    @toggled.setter
    def toggled(self, value):
        self.__toggled = value

    def __handle_toggled(self, checked):
        if callable(self.toggled):
            self.toggled(checked)

    def click(self):
        self.qt.click()

@bind(QtWidgets.QPushButton)
class Button(BaseButton):

    def __init__(self, text=None, *, default=False, auto_default=False,
                 flat=None, **kwargs):
        super().__init__(text, **kwargs)
        if default is not None:
            self.default = default
        if auto_default is not None:
            self.auto_default = auto_default
        if flat is not None:
            self.flat = flat

    @property
    def default(self):
        return self.qt.isDefault()

    @default.setter
    def default(self, value):
        self.qt.setDefault(value)

    @property
    def auto_default(self):
        return self.qt.isAutoDefault()

    @auto_default.setter
    def auto_default(self, value):
        self.qt.setAutoDefault(value)

    @property
    def flat(self):
        return self.qt.isFlat()

    @flat.setter
    def flat(self, value):
        self.qt.setFlat(value)

@bind(QtWidgets.QRadioButton)
class RadioButton(BaseButton):

    pass
