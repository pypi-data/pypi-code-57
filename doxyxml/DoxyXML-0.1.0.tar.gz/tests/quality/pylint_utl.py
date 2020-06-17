#!/usr/bin/env python
"""
Helper methods for managing code inspection.

See this style guide for best-practice references : https://google.github.io/styleguide/pyguide.html
"""
import os
import os.path as opth
import re
import time

from pylint import lint
from pylint.reporters.text import TextReporter

root_path = os.path.abspath(os.path.join(__file__, os.pardir, '..'))
list_target_project_path = [
    os.path.abspath(os.path.join(root_path, '..')),
]


root_references_results = os.path.join(root_path, 'resources', 'code_inspection', 'references')

# Results file path for Error (E) and Warning (W) code inspections
pylint_results_err_warn_file_path = os.path.join(root_references_results, 'pylint_err_warn_results.txt')
pylint_results_err_warn_file_path_summary = os.path.join(root_references_results, 'pylint_err_warn_summary.txt')

# Results file path for Convention (C) and Refactor (R) code inspections
pylint_results_conv_ref_file_path = os.path.join(root_references_results, 'pylint_conv_ref_results.txt')
pylint_results_conv_ref_file_path_summary = os.path.join(root_references_results, 'pylint_conv_ref_summary.txt')

pylint_sanity_results_file_path = os.path.join(root_references_results, 'pylint_sanity_results.txt')

# Pylint configuration file for error and warning code inspections
pylintrc_err_warn_file_path = os.path.join(root_path, 'resources', 'code_inspection', 'config', 'pylintrc_err_warn')
# Pylint configuration file for convention and refactor code inspections
pylintrc_conv_ref_file_path = os.path.join(root_path, 'resources', 'code_inspection', 'config', 'pylintrc_conv_ref')

PYLINTRC_TYPE_ERR_WARN = "ERR_WARN"
PYLINTRC_TYPE_CONV_REF = "CONV_REF"


def sort_by_index(in_iterable, in_index, in_reverse=False):
    """
    Sort an iterable (list, tuple) by a given index (column) using the built-in fucntion sorted

    References:
    * [1] https://docs.python.org/fr/3/library/functions.html#sorted
    * [2] https://docs.python.org/fr/3/howto/sorting.html
    :param in_iterable: iterable to be used with an index (list, tuple)
    :type in_iterable: list

    :param in_index: index to be used
    :type in_index: int

    :param in_reverse: order to be used, in_reverse=True means in descending order, otherwise in ascending order
    :type in_reverse: bool

    :return: sorted iterable
    :rtype: iter
    """
    return sorted(in_iterable, key=lambda x: x[in_index], reverse=in_reverse)

def get_list_files_paths_from_dir(in_root_path, in_pattrn=""):
    """
    Retrieve the files path from a given directory and its sub-directories
    :param in_root_path: in_root directory to walk through
    :param in_pattrn: in_pattern to be applied to file name for filtering output
    :return: list of files found
    """
    list_file_path = []
    for root, _, files in os.walk(in_root_path):  # _ is subdirs

        if files:
            for file_path in files:
                if in_pattrn:
                    # filter paths based on given pattern
                    full_path = opth.abspath(opth.join(root, file_path))
                    if re.findall(in_pattrn, full_path):
                        list_file_path.append(full_path)
                else:
                    list_file_path.append(opth.abspath(opth.join(root, file_path)))

    return list_file_path


def get_chunks(in_data, in_nb_rows=1000):
    """
    Divide data into subset of rows
    :param in_data: original data to be exploded
    :param in_nb_rows: number of parts in which data will be exploded
    :return:
    """
    for i in range(0, len(in_data), in_nb_rows):
        yield in_data[i:i + in_nb_rows]


def sanity_check_com(in_line) -> str:
    """
    Basic sanity check for com package.
    :param in_line: Line to parse and sanitize
    :type in_line: str
    :return: sanitized line
    :rtype: str
    """
    line = in_line.rstrip()
    line = re.sub(r'.*?sde[/\\]+', '$root/sde/', line)

    out_line = line.replace(r' *\(previous run.*\)$', '')

    return out_line.strip()


