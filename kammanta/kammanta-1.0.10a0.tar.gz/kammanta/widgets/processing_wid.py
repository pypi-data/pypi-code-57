import logging
import os
import time
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import kammanta.model
import kammanta.widgets.checklist_cw
import kammanta.widgets.calendar_input_dlg
import kammanta.glob
import kammanta.gtd_info
import kammanta.widgets.ref_file_selection_dlg

TITLE_STR = "Processing"


class ProcessingWidgetInDock(QtWidgets.QWidget):
    closed_clicked_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout(self)
        self.setLayout(vbox_l1)
        self.setSizePolicy(
            self.sizePolicy().horizontalPolicy(),
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.source_path_str = ""

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.source_type_qbg = QtWidgets.QButtonGroup()

        self.file_source_qrb = QtWidgets.QRadioButton("File")
        self.source_type_qbg.addButton(self.file_source_qrb)
        hbox_l2.addWidget(self.file_source_qrb)
        self.file_source_qrb.clicked.connect(self.on_file_source_clicked)

        self.select_source_file_qpb = QtWidgets.QPushButton("Select")
        hbox_l2.addWidget(self.select_source_file_qpb)
        self.select_source_file_qpb.clicked.connect(self.on_select_source_file_clicked)

        self.other_source_qrb = QtWidgets.QRadioButton("Other")
        self.source_type_qbg.addButton(self.other_source_qrb)
        hbox_l2.addWidget(self.other_source_qrb)
        self.other_source_qrb.clicked.connect(self.on_other_source_clicked)

        hbox_l2.addStretch(1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.source_path_qll = QtWidgets.QLabel()
        # self.source_path_qll = QtWidgets.QLineEdit()  # QLabel()
        # self.source_path_qll.setDisabled(True)
        self.source_path_qll.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.source_path_qll.setWordWrap(True)
        hbox_l2.addWidget(self.source_path_qll, stretch=1)
        # hbox_l2.addStretch(1)

        self.file_actions_menu = QtWidgets.QMenu()

        self.open_file_action = QtWidgets.QAction("Open")
        self.open_file_action.triggered.connect(self.on_open_file_triggered)
        self.file_actions_menu.addAction(self.open_file_action)

        self.copy_path_file_action = QtWidgets.QAction("Copy path")
        self.copy_path_file_action.triggered.connect(self.on_copy_path_triggered)
        self.file_actions_menu.addAction(self.copy_path_file_action)

        self.actions_qpb = QtWidgets.QPushButton("...")
        self.actions_qpb.setFixedWidth(35)
        hbox_l2.addWidget(self.actions_qpb)
        self.actions_qpb.setMenu(self.file_actions_menu)

        self.source_qsw = QtWidgets.QStackedWidget()
        vbox_l1.addWidget(self.source_qsw, stretch=1)
        self.source_qpte = QtWidgets.QPlainTextEdit()
        self.source_qsw.addWidget(self.source_qpte)
        ###self.source_qpte.setFont(new_font)
        self.source_qpte.setReadOnly(True)
        self.source_image_qll = QtWidgets.QLabel()
        self.source_qsw.addWidget(self.source_image_qll)
        self.source_other_qll = QtWidgets.QLabel("Other source (ex paper), or simply manual input")
        self.source_qsw.addWidget(self.source_other_qll)
        # cannot_show_preview_qll

        # ..processing widgets

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.trash = DeleteCw()
        hbox_l2.addWidget(self.trash)

        self.do_widget = DoCw()
        hbox_l2.addWidget(self.do_widget)

        self.new_next_action = NewNAWidget()
        vbox_l1.addWidget(self.new_next_action)

        self.new_project = NewPrjWidget()
        vbox_l1.addWidget(self.new_project)

        self.delegate_widget = DelegateCw()
        vbox_l1.addWidget(self.delegate_widget)

        self.defer_widget = DeferCw()
        vbox_l1.addWidget(self.defer_widget)

        self.someday_maybe_widget = SomedayMaybeCw()
        vbox_l1.addWidget(self.someday_maybe_widget)

        self.incubate_widget = IncubateCw()
        vbox_l1.addWidget(self.incubate_widget)

        self.ref_dest_widget = RefDest()
        vbox_l1.addWidget(self.ref_dest_widget)
        self.ref_dest_widget.setSizePolicy(
            self.ref_dest_widget.sizePolicy().horizontalPolicy(),
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        # Controls

        controls_hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(controls_hbox_l2)
        controls_hbox_l2.addStretch(1)

        vbox_l1.addWidget(HLine())

        """
        self.auto_next_qcb = QtWidgets.QCheckBox("auto next")
        controls_hbox_l2.addWidget(self.auto_next_qcb)
        self.auto_next_qcb.setChecked(False)
        self.auto_next_qcb.setEnabled(False)

        self.delete_source_on_exit_qcb = QtWidgets.QCheckBox("del on exit")
        controls_hbox_l2.addWidget(self.delete_source_on_exit_qcb)
        self.delete_source_on_exit_qcb.setChecked(False)
        """

        controls_hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(controls_hbox_l2)
        controls_hbox_l2.addStretch(1)

        self.close_qpb = QtWidgets.QPushButton("Close")
        controls_hbox_l2.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_clicked)

        self.close_and_delete_qpb = QtWidgets.QPushButton("+del")
        controls_hbox_l2.addWidget(self.close_and_delete_qpb)
        self.close_and_delete_qpb.clicked.connect(self.on_close_and_delete_clicked)

        controls_hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(controls_hbox_l2)
        controls_hbox_l2.addStretch(1)

        self.next_qpb = QtWidgets.QPushButton("Next")
        controls_hbox_l2.addWidget(self.next_qpb)
        self.next_qpb.clicked.connect(self.on_next_clicked)

        self.next_and_delete_qpb = QtWidgets.QPushButton("+del")
        controls_hbox_l2.addWidget(self.next_and_delete_qpb)
        self.next_and_delete_qpb.clicked.connect(self.on_next_and_delete_clicked)

        self.update_gui()
        self.file_source_qrb.click()

    def on_open_file_triggered(self):
        kammanta.glob.launch_string(self.source_path_str)

    def on_copy_path_triggered(self):
        qt_clipboard = QtGui.QGuiApplication.clipboard()
        qt_clipboard.setText(self.source_path_str)

    def on_next_clicked(self):
        all_inbox_items = kammanta.model.inbox_dir.get_all_items(i_sort_by_name=False)
        if len(all_inbox_items) > 0:
            last_inbox_item = all_inbox_items[0]
            new_source_path_str = last_inbox_item.get_path()
            self.set_source_path(new_source_path_str)
        else:
            self.on_close_clicked()

    def on_next_and_delete_clicked(self):
        kammanta.glob.remove_fd(self.source_path_str)
        time.sleep(1)  # -TODO: timing issue here!
        self.on_next_clicked()

    def on_close_clicked(self):
        self.closed_clicked_signal.emit()

    def on_close_and_delete_clicked(self):
        kammanta.glob.remove_fd(self.source_path_str)
        self.on_close_clicked()

    def on_file_source_clicked(self):
        if self.source_path_str:
            self.update_gui()

    def on_other_source_clicked(self):
        self.update_gui()

    def on_select_source_file_clicked(self):
        reference_path_str = kammanta.glob.get_ref_path()
        new_source_path_str = kammanta.widgets.ref_file_selection_dlg.RefFileDialog.open_dlg_and_get_file_path()
        # (self.source_path_str, filter_str) = QtWidgets.QFileDialog.getOpenFileName(self, "caption", reference_path_str)

        if new_source_path_str:
            self.source_path_str = new_source_path_str
            self.file_source_qrb.click()

    def set_source_path(self, i_new_source_path: str):
        self.source_path_str = i_new_source_path
        self.update_gui()

    # overridden
    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        pass
        # self.update_gui()
        # -removed for now since this has been seen (only once) to cause an infinite loop

    def update_gui(self):
        self.source_path_qll.setText(self.source_path_str)

        # Checking the type of file that we have
        df_type = kammanta.glob.get_type(self.source_path_str)

        if df_type in (kammanta.glob.TypeEnum.note_file, kammanta.glob.TypeEnum.text_file):
            try:
                with open(self.source_path_str, "r") as file:
                    self.source_qpte.setPlainText(file.read())
            except UnicodeDecodeError:
                pass
            self.source_qsw.setCurrentWidget(self.source_qpte)
        elif df_type == kammanta.glob.TypeEnum.image_file:
            pixmap = QtGui.QPixmap(self.source_path_str)
            pixmap = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.source_image_qll.setPixmap(pixmap)
            self.source_qsw.setCurrentWidget(self.source_image_qll)
        else:
            self.source_qsw.setCurrentWidget(self.source_other_qll)

        self.incubate_widget.set_source_path(self.source_path_str)
        self.ref_dest_widget.set_source_path(self.source_path_str)


class DeleteCw(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        self.do_qll = QtWidgets.QLabel("Delete")
        vbox_l1.addWidget(self.do_qll)


class DoCw(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        self.do_qll = QtWidgets.QLabel("Do if less than x minutes")
        vbox_l1.addWidget(self.do_qll)


class NewNAWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.group_qcb = QtWidgets.QComboBox()
        hbox_l2.addWidget(self.group_qcb)
        self.group_qcb.setMaximumWidth(150)

        self.new_qle = QtWidgets.QLineEdit()
        hbox_l2.addWidget(self.new_qle, stretch=2)
        self.new_qle.setPlaceholderText("New Next Action")

        self.add_new_qpb = AddButton()
        hbox_l2.addWidget(self.add_new_qpb)
        self.add_new_qpb.clicked.connect(self.on_add_new_clicked)

        self.update_gui()

    def update_gui(self):
        context_objlist = kammanta.model.na_files.get_all_items(i_sort_by_name=True)
        context_strlist = [c.get_id() for c in context_objlist]
        self.group_qcb.addItems(context_strlist)

    def on_add_new_clicked(self):
        new_name_str = self.new_qle.text()
        self.new_qle.clear()
        group_name_str = self.group_qcb.currentText()
        destination_context_obj = kammanta.model.na_files.get_item(group_name_str)
        destination_context_obj.add_new_item(new_name_str)

        # Please note that since we have FileSystemWatcher for the NA (and ohter) files,
        # we don't need to emit/fire a signal here to update the whole GUI.
        # Please note that THIS APPLIES TO THE OTHER on_add_new_clicked FUNCTIONS AS WELL!


class AddButton(QtWidgets.QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("+")
        self.setFixedWidth(25)


class NewPrjWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.group_qcb = QtWidgets.QComboBox()
        hbox_l2.addWidget(self.group_qcb)
        self.group_qcb.setMaximumWidth(150)

        self.new_qle = QtWidgets.QLineEdit()
        hbox_l2.addWidget(self.new_qle, stretch=2)
        self.new_qle.setPlaceholderText("New Project")

        self.add_new_qpb = AddButton()
        hbox_l2.addWidget(self.add_new_qpb)
        self.add_new_qpb.clicked.connect(self.on_add_new_clicked)

        self.update_gui()

    def update_gui(self):
        group_objlist = kammanta.model.prj_fds.get_all_items(i_sort_by_name=True)
        group_strlist = [c.get_id() for c in group_objlist]
        self.group_qcb.addItems(group_strlist)

    def on_add_new_clicked(self):
        new_name_str = self.new_qle.text()
        self.new_qle.clear()
        group_name_str = self.group_qcb.currentText()
        destination_context_obj = kammanta.model.prj_fds.get_item(group_name_str)
        destination_context_obj.add_new_item(new_name_str)


class DelegateCw(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.open_email_qpb = QtWidgets.QPushButton("Delegate (open email)")
        hbox_l2.addWidget(self.open_email_qpb)
        self.open_email_qpb.clicked.connect(self.on_open_email_clicked)
        # self.open_email_qpb.setFont(gtd.glob.get_button_font(True))
        self.open_email_qpb.setStyleSheet(kammanta.glob.EXT_BTN_STYLE_SHEET_STR)

        self.new_waiting_for_qle = QtWidgets.QLineEdit()
        hbox_l2.addWidget(self.new_waiting_for_qle, stretch=2)
        self.new_waiting_for_qle.setPlaceholderText("Add to waiting-for")

        self.add_new_qpb = AddButton()
        hbox_l2.addWidget(self.add_new_qpb)
        self.add_new_qpb.clicked.connect(self.on_add_new_clicked)

    def on_add_new_clicked(self):
        new_name_str = self.new_waiting_for_qle.text()
        self.new_waiting_for_qle.clear()
        waiting_for_obj = kammanta.model.na_files.get_item(kammanta.glob.WAITING_FOR_STR)
        waiting_for_obj.add_new_item(new_name_str)

    def on_open_email_clicked(self):
        email_str = kammanta.glob.get_string_from_config(
            kammanta.glob.SETTINGS_SECTION_EXTERNAL_TOOLS_STR,
            kammanta.glob.SETTINGS_EMAIL_STR,
            "thunderbird"
        )
        kammanta.glob.launch_string(email_str)


class DeferCw(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.open_calendar_qpb = QtWidgets.QPushButton("Schedule (open Calendar)")
        hbox_l2.addWidget(self.open_calendar_qpb)
        self.open_calendar_qpb.clicked.connect(self.on_open_calendar_clicked)
        # self.open_calendar_qpb.setFont(gtd.glob.get_button_font(True))
        self.open_calendar_qpb.setStyleSheet(kammanta.glob.EXT_BTN_STYLE_SHEET_STR)

    def on_open_calendar_clicked(self):
        calendar_str = kammanta.glob.get_string_from_config(
            kammanta.glob.SETTINGS_SECTION_EXTERNAL_TOOLS_STR,
            kammanta.glob.SETTINGS_CALENDAR_STR,
            "https://calendar.google.com/calendar/r/week"
        )
        kammanta.glob.launch_string(calendar_str)


class SomedayMaybeCw(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        self.new_someday_maybe_qle = QtWidgets.QLineEdit()
        hbox_l2.addWidget(self.new_someday_maybe_qle, stretch=2)
        self.new_someday_maybe_qle.setPlaceholderText("Add to someday/maybe list")

        self.add_new_qpb = AddButton()
        hbox_l2.addWidget(self.add_new_qpb)
        self.add_new_qpb.clicked.connect(self.on_add_new_clicked)

        #### self.next_actions_widget.set_active_item(waiting_for_obj.get_id())
        # self.next_actions_widget.coll_selection_qcb.setCurrentText(gtd.model.WAITING_FOR_STR)

    def on_add_new_clicked(self):
        new_name_str = self.new_someday_maybe_qle.text()
        self.new_someday_maybe_qle.clear()
        someday_maybe_obj = kammanta.model.prj_fds.get_item(kammanta.glob.SOMEDAY_MAYBE_STR)
        someday_maybe_obj.add_new_item(new_name_str)


class IncubateCw(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.source_path_str = ""

        hbox_l1 = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_l1)

        self.title_qll = QtWidgets.QLabel("Incubate:")
        # for later descision
        hbox_l1.addWidget(self.title_qll)

        hbox_l1.addStretch(1)

        self.nr_of_days_qsb = QtWidgets.QSpinBox()
        hbox_l1.addWidget(self.nr_of_days_qsb)

        self.date_time_qdte = QtWidgets.QDateTimeEdit()
        hbox_l1.addWidget(self.date_time_qdte)
        self.date_time_qdte.setCalendarPopup(True)

        self.add_new_qpb = AddButton()
        hbox_l1.addWidget(self.add_new_qpb)
        self.add_new_qpb.clicked.connect(self.on_add_new_clicked)

        self.reset_datetime()

        # self.calendar_input_widget = gtd.widgets.calendar_input_dlg.CalendarCw(7)
        # vbox_l1.addWidget (self.calendar_input_widget)

    def set_source_path(self, i_source_path: str):
        self.source_path_str = i_source_path

    def on_add_new_clicked(self):
        ############ design: files and notes

        qt_date = self.date_time_qdte.date()
        qt_time = self.date_time_qdte.time()
        self.reset_datetime()
        qt_dt = QtCore.QDateTime(qt_date, qt_time)
        datetime_str = qt_dt.toString(kammanta.glob.QT_DATETIME_FORMAT_STR)

        dest_path_str = kammanta.glob.add_tickler_file(datetime_str, self.source_path_str, False)

        # Opening a text editor
        kammanta.glob.launch_string(dest_path_str)

    def reset_datetime(self):
        now_qdate = QtCore.QDateTime.currentDateTime()
        self.date_time_qdte.setDateTime(now_qdate)


class RefDest(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l4)

        """
        self.select_dest_qpb = QtWidgets.QPushButton("select dest (gtd)")
        hbox_l4.addWidget(self.select_dest_qpb)
        self.select_dest_qpb.clicked.connect(self.on_select_dest_clicked)
        """

        self.select_dest_gen_qpb = QtWidgets.QPushButton("Add to reference")
        # select dest (gen ref)
        hbox_l4.addWidget(self.select_dest_gen_qpb)
        self.select_dest_gen_qpb.clicked.connect(self.on_select_dest_clicked)

        # self.add_new_qpb = QtWidgets.QPushButton("Add")
        # hbox_l4.addWidget(self.add_new_qpb)

        # self.dest_text_qpte = QtWidgets.QPlainTextEdit()
        # vbox_l1.addWidget(self.dest_text_qpte, stretch=1)

        # hbox_l2.addWidget(self.dest_qpte)
        # self.dest_text_qpte.setFont(new_font)

    def set_source_path(self, i_source_path: str):
        self.source_path_str = i_source_path

    def on_select_dest_clicked(self):
        reference_path_str = kammanta.glob.get_ref_path()
        source_file_name_str = os.path.basename(self.source_path_str)
        refenence_path_with_file_name_str = os.path.join(reference_path_str, source_file_name_str)
        # (dest_path_str, filter_str) = QtWidgets.QFileDialog.getSaveFileName(self, "caption", refenence_path_with_file_name_str)
        dest_path_str = kammanta.widgets.ref_file_selection_dlg.RefFileDialog.open_dlg_and_get_file_path(source_file_name_str)

        # Add the predefined file name as the default
        logging.debug(dest_path_str)
        # logging.debug(result_bool)

        if dest_path_str:
            source_contents_str = ""
            if os.path.exists(dest_path_str):
                source_contents_str = "\n\n\n***\n\n\n"
            try:
                with open(self.source_path_str, "r") as file:
                    source_contents_str += file.read()
                # if not os.path.isfile(dest_path_str):
                with open(dest_path_str, "a+") as file:
                    file.write(source_contents_str)
            except:
                pass
                # binary file: copy but with a new name
                kammanta.glob.copy_fd(self.source_path_str, dest_path_str)
            # Opening a text editor
            kammanta.glob.launch_string(dest_path_str)

        """
        if result_bool:
            # self.right_qsw.setCurrentWidget(self.dest_text_qpte)
            self.dest_path_qll.setText(dest_path_str)
            if not os.path.isfile(dest_path_str):
                with open(dest_path_str, "x") as file:
                    pass
            with open(dest_path_str, "r") as file:
                self.dest_text_qpte.setPlainText(file.read())
        """


class HLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setLineWidth(1)


