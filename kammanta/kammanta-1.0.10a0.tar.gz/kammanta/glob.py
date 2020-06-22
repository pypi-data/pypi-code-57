import configparser
import os
import shutil
import time
import webbrowser
import subprocess
import enum
import typing
import logging
import re
import datetime
from PyQt5 import QtCore
from PyQt5 import QtGui

WAITING_FOR_STR = "waiting-for.txt"
SOMEDAY_MAYBE_STR = "someday-maybe"


DAYS_SECS_INT = 60 * 60 * 24
HOURS_SECS_INT = 60 * 60
MINUTES_SECS_INT = 60

SETTINGS_FILE_NAME_STR = "settings.ini"
SETTINGS_SECTION_GENERAL_STR = "general"
SETTINGS_BASE_DIR_STR = "base_dir_str"
SETTINGS_REFERECE_DIR_STR = "reference_dir_str"
SETTINGS_SECTION_FAVORITE_REFERENCES_STR = "favorite_references"
SETTINGS_SECTION_EXTERNAL_TOOLS_STR = "external_tools"
SETTINGS_EMAIL_STR = "email"
SETTINGS_CALENDAR_STR = "calendar"

PY_DATETIME_FILENAME_FORMAT_STR = "%Y-%m-%dT%H-%M"
PY_DATE_FILENAME_FORMAT_STR = "%Y-%m-%d"
QT_DATETIME_FORMAT_STR = "yyyy-MM-ddTHH-mm"

APPLICATION_TITLE_STR = "Kammanta"

INBOX_DIR_STR = "inbox"
TICKLER_DIR_STR = "tickler"
CONTACTS_DIR_STR = "contacts"
AGENDAS_DIR_STR = "agendas"
DEFAULT_USER_DIR_STR = "user_files"
TRASH_DIR_STR = ".trash"
TEXT_SUFFIX_STR = ".txt"
COMPL_PREF_STR = "x_"
FAV_PREF_STR = "_"
SUPPORT_DELIMITER_STR = "|"
NOTE_FILE_PREFIX_STR = "note_"
DATE_FILENAME_FORMAT_STR = "%Y-%m-%d"
EXT_BTN_STYLE_SHEET_STR = "font: italic"
APPLICATION_PATH_FORMATTED_STR = "[appl_path]"
EXAMPLE_TESTING_PATH_STR = "/home/sunyata/PycharmProjects/kammanta/example"
IMAGE_FILES_TE = (".png", ".jpg", ".jpeg")
testing_bool = False
example_bool = False


def add_tickler_file(i_reminder_time_string: str, i_source_path: str, i_move_or_copy: bool) -> str:
    # source_basename_str = os.path.basename(i_source_path)
    # source_basename_str = gtd.glob.remove_datetime_prefix(source_basename_str)
    # base_file_name_str = i_reminder_time_string + "_" + source_basename_str
    # file_name_str = base_file_name_str + "_" + str(counter_int) + ".txt"
    # tickler_dir_path_str = gtd.glob.get_path(gtd.glob.TICKLER_DIR_STR)
    dest_path_str = get_path(TICKLER_DIR_STR)
    if i_move_or_copy:
        dest_path_str = move_fd(i_source_path, dest_path_str, i_reminder_time_string)
    else:
        dest_path_str = copy_fd(i_source_path, dest_path_str, i_reminder_time_string)
    return dest_path_str


def add_contact(i_name: str) -> None:
    new_file_name_str = i_name
    if not new_file_name_str.lower().endswith(".txt"):
        new_file_name_str += ".txt"
    contact_path_str = get_path(CONTACTS_DIR_STR)
    new_file_path_str = create_and_get_path(contact_path_str, i_name)

    # template_file_relative_path_str = "contact_template.txt"
    template_file_path_str = get_appl_path("kammanta", "contact_template.txt")
    template_str = ""
    with open(template_file_path_str, "r") as f:
        template_str = f.read()
    with open(new_file_path_str, "w") as f:
        f.write(template_str)


