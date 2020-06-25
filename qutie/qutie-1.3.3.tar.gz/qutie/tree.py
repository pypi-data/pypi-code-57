"""Simple item based tree view.

For more information on the underlying Qt5 objects see [QTreeWidget](https://doc.qt.io/qt-5/qtreewidget.html) and [QTreeWidgetItem](https://doc.qt.io/qt-5/qtreewidgetitem.html).
"""

from .qt import QtCore
from .qt import QtGui
from .qt import QtWidgets
from .qt import bind

from .base import Base
from .icon import Icon
from .list import BaseItemView

__all__ = ['Tree', 'TreeItem', 'TreeItemColumn']

@bind(QtWidgets.QTreeWidget)
class Tree(BaseItemView):
    """Tree widget.

    >>> tree = Tree(header=["Key", "Value"])
    >>> tree.append(["Spam", "Eggs"])
    >>> for item in tree:
    ...     item[0].checked =True
    ...     item[1].color = "blue"
    ...     child = item.append(["Ham", "Spam"])
    ...     child.checked = False
    >>> tree.clear()
    """

    def __init__(self, items=None, *, header=None, sortable=False, indentation=None,
                 activated=None, changed=None, clicked=None,
                 double_clicked=None, selected=None, **kwargs):
        super().__init__(**kwargs)
        if items is not None:
            self.items = items
        self.header = header or []
        self.sortable = sortable
        if indentation is not None:
            self.indentation = indentation
        self.activated = activated
        self.changed = changed
        self.clicked = clicked
        self.double_clicked = double_clicked
        self.selected = selected
        # Connect signals
        self.qt.itemActivated.connect(self.__handle_activated)
        self.qt.itemChanged.connect(self.__handle_changed)
        self.qt.itemClicked.connect(self.__handle_clicked)
        self.qt.itemDoubleClicked.connect(self.__handle_double_clicked)
        self.qt.itemSelectionChanged.connect(self.__handle_selected)

    @property
    def header(self):
        return self.qt.headerLabels()

    @header.setter
    def header(self, value):
        self.qt.setColumnCount(len(value))
        self.qt.setHeaderLabels(value)

    @property
    def sortable(self):
        return self.qt.isSortingEnabled()

    @sortable.setter
    def sortable(self, value):
        self.qt.setSortingEnabled(value)

    @property
    def indentation(self):
        return self.qt.indentation()

    @indentation.setter
    def indentation(self, value):
        self.qt.setIndentation(value)

    @property
    def activated(self):
        return self.__activated

    @activated.setter
    def activated(self, value):
        self.__activated = value

    def __handle_activated(self, item, index):
        if callable(self.activated):
            data = item.data(0, item.UserType)
            if data is not None:
                self.activated(index, data)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, value):
        self.__changed = value

    def __handle_changed(self, item, index):
        if callable(self.changed):
            data = item.data(0, item.UserType)
            if data is not None:
                self.changed(index, data)

    @property
    def clicked(self):
        return self.__clicked

    @clicked.setter
    def clicked(self, value):
        self.__clicked = value

    def __handle_clicked(self, item, index):
        if callable(self.clicked):
            data = item.data(0, item.UserType)
            if data is not None:
                self.clicked(index, data)

    @property
    def double_clicked(self):
        return self.__double_clicked

    @double_clicked.setter
    def double_clicked(self, value):
        self.__double_clicked = value

    def __handle_double_clicked(self, item, index):
        if callable(self.double_clicked):
            data = item.data(0, item.UserType)
            if data is not None:
                self.double_clicked(index, data)

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value):
        self.__selected = value

    def __handle_selected(self):
        if callable(self.selected):
            items = self.qt.selectedItems()
            if items:
                first = items[0].data(0, items[0].UserType)
                self.selected(first)

    def append(self, item):
        """Append item or item labels, returns appended item.
        >>> tree.append(TreeItem(["Spam", "Eggs"]))
        or
        >>> tree.append(["Spam", "Eggs"])
        """
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.addTopLevelItem(item.qt)
        item.expanded = True
        return item

    def insert(self, index, item):
        """Insert item or item labels at index, returns inserted item.
        >>> tree.insert(0, TreeItem(["Spam", "Eggs"]))
        or
        >>> tree.insert(0, ["Spam", "Eggs"])
        """
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.insertTopLevelItem(index, item.qt)
        item.expanded = True
        return item

    def remove(self, item):
        index = self.qt.indexOfTopLevelItem(item.qt)
        self.qt.takeTopLevelItem(index)

    def clear(self):
        self.qt.clear()

    @property
    def current(self):
        """Returns current tree item or None."""
        item = self.qt.currentItem()
        if item is not None:
            return item.data(0, item.UserType)
        return item

    @current.setter
    def current(self, value):
        assert isinstance(value, TreeItem)
        self.qt.setCurrentItem(value.qt)

    def index(self, item):
        return self.qt.indexOfTopLevelItem(item.qt)

    @property
    def stretch(self):
        return self.qt.header().stretchLastSection()

    @stretch.setter
    def stretch(self, value):
        self.qt.header().setStretchLastSection(value)

    def fit(self, column=None):
        if column is None:
            for column in range(self.qt.columnCount()):
                self.qt.resizeColumnToContents(column)
        else:
            self.qt.resizeColumnToContents(column)

    def scroll_to(self, item):
        """Scroll to item to ensure item is visible."""
        self.qt.scrollToItem(item.qt)

    def __getitem__(self, key):
        item = self.qt.topLevelItem(key)
        return item.data(0, item.UserType)

    def __setitem__(self, key, value):
        self.remove(value)
        self.insert(key, value)

    def __delitem__(self, key):
        item = self.qt.topLevelItem(key)
        self.remove(item)

    def __len__(self):
        return self.qt.topLevelItemCount()

    def __iter__(self):
        return (self[index] for index in range(len(self)))

