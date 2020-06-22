import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import kammanta.model
import kammanta.glob
import kammanta.gtd_info
import kammanta.widgets.md_input_dlg

TITLE_STR = "Focus/Direction"


class FocusDirection(QtWidgets.QWidget):
    def __init__(self, i_parent):
        super().__init__(i_parent)

        grid_l2 = QtWidgets.QGridLayout()
        self.setLayout(grid_l2)
        self.aoi_cw4 = FDArea(kammanta.model.aoi_obj)
        grid_l2.addWidget(self.aoi_cw4, 0, 0)
        self.aoi_cw4.setWhatsThis(kammanta.gtd_info.AOI_STR)
        """
        gtd.gtd_global.clear_fsw()
        aoi_path_str = gtd.model.aoi_obj.get_path()
        gtd.gtd_global.get_filesyswatcher().addPath(aoi_path_str)
        gtd.gtd_global.get_filesyswatcher().fileChanged.connect(self.on_file_changed)

        self.qfsw = QtCore.QFileSystemWatcher()
        aoi_path_str = gtd.model.aoi_obj.get_path()
        self.qfsw.addPath(aoi_path_str)
        self.qfsw.fileChanged.connect(self.on_file_changed)
        """
        self.goals_cw4 = FDArea(kammanta.model.go_obj)
        grid_l2.addWidget(self.goals_cw4, 0, 1)
        self.goals_cw4.setWhatsThis(kammanta.gtd_info.GOALS_STR)
        self.visions_cw4 = FDArea(kammanta.model.vision_obj)
        grid_l2.addWidget(self.visions_cw4, 1, 0)
        self.visions_cw4.setWhatsThis(kammanta.gtd_info.VISION_STR)
        self.purpose_and_principles_cw4 = FDArea(kammanta.model.pp_obj)
        grid_l2.addWidget(self.purpose_and_principles_cw4, 1, 1)
        self.purpose_and_principles_cw4.setWhatsThis(kammanta.gtd_info.PURPOSE_AND_PRINCIPLES_STR)

        self.update_gui()

    # overridden
    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.update_gui()

    def update_gui(self):
        self.aoi_cw4.update_gui()
        self.goals_cw4.update_gui()
        self.visions_cw4.update_gui()
        self.purpose_and_principles_cw4.update_gui()


class FDArea(QtWidgets.QWidget):
    text_edited_signal = QtCore.pyqtSignal()

    def __init__(self, i_ref_df_obj: kammanta.model.File, i_minimal_layout: bool=False):
        super().__init__()

        self.setContentsMargins(0, 0, 0, 0)

        self.ref_df_obj = i_ref_df_obj

        vbox_l4 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l4)

        hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_l5)

        if not i_minimal_layout:
            title_str = self.ref_df_obj.get_main_title()
            self.title_qll = QtWidgets.QLabel(title_str)
            hbox_l5.addWidget(self.title_qll)
            new_font = QtGui.QFont()
            new_font.setPointSize(13)
            self.title_qll.setFont(new_font)

        hbox_l5.addStretch(1)

        if not i_minimal_layout:
            self.edit_qpb = QtWidgets.QPushButton("Edit")
            hbox_l5.addWidget(self.edit_qpb)
            self.edit_qpb.setSizePolicy(
                QtWidgets.QSizePolicy.Maximum,
                self.edit_qpb.sizePolicy().verticalPolicy()
            )
            self.edit_qpb.clicked.connect(self.on_edit_clicked)

        self.text_qtb = QtWidgets.QTextBrowser()
        vbox_l4.addWidget(self.text_qtb)
        self.text_qtb.setReadOnly(True)
        if not i_minimal_layout:
            self.text_qtb.zoomIn(2)
        else:
            self.text_qtb.zoomIn(1)
        self.text_qtb.setOpenLinks(False)
        # self.text_qte.setOpenExternalLinks(True)
        self.text_qtb.anchorClicked.connect(self.on_text_anchor_clicked)

        path_str = self.ref_df_obj.get_path()
        kammanta.glob.FswSingleton.get().addPath(path_str)

        self.update_gui()

    def on_text_anchor_clicked(self, i_qurl: QtCore.QUrl):
        text_str = i_qurl.toString()
        # utf = text_str.en
        # text_str = i_qurl.toLocalFile()
        kammanta.glob.launch_string(text_str)

    def on_edit_clicked(self):
        (new_text_str, okay_bool) = kammanta.widgets.md_input_dlg.MarkdownInputDialog.open_dlg_and_get_text(
                self.ref_df_obj.get_path())
        if okay_bool:
            with open(self.ref_df_obj.get_path(), "w") as file:
                file.write(new_text_str)
            self.text_edited_signal.emit()
            self.ref_df_obj.set_text_contents(new_text_str)
        self.update_gui()

    def update_gui(self):
        """
        file_contents_str = self.ref_df_obj.get_text_contents()
        qt_document = QtGui.QTextDocument()
        qt_document.markd

        """
        file_contents_str = self.ref_df_obj.get_text_contents()
        try:
            self.text_qtb.setMarkdown(file_contents_str)
        except AttributeError:
            self.text_qtb.setText(file_contents_str)