def add_tickler_note(i_reminder_time_string: str, i_text_to_add: str):
    base_file_name_str = i_reminder_time_string + "_note_" + datetime.datetime.now().strftime(DATE_FILENAME_FORMAT_STR)
    counter_int = 1
    file_name_str = base_file_name_str + "_" + str(counter_int) + TEXT_SUFFIX_STR
    file_path_str = get_path(TICKLER_DIR_STR)
    while os.path.exists(file_path_str) and counter_int < 1000:
        counter_int += 1
        file_name_str = base_file_name_str + "_" + str(counter_int) + TEXT_SUFFIX_STR
        file_path_str = get_path(TICKLER_DIR_STR, file_name_str)
    with open(file_path_str, "w+") as file:
        file.write(i_text_to_add)


def setup_minimal_config():
    # WIP
    wf_path_str = get_path(WAITING_FOR_STR)
    with open(wf_path_str, "x") as f:
        pass


def get_icon_rel_path() -> str:
    icon_rel_path_str = "icon.png"
    if testing_bool or example_bool:
        icon_rel_path_str = "testing/icon-testing.png"
    return icon_rel_path_str


def copy_and_setup_testing():
    # -as of this writing this function is used both for testing *and for the example*
    # copying
    src_path_str = os.path.join(get_appl_path(), "testing", "example")
    dst_path_str = get_path()
    # old_path_str = os.path.join(get_path(), "example")
    if os.path.exists(dst_path_str):
        shutil.rmtree(dst_path_str)
    shutil.copytree(src_path_str, dst_path_str)

    # tickler setup
    tickler_path_str = os.path.join(dst_path_str, TICKLER_DIR_STR)

    today_date_str = datetime.datetime.now().strftime(DATE_FILENAME_FORMAT_STR)
    add_tickler_note(today_date_str, "today tickler text")

    yesterday_date = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_date_str = yesterday_date.strftime(DATE_FILENAME_FORMAT_STR)
    add_tickler_note(yesterday_date_str, "yesterday tickler text")

    tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow_date_str = tomorrow_date.strftime(DATE_FILENAME_FORMAT_STR)
    add_tickler_note(tomorrow_date_str, "tomorrow tickler text")

    future_date = datetime.datetime.now() + datetime.timedelta(days=10)
    future_date_str = future_date.strftime(DATE_FILENAME_FORMAT_STR)
    add_tickler_note(future_date_str, "future tickler text, etc text\nanother line\nthird line")


# -Please note: "filesystemwatcher = QtCore.QFileSystemWatcher()" doesn't work, maybe because the initialization
#  is too early?
# global filesystemwatcher

class FswSingleton:
    # -on_file_or_dir_changed in MainWindow handles all changes
    file_system_watcher = None

    @classmethod
    def get(cls) -> QtCore.QFileSystemWatcher:
        if cls.file_system_watcher is None:
            cls.file_system_watcher = QtCore.QFileSystemWatcher()
        return cls.file_system_watcher


"""
def add_path_to_fsw(i_new_path: str):
    fsw = get_filesyswatcher()
    file_path_list = fsw.files()
    dir_path_list = fsw.directories()
    if not i_new_path in file_path_list and not i_new_path in dir_path_list:
        fsw.addPath(i_new_path)
"""


def clear_dir(i_dir_path: str):
    for file_or_dir_name in os.listdir(i_dir_path):
        file_or_dir_path = os.path.join(i_dir_path, file_or_dir_name)
        if os.path.isdir(file_or_dir_path):
            clear_dir(file_or_dir_path)
            os.rmdir(file_or_dir_path)
        else:
            os.remove(file_or_dir_path)


def clear_trash():
    trash_dir_path = get_path(TRASH_DIR_STR)
    clear_dir(trash_dir_path)


