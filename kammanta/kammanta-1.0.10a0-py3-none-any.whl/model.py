import os
import shutil
import re
import logging
import fileinput
import pathlib
import datetime
import abc
import typing
import distutils.dir_util
from string import Template
import kammanta.glob
import kammanta.widgets.path_sel_dlg

NA_DEFAULT_SUPPORT_DIR = "na_support"
PROJECTS_PERSONAL_STR = "projects-personal"
PROJECTS_PROFESSIONAL_STR = "projects-professional"

FOCUS_DIRECTION_DIR_NAME_STR = "focus-direction"
AOI_FILE_NAME_STR = "areas-of-interest-and-accountability.txt"
GO_FILE_NAME_STR = "goals-and-objectives.txt"
VISION_FILE_NAME_STR = "vision.txt"
PP_FILE_NAME_STR = "purpose-and-principles.txt"

AOI_STR = "Areas of Interest"
GO_STR = "Goals and Objectives"
VISION_STR = "Vision"
PP_STR = "Purpose and Principles"
TICKLER_TITLE_STR = "Tickler"
NEXT_ACTIONS_TITLE_STR = "Next Actions"
AGENDAS_TITLE_STR = "Agendas"
PROJECTS_TITLE_STR = "Projects"
INBOX_TITLE_STR = "Inbox"
CONTACTS_TITLE_STR = "Contacts"


def matches_dirs_desk(i_path: str) -> bool:
    is_desktop_file_bool = i_path.endswith(".desktop") and os.path.isfile(i_path)
    is_dir = os.path.isdir(i_path)
    if is_desktop_file_bool or is_dir:
        return True
    return False


def matches_txt_files(i_path: str) -> bool:
    is_txt_file_bool = i_path.endswith(".txt") and os.path.isfile(i_path)
    if is_txt_file_bool:
        return True
    return False


def matches_project_collection_dirs(i_path: str) -> bool:
    basename_str = os.path.basename(i_path)
    is_project_collection_dir = basename_str.lower().startswith("projects") and os.path.isdir(i_path)
    is_someday_maybe_dir = basename_str.lower() == kammanta.glob.SOMEDAY_MAYBE_STR
    if is_project_collection_dir or is_someday_maybe_dir:
        return True
    return False


def matches_all(i_path_unused: str) -> bool:
    return True


class SharedEntity(abc.ABC):
    # Abstract class, overridden
    # TBD: Finding a better name for this which captures Files+Dirs+Lines (but excludes and cmds, web links)
    def __init__(self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path_strlist: [str]):
        # self.main_title_str = i_title
        self.collection_type = i_collection_type
        self.rel_path_strlist: [str] = i_rel_path_strlist
        # -this list holds the the path relative to the main gtd dir.
        #  Each part of the path is one element in the list

    def get_collection_type(self) -> kammanta.glob.CollTypeEnum:
        return self.collection_type

    def get_main_title(self) -> str:
        return self.collection_type.get_name()

    def get_path(self) -> str:
        path_str = kammanta.glob.create_and_get_path(*self.rel_path_strlist)
        # -is it better to just give the path here, and not create it?
        return path_str

    @abc.abstractmethod
    def get_type(self) -> kammanta.glob.TypeEnum:
        pass

    @abc.abstractmethod
    def get_id(self) -> str:
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        # For files and dirs this is the "basename", and for lines this is the contents of the line
        pass

    @abc.abstractmethod
    def set_name(self, i_new_name: str) -> None:
        pass

    @abc.abstractmethod
    def get_core_name(self) -> str:
        pass

    @abc.abstractmethod
    def set_completed(self, i_new_status: bool) -> None:
        pass

    # set_core_name here?

    # get and set support path here?

    # get and set completed here?