def format_and_write_to_file(in_file_path, in_file_path_summary, in_pylint_results_arr, in_header_file_str=None):
    """
    Format the given data in array and write it in given file path
    :param in_file_path_summary: summary of results
    :type in_file_path_summary: str
    :param in_header_file_str: Header string to add to file
    :type in_header_file_str: str
    :param in_file_path: destination file path
    :type in_file_path: str
    :param in_pylint_results_arr: Array containing data to be written
    :type in_pylint_results_arr: list
    :return: the number of data written and the list of errors found
    :rtype: Union[int, list]
    """
    err_array = []
    list_data_err = []
    list_data_warn = []
    list_data_ref = []
    list_data_conv = []
    list_data_other = []
    for row in in_pylint_results_arr:
        if re.findall(r'^\*\*\*', row):
            continue
        val_arr = re.findall(r'(^.*\.py:[0-9]+):[0-9]+:([A-Z][0-9]+) \(.*', row)
        if val_arr and len(val_arr[0]) > 1:
            res_arr = (val_arr[0][0], val_arr[0][1], row)
            msg_id = res_arr[1]
            if msg_id.startswith('E') or msg_id.startswith('F'):
                list_data_err.append(res_arr)
            elif msg_id.startswith('W'):
                list_data_warn.append(res_arr)
            elif msg_id.startswith('R'):
                list_data_ref.append(res_arr)
            elif msg_id.startswith('C'):
                list_data_conv.append(res_arr)
            else:
                list_data_other.append(res_arr)

    list_data_err = sort_by_index(list_data_err, 0)
    list_data_warn = sort_by_index(list_data_warn, 0)
    list_data_ref = sort_by_index(list_data_ref, 0)
    list_data_conv = sort_by_index(list_data_conv, 0)
    list_data_other = sort_by_index(list_data_other, 0)
    list_data = list_data_err + list_data_warn + list_data_ref + list_data_conv + list_data_other

    stats_str = "pylint_stats;NB_ERROR:%d\n" % len(list_data_err)
    stats_str += "pylint_stats;NB_WARNING:%d\n" % len(list_data_warn)
    stats_str += "pylint_stats;NB_CONVENTION:%d\n" % len(list_data_conv)
    stats_str += "pylint_stats;NB_REFACTOR:%d\n" % len(list_data_ref)
    stats_str += "pylint_stats;NB_OTHERS:%d\n" % len(list_data_other)

    with open(in_file_path_summary, 'w') as f:
        f.write('%s\n' % stats_str)

    with open(in_file_path, 'w') as f:
        if in_header_file_str:
            f.write('%s\n' % in_header_file_str)

        for row in list_data:
            f.write('%s\n' % row[2])

    return len(list_data), err_array


class FooWritableObject(object):
    """Dummy writable object that could be replaced by built-in StringIO class"""

    def __init__(self):
        self._content_arr = []

    def write(self, in_data):
        """
        Basic write function.
        :param in_data: string of data to be written
        :type in_data: str
        """
        self._content_arr.append(in_data)

    def read(self):
        """
        Basic reader.
        :return: list of data read.
        :rtype: list
        """
        return self._content_arr


def run_on_file(in_file_paths_arr, in_pylintrc_type, in_pylintrc_custom_file=None):
    """
    Run pylint on given file paths in the array, individually.

    :param in_file_paths_arr: list of file paths
    :type in_file_paths_arr: list
    :param in_pylintrc_type: type of configuration file
    :type in_pylintrc_type: str
    :param in_pylintrc_custom_file: path of a custom configuration file
    :type in_pylintrc_custom_file: str
    :return: An iterator on found data
    :rtype: iter
    """
    pylint_options = []

    if in_pylintrc_custom_file:
        pylint_options.append('--rcfile=%s' % in_pylintrc_custom_file)
    else:
        if in_pylintrc_type == PYLINTRC_TYPE_ERR_WARN:
            pylint_options.append('--rcfile=%s' % pylintrc_err_warn_file_path)
        elif in_pylintrc_type == PYLINTRC_TYPE_CONV_REF:
            pylint_options.append('--rcfile=%s' % pylintrc_conv_ref_file_path)

    pylint_out = FooWritableObject()
    text_reporter = TextReporter(pylint_out)
    if isinstance(in_file_paths_arr, list):
        lint.Run(in_file_paths_arr + pylint_options, reporter=text_reporter, do_exit=False)
    else:
        lint.Run(list(in_file_paths_arr) + pylint_options, reporter=text_reporter, do_exit=False)

    return pylint_out


def generate_quality_report_folder(in_folder, in_results_file_path=None, in_pylintrc_type=None,
                                   in_exclusion_list=None) -> list:
    """
    Generate report for pylint run on a given folder.

    :param in_folder: folder to run pylint on
    :type in_folder: str
    :param in_exclusion_list: list of pattern to exclude for the analysis
    :type in_exclusion_list: list
    :param in_results_file_path: destination file path for storing results. Beware that if this file is not provided,
    a list of data found is returned.
    :type in_results_file_path: str
    :param in_pylintrc_type: path of the configuration file
    :type in_pylintrc_type: str
    :return: A list of data found
    :rtype:
    """
    # sanity check for not overwriting configuration file
    if in_results_file_path in [pylintrc_err_warn_file_path, pylintrc_conv_ref_file_path]:
        print("Cannot overwrite configuration file:%s" % in_results_file_path)
        return []

    os.makedirs(root_references_results, exist_ok=True)

    pylint_results_arr = []
    pylint_results_file = None
    if in_results_file_path:
        pylint_results_file = open(in_results_file_path, 'w')

    list_files = get_list_files_paths_from_dir(in_folder, r'.py$')
    if in_exclusion_list:
        for val in in_exclusion_list:
            list_files = [f for f in list_files if not re.findall(r'%s' % val, f)]

    nb_files = len(list_files)

    list_files_chunks = get_chunks(list_files, 110)  # chunk size to be adapted
    iter_data = 0
    for rows in list_files_chunks:
        iter_data += len(rows)
        if iter_data > 99999999:  # Watchdog for number of iteration
            break
        print("Processing file...:(%d/%d)" % (iter_data, nb_files))
        out = run_on_file(rows, in_pylintrc_type=in_pylintrc_type)

        for line in out.read():
            line = line.strip()
            if line:
                pylint_results_arr.append(line)
                if pylint_results_file:
                    pylint_results_file.write("%s\n" % line)

        if pylint_results_file:
            pylint_results_file.flush()

    if pylint_results_file:
        pylint_results_file.close()

    # formatting file
    if in_results_file_path:
        format_and_write_to_file(in_results_file_path, pylint_results_conv_ref_file_path_summary, pylint_results_arr)

    return pylint_results_arr


