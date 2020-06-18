import logging
import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSlot, QThreadPool

from .wait_window import WaitWindow
from .tools import Worker
from .update_version import update_version
from .check_version import check_outdated, CheckVersionMessage


class MainWindow(QWidget):
    log = logging.getLogger(__name__)

    EXIT_CODE_REBOOT: int = -123456789

    def __init__(self, version: str):
        super().__init__()
        self.status = CheckVersionMessage.not_checked

        self.wait_window = WaitWindow()
        self.wait_window.sigUpdateClicked.connect(self._update_version)
        self.q_thread_pool = QThreadPool()
        self.worker = Worker(check_outdated, version)
        self.worker.signals.result.connect(self.wait_window.get_result)
        self.worker.signals.result.connect(self._set_status)
        self.q_thread_pool.start(self.worker)

    @pyqtSlot(object, name='setStatus')
    def _set_status(self, res: CheckVersionMessage):
        self.status = res

    @pyqtSlot(name='updateVersion')
    def _update_version(self):
        self.worker1 = Worker(update_version)
        self.worker1.signals.result.connect(self._on_updated)
        self.q_thread_pool.start(self.worker1)

    @pyqtSlot(object, name='onUpdatedFinished')
    def _on_updated(self, updated: bool):
        if updated:
            qApp = QApplication.instance()
            qApp.closeAllWindows()
            qApp.exit(self.EXIT_CODE_REBOOT)
        else:
            self.wait_window.show_info('Auto update failed. Please, update the program manually.')
