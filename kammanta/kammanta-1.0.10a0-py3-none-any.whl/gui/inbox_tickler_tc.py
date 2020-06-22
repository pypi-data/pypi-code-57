import logging
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
# Removed: from PyQt5 import QtWebEngineWidgets
# -example: https://github.com/smoqadam/PyFladesk/blob/master/pyfladesk/__init__.py
import kammanta.model
import kammanta.glob
import kammanta.gtd_info
import kammanta.widgets.file_list_cw
import kammanta.widgets.calendar_input_dlg
import kammanta.widgets.input_cw

NOTE_BTN_ID_INT = 1
FILE_BTN_ID_INT = 2
TITLE_STR = "Inbox and Tickler"
INBOX_TITLE_STR = "Inbox"


class InboxTicklerMain(QtWidgets.QWidget):
    def __init__(self, i_parent):
        super().__init__(i_parent)

        grid_l2 = QtWidgets.QGridLayout()
        self.setLayout(grid_l2)

        self.inbox_cw = kammanta.widgets.file_list_cw.FileListCw(kammanta.model.inbox_dir, False)
        grid_l2.addWidget(self.inbox_cw, 0, 0)
        # , stretch=1
        self.inbox_cw.setWhatsThis(kammanta.gtd_info.INBOX_STR)

        self.tickler_cw = kammanta.widgets.file_list_cw.FileListCw(kammanta.model.tickler_files, False)
        # TicklerCw()
        grid_l2.addWidget(self.tickler_cw, 0, 1)
        self.tickler_cw.setWhatsThis(kammanta.gtd_info.TICKLER_STR)

        self.input_widget = kammanta.widgets.input_cw.InputCw()
        grid_l2.addWidget(self.input_widget, 1, 0)

        self.calendar_widget = kammanta.widgets.calendar_input_dlg.CalendarCw(7)
        grid_l2.addWidget(self.calendar_widget, 1, 1)

        self.add_new_inbox_item_qpb = QtWidgets.QPushButton("add new inbox item (note/file)")
        grid_l2.addWidget(self.add_new_inbox_item_qpb, 2, 0)
        self.add_new_inbox_item_qpb.clicked.connect(self.on_add_new_inbox_item_clicked)

        self.add_new_tickler_item_qpb = QtWidgets.QPushButton("add new tickler item (note/file)")
        grid_l2.addWidget(self.add_new_tickler_item_qpb, 2, 1)
        self.add_new_tickler_item_qpb.clicked.connect(self.on_add_new_tickler_item_clicked)

        inbox_dir_path_str = kammanta.model.inbox_dir.get_path()
        kammanta.glob.FswSingleton.get().addPath(inbox_dir_path_str)
        tickler_dir_path_str = kammanta.model.tickler_files.get_path()
        kammanta.glob.FswSingleton.get().addPath(tickler_dir_path_str)

    # overridden
    def keyPressEvent(self, i_qkeyevent):
        # -TODO: unclear how to distinguish between adding a tickler item and an inbox item
        super().keyPressEvent(i_qkeyevent)
        """
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            if i_qkeyevent.key() == QtCore.Qt.Key_Enter or i_qkeyevent.key() == QtCore.Qt.Key_Return:
                logging.debug("Ctrl + Enter/Return")
                self.add_new_qpb.click()
                return
        """

    def on_add_new_inbox_item_clicked(self):
        if self.input_widget.choice_qbg.checkedId() == FILE_BTN_ID_INT:
            # file_name_str = self.input_widget.file_name_qle.text()
            self.input_widget.file_name_qll.clear()
            # gtd.model.inbox_dir.
            source_path_str = self.input_widget.source_path_str
            dest_dir_path_str = kammanta.glob.get_path(kammanta.glob.INBOX_DIR_STR)
            if self.input_widget.move_qrb.isChecked():
                kammanta.glob.move_fd(source_path_str, dest_dir_path_str)
            elif self.input_widget.copy_qrb.isChecked():
                kammanta.glob.copy_fd(source_path_str, dest_dir_path_str)

        elif self.input_widget.choice_qbg.checkedId() == NOTE_BTN_ID_INT:
            self.input_widget.file_name_qll.clear()

            contents_str = self.input_widget.tickler_note_qte.toPlainText()
            self.input_widget.tickler_note_qte.clear()

            kammanta.model.inbox_dir.add_new_note(contents_str)
        self.update_gui()

    def on_add_new_tickler_item_clicked(self):
        if self.input_widget.choice_qbg.checkedId() == FILE_BTN_ID_INT:
            # file_name_str = self.input_widget.file_name_qll.text()
            # self.input_widget.file_name_qll.clear()
            # source_dir_str = os.path.dirname(source_path_str)
            # source_file_name_str = os.path.basename(source_path_str)
            source_path_str = self.input_widget.source_path_str
            datetime_str = self.calendar_widget.get_datetime_string()
            kammanta.glob.add_tickler_file(datetime_str, source_path_str, self.input_widget.move_qrb.isChecked())

        elif self.input_widget.choice_qbg.checkedId() == NOTE_BTN_ID_INT:
            # file_name_str = self.input_widget.file_name_qll.text()
            # gtd.model.inbox_dir.add_new_item(file_name_str)
            # item_obj = gtd.model.inbox_dir.get_item(file_name_str)
            contents_str = self.input_widget.tickler_note_qte.toPlainText()
            self.input_widget.tickler_note_qte.clear()
            datetime_str = self.calendar_widget.get_datetime_string()
            kammanta.glob.add_tickler_note(datetime_str, contents_str)
        self.calendar_widget.reset_datetime()
        self.update_gui()

    def update_gui(self):
        self.inbox_cw.update_gui()
        self.tickler_cw.update_gui()


class InboxDock(QtWidgets.QWidget):
    row_changed_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        self.inbox_list = kammanta.widgets.file_list_cw.FileListCw(kammanta.model.inbox_dir, i_mini_layout=True)
        vbox_l2.addWidget(self.inbox_list, stretch=2)
        self.inbox_list.row_selected_signal.connect(self.on_row_selected_triggered)

        vbox_l2.addWidget(QtWidgets.QLabel("New note"))

        self.input_area_qpte = QtWidgets.QPlainTextEdit()
        vbox_l2.addWidget(self.input_area_qpte, stretch=1)
        self.input_area_qpte.setMinimumHeight(64)
        self.input_area_qpte.setMaximumHeight(300)

        self.add_new_qpb = QtWidgets.QPushButton("Add new")
        vbox_l2.addWidget(self.add_new_qpb)
        self.add_new_qpb.clicked.connect(self.on_add_new_clicked)

    # overridden
    def keyPressEvent(self, i_qkeyevent):
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            if i_qkeyevent.key() == QtCore.Qt.Key_Enter or i_qkeyevent.key() == QtCore.Qt.Key_Return:
                logging.debug("Ctrl + Enter/Return")
                self.add_new_qpb.click()
                return
        super().keyPressEvent(i_qkeyevent)

    def on_row_selected_triggered(self, i_id: str):
        self.row_changed_signal.emit(i_id)

    def on_add_new_clicked(self):
        contents_str = self.input_area_qpte.toPlainText()
        self.input_area_qpte.clear()

        kammanta.model.inbox_dir.add_new_note(contents_str)

        self.update_gui()

    def update_gui(self):
        self.inbox_list.update_gui()