def get_appl_path(*args, formatted_bl=False) -> str:
    if formatted_bl:
        application_dir_str = APPLICATION_PATH_FORMATTED_STR
    else:
        application_dir_str = os.path.dirname(os.path.dirname(__file__))
    full_path_str = application_dir_str
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    return full_path_str


def get_config_path(*args) -> str:
    # application_dir_str = os.path.dirname(os.path.dirname(__file__))
    config_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    config_dir = os.path.join(config_dir, "kammanta")
    if testing_bool or example_bool:
        config_dir = os.path.join(config_dir, "example_testing")
    full_path_str = config_dir
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    return full_path_str


def get_path(*args) -> str:
    if testing_bool or example_bool:
        user_dir_path_str = EXAMPLE_TESTING_PATH_STR
    else:
        application_dir_str = get_config_path()
        default_user_dir_path_str = os.path.join(application_dir_str, DEFAULT_USER_DIR_STR)
        user_dir_path_str = get_string_from_config(
            SETTINGS_SECTION_GENERAL_STR, SETTINGS_BASE_DIR_STR, default_user_dir_path_str
        )
    full_path_str = user_dir_path_str
    for arg in args:
        if arg != "":
            full_path_str = os.path.join(full_path_str, arg)
    return full_path_str


def get_ref_path() -> str:
    if testing_bool or example_bool:
        user_ref_path_str = EXAMPLE_TESTING_PATH_STR
    else:
        application_dir_str = get_config_path()
        # -TODO: is this the default ref path that we want?
        user_ref_path_str = get_string_from_config(
            SETTINGS_SECTION_GENERAL_STR, SETTINGS_REFERECE_DIR_STR, application_dir_str
        )
    return user_ref_path_str


"""
try:
    user_dir_path_str = config[SETTINGS_GENERAL_STR][SETTINGS_BASE_DIR_STR]
except KeyError:
    # Using the application dir if the settings can't be read
    application_dir_str = get_appl_path()  # os.path.dirname(os.path.dirname(__file__))
    user_dir_path_str = os.path.join(application_dir_str, DEFAULT_USER_DIR_STR)
    config.add_section("general")
    config.set(SETTINGS_GENERAL_STR, SETTINGS_BASE_DIR_STR, user_dir_path_str)
    with open(SETTINGS_FILE_NAME_STR, "w") as file:
        config.write(file)
"""


def get_nr_items_and_last_mod_time(i_support_path: str) -> (int, int):
    FILE_LIMIT_INT = 50
    nr_of_files_int = 0
    latest_edit_time_ts_int = int(os.path.getmtime(i_support_path))  # -first looking at the dir
    for root_dir_path_str, _, file_name_list in os.walk(i_support_path):
        # file_name_list = [f for f in file_name_list if os.path.isfile(f)]  # -isfile or something else here doesn't work, unknown why
        # -links are also given in the list of files (unknown why)
        nr_of_files_int += len(file_name_list)
        if nr_of_files_int > FILE_LIMIT_INT:
            nr_of_files_int = -1
            break
        for file_name_str in file_name_list:
            file_path_str = os.path.join(root_dir_path_str, file_name_str)
            if not os.path.isfile(file_path_str):
                continue
            edit_time_ts_int = int(os.path.getmtime(file_path_str))
            if edit_time_ts_int > latest_edit_time_ts_int:
                latest_edit_time_ts_int = edit_time_ts_int
    nr_of_files_str = f"more than {str(FILE_LIMIT_INT)}"
    """
    if nr_of_files_int != -1:
        nr_of_files_str = str(nr_of_files_int)
    newest_str = "Hasn't been edited"
    if latest_edit_time_ts_int != -1:
        newest_dt = datetime.date.fromtimestamp(latest_edit_time_ts_int)
        newest_str = str(newest_dt)
    """
    return (nr_of_files_int, latest_edit_time_ts_int)


