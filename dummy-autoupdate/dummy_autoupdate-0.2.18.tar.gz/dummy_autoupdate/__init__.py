from dummy_autoupdate.main_window import MainWindow
from dummy_autoupdate.__version import __version__

__author__ = 'Vladimir Starostin'
__email__ = 'v.starostin.m@gmail.com'


def run():
    import logging

    from PyQt5.QtWidgets import QApplication

    log_file = 'dummy_autoupdate_log.txt'

    logging.basicConfig(level=logging.INFO, filename=log_file)

    qapp = QApplication([])
    logger = logging.getLogger(__name__)
    window = MainWindow(__version__)

    try:
        with open(log_file, 'r') as f:
            log = f.read()
            window.debug_window.widget.appendPlainText(log)
    except FileNotFoundError:
        pass

    logger.info(f'{"*" * 10}')
    logger.info(f'Starting version {__version__}!')
    logger.info(f'{"*" * 10}')

    return qapp.exec_()


if __name__ == '__main__':
    run()
