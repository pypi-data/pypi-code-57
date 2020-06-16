from .qt import QtWidgets
from .qt import bind

from .frame import Frame
from .pixmap import Pixmap

__all__ = ['Label']

@bind(QtWidgets.QLabel)
class Label(Frame):
    """A label widget.

    >>> label = Label('lorem')
    >>> label.text
    'lorem'

    Use a pixmap instead of text.

    >>> label = Label(pixmap='sample.png')
    """

    def __init__(self, text=None, *, indent=None, margin=None, pixmap=None,
                 word_wrap=None, **kwargs):
        super().__init__(**kwargs)
        if text is not None:
            self.text = text
        if indent is not None:
            self.indent = indent
        if margin is not None:
            self.margin = margin
        if pixmap is not None:
            self.pixmap = pixmap
        if word_wrap is not None:
            self.word_wrap = word_wrap

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, value):
        self.qt.setText(format(value))

    @property
    def indent(self):
        return self.qt.indent()

    @indent.setter
    def indent(self, value):
        self.qt.setIndent(int(value))

    @property
    def margin(self):
        return self.qt.margin()

    @margin.setter
    def margin(self, value):
        self.qt.setMargin(int(value))

    @property
    def pixmap(self):
        pixmap = self.qt.pixmap()
        if pixmap is not None:
            return Pixmap(qt=pixmap)
        return None

    @pixmap.setter
    def pixmap(self, value):
        if not isinstance(value, Pixmap):
            value = Pixmap(value)
        self.qt.setPixmap(value.qt)

    @property
    def word_wrap(self):
        """Enable automatic word wrap."""
        return self.qt.wordWrap()

    @word_wrap.setter
    def word_wrap(self, value):
        self.qt.setWordWrap(bool(value))

    @property
    def selected_text(self):
        return self.qt.selectedText()

    def clear(self):
        """Clears label contents."""
        self.qt.clear()
