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


class MarkdownInputDialog(QtWidgets.QDialog):
    def __init__(self, i_file_path: str):
        super().__init__()
        # , *args, **kwargs

        contents_str = ""
        with open(i_file_path, "r") as f:
            contents_str = f.read()

        self.setMinimumWidth(500)
        self.setMinimumHeight(700)

        self.setSizeGripEnabled(True)
        self.setWindowTitle("Markdown input")

        vbox_l1 = QtWidgets.QVBoxLayout(self)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.md_edit_qll = QtWidgets.QLabel("Markdown tools: ")
        hbox_l2.addWidget(self.md_edit_qll)

        self.h2_qpb = QtWidgets.QPushButton("h2")
        hbox_l2.addWidget(self.h2_qpb)
        self.h2_qpb.clicked.connect(self.on_h2_clicked)

        self.h3_qpb = QtWidgets.QPushButton("h3")
        hbox_l2.addWidget(self.h3_qpb)
        self.h3_qpb.clicked.connect(self.on_h3_clicked)

        self.h4_qpb = QtWidgets.QPushButton("h4")
        hbox_l2.addWidget(self.h4_qpb)
        self.h4_qpb.clicked.connect(self.on_h4_clicked)

        self.insert_template_qpb = QtWidgets.QPushButton("Insert Template")
        hbox_l2.addWidget(self.insert_template_qpb)
        self.insert_template_qpb.clicked.connect(self.on_insert_template_clicked)

        self.editor_qpte = QtWidgets.QPlainTextEdit()
        vbox_l1.addWidget(self.editor_qpte)
        self.editor_qpte.setPlainText(contents_str)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox_l1.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def on_insert_template_clicked(self):
        # template_file_relative_path_str = "contact_template.txt"
        template_file_path_str = kammanta.glob.get_appl_path("gtd", "contact_template.txt")
        template_str = ""
        with open(template_file_path_str, "r") as f:
            template_str = f.read()

        old_text_str = self.editor_qpte.toPlainText()
        new_text_str = old_text_str + "\n\n\n" + template_str

        self.editor_qpte.setPlainText(new_text_str)

    def on_h2_clicked(self):
        self._set_header("## ")

    def on_h3_clicked(self):
        self._set_header("### ")

    def on_h4_clicked(self):
        self._set_header("#### ")

    def _set_header(self, i_header_text: str):
        text_cursor=self.editor_qpte.textCursor()
        text_cursor.movePosition(QtGui.QTextCursor.StartOfBlock)  # -"block" means line!
        text_cursor.setKeepPositionOnInsert(True)

        text_cursor.insertText(i_header_text)

        text_cursor.setKeepPositionOnInsert(False)

        text_cursor.clearSelection()
        self.editor_qpte.setTextCursor(text_cursor)


    @staticmethod
    def open_dlg_and_get_text(i_file_path: str) -> (str, bool):
        file_and_dir_dlg = MarkdownInputDialog(i_file_path)
        dialog_result = file_and_dir_dlg.exec_()
        if dialog_result == QtWidgets.QDialog.Accepted:
            contents_str = file_and_dir_dlg.editor_qpte.toPlainText()
            return (contents_str, True)
        else:
            return ("", False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Existing file
    MarkdownInputDialog.open_dlg_and_get_text(
        "/home/sunyata/context_1.txt",
    )

    sys.exit()

