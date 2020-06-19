import os

from PyQt5.QtWidgets import QApplication

from dummy_autoupdate.main_window import MainWindow
from dummy_autoupdate.__version import __version__

__author__ = 'Vladimir Starostin'
__email__ = 'v.starostin.m@gmail.com'


def run():
    import sys
    import logging

    log_file = 'dummy_autoupdate_log.txt'

    logging.basicConfig(level=logging.DEBUG, filename=log_file)

    qapp = QApplication([])
    logger = logging.getLogger(__name__)
    window = MainWindow(__version__)

    try:
        with open(log_file, 'r') as f:
            log = f.read()
            window.debug_window.widget.appendPlainText(log)
    except FileNotFoundError:
        pass

    reboot_exit = window.EXIT_CODE_REBOOT
    exit_code = qapp.exec_()

    if exit_code == reboot_exit:
        python = sys.executable
        logger.info(f'Rebooting the program with {python}...')
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    run()
