from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import kammanta.model
import kammanta.widgets.checklist_cw
import kammanta.glob
import kammanta.gtd_info

TITLE_STR = "Next Actions and Projects"


class NAsPrjs(QtWidgets.QWidget):
    focus_active_signal = QtCore.pyqtSignal(bool)

    def __init__(self, i_parent):
        super().__init__(i_parent)

        hbox_l3 = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_l3)

        self.next_actions_column = kammanta.widgets.checklist_cw.ChecklistWidget(self, kammanta.model.na_files)
        hbox_l3.addWidget(self.next_actions_column)
        self.next_actions_column.setWhatsThis(kammanta.gtd_info.NA_STR)
        self.next_actions_column.focus_active_signal.connect(self.focus_active_signal.emit)

        self.projects_column = kammanta.widgets.checklist_cw.ChecklistWidget(self, kammanta.model.prj_fds)
        hbox_l3.addWidget(self.projects_column)
        self.projects_column.setWhatsThis(kammanta.gtd_info.PRJ_STR)
        self.projects_column.focus_active_signal.connect(self.focus_active_signal.emit)

        self.update_gui()

    # overridden
    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        pass
        # self.update_gui()
        # -removed for now since this has been seen (only once) to cause an infinite loop

    def add_fsw_dirs(self):
        main_dir_str = kammanta.model.na_files.get_path()
        kammanta.glob.FswSingleton.get().addPath(main_dir_str)

        """
        na_path_dir_str = kammanta.model.na_files.get_path()
        kammanta.glob.FswSingleton.get().addPath(na_path_dir_str)
        prj_path_dir_str = kammanta.model.prj_fds.get_path()
        kammanta.glob.FswSingleton.get().addPath(prj_path_dir_str)
        """

    def update_gui(self):
        self.add_fsw_dirs()

        # self.next_actions_column.update_gui_and_ids()
        # self.projects_column.update_gui_and_ids()

        self.next_actions_column.update_gui_item_list_and_ids()
        self.projects_column.update_gui_item_list_and_ids()