def create_and_get_path(*args) -> str:
    # Please note that whether a file or a dir is created depends on the suffix
    path_str = get_path(*args)
    """
    if not args:
        return path_str
    """
    # or os.path.exists(args[-1])
    is_new_file_bool = False
    if len(args) > 0:
        last_arg: str = args[-1]
        is_new_file_bool = last_arg.endswith((TEXT_SUFFIX_STR, ".desktop"))
    is_existing_file_bool = os.path.isfile(path_str)
    if is_existing_file_bool:
        return path_str
    # Creating dirs
    if is_new_file_bool:
        dir_path_str = os.path.dirname(path_str)
        # input_string_is_file_bool = True
    else:
        dir_path_str = path_str
    if not os.path.exists(dir_path_str):
        os.makedirs(dir_path_str, exist_ok=True)
    # Creating file
    if is_new_file_bool:
        with open(path_str, "x") as new_file:
            pass  # -just creating the file
    return path_str


def launch_string(i_string: str):
    path_formatted_str = i_string.strip()
    string_type = get_type(i_string)
    if string_type == TypeEnum.web_link:
        # try: urllib.parse.urlparse(i_path)
        webbrowser.open(path_formatted_str)
    elif string_type in any_file_enumlist + [TypeEnum.dir]:
        time.sleep(0.8)  # - 0.7 doesn't work
        subprocess.Popen(["xdg-open", path_formatted_str])
        # BUG: error messages are forwarded from thunderbird (so probably all applications started with launch_string)
    elif string_type == TypeEnum.command:
        # subprocess.run([path_formatted_str])
        subprocess.Popen([path_formatted_str])
    else:
        raise Exception("Case not covered")


def add_suffix(i_name: str, i_suffix: str) -> str:
    if not i_name.endswith(i_suffix):
        return i_name + i_suffix
    else:
        return i_name


def add_prefix(i_name: str, i_prefix: str) -> str:
    if not i_name.startswith(i_prefix):
        return i_prefix + i_name
    else:
        return i_name


def add_prefix_to_basename(i_path: str, i_prefix: str) -> str:
    basename_str = os.path.basename(i_path)
    dirname_str = os.path.dirname(i_path)
    new_basename_str = add_prefix(basename_str, i_prefix)
    new_path_str = os.path.join(dirname_str, new_basename_str)
    return new_path_str


def remove_prefix(i_whole_text: str, i_prefix_text: str) -> str:
    if i_prefix_text not in i_whole_text:
        return i_whole_text
    if i_whole_text.startswith(i_prefix_text):
        return i_whole_text[len(i_prefix_text):]
    else:
        return i_whole_text


def get_reminder_time(i_text: str) -> typing.Optional[datetime.datetime]:
    name_split_list = i_text.split("_")
    datetime_str = name_split_list[0]
    try:
        ret_dt = datetime.datetime.strptime(datetime_str, PY_DATETIME_FILENAME_FORMAT_STR)
    except ValueError:
        return None
    # timestamp, for time of day+date
    return ret_dt


def has_reminder_time(i_text: str) -> bool:
    result_bool = False
    if get_reminder_time(i_text) is not None:
        result_bool = True
    return result_bool


def remove_datetime_prefix(i_file_name: str) -> str:
    updated_file_name_str = i_file_name
    while has_reminder_time(updated_file_name_str):
        (before_str, sep_str, after_str) = updated_file_name_str.rpartition("_")
        updated_file_name_str = before_str
    return updated_file_name_str

    """
    re_search_result = re.search(r'URL=(.*)\n', contents_str)
    if re_search_result is not None:
        support_path_str = re_search_result.group(1)
    """


def remove_any_dot_suffix(i_whole_text: str) -> str:
    if "." in i_whole_text:
        (before_str, sep_str, after_str) = i_whole_text.rpartition(".")
        return before_str
    return i_whole_text

    """
    separator_char = "."
    if not separator_char in i_whole_text:
        return i_whole_text
    split_str = i_whole_text.split(separator_char)
    result_str = separator_char.join(split_str[:-1])
    return result_str
    """


