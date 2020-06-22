import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import kammanta.model
import kammanta.glob
import kammanta.widgets.path_sel_dlg
import kammanta.do_timer


class FocusDlg(QtWidgets.QDialog):
    def __init__(self, i_focus_item):
        # -giving type hint for focus_item here?
        # Please note: LxQt shows the minimize button even though we have a dialog
        # Documentation: https://doc.qt.io/qt-5/qt.html#WindowType-enum
        # self.setWindowFlags(QtCore.Qt.Popup)
        # self.setWindowFlag(QtCore.Qt.Popup)

        super().__init__()
        # , *args, **kwargs

        logging.info("init for FocusDlg")

        self.focus_item = i_focus_item

        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        # self.setSizeGripEnabled(True)
        self.setWindowTitle("Focus")


        vbox_l1 = QtWidgets.QVBoxLayout(self)

        self.item_name_qll = QtWidgets.QLabel()
        vbox_l1.addWidget(self.item_name_qll, alignment=QtCore.Qt.AlignCenter, stretch=1)
        self.item_name_qll.setWordWrap(True)
        self.item_name_qll.setText(self.focus_item.get_core_name())
        name_font = QtGui.QFont()
        name_font.setPointSize(24)
        self.item_name_qll.setFont(name_font)

        # Support

        self.open_support_qpb = QtWidgets.QPushButton("Open support")
        vbox_l1.addWidget(self.open_support_qpb, alignment=QtCore.Qt.AlignCenter, stretch=1)
        self.open_support_qpb.clicked.connect(self.on_open_support_clicked)
        open_support_font = QtGui.QFont()
        open_support_font.setPointSize(18)
        self.open_support_qpb.setFont(open_support_font)

        # Timer
        # Idea: setting another icon in the systray during focus?
        # Also, instead of opening the application on left click (activated) we can open the dialog

        self.timer = kammanta.do_timer.DoTimer()
        self.timer.start()
        self.timer.update_signal.connect(self.update_gui)

        self.timer_qll = QtWidgets.QLabel()
        # self.timer.get_formatted_time()
        vbox_l1.addWidget(self.timer_qll, alignment=QtCore.Qt.AlignCenter, stretch=1)
        timer_font = QtGui.QFont()
        timer_font.setPointSize(64)
        self.timer_qll.setFont(timer_font)

        # hbox_l2 = QtWidgets.QHBoxLayout()
        # vbox_l1.addLayout(hbox_l2)

        self.done_qpb = QtWidgets.QPushButton("Done")
        vbox_l1.addWidget(self.done_qpb, alignment=QtCore.Qt.AlignCenter, stretch=1)
        self.done_qpb.clicked.connect(self.on_done_clicked)
        done_font = QtGui.QFont()
        done_font.setPointSize(24)
        self.done_qpb.setFont(done_font)

        self.update_gui()

    def on_done_clicked(self):
        self.focus_item.set_completed(True)
        self.close()

    def on_open_support_clicked(self):
        sp_str = self.focus_item.get_support_path()
        sp_str = sp_str.strip()
        # -removing space at beginning
        if sp_str:
            try:
                kammanta.glob.launch_string(sp_str)
            except Exception:
                QtWidgets.QMessageBox.warning(self, "title", "cannot open, if file it may not exist")

    def update_gui(self):
        sp_str = self.focus_item.get_support_path()
        if sp_str:
            self.open_support_qpb.setEnabled(True)
        else:
            self.open_support_qpb.setEnabled(False)

        elapsed_time_str = self.timer.get_formatted_time()
        self.timer_qll.setText(elapsed_time_str)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.timer.stop()
        super().closeEvent(a0)

    def restore_and_activate(self):
        self.show()
        self.raise_()
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()
        self.activateWindow()
        self.setFocus()

