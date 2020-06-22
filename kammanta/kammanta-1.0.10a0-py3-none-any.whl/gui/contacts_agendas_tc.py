import logging
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import kammanta.model
import kammanta.glob
import kammanta.widgets.checklist_cw
import kammanta.gtd_info
import kammanta.widgets.md_input_dlg

TITLE_STR = "Contacts and Agendas"


class ContactsAgendas(QtWidgets.QWidget):
    def __init__(self, i_parent):
        super().__init__(i_parent)

        hbox_l2 = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_l2)

        self.contacts_cw = ContactsCw()
        hbox_l2.addWidget(self.contacts_cw)
        self.contacts_cw.setWhatsThis(kammanta.gtd_info.CONTACTS_STR)

        self.agenda_items_cw = kammanta.widgets.checklist_cw.ChecklistWidget(self, kammanta.model.agenda_files)
        hbox_l2.addWidget(self.agenda_items_cw)
        self.agenda_items_cw.setWhatsThis(kammanta.gtd_info.AGENDAS_STR)

        self.contacts_cw.show_create_agenda_signal.connect(self.on_contacts_show_create_agenda)

        self.update_gui()

    def on_contacts_show_create_agenda(self, i_new_agenda_name: str):
        # Showing
        for agenda_item in kammanta.model.agenda_files.get_all_items():
            if i_new_agenda_name == agenda_item.get_name():
                kammanta.model.agenda_files.set_active_item(agenda_item.get_id())
                self.agenda_items_cw.update_gui_and_ids()
                return

        # Creating
        agenda_name_str = kammanta.glob.add_suffix(i_new_agenda_name, kammanta.glob.TEXT_SUFFIX_STR)
        kammanta.model.agenda_files.add_new_item(agenda_name_str)
        self.agenda_items_cw.update_gui_and_ids()
        # -Unclear why this is needed, but otherwise we get the wrong ordering
        for agenda_item in kammanta.model.agenda_files.get_all_items():
            if agenda_name_str == agenda_item.get_name():
                kammanta.model.agenda_files.set_active_item(agenda_item.get_id())
                self.agenda_items_cw.update_gui_and_ids()

    # overridden
    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.update_gui()

    def update_gui(self):
        self.contacts_cw.update_gui()
        self.agenda_items_cw.update_gui_and_ids()