class LineInFile(SharedEntity):
    # Concrete class, not overridden
    def __init__(self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path: [str], i_row_nr: int):
        super().__init__(i_collection_type, i_rel_path)
        self.file_row_nr_int = i_row_nr
        # -This works as the ID (we don't need the context to be a part since only one context is shown at a time)

    def get_type(self) -> kammanta.glob.TypeEnum:
        return kammanta.glob.TypeEnum.line

    def get_id(self) -> str:
        return str(self.file_row_nr_int)

    def get_name(self) -> str:
        text_file_name_str = self.get_path()
        alt_count_int = 0
        with open(text_file_name_str, "r") as file:
            for (count_int, line_str) in enumerate(file):
                if count_int == self.file_row_nr_int:
                    line_formatted_str = line_str.strip()
                    return line_formatted_str
                alt_count_int += 1
        raise Exception("Line "+str(alt_count_int)+" not found!")

    def set_name(self, i_new_line: str) -> None:
        text_file_name_str = self.get_path()
        count_int = 0
        for line_str in fileinput.FileInput(text_file_name_str, inplace=True):
            if count_int == self.file_row_nr_int:
                # If we are at the specified line: Replace with new contents
                print(i_new_line.strip())
            else:
                # ..otherwise using old contents
                formatted_line_str = line_str.strip()
                if formatted_line_str:
                    print(formatted_line_str)
            count_int += 1

    def get_core_name(self):
        core_name_str = kammanta.glob.remove_delimiter_and_after(self.get_name(), kammanta.glob.SUPPORT_DELIMITER_STR)
        core_name_str = kammanta.glob.remove_prefix(core_name_str, kammanta.glob.COMPL_PREF_STR)
        return core_name_str

    def set_core_name(self, i_new_display_name: str) -> None:
        is_completed_str = ""
        if self.is_completed():
            is_completed_str = kammanta.glob.COMPL_PREF_STR
        support_str = ""
        support_path_str = self.get_support_path()
        if support_path_str:
            support_str = kammanta.glob.SUPPORT_DELIMITER_STR + support_path_str

        entire_line_str = is_completed_str + i_new_display_name + support_str
        self.set_name(entire_line_str)

    def get_support_path(self) -> str:
        entire_line_str = self.get_name()
        line_parts_list = entire_line_str.split(kammanta.glob.SUPPORT_DELIMITER_STR)
        if len(line_parts_list) > 1:
            psm_path_str = line_parts_list[-1]  # -getting the last element
            return psm_path_str
        else:
            return ""

    def set_support_path(self, i_new_support_path: str) -> None:
        entire_line_str = self.get_name()
        delimeter_and_after_removed_str = kammanta.glob.remove_delimiter_and_after(
            entire_line_str, kammanta.glob.SUPPORT_DELIMITER_STR
        )
        new_line = delimeter_and_after_removed_str + kammanta.glob.SUPPORT_DELIMITER_STR + i_new_support_path.strip()
        self.set_name(new_line)

    def is_completed(self) -> bool:
        if self.get_name().startswith(kammanta.glob.COMPL_PREF_STR):
            return True
        return False

    def set_completed(self, i_new_status: bool) -> None:
        if i_new_status == self.is_completed():
            return
        prev_line_str = self.get_name()
        new_line_str = ""
        if not self.is_completed() and i_new_status:
            new_line_str = kammanta.glob.COMPL_PREF_STR + prev_line_str
        elif self.is_completed() and not i_new_status:
            new_line_str = kammanta.glob.remove_prefix(prev_line_str, kammanta.glob.COMPL_PREF_STR)
        if new_line_str:
            self.set_name(new_line_str)
        else:
            logging.warning("set_completed --- new status already matches old status")


class DirOrFile(SharedEntity):
    # Abstract class, overridden
    def __init__(self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path: [str]):
        super().__init__(i_collection_type, i_rel_path)

        """
        Strange: When adding the path here it makes it so that we don't get a signal from the FSW
        This despite that we have another place where we add the same path
        
        fsw_ref = kammanta.glob.FswSingleton.get()
        path_str = self.get_path()
        fsw_ref.addPath(path_str)
        """

    @abc.abstractmethod
    def set_active_item(self, i_id: str) -> None:
        pass

    @abc.abstractmethod
    def get_item(self, i_id: str):
        pass

    @abc.abstractmethod
    def delete_item(self, i_id: str) -> None:
        pass

    @abc.abstractmethod
    def get_nr_of_files(self) -> int:
        pass
        # Moving this to the Directory class?

    def get_id(self) -> str:
        return self.get_name()

    def get_core_name(self):
        core_name_str = kammanta.glob.remove_any_dot_suffix(self.get_name())
        core_name_str = kammanta.glob.remove_prefix(core_name_str, kammanta.glob.COMPL_PREF_STR)
        core_name_str = kammanta.glob.remove_prefix(core_name_str, kammanta.glob.FAV_PREF_STR)
        core_name_str = core_name_str.replace("_", " ")
        return core_name_str

    def set_core_name(self, i_new_display_name: str) -> None:
        is_completed_str = ""
        if self.is_completed():
            is_completed_str = kammanta.glob.COMPL_PREF_STR
        split_str_list = self.get_name().split(".")
        suffix_str = ""
        if len(split_str_list) > 1:
            suffix_str = "." + split_str_list[-1]
        entire_line_str = is_completed_str + i_new_display_name + suffix_str
        self.set_name(entire_line_str)

    def get_name(self) -> str:
        base_name_str = os.path.basename(self.get_path())
        return base_name_str

    def set_name(self, i_new_name: str):
        root_path_str = os.path.dirname(self.get_path())
        new_path_str = os.path.join(root_path_str, i_new_name)
        os.rename(self.get_path(), new_path_str)
        self.rel_path_strlist[-1] = i_new_name
        ######time.sleep(0.5)

    def set_completed(self, i_new_status: bool) -> None:
        if i_new_status == self.is_completed():
            return
        prev_name_str = self.get_name()
        if i_new_status:
            new_fod_name_str = kammanta.glob.COMPL_PREF_STR + prev_name_str
        else:
            new_fod_name_str = kammanta.glob.remove_prefix(prev_name_str, kammanta.glob.COMPL_PREF_STR)
        self.set_name(new_fod_name_str)

    def is_completed(self) -> bool:
        if self.get_name().startswith(kammanta.glob.COMPL_PREF_STR):
            # .lower()
            return True
        return False

    def get_last_edit_time(self) -> int:
        path_str = self.get_path()
        (_, mtime_secs_int) = kammanta.glob.get_nr_items_and_last_mod_time(path_str)
        # mtime_secs_int = int(os.path.getmtime(path_str))
        return mtime_secs_int

    def has_reminder_time(self) -> bool:
        if self.get_reminder_time() is not None:
            return True
        else:
            return False

    def get_reminder_time(self) -> typing.Optional[datetime.datetime]:
        name_str = self.get_name()
        name_split_list = name_str.split("_")
        datetime_str = name_split_list[0]
        try:
            ret_dt = datetime.datetime.strptime(datetime_str, kammanta.glob.PY_DATETIME_FILENAME_FORMAT_STR)
        except ValueError:
            try:
                ret_dt = datetime.datetime.strptime(datetime_str, kammanta.glob.PY_DATE_FILENAME_FORMAT_STR)
            except ValueError:
                return None
        # timestamp, for time of day+date
        return ret_dt

    def set_reminder_time(self, i_new_reminder_time: datetime.datetime) -> None:
        new_name_str = self.get_name()
        new_name_str = kammanta.glob.remove_datetime_prefix(new_name_str)
        if self.get_reminder_time() is not None:
            new_name_list = new_name_str.split("_")
            new_name_str = "_".join(new_name_list[1:])
        datetime_str = i_new_reminder_time.strftime(kammanta.glob.PY_DATETIME_FILENAME_FORMAT_STR)
        new_name_str = datetime_str + new_name_str
        self.set_name(new_name_str)


