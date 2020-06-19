import os
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from dummy_autoupdate.main_window import MainWindow
from dummy_autoupdate.__version import __version__


def run():
    import sys
    import logging

    logging.basicConfig(level=logging.DEBUG)

    qapp = QApplication([])
    logger = logging.getLogger(__name__)
    window = MainWindow(__version__)
    reboot_exit = window.EXIT_CODE_REBOOT
    exit_code = qapp.exec_()

    if exit_code == reboot_exit:
        python = sys.executable
        logger.info(f'Rebooting the program with {python}...')
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    run()
