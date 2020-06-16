from .qt import QtCore
from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget

__all__ = ['CheckBox']

@bind(QtWidgets.QCheckBox)
class CheckBox(BaseWidget):

    def __init__(self, text=None, *, checked=False, changed=None, **kwargs):
        super().__init__(**kwargs)
        if text is not None:
            self.text = text
        self.checked = checked
        self.changed = changed
        # Connect signals
        self.qt.stateChanged.connect(self.__handle_changed)

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, value):
        self.qt.setText(value)

    @property
    def checked(self):
        return self.qt.checkState() == QtCore.Qt.Checked

    @checked.setter
    def checked(self, value):
        self.qt.setChecked(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, value):
        self.__changed = value

    def __handle_changed(self, state):
        if callable(self.changed):
            self.changed(state == QtCore.Qt.Checked)