class Directory(DirOrFile):
    # Concrete class, not overridden
    def __init__(
            self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path: [str],
            i_matching_func_first: typing.Callable[[str], bool],
            i_matching_func_second: typing.Optional[typing.Callable[[str], bool]]):
        super().__init__(i_collection_type, i_rel_path)
        self.active_fd_obj = None
        self.matching_func_first = i_matching_func_first
        self.matching_func_second = i_matching_func_second

    # overridden
    def get_type(self) -> kammanta.glob.TypeEnum:
        return kammanta.glob.TypeEnum.dir

    def get_nr_of_files(self) -> int:
        support_path_str = self.get_support_path()
        dir_strlist = os.listdir(support_path_str)
        return len(dir_strlist)

    def move_active_granditem(self, i_dest_coll_id: str):
        source_coll = self.get_active_item()
        source_item = source_coll.get_active_item()

        source_coll.set_active_item("")

        dest_coll = self.get_item(i_dest_coll_id)

        if source_item.get_type() == kammanta.glob.TypeEnum.line:
            move_item_line_str = source_item.get_name()
            move_item_id_str = source_item.get_id()
            source_coll.delete_item(move_item_id_str)
            dest_coll.add_new_item(move_item_line_str)
        else:
            kammanta.glob.move_fd(source_item.get_path(), dest_coll.get_path())

    def clear_completed(self) -> None:
        for fd_item in self.get_all_items():
            if fd_item.is_completed():
                self.delete_item(fd_item.get_id())
                # fd_item.delete()

    def set_support_path(self, i_support_path: str):
        raise Exception("Unsupported operation for Directories")
        """
        if i_support_path == "":
            # -the file or dir itself, rather than a desktop file
            pass
        else:
            # desktop file
            pass
        """

    def get_support_path(self) -> str:
        return self.get_path()

    def delete_item(self, i_id: str) -> None:
        self.set_active_item("")
        # remove_fd(self.get_path())
        to_remove_obj = self.get_item(i_id)
        kammanta.glob.remove_fd(to_remove_obj.get_path())
        # Please note that we do not want to remove the support path for .desktop files, since this might be risky!!!

    def get_item(self, i_name: str):
        fd_obj = None
        fd_path_str = kammanta.glob.get_path(self.get_path(), i_name)
        if self.matching_func_first(fd_path_str):
            if os.path.isdir(fd_path_str):
                path_list = self.rel_path_strlist + [i_name]
                fd_obj = Directory(self.collection_type, path_list, self.matching_func_second, None)
            elif os.path.isfile(fd_path_str):
                class_type = File
                fd_type_enum = kammanta.glob.get_type(fd_path_str)
                if fd_type_enum == kammanta.glob.TypeEnum.note_file:
                    class_type = NoteFile
                elif fd_type_enum == kammanta.glob.TypeEnum.text_file:
                    class_type = TextFile
                elif fd_type_enum == kammanta.glob.TypeEnum.image_file:
                    class_type = ImageFile
                elif fd_type_enum == kammanta.glob.TypeEnum.desktop_file:
                    class_type = DesktopFile
                else:
                    pass
                path_list = self.rel_path_strlist + [i_name]
                fd_obj = class_type(self.collection_type, path_list)
        return fd_obj

    def get_all_items(self, i_sort_by_name: bool = True):
        if self.matching_func_first is None:
            raise Exception("Operation not allowed")
        # -> [File]
        dir_content_list = os.listdir(self.get_path())
        fd_obj_list = []
        for fd_name_str in dir_content_list:
            fd_path_str = kammanta.glob.get_path(self.get_path(), fd_name_str)
            if self.matching_func_first(fd_path_str):
                if os.path.isdir(fd_path_str):
                    new_list = self.rel_path_strlist + [fd_name_str]
                    fd_obj = Directory(self.collection_type, new_list, self.matching_func_second, None)
                    fd_obj_list.append(fd_obj)
                elif os.path.isfile(fd_path_str):
                    class_type = File
                    fd_type_enum = kammanta.glob.get_type(fd_path_str)
                    if fd_type_enum == kammanta.glob.TypeEnum.note_file:
                        class_type = NoteFile
                    elif fd_type_enum == kammanta.glob.TypeEnum.text_file:
                        class_type = TextFile
                    elif fd_type_enum == kammanta.glob.TypeEnum.image_file:
                        class_type = ImageFile
                    elif fd_type_enum == kammanta.glob.TypeEnum.desktop_file:
                        class_type = DesktopFile
                    else:
                        pass
                    new_list = self.rel_path_strlist + [fd_name_str]
                    fd_obj = class_type(self.collection_type, new_list)
                    fd_obj_list.append(fd_obj)



                kammanta.glob.FswSingleton.get().addPath(fd_path_str)




        if i_sort_by_name:
            fd_obj_list = sorted(
                fd_obj_list,
                key=lambda file_obj: file_obj.get_name().lower(),
                reverse=False
            )
            # -this will put the completed items last. Otherwise we can use get_core_name()
        else:
            fd_obj_list = sorted(
                fd_obj_list,
                key=lambda file_obj: file_obj.get_last_edit_time(),
                reverse=False
            )
        return fd_obj_list

    def get_active_item(self):
        return self.active_fd_obj

    def set_active_item(self, i_active_dir_id: str) -> None:
        if not i_active_dir_id:
            self.active_fd_obj = None
            return
        self.active_fd_obj = self.get_item(i_active_dir_id)

    def add_new_item(self, i_name: str):
        # , i_type: kammanta.glob.TypeEnum
        name_formatted_str = i_name.strip()
        new_path_str = os.path.join(self.get_path(), name_formatted_str)
        # -can be a file or a directory

        """
        if i_type == kammanta.glob.TypeEnum.dir:
        elif i_type == kammanta.glob.TypeEnum.desktop_file:
        elif i_type in kammanta.glob.any_file_enumlist:
            kammanta.glob.create_and_get_path(new_path_str)
        """

        kammanta.glob.create_and_get_path(new_path_str)
        if os.path.isfile(new_path_str) and new_path_str.endswith(".desktop"):
            (path_str, result_enum) = kammanta.widgets.path_sel_dlg.PathSelDlg.open_dlg_and_get_path(
                kammanta.widgets.path_sel_dlg.PathSelectionEnum.dir, "", ""
            )
            if result_enum != kammanta.widgets.path_sel_dlg.PathSelectionEnum.cancelled:
                new_rel_path_strlist = self.rel_path_strlist + [name_formatted_str]
                new_file_obj = kammanta.model.DesktopFile(self.collection_type, new_rel_path_strlist)
                new_file_obj.update_desktop_file(path_str)
        new_obj = self.get_item(name_formatted_str)
        return new_obj

    def add_new_note(self, i_text_to_add: str):
        base_file_name_str = "note_" + datetime.datetime.now().strftime(kammanta.glob.DATE_FILENAME_FORMAT_STR)

        counter_int = 1
        file_name_str = base_file_name_str + "_" + str(counter_int) + ".txt"
        file_path_str = kammanta.glob.get_path(self.get_path(), file_name_str)
        while os.path.exists(file_path_str) and counter_int < 1000:
            counter_int += 1
            file_name_str = base_file_name_str + "_" + str(counter_int) + ".txt"
            file_path_str = kammanta.glob.get_path(kammanta.glob.INBOX_DIR_STR, file_name_str)
        with open(file_path_str, "w+") as file:
            #     check_and_create_path
            file.write(i_text_to_add)

    def _create_empty_text_file_from_old_path(self, i_id: str):
        """
        This method is used when we are converting dirs to files, where there are no files in directories
        :param i_id:
        :return:
        """
        # i_old_path: str,
        item_to_convert = self.get_item(i_id)
        old_path_str = item_to_convert.get_path()
        new_text_file_path_str = kammanta.glob.remove_any_dot_suffix(old_path_str) + ".txt"
        with open(new_text_file_path_str, "x") as f:
            pass
        self.delete_item(i_id)

    def _move_single_file_from_old_path(self, i_id: str, i_dest_file_path: str):
        item_to_convert = self.get_item(i_id)
        # old_path_str = item_to_convert.get_path()
        old_support_path_str = item_to_convert.get_support_path()
        single_file_path_str = ""
        if os.path.isfile(old_support_path_str):
            single_file_path_str = old_support_path_str
        elif os.path.isdir(old_support_path_str):
            all_support_files_list = os.listdir(old_support_path_str)
            single_file_name_str = all_support_files_list[0]
            single_file_path_str = os.path.join(old_support_path_str, single_file_name_str)
        else:
            raise Exception("file system entity is neither file nor directory")
        suffix_str = kammanta.glob.get_dsuffix(single_file_path_str)
        if not suffix_str:
            if kammanta.glob.is_text(single_file_path_str):
                pass
            else:
                suffix_str = "txt"
        if not suffix_str:
            suffix_str = "." + suffix_str
        dest_file_path_str = kammanta.glob.remove_any_dot_suffix(i_dest_file_path) + "." + suffix_str
        shutil.move(single_file_path_str, dest_file_path_str)
        self.delete_item(i_id)

    # Refactoring done and tested!
    def convert_item_to_file(self, i_id: str) -> bool:
        """
        :returns the success of the operation
        """
        item_to_convert = self.get_item(i_id)
        old_path_str = item_to_convert.get_path()
        dest_dir_path_str = os.path.dirname(old_path_str)
        dest_file_name_str = os.path.basename(item_to_convert.get_path())
        dest_file_path_str = os.path.join(dest_dir_path_str, dest_file_name_str)
        item_type_enum = item_to_convert.get_type()
        if item_type_enum == kammanta.glob.TypeEnum.dir:
            all_support_files_list = os.listdir(old_path_str)
            nr_of_support_files_int = len(all_support_files_list)
            if nr_of_support_files_int == 0:
                self._create_empty_text_file_from_old_path(i_id)
                return True
            elif nr_of_support_files_int == 1:
                self._move_single_file_from_old_path(i_id, dest_file_path_str)
                return True
            else:
                # Conversion not possible
                pass
        elif item_type_enum == kammanta.glob.TypeEnum.desktop_file:
            old_support_path_str = item_to_convert.get_support_path()
            old_support_type_enum = kammanta.glob.get_type(old_support_path_str)
            if old_support_type_enum == kammanta.glob.TypeEnum.dir:
                all_support_files_list = os.listdir(old_support_path_str)
                nr_of_support_files_int = len(all_support_files_list)
                # Moving all the files
                if nr_of_support_files_int == 0:
                    self._create_empty_text_file_from_old_path(i_id)
                    return True
                elif nr_of_support_files_int == 1:
                    self._move_single_file_from_old_path(i_id, dest_file_path_str)
                    return True
                else:
                    # raise Exception("More than one file present in support directory")
                    return False
            elif old_support_type_enum in kammanta.glob.any_file_enumlist:
                self._move_single_file_from_old_path(i_id, dest_file_path_str)
                return True
            else:
                pass
                # raise Exception("Should not be possible to get here: support type must be either file or dir")
        return False
        # raise Exception("Should not be possible to get here")

    def _create_desktop_file(self, i_id: str, i_new_support_dest_dir_path: str):
        item_to_convert = self.get_item(i_id)
        old_path_str = item_to_convert.get_path()
        old_name_str = item_to_convert.get_name()
        new_df_name_str = os.path.basename(old_path_str)
        new_support_dest_path_str = os.path.join(i_new_support_dest_dir_path, new_df_name_str)

        link_file_name_str = old_name_str.lower()
        link_file_name_str = link_file_name_str.replace(" ", "_")
        link_file_name_str = kammanta.glob.remove_any_dot_suffix(link_file_name_str) + ".desktop"
        link_path_str = os.path.join(pathlib.Path(old_path_str).parent.absolute(), link_file_name_str)

        # Creating the link (.desktop) file
        template_file_path_str = "gtd/link_template.desktop"
        with open(template_file_path_str, "r") as file:
            template = Template(file.read())
            shortcut_text_str = template.substitute(
                name_str=old_name_str + " (shortcut to " + new_df_name_str + ")",
                url_str=new_support_dest_path_str
            )
        with open(link_path_str, "w+") as file:
            file.write(shortcut_text_str)

        """
        
            # Creating the link (.desktop) file
            template_file_path_str = "gtd/link_template.desktop"
            with open(template_file_path_str, "r") as file:
                template = Template(file.read())
                shortcut_text_str = template.substitute(
                    name_str=self.get_name() + " (shortcut to " + old_name_str + ")",
                    url_str=new_support_dest_path_str)
            with open(link_path_str, "w+") as file:
                file.write(shortcut_text_str)
            time.sleep(1)
        """

    # Refactored and tested!
    def convert_item_to_link(self, i_id: str, i_new_support_dest_dir_path: str) -> bool:
        """
        :returns the success of the operation
        """
        item_to_convert = self.get_item(i_id)
        old_path_str = item_to_convert.get_path()
        old_name_str = item_to_convert.get_name()
        new_df_name_str = os.path.basename(old_path_str)
        new_support_dest_path_str = os.path.join(i_new_support_dest_dir_path, new_df_name_str)

        item_type_enum = item_to_convert.get_type()
        if item_type_enum == kammanta.glob.TypeEnum.dir:
            # Moving the files
            # gtd.glob.copy_fd(old_path_str, i_new_support_dest_dir_path)
            # distutils.dir_util.copy_tree(old_path_str, i_new_support_dest_dir_path)
            shutil.copytree(old_path_str, new_support_dest_path_str)

            self._create_desktop_file(i_id, i_new_support_dest_dir_path)
            self.delete_item(i_id)

            return True
        elif item_type_enum == kammanta.glob.TypeEnum.desktop_file:
            return False
        elif item_type_enum in kammanta.glob.any_file_enumlist:
            """
            i_new_dest_file_path - the new destination for the support file
            :returns the success of the operation
            # we need to let the user decide the place of the dir or file that she wants to use as the destination
            """
            # old_file_name_str = os.path.basename(old_path_str)
            # new_support_dest_path_str = os.path.join(i_new_support_dest_path, old_file_name_str)
            # gtd.glob.move_fd(old_path_str, i_new_support_dest_path)

            # Moving the files
            # gtd.glob.copy_fd(old_path_str, i_new_support_dest_dir_path)
            shutil.copy(old_path_str, new_support_dest_path_str)

            self._create_desktop_file(i_id, i_new_support_dest_dir_path)
            self.delete_item(i_id)

            return True
        return False

    # Done and tested!
    def convert_item_to_dir(self, i_id: str) -> bool:
        """
        Two cases:
        * The file to be converted is a .desktop file, this is handled in an override of this method
        * or the file is another file (ex: txt or img), this is handled here

        :returns the success of the operation
        """

        item_to_convert = self.get_item(i_id)
        old_path_file_str = item_to_convert.get_path()
        old_file_name_str = item_to_convert.get_name()
        old_support_path_str = item_to_convert.get_support_path()
        old_support_file_name_str = os.path.basename(item_to_convert.get_support_path())
        old_support_type_enum = kammanta.glob.get_type(old_support_path_str)

        # Creating the new directory
        new_path_dir_str = kammanta.glob.remove_any_dot_suffix(old_path_file_str)
        os.mkdir(new_path_dir_str)

        # Moving file(s)

        item_type_enum = item_to_convert.get_type()
        if item_type_enum == kammanta.glob.TypeEnum.desktop_file:
            if old_support_type_enum == kammanta.glob.TypeEnum.dir:
                to_move_file_name_strlist = os.listdir(old_support_path_str)
                for fn_str in to_move_file_name_strlist:
                    fp_str = os.path.join(old_support_path_str, fn_str)
                    shutil.move(fp_str, new_path_dir_str)
                self.delete_item(i_id)
                return True
            elif old_support_type_enum in kammanta.glob.any_file_enumlist:
                new_path_with_file_str = os.path.join(new_path_dir_str, old_support_file_name_str)
                shutil.move(old_support_path_str, new_path_with_file_str)
                self.delete_item(i_id)
                return True
            else:
                return False
        elif item_type_enum in kammanta.glob.any_file_enumlist:
            shutil.copy(old_support_path_str, new_path_dir_str)
            self.delete_item(i_id)
            return True
        return False


