"""Single line text input.

For more information on the underlying Qt5 object see [QLineEdit](https://doc.qt.io/qt-5/qlineedit.html).
"""

from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget

__all__ = ['Text']

@bind(QtWidgets.QLineEdit)
class Text(BaseWidget):
    """Text input widget.

    >>> text = Text('lorem')
    >>> text.append(' ispum')
    >>> text.value
    'lorem ipsum'
    >>> tree.clear()
    text.value
    ''
    """

    def __init__(self, value=None, *, readonly=False, clearable=False,
                 changed=None, editing_finished=None, **kwargs):
        super().__init__(**kwargs)
        self.readonly = readonly
        self.clearable = clearable
        if value is not None:
            self.value = value
        self.changed = changed
        self.editing_finished = editing_finished
        # Connect signals
        self.qt.textChanged.connect(self.__handle_changed)
        self.qt.editingFinished.connect(self.__handle_editing_finished)

    @property
    def value(self):
        return self.qt.text()

    @value.setter
    def value(self, value):
        self.qt.setText(format(value))

    @property
    def readonly(self):
        """Read only enabled.

        >>> text.readonly = True
        >>> text.readonly
        True
        """
        return self.qt.isReadOnly()

    @readonly.setter
    def readonly(self, value):
        self.qt.setReadOnly(value)

    @property
    def clearable(self):
        """Inline clear button enabled.

        >>> text.clearable = True
        >>> text.clearable
        True
        """
        return self.qt.isClearButtonEnabled()

    @clearable.setter
    def clearable(self, value):
        self.qt.setClearButtonEnabled(bool(value))

    @property
    def changed(self):
        """Event called when value changed."""
        return self.__changed

    @changed.setter
    def changed(self, value):
        self.__changed = value

    def __handle_changed(self, text):
        if callable(self.changed):
            self.changed(text)

    @property
    def editing_finished(self):
        """Event called when editing finished."""
        return self.__editing_finished

    @editing_finished.setter
    def editing_finished(self, value):
        self.__editing_finished = value

    def __handle_editing_finished(self):
        if callable(self.editing_finished):
            self.editing_finished()

    def append(self, text):
        """Append text to current value.

        >>> text =Text('lorem')
        >>> text.append(' ipsum')
        >>> text.value
        'lorem ipsum'
        """
        self.value = ''.join((self.value, format(text)))

    def clear(self):
        """Clear current value.

        >>> text.clear()
        >>> text.value
        ''
        """
        self.qt.clear()