@bind(QtWidgets.QTreeWidgetItem)
class TreeItem(Base):
    """Tree item class."""

    def __init__(self, values=None, **kwargs):
        super().__init__(**kwargs)
        self.__default_foreground = self.qt.foreground(0)
        self.__default_background = self.qt.background(0)
        self.qt.setData(0, self.qt.UserType, self)
        if values is not None:
            for column, value in enumerate(values):
                self[column].value = value

    @property
    def children(self):
        """List of tree item's children."""
        items = []
        for index in range(self.qt.childCount()):
            item = self.qt.child(index)
            items.append(item.data(0, item.UserType))
        return items

    def append(self, item):
        """Append child item to this item."""
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.addChild(item.qt)
        return item

    def insert(self, index, item):
        """Insert child item to this item."""
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.insertChild(index, item.qt)
        return item

    @property
    def checkable(self):
        """Checkable state, `True` if item is checkable by user."""
        return self.qt.flags() & QtCore.Qt.ItemIsUserCheckable

    @checkable.setter
    def checkable(self, value):
        if value:
            flags = self.qt.flags() | QtCore.Qt.ItemIsUserCheckable
        else:
            flags = self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable
        self.qt.setFlags(flags)

    @property
    def expanded(self):
        """Expanded state, `True` if item is expanded."""
        return self.qt.isExpanded()

    @expanded.setter
    def expanded(self, value):
        self.qt.setExpanded(value)

    def __getitem__(self, column):
        return TreeItemColumn(column, self.qt)

    def __len__(self):
        return self.qt.columnCount()

    def __iter__(self):
        return (TreeItemColumn(column, self.qt) for column in range(len(self)))

class TreeItemColumn:
    """This class provides access to tree item column specific properties."""

    def __init__(self, column, qt):
        self.__column = column
        self.__qt = qt

    @property
    def column(self):
        return self.__column

    @property
    def qt(self):
        return self.__qt

    @property
    def value(self):
        """Column value."""
        return self.qt.data(self.column, self.qt.Type)

    @value.setter
    def value(self, value):
        return self.qt.setData(self.column, self.qt.Type, value)

    @property
    def color(self):
        return self.qt.foreground(self.column).color().name()

    @color.setter
    def color(self, value):
        if value is None:
            brush = QtGui.QBrush(self.__default_foreground)
        else:
            brush = QtGui.QBrush(QtGui.QColor(value))
        self.qt.setForeground(self.column, brush)

    @property
    def background(self):
        return self.qt.background(self.column).color().name()

    @background.setter
    def background(self, value):
        if value is None:
            brush = QtGui.QBrush(self.__default_background)
        else:
            brush = QtGui.QBrush(QtGui.QColor(value))
        self.qt.setBackground(self.column, brush)

    @property
    def icon(self):
        """Column icon, can be a `Pixmap`, filename or color."""
        icon = self.qt.icon(self.column)
        if icon.isNull():
            return None
        return Icon(qt=icon)

    @icon.setter
    def icon(self, value):
        if value is None:
            self.qt.setIcon(self.column, QtGui.QIcon())
        else:
            if not isinstance(value, Icon):
                value = Icon(value)
            self.qt.setIcon(self.column, value.qt)

    @property
    def checked(self):
        return self.qt.checkState(self.column) == QtCore.Qt.Checked

    @checked.setter
    def checked(self, value):
        self.qt.setCheckState(self.column, QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)
