from pathlib import Path
import logging

from PyQt5.QtWidgets import (QMainWindow, QWidget, QSizePolicy,
                             QApplication, QShortcut, QMessageBox,
                             QFileDialog)
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtGui import QKeySequence

import qdarkstyle
import qdarkgraystyle

from ..app import App
from .dock_area import AppDockArea
from .basic_widgets import ToolBar
from .tools import Icon, get_image_filepath, get_folder_filepath, save_file_dialog

from .init_window import InitWindow
from .debug_widgets import DebugWindow
from .exception_message import UncaughtHook
from ..__version import __version__
from ..update import CheckVersionMessage


class GIWAXSMainController(QObject):

    EXIT_CODE_REBOOT: int = -123456789

    log = logging.getLogger(__name__)

    def __init__(self, res: CheckVersionMessage):

        super().__init__()

        self.app = App()
        self.main_window = GIWAXSMainWindow(res)
        self.main_window.sigCloseApp.connect(self.close_app)
        # self.main_window.sigRestartApp.connect(self.restart_app)

        if self.log.level <= logging.DEBUG:
            self.debug_window = DebugWindow()
        self.exception_hook = UncaughtHook()

        self.log.info(f'{"*" * 10}')
        self.log.info(f'Starting GIWAXS analysis {__version__}!')
        self.log.info(f'{"*" * 10}')

    # def restart_app(self):
    #     self.app.close()
    #     q_app = QApplication.instance()
    #     App._instance = None
    #     q_app.exit(self.EXIT_CODE_REBOOT)

    def close_app(self):
        self.app.close()
        q_app = QApplication.instance()
        App._instance = None
        q_app.exit(0)


