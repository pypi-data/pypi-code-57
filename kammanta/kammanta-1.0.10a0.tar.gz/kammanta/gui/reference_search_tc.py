from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import os
import kammanta.model
import kammanta.glob
import kammanta.widgets.path_sel_dlg

TITLE_STR = "Reference and Search"


class ReferenceSearch(QtWidgets.QWidget):
    def __init__(self, i_parent):
        super().__init__(i_parent)

        self.custom_scope_path_str = ""

        hbox_l2 = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_l2)

        # Navigation and favorites

        left_vbox_l3 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(left_vbox_l3)
        self.favorites_qll = QtWidgets.QLabel("Favorites", parent=self)
        left_vbox_l3.addWidget(self.favorites_qll)
        #self.favorites_qll.setFixedWidth(100)

        self.favorites_qlw = QtWidgets.QListWidget(self)
        left_vbox_l3.addWidget(self.favorites_qlw)
        self.favorites_qlw.currentItemChanged.connect(self.on_favourites_item_changed)

        hbox_l4 = QtWidgets.QHBoxLayout()
        left_vbox_l3.addLayout(hbox_l4)
        self.add_new_fav_path_qll = QtWidgets.QLabel("- selected path here -", parent=self)
        hbox_l4.addWidget(self.add_new_fav_path_qll)
        self.select_new_fav_path_qpb = QtWidgets.QPushButton("Select file or dir")
        hbox_l4.addWidget(self.select_new_fav_path_qpb)
        self.select_new_fav_path_qpb.clicked.connect(self.on_select_new_fav_path_clicked)

        hbox_l4 = QtWidgets.QHBoxLayout()
        left_vbox_l3.addLayout(hbox_l4)
        self.add_new_fav_name_qle = QtWidgets.QLineEdit(parent=self)
        hbox_l4.addWidget(self.add_new_fav_name_qle)
        self.add_new_fav_name_qle.setPlaceholderText("Description/name")
        self.add_new_fav_qpb = QtWidgets.QPushButton("Add")
        hbox_l4.addWidget(self.add_new_fav_qpb)
        self.add_new_fav_qpb.clicked.connect(self.on_add_fav_clicked)
        self.add_new_fav_name_qle.returnPressed.connect(self.add_new_fav_qpb.click)

        # self.latest_qlw = QtWidgets.QListWidget()
        # left_vbox_l3.addWidget(self.latest_qlw)

        # File list (search results and dir listings)

        df_list_vbox_l3 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(df_list_vbox_l3, stretch=2)
        controls_hbox_l4 = QtWidgets.QHBoxLayout()
        df_list_vbox_l3.addLayout(controls_hbox_l4)

        scope_hbox_l4 = QtWidgets.QHBoxLayout()
        df_list_vbox_l3.addLayout(scope_hbox_l4)

        self.search_scope_qbg = QtWidgets.QButtonGroup()
        self.main_dir_scope_qrb = QtWidgets.QRadioButton("Main dir")
        self.search_scope_qbg.addButton(self.main_dir_scope_qrb)
        scope_hbox_l4.addWidget(self.main_dir_scope_qrb)
        self.ref_dir_scope_qrb = QtWidgets.QRadioButton("Reference dir")
        self.search_scope_qbg.addButton(self.ref_dir_scope_qrb)
        scope_hbox_l4.addWidget(self.ref_dir_scope_qrb)
        self.main_and_ref_dir_scope_qrb = QtWidgets.QRadioButton("Ref + GTD dir")
        self.search_scope_qbg.addButton(self.main_and_ref_dir_scope_qrb)
        scope_hbox_l4.addWidget(self.main_and_ref_dir_scope_qrb)
        self.custom_scope_qrb = QtWidgets.QRadioButton("Custom [todo]")
        self.search_scope_qbg.addButton(self.custom_scope_qrb)
        scope_hbox_l4.addWidget(self.custom_scope_qrb)
        self.custom_scope_qpb = QtWidgets.QPushButton("Choose dir")
        scope_hbox_l4.addWidget(self.custom_scope_qpb)

        self.search_type_qbg = QtWidgets.QButtonGroup()
        self.file_name_search_qrb = QtWidgets.QRadioButton("File name")
        self.search_type_qbg.addButton(self.file_name_search_qrb)
        controls_hbox_l4.addWidget(self.file_name_search_qrb)
        self.text_search_qrb = QtWidgets.QRadioButton("Text in files")
        self.search_type_qbg.addButton(self.text_search_qrb)
        controls_hbox_l4.addWidget(self.text_search_qrb)
        self.search_qle = QtWidgets.QLineEdit()
        controls_hbox_l4.addWidget(self.search_qle)
        self.search_qpb = QtWidgets.QPushButton("Search")
        controls_hbox_l4.addWidget(self.search_qpb)
        self.search_qpb.clicked.connect(self.on_search_clicked)
        self.search_qle.returnPressed.connect(self.search_qpb.click)

        self.result_list_cw = QtWidgets.QListWidget()
        df_list_vbox_l3.addWidget(self.result_list_cw)
        new_font = self.result_list_cw.font()
        new_font.setPointSize(13)
        self.result_list_cw.setFont(new_font)
        self.result_list_cw.currentItemChanged.connect(self.on_result_item_changed)
        # self.result_list_cw.setSpacing(3)
        self.result_list_cw.setStyleSheet("QListWidget::item { margin: 5px; }")
        self.result_list_cw.setWordWrap(True)

        # Selected preview, details and actions/controls

        selected_vbox_l3 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(selected_vbox_l3, stretch=2)

        hbox_l4 = QtWidgets.QHBoxLayout()
        # selected_hbox_l4.setSizeConstraint()
        # https://doc.qt.io/qt-5/qlayout.html#sizeConstraint-prop
        selected_vbox_l3.addLayout(hbox_l4)

        # df_info_vbox_l5 = QtWidgets.QVBoxLayout()
        # hbox_l4.addLayout(df_info_vbox_l5)

        self.file_info_qll = QtWidgets.QLabel("file info")
        hbox_l4.addWidget(self.file_info_qll)

        df_actions_vbox_l5 = QtWidgets.QVBoxLayout()
        hbox_l4.addLayout(df_actions_vbox_l5)


        self.open_containing_dir_qpb = QtWidgets.QPushButton("Open containing dir")
        df_actions_vbox_l5.addWidget(self.open_containing_dir_qpb)
        self.open_containing_dir_qpb.clicked.connect(self.on_open_containing_dir_clicked)

        self.open_fod_qpb = QtWidgets.QPushButton("Open")
        df_actions_vbox_l5.addWidget(self.open_fod_qpb)
        self.open_fod_qpb.clicked.connect(self.on_open_fod_clicked)

        self.copy_path_fod_qpb = QtWidgets.QPushButton("Copy path")
        df_actions_vbox_l5.addWidget(self.copy_path_fod_qpb)
        self.copy_path_fod_qpb.clicked.connect(self.on_copy_fod_path_clicked)

        self.move_fod_qpb = QtWidgets.QPushButton("Move")
        df_actions_vbox_l5.addWidget(self.move_fod_qpb)
        self.move_fod_qpb.setDisabled(True)

        self.delete_fod_qpb = QtWidgets.QPushButton("Delete")
        df_actions_vbox_l5.addWidget(self.delete_fod_qpb)
        self.delete_fod_qpb.setDisabled(True)

        self.fav_fod_qpb = QtWidgets.QPushButton("Favorite")
        df_actions_vbox_l5.addWidget(self.fav_fod_qpb)
        self.fav_fod_qpb.setCheckable(True)
        self.fav_fod_qpb.setDisabled(True)

        # ..preview

        self.preview_qsw = QtWidgets.QStackedWidget()
        selected_vbox_l3.addWidget(self.preview_qsw)
        # self.preview_qsw.setObjectName("preview_qsw")
        # self.preview_qsw.setFixedWidth(WIDTH_AND_HEIGHT_INT)

        self.empty_preview_qll = QtWidgets.QLabel("no preview")
        self.preview_qsw.addWidget(self.empty_preview_qll)

        self.text_preview_qtb = QtWidgets.QTextBrowser()
        self.preview_qsw.addWidget(self.text_preview_qtb)

        self.image_preview_qll = QtWidgets.QLabel()
        self.preview_qsw.addWidget(self.image_preview_qll)
        self.image_preview_qll.setMaximumWidth(300)

        self.dir_preview_qtb = QtWidgets.QTextBrowser()
        self.preview_qsw.addWidget(self.dir_preview_qtb)

        self.preview_qsw.setCurrentWidget(self.empty_preview_qll)

        """
        self.file_preview_qll = QtWidgets.QLabel("preview")
        self.file_preview_qll.setFixedHeight(240)
        selected_vbox_l3.addWidget(self.file_preview_qll)
        self.file_preview_qll.setWordWrap(True)
        """

        """
        Do we want to add reference files to the fsw?
        contacts_dir_path_str = kammanta.model.contacts_dir.get_path()
        kammanta.glob.FswSingleton.get().addPath(contacts_dir_path_str)
        """

        self.update_gui()
        self.file_name_search_qrb.click()
        self.main_and_ref_dir_scope_qrb.click()

    def on_copy_fod_path_clicked(self):
        active_item = self.result_list_cw.currentItem()
        if not active_item:
            return
        active_id_and_path_str = active_item.data(QtCore.Qt.UserRole)  # -the path is the id
        qt_clipboard = QtGui.QGuiApplication.clipboard()
        qt_clipboard.setText(active_id_and_path_str)

    def on_open_containing_dir_clicked(self):
        active_item = self.result_list_cw.currentItem()
        if not active_item:
            return
        active_id_str = active_item.data(QtCore.Qt.UserRole)  # -the path is the id
        containing_dir_path_str = os.path.dirname(active_id_str)
        kammanta.glob.launch_string(containing_dir_path_str)
        # self.update_fod_details(active_id_str)

    def on_open_fod_clicked(self):
        active_item = self.result_list_cw.currentItem()
        if not active_item:
            return
        active_id_int = active_item.data(QtCore.Qt.UserRole)  # -the path is the id
        kammanta.glob.launch_string(active_id_int)
        # self.update_fod_details(active_id_int)

    def on_result_item_changed(self, i_current: QtWidgets.QListWidgetItem, i_previous: QtWidgets.QListWidgetItem):
        if i_current:
            path_str = i_current.data(QtCore.Qt.UserRole)
            self.update_fod_details(path_str)

    def update_fod_details(self, i_path: str):
        # Determining the type of file/dir: Text, image, other file, directory

        type_enum = kammanta.glob.get_type(i_path)
        # self.file_preview_qll.setPixmap(None)
        if type_enum == kammanta.glob.TypeEnum.dir:
            dir_contents_fn_strlist = os.listdir(i_path)
            dir_contents_str = "\n".join(dir_contents_fn_strlist)
            self.dir_preview_qtb.setPlainText(dir_contents_str)
            self.preview_qsw.setCurrentWidget(self.dir_preview_qtb)
        elif type_enum in (kammanta.glob.TypeEnum.text_file, kammanta.glob.TypeEnum.note_file):
            with open(i_path, "r") as file:
                first_lines_strlist = []
                line_item = True
                i = 0
                while i < 1000:
                    line_item = next(file, False)
                    if line_item == False:
                        break
                    first_lines_strlist.append(line_item)
                    i += 1
                # first_lines_strlist = [next(file) for x in range(10)]
                # text_file_content_str = file.read()
                first_lines_str = "".join(first_lines_strlist)
                self.text_preview_qtb.setPlainText(first_lines_str)
                self.preview_qsw.setCurrentWidget(self.text_preview_qtb)
        elif type_enum == kammanta.glob.TypeEnum.image_file:
            pixmap = QtGui.QPixmap(i_path)
            pixmap = pixmap.scaled(300, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.image_preview_qll.setPixmap(pixmap)
            self.preview_qsw.setCurrentWidget(self.image_preview_qll)
        else:
            self.preview_qsw.setCurrentWidget(self.empty_preview_qll)

        file_name_str = os.path.basename(i_path)
        # last_mod_str = os.
        self.file_info_qll.setText(file_name_str)

    def on_select_new_fav_path_clicked(self):
        (file_path_str, result_enum) = kammanta.widgets.path_sel_dlg.PathSelDlg.open_dlg_and_get_path(
            kammanta.widgets.path_sel_dlg.PathSelectionEnum.dir, "/home", ""
        )
        if not result_enum == kammanta.widgets.path_sel_dlg.PathSelectionEnum.cancelled:
            self.add_new_fav_path_qll.setText(file_path_str)

    def on_add_fav_clicked(self):
        new_fav_name_str = self.add_new_fav_name_qle.text()
        self.add_new_fav_name_qle.clear()

        new_fav_path_str = self.add_new_fav_path_qll.text()
        self.add_new_fav_path_qll.clear()

        """
        config_parser = configparser.ConfigParser()
        config_file_path_str = gtd.gtd_global.get_appl_path(gtd.gtd_global.SETTINGS_FILE_NAME_STR)
        config_parser.read(config_file_path_str)
        if not config_parser.has_section(gtd.gtd_global.SETTINGS_SECTION_FAVORITE_REFERENCES_STR):
            config_parser.add_section(gtd.gtd_global.SETTINGS_SECTION_FAVORITE_REFERENCES_STR)
        config_parser.set(gtd.gtd_global.SETTINGS_SECTION_FAVORITE_REFERENCES_STR, new_fav_name_str, new_fav_path_str)
        with open(config_file_path_str, "w") as file:
            config_parser.write(file)
        """

        kammanta.glob.add_string_to_config(
            kammanta.glob.SETTINGS_SECTION_FAVORITE_REFERENCES_STR, new_fav_name_str, new_fav_path_str
        )

        self.update_gui()

    def on_favourites_item_changed(self, i_new_item: QtWidgets.QListWidgetItem, i_prev_item: QtWidgets.QListWidgetItem):
        if i_new_item is None:
            return
        new_name_str = i_new_item.data(QtCore.Qt.UserRole)
        # -the name is the key in the settings file

        """
        config_parser = configparser.ConfigParser()
        config_file_path_str = gtd.gtd_global.get_appl_path(gtd.gtd_global.SETTINGS_FILE_NAME_STR)
        config_parser.read(config_file_path_str)
        favorites_dict = dict(config_parser.items(gtd.gtd_global.SETTINGS_SECTION_FAVORITE_REFERENCES_STR))
        """
        favorites_dict = kammanta.glob.get_dictionary_from_config(
            kammanta.glob.SETTINGS_SECTION_FAVORITE_REFERENCES_STR
        )

        new_path_str = favorites_dict[new_name_str]

        self.result_list_cw.clear()
        self.preview_qsw.setCurrentWidget(self.empty_preview_qll)

        main_path_str = kammanta.glob.get_path()
        ref_path_str = kammanta.glob.get_ref_path()
        for name_str in os.listdir(new_path_str):
            # main_path_first_bool
            path_str = os.path.join(new_path_str, name_str)
            title_str = path_str
            if path_str.startswith(main_path_str):
                rest_of_path_str = os.path.relpath(path_str, start=main_path_str)
                title_str = "[main-dir]/" + rest_of_path_str
            elif path_str.startswith(ref_path_str):
                rest_of_path_str = os.path.relpath(path_str, start=ref_path_str)
                title_str = "[ref-dir]/" + rest_of_path_str

            qlwi = QtWidgets.QListWidgetItem()
            # qlwi.margin
            qlwi.setText(title_str)
            qlwi.setData(QtCore.Qt.UserRole, path_str)  # -the path works as the id
            self.result_list_cw.addItem(qlwi)


        # TODO: self.update_gui()

        """
        self.file_preview_qll.setText("")
        if os.path.isfile(new_path_str):
            # self.file_info_qll
            with open(new_path_str, "r") as file:
                try:
                    text_contents_str = file.read()
                    text_contents_str = text_contents_str[:50]
                    self.file_preview_qll.setText(text_contents_str)
                except UnicodeDecodeError:
                    pass
        elif os.path.isdir(new_path_str):
            files_in_dir_list = os.listdir(new_path_str)
            self.result_list_cw.addItems(files_in_dir_list)
        """

    def on_search_clicked(self):
        self.result_list_cw.clear()
        output_path_strlist = []
        search_str = self.search_qle.text()

        search_dir_path_strlist = []
        if self.main_dir_scope_qrb.isChecked():
            search_dir_path_strlist.append(kammanta.glob.get_path())
        elif self.ref_dir_scope_qrb.isChecked():
            search_dir_path_strlist.append(kammanta.glob.get_ref_path())
        elif self.main_and_ref_dir_scope_qrb.isChecked():
            search_dir_path_strlist.append(kammanta.glob.get_path())
            search_dir_path_strlist.append(kammanta.glob.get_ref_path())
        elif self.custom_scope_qpb.isChecked():
            search_dir_path_strlist.append(self.custom_scope_path_str)

        main_path_str = kammanta.glob.get_path()
        ref_path_str = kammanta.glob.get_ref_path()
        main_path_first_bool = True
        if ref_path_str.startswith(main_path_str):
            main_path_first_bool = False

        if self.file_name_search_qrb.isChecked():
            output_path_strlist = self.search_file_names(search_str, search_dir_path_strlist)
            for path_str in output_path_strlist:
                # main_path_first_bool
                title_str = path_str
                if path_str.startswith(main_path_str):
                    rest_of_path_str = os.path.relpath(path_str, start=main_path_str)
                    title_str = "[main-dir]/" + rest_of_path_str
                elif path_str.startswith(ref_path_str):
                    rest_of_path_str = os.path.relpath(path_str, start=ref_path_str)
                    title_str = "[ref-dir]/" + rest_of_path_str

                qlwi = QtWidgets.QListWidgetItem()
                # qlwi.margin
                qlwi.setText(title_str)
                qlwi.setData(QtCore.Qt.UserRole, path_str)  # -the path works as the id
                self.result_list_cw.addItem(qlwi)

        elif self.text_search_qrb.isChecked():
            output_path_tuplelist = self.search_text_in_files(search_str, search_dir_path_strlist)
            for (path_str, extra_info_str) in output_path_tuplelist:
                # main_path_first_bool
                title_str = path_str
                if path_str.startswith(main_path_str):
                    rest_of_path_str = os.path.relpath(path_str, start=main_path_str)
                    title_str = "[main-dir]/" + rest_of_path_str
                elif path_str.startswith(ref_path_str):
                    rest_of_path_str = os.path.relpath(path_str, start=ref_path_str)
                    title_str = "[ref-dir]/" + rest_of_path_str
                title_str = title_str + "\n" + extra_info_str

                qlwi = QtWidgets.QListWidgetItem()
                qlwi.setText(title_str)
                qlwi.setData(QtCore.Qt.UserRole, path_str)  # -the path works as the id
                self.result_list_cw.addItem(qlwi)

    def search_file_names(self, i_search_text: str, i_search_area_path_strlist: list):
        # https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
        # file_name_strlist = os.listdir(gtd.model.get_path())
        output_strlist = []

        entire_walk_result_tuple = []
        for search_area_path_str in i_search_area_path_strlist:
            result_tuple_list = os.walk(search_area_path_str)
            for triple_tuple in result_tuple_list:
                if triple_tuple not in entire_walk_result_tuple:
                    entire_walk_result_tuple.append(triple_tuple)

        for root_str, dir_name_strlist, file_name_strlist in entire_walk_result_tuple:
            for file_name_str in file_name_strlist:
                if i_search_text in file_name_str:
                    file_path_str = os.path.join(root_str, file_name_str)
                    # relative_file_path_str = os.path.relpath(file_path_str, start=i_search_area_path)
                    # output_strlist.append("[ref-dir]/" + relative_file_path_str)
                    output_strlist.append(file_path_str)
            for dir_name_str in dir_name_strlist:
                if i_search_text in dir_name_str:
                    dir_path_str = os.path.join(root_str, dir_name_str)
                    output_strlist.append(dir_path_str)
        return output_strlist

    def search_text_in_files(self, i_search_text: str, i_search_area_path_strlist: list) -> [tuple]:
        # , i_shortened_base: str = ""
        output_tuplelist = []

        entire_walk_result_tuple = []
        for search_area_path_str in i_search_area_path_strlist:
            result_tuple_list = os.walk(search_area_path_str)
            for triple_tuple in result_tuple_list:
                if triple_tuple not in entire_walk_result_tuple:
                    entire_walk_result_tuple.append(triple_tuple)

        for root_str, dir_name_strlist, file_name_strlist in entire_walk_result_tuple:
            for file_name_str in file_name_strlist:
                file_path_str = os.path.join(root_str, file_name_str)
                if not os.path.isfile(file_path_str):
                    continue  # -for when we have a symlink
                with open(file_path_str, "r") as file:
                    try:
                        text_line_list = file.readlines()
                        for count_int, text_line in enumerate(text_line_list):
                            if i_search_text in text_line:
                                # -this can give us many results for the same file. Please note that this also
                                #  means that we can have the same id for many search hits. TODO: Fixing this
                                formatted_file_path_str = file_path_str
                                extra_search_info_str = "Line nr: " + str(count_int) + " | Line: " + text_line.rstrip()
                                output_tuplelist.append((formatted_file_path_str, extra_search_info_str))
                                # -Using yeild instead so that we get results in realtime?
                    except UnicodeDecodeError:
                        pass
                        # -not a text file(?)
                        # https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python

        return output_tuplelist

    # overridden
    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.update_gui()

    def update_gui(self):
        # Favorites
        """
        config_parser = configparser.ConfigParser()
        config_file_path_str = gtd.gtd_global.get_appl_path(gtd.gtd_global.SETTINGS_FILE_NAME_STR)
        config_parser.read(config_file_path_str)
        favorites_dict = {}
        if config_parser.has_section(gtd.gtd_global.SETTINGS_SECTION_FAVORITE_REFERENCES_STR):
            favorites_dict = dict(config_parser.items(gtd.gtd_global.SETTINGS_SECTION_FAVORITE_REFERENCES_STR))
        """
        favorites_dict = kammanta.glob.get_dictionary_from_config(
            kammanta.glob.SETTINGS_SECTION_FAVORITE_REFERENCES_STR
        )
        self.favorites_qlw.clear()
        for name_str, path_str in favorites_dict.items():
            qlwi = QtWidgets.QListWidgetItem()
            qlwi.setText(name_str + " | " + path_str)
            qlwi.setData(QtCore.Qt.UserRole, name_str)
            self.favorites_qlw.addItem(qlwi)

        """
        # Latest
        self.latest_qlw.clear()
        latest_telist = []
        # output_strlist = []
        # file_name_strlist = os.listdir(gtd.gtd_global.get_path())
        # for file_name in file_name_strlist:
        for root_str, dir_name_strlist, file_name_strlist in os.walk(gtd.glob.get_path()):
            file_name_strlist = [f for f in file_name_strlist if os.path.isfile(f)]
            for file_name_str in file_name_strlist:
                file_path_str = os.path.join(root_str, file_name_str)
                mtime_int = int(os.path.getmtime(file_path_str))
                # output_strlist.append(file_path_str + " " + str(mtime))
                latest_telist.append((mtime_int, file_name_str + " | " + str(mtime_int)))
                # output_strlist.append(file_name_str + " | " + str(mtime_int))
        latest_telist = sorted(latest_telist, key=lambda x: x[0], reverse=True)
        latest_strlist = [x[1] for x in latest_telist]
        latest_strlist = latest_strlist[:15]
        self.latest_qlw.addItems(latest_strlist)
        """

        ###############

        #https://docs.python.org/3/library/os.html#os.walk
        #https://www.quora.com/Whats-the-easiest-way-to-recursively-get-a-list-of-all-the-files-in-a-directory-tree-in-Python


class SearchDockContainer(QtWidgets.QWidget):
    search_clicked_signal = QtCore.pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.setSizePolicy(self.sizePolicy().horizontalPolicy(), QtWidgets.QSizePolicy.Maximum)
        vbox_l1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)
        self.file_name_search_qrb = QtWidgets.QRadioButton("File name")
        hbox_l2.addWidget(self.file_name_search_qrb)
        self.text_search_qrb = QtWidgets.QRadioButton("Text in files")
        hbox_l2.addWidget(self.text_search_qrb)

        hbox_l2 = QtWidgets.QHBoxLayout()
        vbox_l1.addLayout(hbox_l2)
        self.search_qle = QtWidgets.QLineEdit()
        hbox_l2.addWidget(self.search_qle)
        self.search_qpb = QtWidgets.QPushButton("Search")
        hbox_l2.addWidget(self.search_qpb)
        self.search_qpb.clicked.connect(self.on_search_clicked)

        self.search_qle.returnPressed.connect(self.search_qpb.click)

        self.file_name_search_qrb.click()

    def on_search_clicked(self):
        is_file_name_search_bool = self.file_name_search_qrb.isChecked()
        search_text_str = self.search_qle.text()
        self.search_clicked_signal.emit(is_file_name_search_bool, search_text_str)



