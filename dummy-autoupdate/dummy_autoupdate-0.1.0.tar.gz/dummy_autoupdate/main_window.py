import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, QThreadPool

from .wait_window import WaitWindow
from .tools import Worker
from .update_version import update_version
from .check_version import check_outdated, CheckVersionMessage
from .restart import restart


class MainWindow(QWidget):
    log = logging.getLogger(__name__)

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
        self.worker = Worker(update_version)
        self.worker.signals.finished.connect(self._on_updated)
        self.q_thread_pool.start(self.worker)

    @pyqtSlot(bool, name='onUpdated')
    def _on_updated(self, updated: bool):
        if updated:
            restart()
        else:
            self.wait_window.show_info('Auto update failed. Please, update the program manually.')