class FnDDockContainer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        fnd_dock_vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(fnd_dock_vbox_l2)

        dock_hbox_l3 = QtWidgets.QHBoxLayout()
        fnd_dock_vbox_l2.addLayout(dock_hbox_l3)
        fnd_dock_vbox_l2.setAlignment(QtCore.Qt.AlignTop)

        self.fnd_selection_qbg = QtWidgets.QButtonGroup()
        self.fnd_selection_qbg.setExclusive(False)
        self.fnd_selection_qbg.buttonClicked.connect(self.on_fnd_btn_clicked)

        self.fnd_aoi_qpb = QtWidgets.QPushButton("AoI")
        self.fnd_aoi_qpb.setToolTip("Areas of Interest and Accountability")
        self.fnd_aoi_qpb.setCheckable(True)
        self.fnd_selection_qbg.addButton(self.fnd_aoi_qpb)
        dock_hbox_l3.addWidget(self.fnd_aoi_qpb)

        self.fnd_goals_qpb = QtWidgets.QPushButton("Goals")
        self.fnd_goals_qpb.setToolTip("Goals and Objectives")
        self.fnd_goals_qpb.setCheckable(True)
        self.fnd_selection_qbg.addButton(self.fnd_goals_qpb)
        dock_hbox_l3.addWidget(self.fnd_goals_qpb)

        self.fnd_vision_qpb = QtWidgets.QPushButton("Vision")
        self.fnd_vision_qpb.setToolTip("Vision")
        self.fnd_vision_qpb.setCheckable(True)
        self.fnd_selection_qbg.addButton(self.fnd_vision_qpb)
        dock_hbox_l3.addWidget(self.fnd_vision_qpb)

        self.fnd_pp_qpb = QtWidgets.QPushButton("Purpose")
        self.fnd_pp_qpb.setToolTip("Principles and Purpose")
        self.fnd_pp_qpb.setCheckable(True)
        self.fnd_selection_qbg.addButton(self.fnd_pp_qpb)
        dock_hbox_l3.addWidget(self.fnd_pp_qpb)

        self.aoi_qtb = QtWidgets.QTextBrowser()
        fnd_dock_vbox_l2.addWidget(self.aoi_qtb)
        self.aoi_qtb.setReadOnly(True)
        self.aoi_qtb.setOpenLinks(False)
        self.aoi_qtb.anchorClicked.connect(self.on_text_anchor_clicked)

        self.goals_qtb = QtWidgets.QTextBrowser()
        fnd_dock_vbox_l2.addWidget(self.goals_qtb)
        self.goals_qtb.setReadOnly(True)
        self.goals_qtb.anchorClicked.connect(self.on_text_anchor_clicked)

        self.vision_qtb = QtWidgets.QTextBrowser()
        fnd_dock_vbox_l2.addWidget(self.vision_qtb)
        self.vision_qtb.setReadOnly(True)
        self.vision_qtb.anchorClicked.connect(self.on_text_anchor_clicked)

        self.pp_qtb = QtWidgets.QTextBrowser()
        fnd_dock_vbox_l2.addWidget(self.pp_qtb)
        self.pp_qtb.setReadOnly(True)
        self.pp_qtb.anchorClicked.connect(self.on_text_anchor_clicked)

        self.fnd_aoi_qpb.click()
        self.fnd_pp_qpb.click()

    def on_text_anchor_clicked(self, i_qurl: QtCore.QUrl):
        # https://doc.qt.io/qt-5/qtextbrowser.html#anchorClicked

        # BUG: the problem here is *double* encoding, which for /with-utf8/åäö gives /with-utf8/Ã¥Ã¤Ã¶
        # This has not been a problem previously so may be a temporary bug in Qt. Right now i will just
        # wait a while and hope that this is resolved. If not i can file a qt bug report
        # Please note that using the options for decoding/encoding will not work because this is a different type
        # of coding (the html coding is using the percent sign). What would be possible if i can set the parsing mode
        # https://doc.qt.io/qt-5/qurl.html#ParsingMode-enum but i have not found a way to do that for a QUrl that is
        # already existing

        text_displaystring_str = i_qurl.path()
        # .toDisplayString()
        logging.debug(text_displaystring_str)

        # i_qurl.setScheme("file")
        text_tostring_str = i_qurl.toString()
        logging.debug(text_tostring_str)

        # text_tostring_str = i_qurl.toString(options=QtCore.QUrl.FullyEncoded)
        # -incorrect warning for options type
        # logging.debug(text_tostring_str)

        # formating_opts = QtCore.QUrl.FormattingOptions(QtCore.QUrl.None_)
        # text_displaystring_str = i_qurl.toDisplayString(formating_opts)
        # QtCore.QUrl.FormattingOptions
        # QtCore.QUrl.UrlFormattingOption.

        kammanta.glob.launch_string(text_tostring_str)

    def on_fnd_btn_clicked(self):
        """
        button_list = self.fnd_selection_qbg.buttons()
        nr_of_buttons_int = len(button_list)

        self.fnd_selection_qbg.checkedButton()
        """
        self.update_gui()

    def update_gui(self):
        self.aoi_qtb.setVisible(self.fnd_aoi_qpb.isChecked())
        self.goals_qtb.setVisible(self.fnd_goals_qpb.isChecked())
        self.vision_qtb.setVisible(self.fnd_vision_qpb.isChecked())
        self.pp_qtb.setVisible(self.fnd_pp_qpb.isChecked())

        try:
            self.aoi_qtb.setMarkdown(kammanta.model.aoi_obj.get_text_contents())
            self.goals_qtb.setMarkdown(kammanta.model.go_obj.get_text_contents())
            self.vision_qtb.setMarkdown(kammanta.model.vision_obj.get_text_contents())
            self.pp_qtb.setMarkdown(kammanta.model.pp_obj.get_text_contents())
        except AttributeError:
            self.aoi_qtb.setText(kammanta.model.aoi_obj.get_text_contents())
            self.goals_qtb.setText(kammanta.model.go_obj.get_text_contents())
            self.vision_qtb.setText(kammanta.model.vision_obj.get_text_contents())
            self.pp_qtb.setText(kammanta.model.pp_obj.get_text_contents())

