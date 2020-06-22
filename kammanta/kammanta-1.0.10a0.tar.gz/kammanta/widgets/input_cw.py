import logging
import datetime
import functools
import time
import subprocess
import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
#### from PyQt5 import QtWebEngineWidgets
# example: https://github.com/smoqadam/PyFladesk/blob/master/pyfladesk/__init__.py
import kammanta.model
import kammanta.glob
import kammanta.gtd_info
import kammanta.widgets.file_list_cw
import kammanta.widgets.calendar_input_dlg

NOTE_BTN_ID_INT = 1
FILE_BTN_ID_INT = 2
TITLE_STR = "Inbox and Tickler"
INBOX_TITLE_STR = "Inbox"


class InputCw(QtWidgets.QWidget):
    # add_note_signal = QtCore.pyqtSignal(str)
    # add_file_signal = QtCore.pyqtSignal(str)
    #add_tickler_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.source_path_str = ""

        self.setFixedHeight(340)
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        # File name (shared)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        hbox_l3.addWidget(QtWidgets.QLabel("File name: "))
        self.file_name_qll = QtWidgets.QLabel()
        hbox_l3.addWidget(self.file_name_qll)
        # self.file_name_qll.setReadOnly(True)

        # Stacked widget and toggle buttons

        self.choice_qbg = QtWidgets.QButtonGroup()

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        self.note_qpb = QtWidgets.QPushButton("Note")
        hbox_l3.addWidget(self.note_qpb)
        self.choice_qbg.addButton(self.note_qpb, NOTE_BTN_ID_INT)
        self.note_qpb.setCheckable(True)
        # self.note

        self.file_qpb = QtWidgets.QPushButton("File")
        hbox_l3.addWidget(self.file_qpb)
        self.choice_qbg.addButton(self.file_qpb, FILE_BTN_ID_INT)
        self.file_qpb.setCheckable(True)

        self.choice_qbg.buttonClicked.connect(self.on_choice_btn_clicked)

        self.note_or_file_qsw = QtWidgets.QStackedWidget()
        vbox_l2.addWidget(self.note_or_file_qsw)

        # Note

        self.note_qw6 = QtWidgets.QWidget()
        self.note_or_file_qsw.addWidget(self.note_qw6)

        vbox_l7 = QtWidgets.QHBoxLayout()
        self.note_qw6.setLayout(vbox_l7)

        self.tickler_note_qte = QtWidgets.QTextEdit()
        vbox_l7.addWidget(self.tickler_note_qte, stretch=1)

        # File

        self.file_qw6 = QtWidgets.QWidget()
        self.note_or_file_qsw.addWidget(self.file_qw6)

        vbox_l7 = QtWidgets.QHBoxLayout()
        self.file_qw6.setLayout(vbox_l7)

        self.select_file_qpb = QtWidgets.QPushButton("select file")
        vbox_l7.addWidget(self.select_file_qpb)
        self.select_file_qpb.clicked.connect(self.on_select_file_clicked)

        self.copy_move_qbg = QtWidgets.QButtonGroup()
        self.copy_qrb = QtWidgets.QRadioButton("Copy")
        vbox_l7.addWidget(self.copy_qrb)
        self.copy_move_qbg.addButton(self.copy_qrb)

        self.move_qrb = QtWidgets.QRadioButton("Move")
        vbox_l7.addWidget(self.move_qrb)
        self.copy_move_qbg.addButton(self.move_qrb)

        # ------

        self.copy_qrb.click()
        self.note_qpb.click()
        self.update_gui()

    def on_choice_btn_clicked(self, i_button: QtWidgets.QPushButton):
        self.update_gui()

        if self.file_qpb.isChecked():
            self.select_file_qpb.click()

    def on_select_file_clicked(self):
        # inbox_dir
        file_path_str, result_bool = QtWidgets.QFileDialog.getOpenFileName(
            self, "Please select a file for the tickler",
            kammanta.glob.get_path(kammanta.glob.INBOX_DIR_STR)
        )
        if result_bool:
            logging.debug(f"{file_path_str}")
            self.source_path_str = file_path_str
            file_name_str = os.path.basename(file_path_str)
            self.file_name_qll.setText(file_name_str)
        else:
            pass

    def update_gui(self):
        if self.choice_qbg.checkedId() == NOTE_BTN_ID_INT:
            self.note_or_file_qsw.setCurrentWidget(self.note_qw6)
            # new_note_name_str = gtd.gtd_global.get_new_note_name()
            # self.file_name_qle.setText(new_note_name_str)
            self.file_name_qll.setText("*new note (with date)*")
        elif self.choice_qbg.checkedId() == FILE_BTN_ID_INT:
            self.note_or_file_qsw.setCurrentWidget(self.file_qw6)

