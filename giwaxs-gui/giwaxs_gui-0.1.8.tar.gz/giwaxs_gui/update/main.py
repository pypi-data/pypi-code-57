from dataclasses import dataclass
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool

from ..__version import __version__

from .check_version import CheckVersionMessage, check_outdated
from .widgets import WaitWindow
from .tools import Worker
from .update_package import update_package


@dataclass
class ResultContainer:
    res: CheckVersionMessage = CheckVersionMessage.not_checked


class MainUpdate(QObject):
    log = logging.getLogger(__name__)

    def __init__(self, res: ResultContainer):
        super().__init__()
        for log in (logging.getLogger(name) for name in logging.root.manager.loggerDict):
            log.setLevel(logging.INFO)

        self.res = res
        self.wait_window = WaitWindow('Checking for updates ...')
        self.q_thread_pool = QThreadPool(self)
        self.worker = Worker(check_outdated, version=__version__)
        # self.worker.autoDelete()
        self.worker.signals.result.connect(self._on_result_received)
        self.log.error(f'Current version is {__version__}')
        self.q_thread_pool.start(self.worker)

    @pyqtSlot(object, name='onResultReceived')
    def _on_result_received(self, res: CheckVersionMessage):
        if res == CheckVersionMessage.new_version_available:
            try:
                self.log.info(f'New version {res.version} available!')
                self._update_package(res.version)
            except AttributeError:
                self.res.res = CheckVersionMessage.failed_updating
                self.close_update()
        else:
            self.res.res = res
            self.close_update()

    def _update_package(self, version: str):
        self.wait_window.set_text('Updating the package')
        self.worker = Worker(update_package, version=version)
        self.worker.signals.result.connect(self._on_updated)
        # self.worker.autoDelete()
        self.q_thread_pool.start(self.worker)

    @pyqtSlot(object, name='onUpdated')
    def _on_updated(self, updated: bool):
        if updated:
            self.res.res = CheckVersionMessage.updated
        else:
            self.res.res = CheckVersionMessage.failed_updating

        self.close_update()

    def close_update(self):
        self.wait_window.close()
        self.q_thread_pool.deleteLater()
        self.deleteLater()
        q_app = QApplication.instance()
        q_app.exit(0)