class File(DirOrFile):
    # Concrete class, overridden

    def __init__(self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path: [str]):
        super().__init__(i_collection_type, i_rel_path)
        self.active_row_obj = None

    # overridden
    def get_type(self) -> kammanta.glob.TypeEnum:
        return kammanta.glob.TypeEnum.file

    def get_nr_of_files(self) -> int:
        path_str = self.get_path()
        if path_str.endswith(".desktop"):
            support_path_str = self.get_support_path()
            if kammanta.glob.get_type(support_path_str) == kammanta.glob.TypeEnum.dir:
                dir_strlist = os.listdir(support_path_str)
                return len(dir_strlist)
            elif kammanta.glob.get_type(support_path_str) == kammanta.glob.TypeEnum.file:
                return 1
            elif kammanta.glob.get_type(support_path_str) in (
                    kammanta.glob.TypeEnum.web_link, kammanta.glob.TypeEnum.command
            ):
                return 0
        else:
            return 1

    # overridden/extended
    def set_name(self, i_new_name: str):
        super().set_name(i_new_name)

    def update_desktop_file(self, i_support_path: str=None):
        assert(self.get_type() == kammanta.glob.TypeEnum.desktop_file)
        if i_support_path is None:
            support_path_str = self.get_support_path()
        else:
            support_path_str = i_support_path
        if kammanta.glob.get_type(support_path_str) == kammanta.glob.TypeEnum.command:
            template_file_path_str = "kammanta/cmd_template.desktop"
            with open(template_file_path_str, "r") as file:
                template = Template(file.read())
                shortcut_text_str = template.substitute(
                    name_str=self.get_name() + " (Custom command: " + support_path_str + ")",
                    cmd_str=support_path_str
                )
            this_path_str = self.get_path()
            with open(this_path_str, "w") as file:
                file.write(shortcut_text_str)
        else:
            template_file_path_str = "kammanta/link_template.desktop"
            with open(template_file_path_str, "r") as file:
                template = Template(file.read())
                shortcut_text_str = template.substitute(
                    name_str=self.get_name() + " (shortcut to " + os.path.basename(support_path_str) + ")",
                    url_str=support_path_str
                )
            this_path_str = self.get_path()
            with open(this_path_str, "w") as file:
                file.write(shortcut_text_str)

    def set_support_path(self, i_support_path: str):
        if self.get_type() == kammanta.glob.TypeEnum.desktop_file:
            self.update_desktop_file(i_support_path)
            # -please note that we are not using get_path() since that will use the path stored in the .ini file
        elif self.get_type == kammanta.glob.TypeEnum.text_file:
            pass
        else:
            pass

    def get_support_path(self) -> str:
        path_str = self.get_path()
        return path_str

    def get_item(self, i_row_id: str) -> LineInFile:
        for row_obj in self.get_all_items():
            if row_obj.file_row_nr_int == int(i_row_id):
                return row_obj
        logging.warning(f"No next action with {i_row_id=} was found")

    def get_active_item(self):
        return self.active_row_obj

    def delete_item(self, i_id: str) -> None:
        self.set_active_item("")
        path_str = self.get_path()
        with open(path_str, "r+") as file:
            line_list = file.readlines()
            file.seek(0)
            for (line_number_int, line_str) in enumerate(line_list):
                if line_number_int != int(i_id):
                    file.write(line_str)
            file.truncate()

    def set_active_item(self, i_id: str) -> None:
        if not i_id:
            self.active_row_obj = None
            return
        self.active_row_obj = LineInFile(self.collection_type, self.rel_path_strlist, int(i_id))

    def add_new_item(self, i_name: str) -> LineInFile:
        self.clear_all_empty_lines()

        name_formatted_str = i_name.strip()

        with open(self.get_path(), "r+") as file:
            # file.write(name_formatted_str + "\n")
            contents_str = file.read()
            offset_int = 0
            end_of_file_int = 2
            file.seek(offset_int, end_of_file_int)
            if contents_str.endswith('\n'):
                file.write(name_formatted_str + "\n")
            else:
                file.write("\n" + name_formatted_str + "\n")
        new_line_nr_int = len(self.get_all_items()) - 1
        # - -1 is needed since we start at 0
        new_obj = self.get_item(str(new_line_nr_int))
        return new_obj

    def clear_all_empty_lines(self):
        text_file_path_str = self.get_path()
        with open(text_file_path_str, "r+") as file:
            # Approaches for removing blank lines:
            # https://codereview.stackexchange.com/questions/145126/open-a-text-file-and-remove-any-blank-lines
            # for (all_rows_count_int, line_str) in enumerate(file):
            nonempty_line_strlist = []
            for line_str in file:
                if line_str.strip():
                    nonempty_line_strlist.append(line_str)
            file.seek(0)
            file.writelines(nonempty_line_strlist)
            file.truncate()

    def get_all_items(self) -> [LineInFile]:
        row_obj_list = []
        text_file_path_str = self.get_path()
        with open(text_file_path_str, "r") as file:
            row_ctr_int = 0
            for line_str in file:
                if line_str.strip():
                    # -only including the non-empty lines
                    row_obj = LineInFile(self.collection_type, self.rel_path_strlist, row_ctr_int)
                    row_obj_list.append(row_obj)
                row_ctr_int += 1
        return row_obj_list

    def clear_completed(self):
        na_context_file_path_str = self.get_path()
        with open(na_context_file_path_str, "r+") as file:
            line_list = file.readlines()
            file.seek(0)
            for (line_number_int, line_str) in enumerate(line_list):
                if not line_str.startswith(kammanta.glob.COMPL_PREF_STR):
                    file.write(line_str)
            file.truncate()
        """
        for na in get_all_next_actions_for_context(i_context):
            if na.is_completed():
                na.delete()
        """


