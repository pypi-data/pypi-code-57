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


class PathSelectionEnum(enum.Enum):
    cancelled = enum.auto()
    dir = enum.auto()
    file = enum.auto()
    cmd_or_weblink = enum.auto()


class HLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setLineWidth(2)
        # self.setStyleSheet("color: #000000")


# Research: https://stackoverflow.com/questions/11028767/asking-for-folder-creation-in-qt


class PathSelDlg(QtWidgets.QFileDialog):
    def __init__(self, i_path_sel_enum: PathSelectionEnum, i_start_dir_path: str, i_file_or_dir_name: str):
        QtWidgets.QFileDialog.__init__(self)
        # , *args, **kwargs

        logging.debug("type(self.layout()) = " + str(type(self.layout())))
        # -expected result: QGridLayout
        self.result_enum = PathSelectionEnum.cancelled
        self.accepted.connect(self.on_dialog_accepted)
        self.setWindowTitle("Dir or file selection")
        ######self.setFixedSize(self.width() + WIDTH_AND_HEIGHT_INT, self.height())

        self.setFileMode(QtWidgets.QFileDialog.AnyFile)
        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        self.setOption(QtWidgets.QFileDialog.DontConfirmOverwrite, True)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        # self.setLabelText(QtWidgets.QFileDialog.Accept, "Select")

        # Sidebar shortcuts
        # sidebar_qurllist = self.sidebarUrls()
        sidebar_qurllist = []
        # sidebar_qurllist.append(QtCore.QUrl.fromLocalFile("/home/sunyata/PycharmProjects"))
        sidebar_qurllist.append(QtCore.QUrl.fromLocalFile(kammanta.glob.get_path()))
        sidebar_qurllist.append(QtCore.QUrl.fromLocalFile(kammanta.glob.get_ref_path()))
        # -when testing "path" and "ref_path" are the same so the second one is not added
        sidebar_qurllist.append(QtCore.QUrl.fromLocalFile(QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.HomeLocation)[0]))
        sidebar_qurllist.append(QtCore.QUrl.fromLocalFile(QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DocumentsLocation)[0]))
        self.setSidebarUrls(sidebar_qurllist)

        vbox_l0 = QtWidgets.QVBoxLayout()
        # OK: self.layout().addLayout(vbox_l2, 1, 3, 1, 1)
        self.layout().addLayout(vbox_l0, 10, 1, 1, 1)
        # OK: self.layout().addLayout(hbox_l1, 10, 1, 1, 2)

        hbox_l1 = QtWidgets.QHBoxLayout()
        vbox_l0.addLayout(hbox_l1)

        self.dir_or_file_qbg = QtWidgets.QButtonGroup()
        self.dir_or_file_qbg.buttonClicked.connect(self.on_dir_or_file_radio_clicked)
        new_font = QtGui.QFont()
        new_font.setPointSize(16)
        # new_font.setBold(True)
        self.file_qrb = QtWidgets.QRadioButton("File")
        self.dir_or_file_qbg.addButton(self.file_qrb)
        hbox_l1.addWidget(self.file_qrb)
        self.file_qrb.setFont(new_font)
        self.dir_qrb = QtWidgets.QRadioButton("Directory")
        self.dir_or_file_qbg.addButton(self.dir_qrb)
        hbox_l1.addWidget(self.dir_qrb)
        self.dir_qrb.setFont(new_font)

        vbox_l0.addWidget(HLine())

        hbox_l1 = QtWidgets.QHBoxLayout()
        vbox_l0.addLayout(hbox_l1)

        self.cmd_or_weblink_qrb = QtWidgets.QRadioButton("Command or web link")
        self.dir_or_file_qbg.addButton(self.cmd_or_weblink_qrb)
        hbox_l1.addWidget(self.cmd_or_weblink_qrb)
        self.cmd_or_weblink_qrb.setFont(new_font)

        self.cmd_or_weblink_qle = QtWidgets.QLineEdit()
        hbox_l1.addWidget(self.cmd_or_weblink_qle)
        self.cmd_or_weblink_qle.textChanged.connect(self.on_cmd_or_weblink_text_changed)

        """
        self.cmd_or_weblink_qpb = QtWidgets.QPushButton("Accept")
        hbox_l1.addWidget(self.cmd_or_weblink_qpb)
        self.cmd_or_weblink_qpb.clicked.connect(self.on_cmd_or_weblink_clicked)
        
        def on_cmd_or_weblink_clicked(self):
            self.accept()
        """

        # self.currentChanged.connect(self.on_current_changed)
        self.fileSelected.connect(self.on_file_or_dir_selected)

        # Setup depending on the in vars
        self.setDirectory(i_start_dir_path)
        # self.setLabelText(QtWidgets.QFileDialog.FileName, "test")

        self._file_selected_str = None

        self.show()

        if i_path_sel_enum == PathSelectionEnum.dir:
            self.selectFile(i_file_or_dir_name)
            self.dir_qrb.click()
        elif i_path_sel_enum == PathSelectionEnum.file:
            self.selectFile(i_file_or_dir_name)
            self.file_qrb.click()
        elif i_path_sel_enum == PathSelectionEnum.cmd_or_weblink:
            # self.selectFile(i_file_or_dir_name)
            self.cmd_or_weblink_qle.setText(i_file_or_dir_name)
            self.cmd_or_weblink_qrb.click()
            self.cmd_or_weblink_qle.setFocus()
            # -important that this is done after self.show(), otherwise the focus will shift to the file name field

        # self.on_dir_or_file_radio_clicked(-1)

    def on_cmd_or_weblink_text_changed(self, i_new_text: str):
        if not self.cmd_or_weblink_qrb.isChecked():
            self.cmd_or_weblink_qrb.click()

    def on_dir_or_file_radio_clicked(self, i_btn_id: int):
        #self.setFilter(QtCore.QDir.AllEntries)
        self.setNameFilter("All files (*)")
        new_font = self.file_qrb.font()
        new_font.setBold(False)
        if self.dir_qrb.isChecked():
            self.setFileMode(QtWidgets.QFileDialog.Directory)
            self.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
            self.file_qrb.setFont(new_font)
            new_font.setBold(True)
            self.dir_qrb.setFont(new_font)
        elif self.file_qrb.isChecked():
            self.setFileMode(QtWidgets.QFileDialog.AnyFile)
            self.setOption(QtWidgets.QFileDialog.ShowDirsOnly, False)
            self.dir_qrb.setFont(new_font)
            new_font.setBold(True)
            self.file_qrb.setFont(new_font)
        elif self.cmd_or_weblink_qrb.isChecked():
            self.cmd_or_weblink_qle.setFocus()
            # -doesn't work at startup, unknown why

    def on_dialog_accepted(self):
        self.result_enum = PathSelectionEnum.cancelled
        if self.dir_qrb.isChecked():
            self.result_enum = PathSelectionEnum.dir
        elif self.file_qrb.isChecked():
            self.result_enum = PathSelectionEnum.file
        elif self.cmd_or_weblink_qrb.isChecked():
            self.result_enum = PathSelectionEnum.cmd_or_weblink
        self.close()

    """
    def on_current_changed(self, i_new_file_path: str):
        pixmap = QtGui.QPixmap(i_new_file_path)
        if pixmap.isNull():
            self.preview_qll.setText("Preview")
        else:
            pass
    """

    def on_file_or_dir_selected(self, i_file: str):
        self._file_selected_str = i_file
        logging.debug("File or dir selected: " + i_file)

    def get_file_or_dir_selected(self) -> str:
        if self.cmd_or_weblink_qrb.isChecked():
            return self.cmd_or_weblink_qle.text()
        else:
            return self._file_selected_str

    @staticmethod
    def open_dlg_and_get_path(
        i_path_sel_enum: PathSelectionEnum,
        i_dir_path: str,
        i_dir_or_file_name: str,
        i_create_file_if_nonexistant: bool=True
    ) -> (str, PathSelectionEnum):
        file_and_dir_dlg = PathSelDlg(i_path_sel_enum, i_dir_path, i_dir_or_file_name)
        file_and_dir_dlg.exec_()
        ret_path_str = ""
        ret_path_str = file_and_dir_dlg.get_file_or_dir_selected()
        if file_and_dir_dlg.result_enum == PathSelectionEnum.dir:
            # if os.path.isdir(ret_path_str):
            return (ret_path_str, PathSelectionEnum.dir)
        elif file_and_dir_dlg.result_enum == PathSelectionEnum.file:
            # if os.path.isfile(ret_path_str):
            if i_create_file_if_nonexistant and not os.path.exists(ret_path_str):
                kammanta.glob.create_and_get_path(ret_path_str)
            return (ret_path_str, PathSelectionEnum.file)
        elif file_and_dir_dlg.result_enum == PathSelectionEnum.cmd_or_weblink:
            return (ret_path_str, PathSelectionEnum.cmd_or_weblink)
        else:
            return (ret_path_str, PathSelectionEnum.cancelled)


def run_example(i_enum: PathSelectionEnum):
    # Existing file
    (path_str, result_enum) = PathSelDlg.open_dlg_and_get_path(
        i_enum,
        "/home/sunyata/PycharmProjects/kammanta/example",
        "default_new_file_name"
    )
    print("result_enum = " + str(result_enum))
    if path_str:
        print("path_str = " + path_str)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    run_example(PathSelectionEnum.file)
    run_example(PathSelectionEnum.dir)
    sys.exit()


"""
* Testing the path selection:
  * Selecting a directory
  * Selection a file
  * txt file
  * .desktop file
  * other file
  * New or existing


"""
