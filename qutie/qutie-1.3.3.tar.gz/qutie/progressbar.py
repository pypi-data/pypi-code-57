"""Progress bar.

For more information on the underlying Qt5 object see [QProgressBar](https://doc.qt.io/qt-5/qprogressbar.html).
"""

from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget
from .mixins import OrientationMixin

__all__ = ['ProgressBar']

@bind(QtWidgets.QProgressBar)
class ProgressBar(BaseWidget, OrientationMixin):

    def __init__(self, value=0, *, minimum=0, maximum=100, format=None,
                 inverted_appearance=False, orientation=None,
                 text_visible=None, value_changed=None, **kwargs):
        super().__init__(**kwargs)
        self.minimum = minimum
        self.maximum = maximum
        if format is not None:
            self.format = format
        self.inverted_appearance = inverted_appearance
        if orientation is not None:
            self.orientation = orientation
        if text_visible is not None:
            self.text_visible = text_visible
        self.value = value
        self.value_changed = value_changed
        # Connect signals
        self.qt.valueChanged.connect(self.__handle_value_changed)

    @property
    def value(self):
        return self.qt.value()

    @value.setter
    def value(self, value):
        self.qt.setValue(value)

    @property
    def minimum(self):
        return self.qt.minimum()

    @minimum.setter
    def minimum(self, value):
        self.qt.setMinimum(value)

    @property
    def maximum(self):
        return self.qt.maximum()

    @maximum.setter
    def maximum(self, value):
        self.qt.setMaximum(value)

    @property
    def format(self):
        """Format for displayed text, placeholders are %p, %v and %m."""
        return self.qt.format()

    @format.setter
    def format(self, value):
        self.qt.setFormat(value)

    def reset_format(self):
        self.qt.resetFormat()

    @property
    def inverted_appearance(self):
        return self.qt.invertedAppearance()

    @inverted_appearance.setter
    def inverted_appearance(self, value):
        self.qt.setInvertedAppearance(value)

    @property
    def text(self):
        return self.qt.text()

    @property
    def text_visible(self):
        return self.qt.isTextVisible()

    @text_visible.setter
    def text_visible(self, value):
        self.qt.setTextVisible(value)

    @property
    def range(self):
        return self.minimum, self.maximum

    @range.setter
    def range(self, value):
        self.minimum = value[0]
        self.maximum = value[1]

    @property
    def value_changed(self):
        return self.__value_changed

    @value_changed.setter
    def value_changed(self, value):
        self.__value_changed = value

    def __handle_value_changed(self, value):
        if callable(self.value_changed):
            self.value_changed(value)

    def reset(self):
        self.qt.reset()