class ImageFile(File):
    # Concrete class, not overridden.
    def __init__(self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path: [str]):
        super().__init__(i_collection_type, i_rel_path)

    # overridden
    def get_type(self) -> kammanta.glob.TypeEnum:
        return kammanta.glob.TypeEnum.image_file


class DesktopFile(File):
    # Concrete class, not overridden
    # A desktop file isn't considered a text file within our model (even though it consists of text).
    # In the future we want compatability with windows, and then this may be another type of link file,
    # (still though it's possible to use .desktop files for windows inside of the applications since we just read
    # the text contents, the only issue is that we cannot use the desktop file independently of the application)
    def __init__(self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path: [str]):
        super().__init__(i_collection_type, i_rel_path)

    # overridden
    def get_type(self) -> kammanta.glob.TypeEnum:
        return kammanta.glob.TypeEnum.desktop_file

    # overridden/extended
    def set_name(self, i_new_name: str):
        super().set_name(i_new_name)
        self.update_desktop_file()

    # def get_text_contents(self) -> str:

    def get_support_path(self) -> str:
        support_path_str = ""
        path_str = self.get_path()
        with open(path_str, "r") as file:
            contents_str = file.read()
            re_search_result = re.search(r'URL=(.*)\n', contents_str)
            if re_search_result is not None:
                support_path_str = re_search_result.group(1)
        return support_path_str


