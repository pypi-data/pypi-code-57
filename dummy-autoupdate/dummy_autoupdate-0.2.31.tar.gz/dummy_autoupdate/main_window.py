import logging

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSlot, QThreadPool

from .wait_window import WaitWindow
from .tools import Worker
from .update_version import update_version
from .check_version import check_outdated, CheckVersionMessage
from .debug_window import QTextEditLogger


class MainWindow(QWidget):
    log = logging.getLogger(__name__)

    EXIT_CODE_REBOOT: int = -123456789

    def __init__(self, version: str):
        super().__init__()
        self.status = CheckVersionMessage.not_checked
        self.current_version = version

        self.wait_window = WaitWindow(f'You use the version {version}.')
        self.debug_window = QTextEditLogger()

        self.wait_window.sigUpdateClicked.connect(self._update_version)
        self.wait_window.sigRestartClicked.connect(self.restart)
        self.wait_window.sigCheckClicked.connect(self.check_version)

        self.q_thread_pool = QThreadPool()

    @pyqtSlot(object, name='setStatus')
    def _set_status(self, res: CheckVersionMessage):
        self.status = res

    @pyqtSlot(name='updateVersion')
    def _update_version(self):
        self.wait_window.on_update()
        try:
            version = self.status.version
        except AttributeError:
            version = None

        self.worker = Worker(update_version, version=version)
        self.worker.signals.result.connect(self._on_updated)
        self.q_thread_pool.start(self.worker)

    @pyqtSlot(name='checkVerison')
    def check_version(self):
        self.wait_window.on_checking()

        self.worker = Worker(check_outdated, self.current_version)
        self.worker.signals.result.connect(self.wait_window.get_result)
        self.worker.signals.result.connect(self._set_status)
        self.q_thread_pool.start(self.worker)

    @pyqtSlot(object, name='onUpdatedFinished')
    def _on_updated(self, updated: bool):
        if updated:
            self.wait_window.show_restart()
        else:
            self.wait_window.show_info('Auto update failed. Please, update the program manually.')

    @pyqtSlot(name='restartApp')
    def restart(self):
        qApp = QApplication.instance()
        qApp.closeAllWindows()
        qApp.exit(self.EXIT_CODE_REBOOT)

