import logging

from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtWidgets import QPlainTextEdit


class QTextEditLogger(logging.Handler, QObject):
    appendPlainText = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        QObject.__init__(self)
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.widget.show()
        self.appendPlainText.connect(self.widget.appendPlainText)
        # self.widget.setMinimumWidth(500)
        # self.widget.setMinimumHeight(500)
        self.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
        logging.getLogger().addHandler(self)
        # logging.getLogger().setLevel(logging.DEBUG)

    def emit(self, record):
        msg = self.format(record)
        try:
            self.appendPlainText.emit(msg)
        except RuntimeError:
            pass
