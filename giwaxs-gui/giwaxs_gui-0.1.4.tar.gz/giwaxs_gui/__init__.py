import sys
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from giwaxs_gui.app import App
from giwaxs_gui.gui import GIWAXSMainController, UncaughtHook, DebugWindow
from giwaxs_gui.__version import __version__
from giwaxs_gui.update import CheckVersionMessage

__author__ = 'Vladimir Starostin'
__email__ = 'v.starostin.m@gmail.com'


def run(res: CheckVersionMessage, logging_level: int = logging.ERROR):
    print(res)

    for log in (logging.getLogger(name) for name in logging.root.manager.loggerDict):
        log.setLevel(logging_level)

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    q_app = QApplication([])

    giwaxs_app = GIWAXSMainController()

    return q_app.exec_()


if __name__ == '__main__':
    sys.exit(run())