class ContactsCw(QtWidgets.QWidget):
    contact_text_changed_signal = QtCore.pyqtSignal(str)
    show_create_agenda_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = True

        #
        # self.contact_selection_qlw = QtWidgets.QListWidget()
        # self.contact_selection_qlw.currentItemChanged.connect(self.on_contact_list_item_changed)
        #
        # self.open_coll_file_qpb = QtWidgets.QPushButton("Open")
        # self.open_coll_file_qpb.clicked.connect(self.open)
        #
        # self.add_new_coll_qle = QtWidgets.QLineEdit()
        # self.add_new_coll_qle.setPlaceholderText("placeholder text ----")
        # # -perhaps allow customization of this, for example in settings.ini (globally) or in each context file
        # self.add_new_coll_qpb = QtWidgets.QPushButton("Add new")
        # self.add_new_coll_qpb.clicked.connect(self.on_add_new_coll_clicked)
        #
        # self.rename_coll_qpb = QtWidgets.QPushButton("Rename")
        # self.rename_coll_qpb.clicked.connect(self.on_rename_coll)
        #
        # self.delete_coll_qpb = QtWidgets.QPushButton("Delete")
        # self.delete_coll_qpb.clicked.connect(self.on_delete_coll)
        # self.add_new_coll_qle.returnPressed.connect(self.add_new_coll_qpb.click)


        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)
        self.title_qll = QtWidgets.QLabel("Contacts")
        vbox_l2.addWidget(self.title_qll)

        hbox_l3.addStretch(1)
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3, stretch=1)





        vbox_l4 = QtWidgets.QVBoxLayout()
        hbox_l3.addLayout(vbox_l4, stretch=1)
        self.search_qle = QtWidgets.QLineEdit()
        vbox_l4.addWidget(self.search_qle)
        self.search_qle.textChanged.connect(self.on_search_text_changed)
        self.search_qle.setPlaceholderText("<search>")

        self.contacts_qlw = QtWidgets.QListWidget()
        vbox_l4.addWidget(self.contacts_qlw, stretch=1)
        self.contacts_qlw.currentItemChanged.connect(self.on_contact_list_item_changed)
        new_font = QtGui.QFont()
        new_font.setPointSize(12)
        self.contacts_qlw.setFont(new_font)
        self.contacts_qlw.setSpacing(1)

        controls_vbox_l5 = QtWidgets.QVBoxLayout()
        hbox_l3.addLayout(controls_vbox_l5)

        controls_vbox_l5.addStretch()

        self.contacts_edit_qpb = QtWidgets.QPushButton("Edit")
        controls_vbox_l5.addWidget(self.contacts_edit_qpb)
        self.contacts_edit_qpb.clicked.connect(self.on_edit_contacts_clicked)

        self.contact_rename_qpb = QtWidgets.QPushButton("Rename")
        controls_vbox_l5.addWidget(self.contact_rename_qpb)
        self.contact_rename_qpb.clicked.connect(self.on_contact_rename_clicked)

        self.show_create_agenda_qpb = QtWidgets.QPushButton("show/create agenda")
        controls_vbox_l5.addWidget(self.show_create_agenda_qpb)
        self.show_create_agenda_qpb.clicked.connect(self.on_show_create_agenda_clicked)

        self.new_contact_qle = QtWidgets.QLineEdit()
        controls_vbox_l5.addWidget(self.new_contact_qle)
        self.new_contact_qle.setPlaceholderText("new contact name")

        self.new_contact_qpb = QtWidgets.QPushButton("Add New")
        controls_vbox_l5.addWidget(self.new_contact_qpb)
        self.new_contact_qpb.clicked.connect(self.on_add_new_contact_clicked)
        self.new_contact_qle.returnPressed.connect(self.new_contact_qpb.click)

        self.delete_contact_qpb = QtWidgets.QPushButton("Delete")
        controls_vbox_l5.addWidget(self.delete_contact_qpb)
        self.delete_contact_qpb.clicked.connect(self.on_delete_contact_clicked)

        self.fav_contact_qcb = QtWidgets.QPushButton("Favorite")
        controls_vbox_l5.addWidget(self.fav_contact_qcb)
        self.fav_contact_qcb.setCheckable(True)
        self.fav_contact_qcb.toggled.connect(self.on_fav_contact_toggled)

        controls_vbox_l5.addStretch()

        self.contact_qte = QtWidgets.QTextBrowser()
        vbox_l2.addWidget(self.contact_qte, stretch=2)
        self.contact_qte.setOpenExternalLinks(True)
        # self.contact_qte.setForma
        self.contact_qte.zoomIn(2)
        self.contact_qte.setReadOnly(True)

        contacts_dir_path_str = kammanta.model.contacts_dir.get_path()
        kammanta.glob.FswSingleton.get().addPath(contacts_dir_path_str)
        agendas_dir_path_str = kammanta.model.agenda_files.get_path()
        kammanta.glob.FswSingleton.get().addPath(agendas_dir_path_str)

        self.update_gui()

        self.updating_gui_bool = False

    def on_fav_contact_toggled(self, i_checked: bool):
        logging.debug(str(i_checked))
        kammanta.model.contacts_dir.get_active_item().set_favorite(i_checked)
        self.update_gui()

    def on_delete_contact_clicked(self):
        code_for_button_clicked_int = QtWidgets.QMessageBox.question(
            self, "Title", "Are you sure you want to delete this?",
            defaultButton=QtWidgets.QMessageBox.No
        )
        if code_for_button_clicked_int == QtWidgets.QMessageBox.Yes:
            active_item_id_str = kammanta.model.contacts_dir.get_active_item().get_id()
            kammanta.model.contacts_dir.delete_item(active_item_id_str)

    def on_search_text_changed(self, i_new_text: str):
        if self.contacts_qlw.count() == 1:
            only_item = self.contacts_qlw.item(0)
            id_str = only_item.data(QtCore.Qt.UserRole)
            kammanta.model.contacts_dir.set_active_item(id_str)

        self.update_gui()

        self.contacts_qlw.setCurrentRow(0)

    def on_show_create_agenda_clicked(self):
        # self.contacts_qlw.
        contact_core_name_str = kammanta.model.contacts_dir.get_active_item().get_core_name()
        self.show_create_agenda_signal.emit(contact_core_name_str)

    def on_add_new_contact_clicked(self):
        contact_name_str = self.new_contact_qle.text().strip()
        self.new_contact_qle.clear()
        if not contact_name_str:
            QtWidgets.QMessageBox.information(self, "Message", "Please enter at least one letter before adding a new contact")
            return
        if not contact_name_str.lower().endswith(kammanta.glob.TEXT_SUFFIX_STR):
            contact_name_str += kammanta.glob.TEXT_SUFFIX_STR
        kammanta.glob.add_contact(contact_name_str)
        kammanta.model.contacts_dir.set_active_item(contact_name_str)

        self.update_gui()

        self.on_edit_contacts_clicked()

    def on_edit_contacts_clicked(self):
        # file_path_str = self.get_file_path()
        #####file_path_str = gtd.model.contacts_dir.get_active_item().get_path()

        active_contact_item = kammanta.model.contacts_dir.get_active_item()
        (new_text_str, okay_bool) = kammanta.widgets.md_input_dlg.MarkdownInputDialog.open_dlg_and_get_text(active_contact_item.get_path())

        # , but you can simply use normal text, but please remember to add an extra line break if you want a new paragraph on the next line
        if okay_bool:
            with open(active_contact_item.get_path(), "w") as file:
                file.write(new_text_str)
            kammanta.model.contacts_dir.get_active_item().set_text_contents(new_text_str)
            # -the user can enter both plain text or html. The widget will guess based on the contents
            self.contact_qte.setMarkdown(new_text_str)
            # -this is the only update we need to do here

    def on_contact_list_item_changed(self, i_new: QtWidgets.QListWidgetItem, i_prev: QtWidgets.QListWidgetItem):
        if i_new is None:
            return
        id_str = i_new.data(QtCore.Qt.UserRole)

        active_contact = kammanta.model.contacts_dir.get_item(id_str)
        if active_contact is not None:
            self.title_qll.setText(f"Contacts [{active_contact.get_core_name()}]")

        kammanta.model.contacts_dir.set_active_item(id_str)
        content_str = kammanta.model.contacts_dir.get_active_item().get_text_contents()
        self.contact_qte.setMarkdown(content_str)

        # self.update_gui()

    def on_contact_rename_clicked(self):
        old_line_str = kammanta.model.contacts_dir.get_active_item().get_core_name()
        (new_line_str, ok_bool) = QtWidgets.QInputDialog.getText(
            self, "Renaming Contact", "Label---", text=old_line_str
        )
        if ok_bool:
            kammanta.model.contacts_dir.get_active_item().set_core_name(new_line_str)
            kammanta.model.contacts_dir.set_active_item("")
            self.update_gui()

    def update_gui(self):
        self.updating_gui_bool = True

        active_item = kammanta.model.contacts_dir.get_active_item()

        if active_item is not None:
            show_create_text_str = "create agenda"
            for agenda_item in kammanta.model.agenda_files.get_all_items():
                if active_item.get_name() == agenda_item.get_name():
                    show_create_text_str = "show agenda"
                    break
            self.show_create_agenda_qpb.setText(show_create_text_str)

            fav_is_checked_bool = active_item.is_favorite()
            self.fav_contact_qcb.setChecked(fav_is_checked_bool)

        all_agenda_names_list = [item.get_core_name() for item in kammanta.model.agenda_files.get_all_items()]
        self.contacts_qlw.clear()
        for contact in kammanta.model.contacts_dir.get_all_items(i_sort_by_name=True):
            # lwi = QtWidgets.QListWidgetItem()
            # self.contacts_qlw.setItemWidget()

            contact_name_str = contact.get_core_name()
            search_text_str = self.search_qle.text()
            if search_text_str == "" or contact_name_str.lower().startswith(search_text_str.lower()):
                entry_str = contact_name_str
                if entry_str in all_agenda_names_list:
                    entry_str = entry_str + " (A)"
                if contact.is_favorite():
                    entry_str = "(*) " + entry_str
                qlwi = QtWidgets.QListWidgetItem(entry_str)
                """
                if entry_str in all_agenda_names_list:
                    new_font = QtGui.QFont()
                    new_font.setUnderline(True)
                    qlwi.setFont(new_font)
                """
                qlwi.setData(QtCore.Qt.UserRole, contact.get_id())
                self.contacts_qlw.addItem(qlwi)
                # self.contacts_qlw.addItem(entry_str)

        self.updating_gui_bool = False

    # def update_gui_contact_info(self):
