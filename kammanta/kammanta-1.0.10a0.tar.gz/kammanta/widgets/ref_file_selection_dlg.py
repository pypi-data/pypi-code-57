import typing
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
# import PIL.Image
# import wbd.wbd_global
import kammanta.glob

WIDTH_AND_HEIGHT_INT = 250


class RefFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        QtWidgets.QFileDialog.__init__(self, *args, **kwargs)

        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        self.setFixedSize(self.width() + WIDTH_AND_HEIGHT_INT, self.height())
        vbox_l2 = QtWidgets.QVBoxLayout()

        # noinspection PyUnresolvedReferences
        self.layout().addLayout(vbox_l2, 1, 3, 1, 1)

        self.preview_qsw = QtWidgets.QStackedWidget()
        vbox_l2.addWidget(self.preview_qsw)
        self.preview_qsw.setObjectName("preview_qsw")
        self.preview_qsw.setFixedWidth(WIDTH_AND_HEIGHT_INT)

        self.empty_preview_qll = QtWidgets.QLabel("no preview")
        self.preview_qsw.addWidget(self.empty_preview_qll)

        self.text_preview_qtb = QtWidgets.QTextBrowser()
        # self.preview_qll.setFixedSize(WIDTH_AND_HEIGHT_INT, WIDTH_AND_HEIGHT_INT)
        # self.preview_qll.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_qsw.addWidget(self.text_preview_qtb)

        self.preview_qsw.setCurrentWidget(self.empty_preview_qll)

        self.currentChanged.connect(self.on_current_changed)
        self.fileSelected.connect(self.on_file_selected)
        self.filesSelected.connect(self.on_files_selected)

        self._file_selected_str = None
        self._files_selected_str_list = []

    def on_current_changed(self, i_new_file_path: str):
        dir_or_file_type = kammanta.glob.get_type(i_new_file_path)
        if dir_or_file_type in (kammanta.glob.TypeEnum.note_file, kammanta.glob.TypeEnum.text_file):
            try:
                with open(i_new_file_path, "r") as file:
                    self.text_preview_qtb.setPlainText(file.read())
                    # self.preview_qll.setPlainText(file.read())
                    self.preview_qsw.setCurrentWidget(self.text_preview_qtb)
            except UnicodeDecodeError:
                pass
            ####self.left_qsw.setCurrentWidget(self.source_qpte)
        else:
            self.preview_qsw.setCurrentWidget(self.empty_preview_qll)
            #####self.left_qsw.setCurrentWidget(self.unknown_file_qll)

        """
        elif dir_or_file_type in (gtd.glob.TypeEnum.image_file,):
            pixmap = QtGui.QPixmap(i_new_file_path)
            pixmap = pixmap.scaled(
                340, 340,
                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            self.preview_qtb.setPixmap(pixmap)
            #####self.left_qsw.setCurrentWidget(self.source_image_qll)
        """

        """
        Image

        pixmap = QtGui.QPixmap(i_new_file_path)
        if pixmap.isNull():
            self.preview_qll.setText("Preview")
        else:
            pixmap = pixmap.scaled(
                WIDTH_AND_HEIGHT_INT,
                WIDTH_AND_HEIGHT_INT,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )

            image_pi: PIL.Image = PIL.Image.open(i_new_file_path)
            rotation_degrees_int = wbd.wbd_global.get_rotation_degrees(image_pi, True)
            # -rotation is done in the other direction than when using Pillow
            if rotation_degrees_int != 0:
                rotation_qtransform = QtGui.QTransform()
                rotation_qtransform.rotate(rotation_degrees_int)
                pixmap = pixmap.transformed(rotation_qtransform)

            self.preview_qll.setPixmap(pixmap)
        """

    def on_file_selected(self, i_file: str):
        self._file_selected_str = i_file

    def on_files_selected(self, i_file: str):
        self._files_selected_str_list = i_file

    def get_file_selected(self) -> str:
        return self._file_selected_str

    def get_files_selected(self) -> typing.List[str]:
        return self._files_selected_str_list

    @staticmethod
    def open_dlg_and_get_file_path(i_filename: str="") -> str:
        image_dlg = RefFileDialog()
        if i_filename:
            image_dlg.selectFile(i_filename)
        # filter="Images (*.png *.jpg)"
        image_dlg.exec_()
        image_path_str = image_dlg.get_file_selected()
        return image_path_str
