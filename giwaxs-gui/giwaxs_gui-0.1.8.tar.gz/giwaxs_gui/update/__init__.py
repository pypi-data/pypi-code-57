from PyQt5.QtWidgets import QApplication

import qdarkgraystyle

from giwaxs_gui.update.main import MainUpdate, ResultContainer, CheckVersionMessage
from giwaxs_gui.update.update_package import giwaxs_gui_update


def check_version_program() -> CheckVersionMessage:
    q_app = QApplication([])
    q_app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
    res = ResultContainer()
    window = MainUpdate(res)
    q_app.exec_()

    return res.res