def remove_specified_suffix(i_whole_text: str, i_suffix_text: str = "") -> (str, bool):
    if i_whole_text.endswith(i_suffix_text):
        ret_new_str = i_whole_text[:-len(i_suffix_text)]
        return (ret_new_str, True)
    else:
        return (i_whole_text, False)


def is_text(i_file_path: str) -> bool:
    try:
        with open(i_file_path, "r"):
            pass
    except UnicodeDecodeError:
        return False
        # -a binary file
    return True


def get_dsuffix(i_whole_text: str) -> str:
    # separator_char = "."
    (before_str, sep_str, after_str) = i_whole_text.rpartition(".")
    return after_str

    """
    separator_char = "."
    if not separator_char in i_whole_text:
        return ""
    split_strlist = i_whole_text.split(separator_char)
    result_str = separator_char.join(split_strlist[-1])
    return result_str
    """


def remove_delimiter_and_after(i_whole_text: str, i_delimiter: str) -> str:
    if not i_delimiter in i_whole_text:
        return i_whole_text
    ret_result_str = i_whole_text.split(i_delimiter)[0]
    ret_result_str = ret_result_str.strip()
    # -unknown why .strip is needed here
    return ret_result_str


def remove_fd(i_source_path: str):
    trash_dir_path_str = get_path(TRASH_DIR_STR)
    move_fd(i_source_path, trash_dir_path_str)


def move_fd(i_source_path: str, i_dest_path: str, i_reminder_time_str="") -> str:
    """
    Please note that the underlying operation is copying, which means that the time of creation/modification
    is going to be set to the time of "moving" (copying). This can matter for inbox items that are tickled,
    but it's not going to work if the user manually moves files into the inbox directory
    """
    create_and_get_path(i_dest_path)

    source_file_name_str = os.path.basename(i_source_path)
    delimiter_str = "."
    suffix_str = ""
    # dir_path_str = os.path.dirname(i_source_path)
    counter_int = 0
    new_file_name_str = source_file_name_str
    if i_reminder_time_str:
        new_file_name_str = remove_datetime_prefix(new_file_name_str)
        new_file_name_str = i_reminder_time_str + "_" + new_file_name_str
    while new_file_name_str in os.listdir(i_dest_path):
        if delimiter_str in source_file_name_str:
            # removing suffix
            suffix_str = get_dsuffix(source_file_name_str)
            source_file_name_str = remove_any_dot_suffix(source_file_name_str)
        new_file_name_str = source_file_name_str + "_" + str(counter_int) + "." + suffix_str
        counter_int += 1

    dest_path_with_file_name_str = os.path.join(i_dest_path, new_file_name_str)
    if os.path.isfile(i_source_path):
        shutil.copy(i_source_path, dest_path_with_file_name_str)
        os.remove(i_source_path)
    elif os.path.isdir(i_source_path):
        shutil.copytree(i_source_path, dest_path_with_file_name_str)
        shutil.rmtree(i_source_path)

    return dest_path_with_file_name_str


# def cp_or_mv(i_source_path: str, i_dest_path: str, i_reminder_time_str="")


def copy_fd(i_source_path: str, i_dest_path: str, i_reminder_time_str="") -> str:
    source_file_name_str = os.path.basename(i_source_path)
    if os.path.isdir(i_dest_path):
        delimiter_str = "."
        suffix_str = ""
        counter_int = 0
        new_file_name_str = source_file_name_str
        if i_reminder_time_str:
            new_file_name_str = i_reminder_time_str + "_" + source_file_name_str
            # TODO: we may want to check if the name without the reminder time exists or not
            while new_file_name_str in os.listdir(i_dest_path):
                if delimiter_str in source_file_name_str:
                    # removing suffix
                    suffix_str = get_dsuffix(source_file_name_str)
                    source_file_name_str = remove_any_dot_suffix(source_file_name_str)
                new_file_name_str = source_file_name_str + "_" + str(counter_int) + "." + suffix_str
                counter_int += 1
            dest_path_with_file_name_str = os.path.join(i_dest_path, new_file_name_str)
            shutil.copy(i_source_path, dest_path_with_file_name_str)
            return dest_path_with_file_name_str
    else:
        shutil.copy(i_source_path, i_dest_path)
        return i_dest_path

    # -does not preserve metadata (like creation and modification date). This is what we want!
    #  (copy2 tries to also copy metadata)


