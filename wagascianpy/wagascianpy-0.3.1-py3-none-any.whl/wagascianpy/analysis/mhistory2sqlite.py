#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
import os

from six import string_types
import wagascianpy.utils.utils
import wagascianpy.database.db_record
from datetime import datetime


def _hst_file_name_parse(root, file_name, file_list, start_time=None, stop_time=None):
    file_name_no_ext, file_extension = os.path.splitext(file_name)
    if file_extension.strip('.') == "hst":
        if start_time is None or stop_time is None:
            file_list.append(os.path.join(root, file_name))
        else:
            time = datetime.strptime(file_name_no_ext, "%y%m%d")
            time = wagascianpy.database.db_record.DBRecord.add_timezone(time)
            if start_time < time < stop_time:
                file_list.append(os.path.join(root, file_name))


def mhistory2sqlite(input_path, output_folder=None, start_time=None, stop_time=None, recursive=False):
    # Check input_path argument
    if not isinstance(input_path, string_types):
        raise TypeError("Input folder must be a string")
    if not input_path:
        raise ValueError("Input folder cannot be empty")
    if not os.path.exists(input_path) or not os.access(input_path, mode=os.R_OK):
        raise OSError("Input folder must exists and be readable : %s" % input_path)

    # Check output_folder argument
    if not output_folder:
        if os.path.isdir(input_path):
            output_folder = input_path
        else:
            output_folder = os.path.dirname(input_path)
    if not isinstance(output_folder, string_types):
        raise TypeError("Output folder must be a string")
    if os.path.exists(output_folder) and not os.access(output_folder, mode=os.R_OK):
        raise OSError("Output folder must exists and be readable : %s" % output_folder)
    if not os.path.exists(output_folder):
        wagascianpy.utils.utils.mkdir_p(output_folder)

    # Check recursive argument
    if not isinstance(recursive, bool):
        raise TypeError("Recursive flag must be a boolean")

    # Check start time and stop time
    if not isinstance(start_time, string_types):
        raise TypeError("Start time must be a string")
    start_time = wagascianpy.database.db_record.DBRecord.str2datetime(start_time)
    if not isinstance(stop_time, string_types):
        raise TypeError("Stop time must be a string")
    stop_time = wagascianpy.database.db_record.DBRecord.str2datetime(stop_time)

    # Check that the mh2sql program exists
    mh2sql = wagascianpy.utils.utils.which(program="mh2sql")
    if not mh2sql:
        raise EnvironmentError("mh2sql program was not found")

    # List the input files
    input_files = []
    if os.path.isfile(input_path):
        input_files.append(input_path)
    if os.path.isdir(input_path):
        if recursive:
            for root, dirs, files in os.walk(input_path):
                for file_name in files:
                    _hst_file_name_parse(root=root, file_name=file_name, file_list=input_files, start_time=start_time,
                                         stop_time=stop_time)
        else:
            for file_name in os.listdir(input_path):
                _hst_file_name_parse(root=input_path, file_name=file_name, file_list=input_files, start_time=start_time,
                                     stop_time=stop_time)

    input_files = sorted(input_files)
    files_list = ' '.join(input_files)

    cmd = "{} --sqlite {} {}".format(mh2sql, output_folder, files_list)
    print(wagascianpy.utils.utils.run_cmd(cmd))
