import logging

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

from .spinner import Spinner
from .tools import center_widget
from .check_version import CheckVersionMessage


class WaitWindow(QWidget):
    sigUpdateClicked = pyqtSignal()

    log = logging.getLogger(__name__)

    def __init__(self, label: str = 'Check for updates ... ', parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setMinimumWidth(500)

        # self.setWindowModality(Qt.ApplicationModal)

        self.spinner = Spinner(self)
        self.update_button = QPushButton('Update')
        self.update_button.clicked.connect(self._update_clicked)
        self.update_button.hide()
        self.update_button.setDisabled(True)
        self.label = QLabel(label)
        self.setMinimumWidth(300)
        self.setFixedHeight(70)
        layout = QGridLayout(self)
        layout.addWidget(self.spinner, 0, 0)
        layout.addWidget(self.label, 0, 1)
        layout.addWidget(self.update_button, 0, 2)

        center_widget(self)
        self.show()

    def set_text(self, text: str):
        self.label.setText(text)

    def _update_clicked(self):
        self.spinner.show()
        self.spinner.resume()
        self.label.setText('Updating version ...')
        self.update_button.hide()
        self.sigUpdateClicked.emit()

    def show_info(self, text: str, hide_spinner: bool = True):
        if hide_spinner:
            self.spinner.pause()
            self.spinner.hide()
        self.label.setText(text)

    @pyqtSlot(object, name='checkOutdated')
    def get_result(self, res: CheckVersionMessage):
        if res == CheckVersionMessage.no_internet:
            self.set_text('Could not check the latest version (connection error).')
        if res == CheckVersionMessage.error:
            self.set_text('Could not check the latest version.')
        if res == CheckVersionMessage.latest_version_installed:
            self.set_text(f'You use the latest version {res.version}!')
        if res == CheckVersionMessage.new_version_available:
            self.set_text(f'New version available: {res.version}. Please, update your program.')
            self.update_button.setDisabled(False)
            self.update_button.show()
        self.spinner.pause()
        self.spinner.hide()