def get_new_note_name() -> str:
    base_file_name_str = NOTE_FILE_PREFIX_STR + datetime.datetime.now().strftime(DATE_FILENAME_FORMAT_STR)
    counter_int = 1
    file_name_str = base_file_name_str + "_" + str(counter_int) + TEXT_SUFFIX_STR
    file_path_str = get_path(INBOX_DIR_STR, file_name_str)
    while os.path.exists(file_path_str) and counter_int < 1000:
        counter_int += 1
        file_name_str = base_file_name_str + "_" + str(counter_int) + TEXT_SUFFIX_STR
        file_path_str = get_path(INBOX_DIR_STR, file_name_str)
    return file_name_str


def add_string_to_config(i_section: str, i_key: str, i_value: str):
    config_parser = configparser.ConfigParser()
    config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser.read(config_file_path_str)
    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
    config_parser.set(i_section, i_key, i_value)
    with open(config_file_path_str, "w") as file:
        config_parser.write(file)


def add_dict_string_to_config(i_section: str, i_key: str, i_value: str):
    config_parser = configparser.ConfigParser()
    config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser.read(config_file_path_str)
    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
    config_parser.set(i_section, i_key, i_value)
    with open(config_file_path_str, "w") as file:
        config_parser.write(file)


def get_string_from_config(i_section: str, i_key: str, i_default_value: str) -> str:
    config_parser = configparser.ConfigParser()
    config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser.read(config_file_path_str)

    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
    if not config_parser.has_option(i_section, i_key):
        config_parser.set(i_section, i_key, i_default_value)
        with open(config_file_path_str, "w") as file:
            config_parser.write(file)

    ret_value_str = config_parser[i_section][i_key]
    return ret_value_str


def get_dictionary_from_config(i_section: str) -> dict:
    # FAV_PREF_STR
    # , i_default_value: dict
    config_parser = configparser.ConfigParser()
    config_file_path_str = get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser.read(config_file_path_str)

    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
        with open(config_file_path_str, "w") as file:
            config_parser.write(file)

    ret_value_str = dict(config_parser.items(i_section))
    return ret_value_str


