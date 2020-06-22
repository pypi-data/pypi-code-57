import enum
import logging
import sys
import os.path
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import kammanta.model
import kammanta.glob

WIDTH_AND_HEIGHT_INT = 250


class MarkdownDisplayDialog(QtWidgets.QDialog):
    def __init__(self, i_title: str, i_text: str):
        super().__init__()
        # , *args, **kwargs

        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        self.setSizeGripEnabled(True)
        self.setWindowTitle(i_title)

        vbox_l1 = QtWidgets.QVBoxLayout(self)

        self.editor_qte = QtWidgets.QTextEdit()
        vbox_l1.addWidget(self.editor_qte)
        self.editor_qte.setReadOnly(True)
        self.editor_qte.setMarkdown(i_text)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox_l1.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    @staticmethod
    def open_dlg(i_title: str, i_text: str) -> None:
        file_and_dir_dlg = MarkdownDisplayDialog(i_title, i_text)
        dialog_result = file_and_dir_dlg.exec_()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Existing file
    MarkdownDisplayDialog.open_dlg(
        "Title test", "# Content test\n\nParagraph text\n\n* List item 1\n* another line",
    )

    sys.exit()

