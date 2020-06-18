from PyQt5.QtWidgets import QApplication

from dummy_autoupdate.main_window import MainWindow

__version__ = '0.1.0'


def run():
    import sys

    qapp = QApplication([])
    window = MainWindow(__version__)
    sys.exit(qapp.exec_())


if __name__ == '__main__':
    run()