def get_title_font(i_bold: bool=False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(14)
    font.setBold(i_bold)
    return font


def get_button_font(i_external: bool=False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(10)
    font.setItalic(i_external)
    return font


class CollTypeEnum(enum.Enum):
    projects = enum.auto()
    next_actions = enum.auto()
    inbox = enum.auto()
    contacts = enum.auto()
    agendas = enum.auto()
    tickler = enum.auto()

    areas_of_interest = enum.auto()
    goals_and_objectives = enum.auto()
    vision = enum.auto()
    purpose_and_principles = enum.auto()

    def get_name(self):
        formatted_name_str = self.name.replace("_", " ")
        formatted_name_str = formatted_name_str.title()
        formatted_name_strlist = formatted_name_str.split(" ")
        formatted_name_str = ""
        for n in formatted_name_strlist:
            if len(n) > 3:
                formatted_name_str += n.capitalize()
            else:
                formatted_name_str += n.lower()
            formatted_name_str += " "
        return formatted_name_str.strip()


class TypeEnum(enum.Enum):
    # Idea: we could use a class instead of an enum for the types, and include the all_text_files inside this class
    line = enum.auto()  # Special, since it is not given from the get_type method (below)

    dir = enum.auto()

    note_file = enum.auto()
    text_file = enum.auto()
    desktop_file = enum.auto()
    image_file = enum.auto()
    file = enum.auto()

    web_link = enum.auto()
    command = enum.auto()
    error = enum.auto()


any_file_enumlist = [
    TypeEnum.note_file, TypeEnum.text_file, TypeEnum.desktop_file, TypeEnum.image_file, TypeEnum.file
]

"""

class EntityType(enum.Enum):
    line = enum.auto()
    directory = enum.auto()
    note_file = enum.auto()
    text_file = enum.auto()
    desktop_file = enum.auto()
    image_file = enum.auto()
    other_file = enum.auto()


class SupportStringTypeEnum(enum.Enum):
    web_link = enum.auto()
    dir = enum.auto()
    file = enum.auto()
    command = enum.auto()
    error = enum.auto()
    
    
def get_df_type(i_path: str) -> EntityType:
    image_files_te = (".png", ".jpg", ".jpeg")
    if os.path.isdir(i_path):
        return EntityType.directory
    elif i_path.endswith(".desktop"):
        return EntityType.desktop_file
    elif NOTE_FILE_PREFIX_STR in i_path and i_path.lower().endswith(TEXT_SUFFIX_STR):
        return EntityType.note_file
    elif i_path.lower().endswith(TEXT_SUFFIX_STR):
        return EntityType.text_file
    elif i_path.endswith(image_files_te):
        return EntityType.image_file
    else:
        return EntityType.other_file


def get_string_type(i_string: str) -> SupportStringTypeEnum:
    if i_string.startswith("http://") or i_string.startswith("https://"):
        return SupportStringTypeEnum.web_link
    elif os.path.isfile(i_string):
        return SupportStringTypeEnum.file
        # -idea: we can verify if the path exists or not
        # -problem: this will catch commands that are used by giving a path /path/to/binary
        #  https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
    elif os.path.isdir(i_string):
        return SupportStringTypeEnum.dir
    elif shutil.which(i_string.partition(" ")[0]) is not None:
        return SupportStringTypeEnum.command
    else:
        return SupportStringTypeEnum.error
"""


def is_valid_command(i_string: str) -> True:
    result_bool = shutil.which(i_string.partition(" ")[0]) is not None
    return result_bool


def get_type(i_string: str) -> TypeEnum:
    if i_string.startswith("http://") or i_string.startswith("https://"):
        return TypeEnum.web_link
    elif os.path.isfile(i_string):
        if i_string.endswith(".desktop"):
            return TypeEnum.desktop_file
        elif i_string.lower().endswith(TEXT_SUFFIX_STR):
            if NOTE_FILE_PREFIX_STR in i_string:
                return TypeEnum.note_file
            return TypeEnum.text_file
        elif i_string.lower().endswith(IMAGE_FILES_TE):
            return TypeEnum.image_file
        return TypeEnum.file
        # -idea: we can verify if the path exists or not
        # -problem: this will catch commands that are used by giving a path /path/to/binary
        #  https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
    elif os.path.isdir(i_string):
        return TypeEnum.dir
    elif is_valid_command(i_string):
        return TypeEnum.command
    return TypeEnum.error


def get_mod_time_delta_as_string(self, i_file_path: str) -> str:
    delta_time_secs_int = int(time.time() - os.path.getmtime(i_file_path))
    delta_time_formatted_str = ""
    if delta_time_secs_int >= DAYS_SECS_INT:
        delta_time_formatted_str = str(delta_time_secs_int // DAYS_SECS_INT) + " days"
    elif delta_time_secs_int >= HOURS_SECS_INT:
        delta_time_formatted_str = str(delta_time_secs_int // HOURS_SECS_INT) + " hours"
    elif delta_time_secs_int >= MINUTES_SECS_INT:
        delta_time_formatted_str = str(delta_time_secs_int // MINUTES_SECS_INT) + " minutes"
    else:
        delta_time_formatted_str = str(delta_time_secs_int) + " seconds"
    # datetime.datetime.strftime(delta_time_secs_ft)
    # delta_time_secs_ft
    delta_ret_str = "Last edit was made " + delta_time_formatted_str + " ago"
    return delta_ret_str