def check_sanity_script() -> list:
    """
    Extract unexpected characters from script file

    :return: list of errors found
    :rtype:list
    """
    out_res = []
    pattrn = r'[^ a-zA-Z0-9&+_.;:"\'\\%-{}()\n\r*#<>!=~|/$\[\]]'

    list_all_files = []
    for row in list_target_project_path:
        list_files = get_list_files_paths_from_dir(row, r'\.(py|cpp|h)$')
        list_all_files.extend([f for f in list_files if not re.findall(r'(venv|docs|eggs)', f)])

    list_all_files = sorted(list_all_files)

    for filepath in list_all_files:
        with open(filepath, 'r') as f:

            filepath_str = re.sub(r'(.*?)sde[/\\]+', '$root/sde/', filepath)
            try:
                data = f.readlines()
            except UnicodeDecodeError as e:
                print("UnicodeDecodeError exception raised in %s" % filepath_str)
                out_res.append([filepath_str, "UnicodeDecodeError exception raised %s" % str(e), ''])
                continue
            except Exception as e:  # pylint: disable=W0703
                print("Exception raised in %s" % filepath_str)
                out_res.append([filepath_str, "Exception raised %s" % str(e), ''])
                continue

            i = 0
            for row in data:
                val_arr = re.findall(pattrn, row)
                i += 1
                if val_arr:
                    # print("Forbidden characters found in %s" % filepath_str, val_arr)
                    out_res.append([filepath_str, "Forbidden characters found in LINE:%d" % i, '{}'.format(val_arr)])

    if out_res:
        print('Found %d lines with forbidden characters; remove them with the following pattern: %s' % (
            len(out_res), pattrn))

    return out_res


def generate_quality_report(in_results_file_path=None, in_results_file_path_summary=None,
                            in_pylintrc_type=None) -> list:
    """
    Generate report for pylint run

    :param in_results_file_path_summary: summary of results found
    :type in_results_file_path_summary: str
    :param in_results_file_path: destination file path for storing results. Beware that if this file is not provided,
    a list of data found is returned.
    :type in_results_file_path: str
    :param in_pylintrc_type: path of the configuration file
    :type in_pylintrc_type: str
    :return: A list of data found
    :rtype:
    """
    # sanity check for not overwriting configuration file
    if in_results_file_path in [pylintrc_err_warn_file_path, pylintrc_conv_ref_file_path]:
        print("Cannot overwrite configuration file:%s" % in_results_file_path)
        return []

    os.makedirs(root_references_results, exist_ok=True)

    pylint_results_arr = []
    pylint_results_file = None
    if in_results_file_path:
        pylint_results_file = open(in_results_file_path, 'w')

    list_files = []
    for row in list_target_project_path:
        list_files.extend(get_list_files_paths_from_dir(row, r'.py$'))
    list_files = sorted(set(list_files))

    # exclusion list
    list_files = [f for f in list_files if not re.findall(r'(.tox|venv|eggs|docs|Tests_package)', f)]
    nb_files = len(list_files)

    list_files_chunks = get_chunks(list_files, 110)  # chunk size to be adapted
    iter_data = 0
    for rows in list_files_chunks:
        iter_data += len(rows)
        if iter_data > 99999999:  # Watchdog for number of iteration
            break
        print("Processing file...:(%d/%d)" % (iter_data, nb_files))
        out = run_on_file(rows, in_pylintrc_type=in_pylintrc_type)

        for line in out.read():
            line = line.strip()
            res_line = sanity_check_com(line)
            if res_line:
                pylint_results_arr.append(res_line)
                if pylint_results_file:
                    pylint_results_file.write("%s\n" % res_line)

        if pylint_results_file:
            pylint_results_file.flush()

    if pylint_results_file:
        pylint_results_file.close()

    # formatting file
    if in_results_file_path:
        format_and_write_to_file(in_results_file_path, in_results_file_path_summary, pylint_results_arr)

    return pylint_results_arr


if __name__ == "__main__":
    '''
    Testing
    '''
    # Error and warning code inspections in priority
    t0 = time.time()
    out_arr = generate_quality_report(
        pylint_results_err_warn_file_path,
        pylint_results_err_warn_file_path_summary,
        in_pylintrc_type=PYLINTRC_TYPE_ERR_WARN)
    t1 = time.time()
    print("pylint_results_err_warn", len(out_arr), '%ds' % round(t1 - t0, 2))

    out_arr = check_sanity_script()
    for main_val in out_arr:
        print(main_val)
