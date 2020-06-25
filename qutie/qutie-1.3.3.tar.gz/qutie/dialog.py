from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget
from .widget import Widget
from .mixins import OrientationMixin

__all__ = [
    'Dialog',
    'DialogButtonBox',
    'filename_open',
    'filenames_open',
    'directory_open',
    'filename_save',
    'get_number',
    'get_text',
    'get_item'
]

@bind(QtWidgets.QDialog)
class Dialog(Widget):

    def __init__(self, *, accepted=None, rejected=None, **kwargs):
        super().__init__(**kwargs)

        self.accepted = accepted
        def accepted_event():
            if callable(self.accepted):
                self.accepted()
        self.qt.accepted.connect(accepted_event)

        self.rejected = rejected
        def rejected_event():
            if callable(self.rejected):
                self.rejected()
        self.qt.rejected.connect(rejected_event)

    def accept(self):
        return self.qt.accept()

    def reject(self):
        return self.qt.reject()

    def run(self):
        return {
            self.qt.Accepted: True,
            self.qt.Rejected: False
        }[self.qt.exec_()]

@bind(QtWidgets.QDialogButtonBox)
class DialogButtonBox(BaseWidget, OrientationMixin):

    QtStandardButtons = {
        'ok': QtWidgets.QDialogButtonBox.Ok,
        'open': QtWidgets.QDialogButtonBox.Open,
        'save': QtWidgets.QDialogButtonBox.Save,
        'cancel': QtWidgets.QDialogButtonBox.Cancel,
        'close': QtWidgets.QDialogButtonBox.Close,
        'discard': QtWidgets.QDialogButtonBox.Discard,
        'apply': QtWidgets.QDialogButtonBox.Apply,
        'reset': QtWidgets.QDialogButtonBox.Reset,
        'restore_defaults': QtWidgets.QDialogButtonBox.RestoreDefaults,
        'help': QtWidgets.QDialogButtonBox.Help,
        'save_all': QtWidgets.QDialogButtonBox.SaveAll,
        'yes': QtWidgets.QDialogButtonBox.Yes,
        'yes_to_all': QtWidgets.QDialogButtonBox.YesToAll,
        'no': QtWidgets.QDialogButtonBox.No,
        'no_to_all': QtWidgets.QDialogButtonBox.NoToAll,
        'abort': QtWidgets.QDialogButtonBox.Abort,
        'retry': QtWidgets.QDialogButtonBox.Retry,
        'ignore': QtWidgets.QDialogButtonBox.Ignore
    }

    def __init__(self, buttons=None, orientation=None, accepted=None,
                 rejected=None, clicked=None, help_requested=None, **kwargs):
        super().__init__(**kwargs)
        if buttons is not None:
            self.buttons = buttons
        if orientation is not None:
            self.orientation = orientation
        self.accepted = accepted
        self.rejected = rejected
        self.clicked = clicked
        self.help_requested = help_requested
        # Connect signals
        self.qt.accepted.connect(self.__handle_accepted)
        self.qt.rejected.connect(self.__handle_rejected)
        self.qt.clicked.connect(self.__handle_clicked)
        self.qt.helpRequested.connect(self.__handle_help_requested)

    @property
    def buttons(self):
        buttons = []
        values = self.qt.standardButtons()
        for key, mask in self.QtStandardButtons.items():
            if values & mask:
                buttons.append(key)
        return tuple(buttons)

    @buttons.setter
    def buttons(self, value):
        buttons = 0
        for button in value:
            buttons |= self.QtStandardButtons.get(button, 0)
        self.qt.setStandardButtons(buttons)

    @property
    def accepted(self):
        return self.__accepted

    @accepted.setter
    def accepted(self, value):
        self.__accepted = value

    def __handle_accepted(self):
        if callable(self.accepted):
            self.accepted()

    @property
    def rejected(self):
        return self.__rejected

    @rejected.setter
    def rejected(self, value):
        self.__rejected = value

    def __handle_rejected(self):
        if callable(self.rejected):
            self.rejected()

    @property
    def clicked(self):
        return self.__clicked

    @clicked.setter
    def clicked(self, value):
        self.__clicked = value

    def __handle_clicked(self, button):
        if callable(self.clicked):
            button = self.qt.standardButton(button)
            for key, value in self.QtStandardButtons.items():
                if button == value:
                    self.clicked(key)
                    break

    @property
    def help_requested(self):
        return self.__help_requested

    @help_requested.setter
    def help_requested(self, value):
        self.__help_requested = value

    def __handle_help_requested(self):
        if callable(self.help_requested):
            self.help_requested()

def filename_open(path=None, *, filter=None, title=None):
    """Shows a filename selection dialog, returns selected filename path.

    >>> filename_open("/home/user", filter="Text (*.txt)")
    '/home/user/example.txt'
    """
    if title is None:
        title = "Open file"
    return QtWidgets.QFileDialog.getOpenFileName(None, title, path, filter)[0] or None

def filenames_open(path=None, *, filter=None, title=None):
    """Shows a multiple filenames selection dialog, returns list of selected
    filename paths.

    >>> filename_open("/home/user", filter="Text (*.txt)")
    ['/home/user/example.txt', '/home/user/another.txt']
    """
    if title is None:
        title = "Open files"
    return QtWidgets.QFileDialog.getOpenFileNames(None, title, path, filter)[0] or None

def directory_open(path=None, *, title=None):
    """Shows a multiple filenames selection dialog, returns selected directory
    path.

    >>> filename_open(""/home/user")
    '/tmp'
    """
    return QtWidgets.QFileDialog.getExistingDirectory(None, title or "Open directory", path) or None

def filename_save(path=None, *, filter=None, title=None):
    """Shows a save filename selection dialog, returns selected filename path.

    >>> filename_save("/home/user/example.txt", filter="Text (*.txt)")
    '/home/user/other.txt'
    """
    if title is None:
        title = "Save file"
    return QtWidgets.QFileDialog.getSaveFileName(None, title, path, filter)[0] or None

def get_number(value=0, *, minimum=None, maximum=None, decimals=0, title=None, label=None):
    """Number input dialog, optionally editable.

    >>> get_number(value=4.2, minimum=0, maximum=10, decimals=1)
    'Pear'
    """
    value = float(value)
    if minimum is None:
        minimum = float('-inf')
    if maximum is None:
        maximum = float('-inf')
    if title is None:
        title = ""
    if label is None:
        label = ""
    value, success = QtWidgets.QInputDialog.getDouble(
        None, title, label, value, minimum, maximum, decimals
    )
    if success:
        return value
    return None

def get_text(text=None, *, title=None, label=None):
    """Text input dialog.

    >>> get_text()
    'Pear'
    """
    text = format(text)
    if title is None:
        title = ""
    if label is None:
        label = ""
    value, success = QtWidgets.QInputDialog.getText(
        None, title, label, QtWidgets.QLineEdit.Normal, text
    )
    if success:
        return value
    return None

def get_item(items, *, current=0, editable=False, title=None, label=None):
    """Select item from input list dialog, optionally editable.

    >>> get_item(["Apple", "Pear", "Nut"])
    'Pear'
    """
    items = [format(item) for item in items]
    if title is None:
        title = ""
    if label is None:
        label = ""
    item, success = QtWidgets.QInputDialog.getItem(
        None, title, label, items, current, editable
    )
    if success:
        return item
    return None