class TextFile(File):
    # Concrete class, overridden
    def __init__(self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path: [str]):
        super().__init__(i_collection_type, i_rel_path)

    # overridden
    def get_type(self) -> kammanta.glob.TypeEnum:
        return kammanta.glob.TypeEnum.text_file

    def get_text_contents(self) -> str:
        text_file_path_str = self.get_path()
        with open(text_file_path_str, "r") as file:
            file_contents_str = file.read()
            return file_contents_str

    def set_text_contents(self, i_new_text: str):
        with open(self.get_path(), "w") as file:
            file.write(i_new_text)
            file.truncate()

    def is_favorite(self) -> bool:
        if self.get_name().startswith(kammanta.glob.FAV_PREF_STR):
            return True
        return False

    def set_favorite(self, i_new_status: bool) -> None:
        # -used for contacts
        old_name_str = self.get_name()
        if not self.is_favorite() and i_new_status:
            new_name_str = kammanta.glob.FAV_PREF_STR + old_name_str
            self.set_name(new_name_str)
        elif self.is_favorite() and not i_new_status:
            new_name_str = kammanta.glob.remove_prefix(old_name_str, kammanta.glob.FAV_PREF_STR)
            self.set_name(new_name_str)


class NoteFile(TextFile):
    # Concrete class, not overridden
    def __init__(self, i_collection_type: kammanta.glob.CollTypeEnum, i_rel_path: [str]):
        super().__init__(i_collection_type, i_rel_path)

    # overridden
    def get_type(self) -> kammanta.glob.TypeEnum:
        return kammanta.glob.TypeEnum.note_file


