import os
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from dummy_autoupdate.main_window import MainWindow
from dummy_autoupdate.__version import __version__


def run():
    import sys
    import logging

    print(sys.executable)

    log_file = 'dummy_autoupdate_log.txt'
    logging.basicConfig(level=logging.DEBUG, filename=log_file)
    print((Path(__file__).parent / log_file).resolve())

    qapp = QApplication([])
    window = MainWindow(__version__)
    reboot_exit = window.EXIT_CODE_REBOOT
    exit_code = qapp.exec_()

    if exit_code == reboot_exit:
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    run()