class GIWAXSMainWindow(QMainWindow):
    _MinimumSize = (500, 500)

    sigCloseApp = pyqtSignal()
    # sigRestartApp = pyqtSignal()

    def __init__(self, res: CheckVersionMessage, parent=None):
        super(GIWAXSMainWindow, self).__init__(parent=parent)
        self.__closing: bool = False
        self.app = App()
        self._init_toolbar()
        self._init_shortcuts()
        self._init_menubar()

        self.dock_area = AppDockArea(self)
        self.app.fm.sigProjectClosed.connect(self.update_window_title)

        self.setCentralWidget(self.dock_area)
        self.update_window_title()
        self.setWindowIcon(Icon('window_icon'))
        self.setMinimumSize(*self._MinimumSize)
        self.setWindowState(Qt.WindowMaximized)
        self.set_style(self.app.fm.config['style'])
        self.init_window = None

        if not self.app.fm.project_opened:
            self.open_init_window(res)
        else:
            self.show()

    def open_init_window(self, res: CheckVersionMessage):
        self.init_window = InitWindow(self.app.fm.recent_projects, res)
        self.init_window.sigOpenProject.connect(self._on_opening_project)
        self.init_window.sigExit.connect(self._close_from_init)

    def update_window_title(self):
        if self.app.fm.project_opened:
            self.setWindowTitle(f'{self.app.fm.project_name} - GIWAXS analysis')
        else:
            self.setWindowTitle('GIWAXS analysis')

    @pyqtSlot(name='exitFromInitWindow')
    def _close_from_init(self):
        self._closing = True
        self.sigCloseApp.emit()

    @pyqtSlot(object, name='NewProject')
    def _on_opening_project(self, path: Path):
        if self.init_window:
            self.init_window.close()
            self.init_window = None
        self.show()
        self.app.fm.open_project(path)
        self.update_window_title()

    @pyqtSlot(name='NewProjectDialog')
    def _new_project_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, 'New project folder')
        if not folder:
            return
        folder = Path(folder)
        if folder.is_dir():
            self._on_opening_project(folder)

    @pyqtSlot(name='newRealTime')
    def _new_real_time(self):
        pass

    @pyqtSlot(name='addExSitu')
    def _add_file_dialog(self):
        filepath = get_image_filepath(self)
        if filepath:
            self.app.fm.add_root_path_to_project(filepath)

    def _save_as_h5(self):
        path = save_file_dialog(self, title='Save project')
        if path:
            self.app.fm.save_as_h5(path)

    def _add_folder_dialog(self):
        filepath = get_folder_filepath(self, message='Choose directory containing images or h5 files')
        if filepath:
            self.app.fm.add_root_path_to_project(filepath)

    def _init_menubar(self):
        self.menubar = self.menuBar()

        # File menu

        self.file_menu = self.menubar.addMenu('File')
        self.file_menu.addAction('New project', self._new_project_dialog)
        recent_projects_menu = self.file_menu.addMenu('Recent projects')

        for project_path in self.app.fm.recent_projects:
            recent_projects_menu.addAction(
                project_path.name, lambda *x, p=project_path: self._on_opening_project(p))

        # Save

        self.save_menu = self.file_menu.addMenu('Save project as ...')
        self.save_menu.addAction('Save as h5 file', self._save_as_h5)

        # Restart

        # self.file_menu.addAction('Restart', lambda *x: self.restart())

        # Data menu

        self.data_menu = self.menubar.addMenu('Data')
        self.add_data_menu = self.data_menu.addMenu('Add data')

        self.add_data_menu.addAction('Add file', self._add_file_dialog)
        self.add_data_menu.addAction('Add folder', self._add_folder_dialog)

        # Preferences menu

        self.preferences = self.menubar.addMenu('Preferences')
        self.themes_menu = self.preferences.addMenu('Themes')
        themes = ['Dark', 'Gray Dark']
        # themes = CSS.list_css() + QStyleFactory.keys()
        for theme in themes:
            theme_action = self.themes_menu.addAction(theme)
            theme_action.triggered.connect(lambda *x, t=theme: self.set_style(t))

    def _init_shortcuts(self):
        self.copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.copy_shortcut.activated.connect(lambda *x: self.app.roi_dict.copy_rois('selected'))

        self.paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.paste_shortcut.activated.connect(lambda *x: self.app.roi_dict.paste_rois())

        self.select_shortcut = QShortcut(QKeySequence("Ctrl+A"), self)
        self.select_shortcut.activated.connect(lambda *x: self.app.roi_dict.select_all())

        self.delete_shortcut = QShortcut(QKeySequence('Del'), self)
        self.delete_shortcut.activated.connect(lambda *x: self.app.roi_dict.delete_selected_roi())

        self.fit_shortcut = QShortcut(QKeySequence('Ctrl+F'), self)
        self.fit_shortcut.activated.connect(lambda *x: self.app.roi_dict.open_fit_rois(True))

        def raise_err(*_):
            raise ValueError('Congratulations, you found an error combination used for testing! '
                             'Your project will be deleted in 3 seconds...')

        self.raise_shortcut = QShortcut(QKeySequence('Ctrl+R'), self)
        self.raise_shortcut.activated.connect(raise_err)

    def _init_toolbar(self):

        docks_toolbar = ToolBar('Docks', self)
        self.addToolBar(docks_toolbar)

        control_widget = docks_toolbar.addAction(Icon('folder'), 'File Manager')
        control_widget.triggered.connect(lambda: self.dock_area.show_hide_docks('file_widget'))

        radial_profile = docks_toolbar.addAction(Icon('radial_profile'), 'Radial profile')
        radial_profile.triggered.connect(lambda: self.dock_area.show_hide_docks('radial_profile'))

        angular_profile = docks_toolbar.addAction(Icon('angular_profile'), 'Angular profile')
        angular_profile.triggered.connect(lambda: self.dock_area.show_hide_docks('angular_profile'))

        interpolation = docks_toolbar.addAction(Icon('interpolate'), 'Polar Viewer')
        interpolation.triggered.connect(lambda: self.dock_area.show_hide_docks('polar'))

        self.gen_toolbar = ToolBar('General')
        self.addToolBar(self.gen_toolbar)
        spacer_widget = QWidget()
        spacer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer_widget.setVisible(True)
        self.gen_toolbar.addWidget(spacer_widget)

        self.fullscreen_action = self.gen_toolbar.addAction(Icon('tofullscreen'), 'Full screen')
        self.fullscreen_action.triggered.connect(self._on_fullscreen_changed)

    def _on_fullscreen_changed(self):
        if self.isFullScreen():
            self.setWindowState(Qt.WindowMaximized)
            self.fullscreen_action.setIcon(Icon('tofullscreen'))
        else:
            self.setWindowState(Qt.WindowFullScreen)
            self.fullscreen_action.setIcon(Icon('fromfullscreen'))

    def set_style(self, name: str = 'Gray Dark'):
        qapp = QApplication.instance()
        if not qapp:
            raise RuntimeError('No running application found.')
        if name == 'Dark':
            qapp.setStyleSheet('')
            qapp.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        elif name == 'Gray Dark':
            qapp.setStyleSheet('')
            qapp.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
        else:
            return

        self.app.fm.config['style'] = name

    # @pyqtSlot(name='restartApp')
    # def restart(self):
    #     self.__closing = True
    #     self.sigRestartApp.emit()

    def closeEvent(self, a0) -> None:
        if self.__closing:
            super().closeEvent(a0)
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to quit? The project will be saved.",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                a0.accept()
                self.__closing = True
                self.sigCloseApp.emit()
            else:
                a0.ignore()
