#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

import os
from datetime import datetime

try:
    # for Python2
    # noinspection PyPep8Naming
    import Tkinter as tkinter
except ImportError:
    # for Python3
    import tkinter

from tkinter import filedialog

from typing import Dict, Optional, List

import pygubu
import wagascianpy.database.wagascidb
import wagascianpy.utils.configuration


def get_time_interval_members(builder):
    # type: (pygubu.Builder) -> (datetime, datetime)
    """Build the interval period
    """
    start_hours = builder.tkvariables.__getitem__('from_hours').get()
    start_minutes = builder.tkvariables.__getitem__('from_minutes').get()
    start_seconds = builder.tkvariables.__getitem__('from_seconds').get()
    start_calendar = builder.get_object('from_calendar')
    try:
        start_datetime = start_calendar.selection
        start_time = start_datetime.replace(hour=start_hours, minute=start_minutes,
                                            second=start_seconds)
    except ValueError as error:
        raise ValueError("Error when building start time string : %s" % str(error))
    except AttributeError as error:
        raise AttributeError("Please select a month and day for start time : %s" % str(error))

    stop_hours = builder.tkvariables.__getitem__('to_hours').get()
    stop_minutes = builder.tkvariables.__getitem__('to_minutes').get()
    stop_seconds = builder.tkvariables.__getitem__('to_seconds').get()
    stop_calendar = builder.get_object('to_calendar')
    try:
        stop_datetime = stop_calendar.selection
        stop_time = stop_datetime.replace(hour=stop_hours, minute=stop_minutes,
                                          second=stop_seconds)
    except ValueError as error:
        raise ValueError("Error when building stop time string : %s" % str(error))
    except AttributeError as error:
        raise AttributeError("Please select a month and day for start time : %s" % str(error))

    if start_time > stop_time:
        raise ValueError("Stop time %s cannot be greater than start time %s"
                         % (stop_time, start_time))

    return start_time, stop_time


def check_repository_and_database_sanity(repository, database):
    # type: (str, str) -> None
    """Check WAGASCI database and repository strings sanity
    """
    if not repository:
        raise ValueError('Repository path is empty')
    if not database:
        raise ValueError('Database path is empty')
    if repository.count(':') == 1:
        tokens = repository.split(':')
        for token in tokens:
            if not token.strip(':'):
                raise ValueError('hostname or path are empty')
    elif repository.count(':') >= 2:
        raise ValueError("Too many ':' in repository string")

    if database.count(':') == 1:
        tokens = database.split(':')
        for token in tokens:
            if not token.strip(':'):
                raise ValueError('hostname or path are empty')
    elif database.count(':') >= 2:
        raise ValueError("Too many ':' in database string")

    if os.path.splitext(database)[1] != '.db':
        raise ValueError("Database extension must be .db")


def check_wagasci_libdir(wagasci_libdir):
    # type: (Optional[str]) -> Optional[str]
    if wagasci_libdir is None or wagasci_libdir == "" or not os.path.exists(wagasci_libdir):
        return None
    if wagasci_libdir.endswith('.so'):
        raise ValueError('You are supposed to provide the library directory, not the library itself')
    return wagasci_libdir


def gui_file_finder():
    # type: (...) -> str
    here = os.path.dirname(os.path.abspath(__file__))
    print(here)
    gui_file = wagascianpy.utils.configuration.conf_file_finder(filename='gui.ui', project_path=here)
    if not os.path.exists(gui_file):
        raise OSError("GUI file not found")
    print("Using GUI file %s" % gui_file)
    return gui_file


def _get_input(text):
    return input(text)


def check_input_folder(input_folder, records, batch_mode):
    # type: (Optional[str], List[Dict], bool) -> Dict[str, str]
    # 1 : Ask the user for download folder
    if not input_folder:
        if not batch_mode:
            dir_opt = {'title': 'Choose the local directory where the WAGASCI raw data has been downloaded',
                       'initialdir': os.curdir, 'mustexist': True}
            input_folder = filedialog.askdirectory(**dir_opt)
        else:
            input_folder = _get_input('Download folder')

    # 3 : check that the download folder exist
    if not os.path.exists(input_folder):
        raise OSError("WAGASCI runs download folder not found : %s" % input_folder)

    # 2 : list folders for each run
    run_dic = {}
    for record in records:
        if os.path.exists(os.path.join(input_folder, record["name"])):
            run_dic[record["name"]] = os.path.join(input_folder, record["name"])
        elif os.path.exists(os.path.join(input_folder, record["run_folder"])):
            run_dic[record["name"]] = os.path.join(input_folder,
                                                   record["run_folder"].strip('/'))
        else:
            print("Run {} not found. Please download it!".format(record["name"]))

    return run_dic
