"""Text area input.

For more information on the underlying Qt5 object see [QTextEdit](https://doc.qt.io/qt-5/qtextedit.html).
"""

from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget

__all__ = ['TextArea']

@bind(QtWidgets.QTextEdit)
class TextArea(BaseWidget):
    """Text area widget.

    >>> textarea = TextArea('lorem')
    >>> textarea.append(' ispum')
    >>> textarea.value
    'lorem ipsum'
    >>> tree.clear()
    textarea.value
    ''
    """

    def __init__(self, value=None, *, readonly=False, richtext=False, **kwargs):
        super().__init__(**kwargs)
        self.readonly = readonly
        self.richtext = richtext
        if value is not None:
            self.value = value

    @property
    def value(self):
        return self.qt.toPlainText()

    @value.setter
    def value(self, value):
        self.qt.setPlainText(value)

    @property
    def readonly(self):
        """Read only enabled.

        >>> textarea.readonly = True
        >>> textarea.readonly
        True
        """
        return self.qt.isReadOnly()

    @readonly.setter
    def readonly(self, value):
        self.qt.setReadOnly(value)

    @property
    def richtext(self):
        """Rich Text enabled.

        >>> textarea.richtext = True
        >>> textarea.richtext
        True
        """
        return self.qt.acceptRichText()

    @richtext.setter
    def richtext(self, value):
        self.qt.setAcceptRichText(value)

    def append(self, text):
        """Append text as paragraph to current value.

        >>> textarea = TextArea('lorem')
        >>> textarea.append(' ipsum')
        >>> textarea.value
        'lorem\n ipsum'
        """
        self.qt.append(text)

    def insert(self, text):
        """Insert text at cursor position.

        >>> textarea.insert('ipsum')
        """
        self.qt.insertPlainText(text)

    def clear(self):
        """Clear current value.

        >>> textarea.clear()
        >>> textarea.value
        ''
        """
        self.qt.clear()

    def select_all(self):
        """Select entire text."""
        self.qt.selectAll()

    def redo(self):
        """Redo last user changes."""
        self.qt.redo()

    def undo(self):
        """Undo last user changes."""
        self.qt.undo()
