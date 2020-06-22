import enum
import logging
import sys
import os.path
import os
import datetime
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import kammanta.model
import kammanta.glob
import kammanta.widgets.path_sel_dlg


class ToReferenceDlg(QtWidgets.QDialog):
    def __init__(self, i_source_path: str, i_delete_source_on_exit: bool=False):
        super().__init__()
        # , *args, **kwargs

        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        self.setSizeGripEnabled(True)
        self.setWindowTitle("")

        vbox_l1 = QtWidgets.QVBoxLayout(self)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)

        new_font = QtGui.QFont()
        new_font.setPointSize(14)

        left_vbox_l3 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(left_vbox_l3)

        hbox_l4 = QtWidgets.QHBoxLayout()
        left_vbox_l3.addLayout(hbox_l4)

        self.source_path_qll = QtWidgets.QLabel("-")
        hbox_l4.addWidget(self.source_path_qll, stretch=1)

        self.delete_source_on_exit_qcb = QtWidgets.QCheckBox("del on exit")
        hbox_l4.addWidget(self.delete_source_on_exit_qcb)
        self.delete_source_on_exit_qcb.setChecked(i_delete_source_on_exit)

        self.source_qpte = QtWidgets.QPlainTextEdit()
        left_vbox_l3.addWidget(self.source_qpte)
        self.source_qpte.setFont(new_font)
        with open(i_source_path, "r") as file:
            self.source_qpte.setPlainText(file.read())

        right_vbox_l3 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(right_vbox_l3)

        hbox_l4 = QtWidgets.QHBoxLayout()
        right_vbox_l3.addLayout(hbox_l4)

        self.dest_path_qll = QtWidgets.QLabel("-")
        hbox_l4.addWidget(self.dest_path_qll, stretch=1)

        self.select_dest_qpb = QtWidgets.QPushButton("select dest (gtd)")
        hbox_l4.addWidget(self.select_dest_qpb)
        self.select_dest_qpb.clicked.connect(self.on_select_dest_clicked)

        self.select_dest_gen_qpb = QtWidgets.QPushButton("select dest (gen ref)")
        hbox_l4.addWidget(self.select_dest_gen_qpb)

        self.right_qsw = QtWidgets.QStackedWidget()
        right_vbox_l3.addWidget(self.right_qsw)

        self.dest_qpte = QtWidgets.QPlainTextEdit()
        self.right_qsw.addWidget(self.dest_qpte)
        # hbox_l2.addWidget(self.dest_qpte)
        self.dest_qpte.setFont(new_font)

        self.empty_qll = QtWidgets.QLabel("Please select a destination above")
        self.right_qsw.addWidget(self.empty_qll)

        self.right_qsw.setCurrentWidget(self.empty_qll)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox_l1.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.showMaximized()

    def on_select_dest_clicked(self):
        # new file, or existing
        """
        (dest_str, result_enum) = gtd.widgets.path_selection_dlg.PathSelectionDialog.open_dlg_and_get_path(
            gtd.widgets.path_selection_dlg.PathSelectionEnum.file,
            "", ""
        )
        """
        main_dir_path_str = kammanta.glob.get_path()
        (dest_str, result_bool) = QtWidgets.QFileDialog.getSaveFileName(
                self, "caption", main_dir_path_str)
        logging.debug(dest_str)
        logging.debug(result_bool)
        # QtWidgets.QFileDialog.getOpenFileName()
        if result_bool:
            self.right_qsw.setCurrentWidget(self.dest_qpte)
            self.dest_path_qll.setText(dest_str)
            if not os.path.isfile(dest_str):
                with open(dest_str, "x") as file:
                    pass
            with open(dest_str, "r") as file:
                self.dest_qpte.setPlainText(file.read())

    @staticmethod
    def show_ref_dlg(i_source_path: str, i_delete_source_on_exit: bool=False) -> None:
        ref_dlg = ToReferenceDlg(i_source_path)
        dialog_result = ref_dlg.exec_()
        if dialog_result == QtWidgets.QDialog.Accepted:
            # selected_qdate = cal_dlg.calendar_cw.calendar_widget.selectedDate()
            # date_str = selected_qdate.toString(gtd.model.QT_DATETIME_FORMAT_STR)
            dest_str = ref_dlg.dest_path_qll.text()
            contents_str = ref_dlg.dest_qpte.toPlainText()
            with open(dest_str, "w") as file:
                file.write(contents_str)
            if ref_dlg.delete_source_on_exit_qcb.isChecked():
                kammanta.glob.remove_fd(i_source_path)

        # return ("", False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    ToReferenceDlg.show_ref_dlg("/home/sunyata/Downloads/for-extracting.txt")

    sys.exit()

