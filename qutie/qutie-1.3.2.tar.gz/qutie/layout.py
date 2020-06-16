from .qt import QtWidgets

from .widget import BaseWidget

__all__ = ['Column', 'Row', 'Spacer']

class BoxLayout(BaseWidget):

    QtLayoutClass = QtWidgets.QBoxLayout

    def __init__(self, *children, stretch=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setLayout(self.QtLayoutClass())
        self.qt.layout().setContentsMargins(0, 0, 0, 0)
        for child in children:
            self.append(child)
        if stretch is not None:
            self.stretch = stretch

    @property
    def children(self):
        return list(self)

    @property
    def stretch(self):
        value = []
        for index in range(len(self)):
            value.append(self.qt.layout().stretch(index))
        return value

    @stretch.setter
    def stretch(self, value):
        value = list(value) + ([0] * (len(self) - len(value)))
        for index in range(len(self)):
            self.qt.layout().setStretch(index, value[index])

    def append(self, child):
        self.qt.layout().addWidget(child.qt)

    def insert(self, index, child):
        self.qt.layout().insertWidget(index, child.qt)

    def remove(self, child):
        index = self.qt.layout().indexOf(child.qt)
        self.qt.layout().takeAt(index)

    def __getitem__(self, key):
        return self.qt.layout().itemAt(key).widget().property(self.QtPropertyKey)

    def __len__(self):
        return self.qt.layout().count()

    def __iter__(self):
        return (self[index] for index in range(len(self)))

class Column(BoxLayout):

    QtLayoutClass = QtWidgets.QVBoxLayout

class Row(BoxLayout):

    QtLayoutClass = QtWidgets.QHBoxLayout

class Spacer(BaseWidget):

    QtSizePolicy = {
        'fixed': QtWidgets.QSizePolicy.Fixed,
        'minimum': QtWidgets.QSizePolicy.Minimum,
        'maximum': QtWidgets.QSizePolicy.Maximum,
        'preferred': QtWidgets.QSizePolicy.Preferred,
        'expanding': QtWidgets.QSizePolicy.Expanding,
        'minimum_expanding': QtWidgets.QSizePolicy.MinimumExpanding,
        'ignored': QtWidgets.QSizePolicy.Ignored
    }

    def __init__(self, horizontal=True, vertical=True, **kwargs):
        super().__init__(**kwargs)
        self.qt.setSizePolicy(
            self.QtSizePolicy.get('expanding' if horizontal else 'fixed'),
            self.QtSizePolicy.get('expanding' if vertical else 'fixed')
        )