aoi_obj = TextFile(
    kammanta.glob.CollTypeEnum.areas_of_interest,
    [FOCUS_DIRECTION_DIR_NAME_STR, AOI_FILE_NAME_STR]
)
go_obj = TextFile(
    kammanta.glob.CollTypeEnum.goals_and_objectives,
    [FOCUS_DIRECTION_DIR_NAME_STR, GO_FILE_NAME_STR]
)
vision_obj = TextFile(
    kammanta.glob.CollTypeEnum.vision,
    [FOCUS_DIRECTION_DIR_NAME_STR, VISION_FILE_NAME_STR]
)
pp_obj = TextFile(
    kammanta.glob.CollTypeEnum.purpose_and_principles,
    [FOCUS_DIRECTION_DIR_NAME_STR, PP_FILE_NAME_STR]
)

inbox_dir = Directory(
    kammanta.glob.CollTypeEnum.inbox,
    [kammanta.glob.INBOX_DIR_STR], matches_all, None
)
tickler_files = Directory(
    kammanta.glob.CollTypeEnum.tickler,
    [kammanta.glob.TICKLER_DIR_STR], matches_all, None
)
na_files = Directory(
    kammanta.glob.CollTypeEnum.next_actions,
    [], matches_txt_files, None
)
prj_fds = Directory(
    kammanta.glob.CollTypeEnum.projects,
    [], matches_project_collection_dirs, matches_all
)
contacts_dir = Directory(
    kammanta.glob.CollTypeEnum.contacts,
    [kammanta.glob.CONTACTS_DIR_STR], matches_txt_files, None
)
agenda_files = Directory(
    kammanta.glob.CollTypeEnum.agendas,
    [kammanta.glob.AGENDAS_DIR_STR], matches_txt_files, None
)
