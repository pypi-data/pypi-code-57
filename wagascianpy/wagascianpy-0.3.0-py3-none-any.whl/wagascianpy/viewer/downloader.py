#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#
from __future__ import print_function

import json
import os
import random
import re
import subprocess
import time
from typing import Type, List, Callable, Optional

try:
    # for Python2
    # noinspection PyPep8Naming
    import Tkinter as tkinter
except ImportError:
    # for Python3
    import tkinter
from tkinter import filedialog

import pygubu
from wagascianpy.utils.configuration import Configuration, RepositoryType
from wagascianpy.database.wagascidb import WagasciRunRecord
import wagascianpy.utils.utils

import wagascianpy.viewer.utils
from wagascianpy.viewer.topology import Topology


def downloader(config,  # type: Type[Configuration]
               records,  # type: List[WagasciRunRecord]
               topology,  # type: Topology
               reporter,  # type: Callable
               overwrite=False,  # type: bool
               batch_mode=False  # type: bool
               ):
    """Download the selected runs listed in the run list frame"""

    if records is None:
        raise ValueError('First get some runs using the "Get All" or "Get Interval" buttons')

    # Ask the user for download folder
    download_folder = config.wagasci_database_configuration.wagasci_download_location()
    if not download_folder:
        if not batch_mode:
            download_folder = filedialog.askdirectory()
        else:
            download_folder = input('Download folder')

    # Create the download directory if necessary
    wagascianpy.utils.utils.mkdir_p(download_folder)

    # Check for write permissions
    if not os.access(download_folder, os.W_OK):
        raise OSError("folder where to restore backup not writable")

    if config.wagasci_database_configuration.repository_type() == RepositoryType.Borg:
        _borg_downloader(records=records,
                         wagasci_repository=config.wagasci_database_configuration.wagasci_repository(),
                         topology=topology,
                         reporter=reporter,
                         overwrite=overwrite,
                         download_folder=download_folder,
                         batch_mode=batch_mode)
    else:
        _simple_downloader(records=records,
                           wagasci_repository=config.wagasci_database_configuration.wagasci_repository(),
                           topology=topology,
                           reporter=reporter,
                           download_folder=download_folder,
                           batch_mode=batch_mode)
    return download_folder


# noinspection PyUnresolvedReferences
def _borg_downloader(records,  # type: List[wagascianpy.database.wagascidb.WagasciRunRecord]
                     wagasci_repository,  # type: str
                     topology,  # type: Topology
                     reporter,  # type: Callable
                     overwrite=True,  # type: bool
                     download_folder=None,  # type: Optional[str]
                     batch_mode=False  # type: bool
                     ):
    # Move to download folder
    with wagascianpy.utils.utils.Cd(download_folder):
        # Create list of borg extract commands
        borg_cmd_list = []
        for record in records:
            borg_extract_header = wagascianpy.utils.utils.which("borg") + " extract --progress --log-json " \
                                  + "--exclude *.json --exclude *.py --exclude *AcqConfig* " \
                                  + wagasci_repository + "::" + record["name"] + " "
            random_raw_file = random.choice(list(record["raw_files"].values()))
            # Extract whole run folder if all detectors are enabled
            if not overwrite:
                run_root_dir = os.path.join(download_folder, os.path.dirname(random_raw_file).strip('/'))
                if os.path.exists(run_root_dir):
                    continue
            if topology.are_all_enabled() is True:
                borg_extract = borg_extract_header + os.path.dirname(random_raw_file).strip('/')
                borg_cmd_list.append(borg_extract)
                del borg_extract
            else:
                # Else extract only the selected sub-detectors
                borg_extract = "%s%s/%s.xml" \
                               % (borg_extract_header, os.path.dirname(random_raw_file).strip('/'), record["name"])
                borg_cmd_list.append(borg_extract)
                del borg_extract
                borg_extract = "%s%s/%s.log" \
                               % (borg_extract_header, os.path.dirname(random_raw_file).strip('/'), record["name"])
                borg_cmd_list.append(borg_extract)
                del borg_extract
                for dif_id in (str(dif.index) for dif in topology.get_enabled()):
                    borg_extract = borg_extract_header + record["raw_files"][dif_id].strip('/')
                    borg_cmd_list.append(borg_extract)
                    del borg_extract

        # Return if there is nothing to download
        if not borg_cmd_list:
            return download_folder

        # Create download progress window
        print("Starting the download ...")
        if not batch_mode:
            builder = pygubu.Builder()
            builder.add_from_file(viewer.utils.gui_file_finder())
            download_window = builder.get_object('download_window')
            download_label_text = builder.get_variable('download_label_text')
            download_label_text.set("Starting the download ...")
            progress_bar = builder.get_object("progress_bar")
            download_window.update()

        # Print list of commands to file for future reference
        with open(download_folder + "/borg_commands.txt", "w+") as borg_cmd_file:
            borg_cmd_string = '\n'.join(borg_cmd_list)
            borg_cmd_file.write(borg_cmd_string)

        # Actual download
        lost_run = None
        for borg_cmd in borg_cmd_list:
            if lost_run is not None and lost_run in borg_cmd:
                continue
            # Spawn a thread with the download process
            progress = wagascianpy.utils.utils.run_borg_cmd(borg_cmd, check_progress=True)
            countdown = 86400  # one day
            # Monitor the thread for progress
            while True:
                time.sleep(1)
                line = progress.stdout.readline()
                if not line:
                    raise RuntimeError("No answer from borgbackup")
                json_out = json.loads(line.decode('utf-8'))
                # If an error occurs do not block the download of all other runs
                if 'levelname' in json_out and json_out['levelname'] in [u'WARNING', u'ERROR', u'CRITICAL']:
                    if reporter:
                        reporter(exc=None, val=json_out['message'], tb=None)
                    if not batch_mode:
                        download_label_text.set(str(json_out['message']))
                    match = re.search(r"Archive ([\S]+) does not exist", str(json_out['message']))
                    if match is not None and len(match.groups()) >= 1:
                        lost_run = match.group(1)
                    break
                # Print the message in the download window
                if 'message' in json_out:
                    if not batch_mode:
                        download_label_text.set(str(json_out['message']))
                        print(download_label_text.get())
                # Calculate progress
                current = float(json_out['current']) if 'current' in json_out else 0
                total = float(json_out['total']) if 'total' in json_out else 0
                percentage = 100 * current / total if total != 0 else 0
                # Exit loop if the download is finished
                if 'finished' in json_out and json_out['finished'] is True or countdown <= 0:
                    break
                if not batch_mode:
                    progress_bar['value'] = percentage
                countdown -= 1
                # Update the window every second
                download_window.update_idletasks()
        if not batch_mode:
            progress_bar['value'] = 100
            download_label_text.set("Download complete (you may close this window now)")
            del download_label_text
            del progress_bar


# noinspection PyUnboundLocalVariable, PyUnresolvedReferences
def _simple_downloader(records,  # type: List[WagasciRunRecord]
                       wagasci_repository,  # type: str
                       topology,  # type: Topology
                       reporter,  # type: Callable
                       download_folder=None,  # type: Optional[str]
                       batch_mode=False  # type: bool
                       ):
    if ':' in wagasci_repository:
        if len(wagasci_repository.split(':', 1)) != 2:
            raise ValueError("Invalid repository location : %s" % wagasci_repository)
        is_remote_repo = True
    else:
        is_remote_repo = False

    # Create download progress window
    print("Starting the download ...")
    if not batch_mode:
        builder = pygubu.Builder()
        builder.add_from_file(viewer.utils.gui_file_finder())
        download_window = builder.get_object('download_window')
        download_label_text = builder.get_variable('download_label_text')
        download_label_text.set("Starting the download ...")
        progress_bar = builder.get_object("progress_bar")
        download_window.update()

    # Move to download folder
    if not is_remote_repo:
        if not os.path.isdir(wagasci_repository):
            raise EnvironmentError("Local WAGASCI repository not found at %s" % wagasci_repository)

    # List all sources to download
    download_list = []
    for record in records:
        if topology.are_all_enabled() is True:
            source = os.path.join(wagasci_repository, record["name"])
            destination = download_folder
            download_list.append((source, destination))
            print("Copying repository %s into location %s" % (source, destination))
        else:
            destination = os.path.join(download_folder, record["name"])
            source = os.path.join(wagasci_repository, record["name"], record["name"] + ".xml")
            download_list.append((source, destination))
            source = os.path.join(wagasci_repository, record["name"], record["name"] + ".log")
            download_list.append((source, destination))
            for dif in topology.get_enabled():
                source = os.path.join(wagasci_repository, record["name"],
                                      "{}_ecal_dif_{}.raw".format(record["name"], dif.index))
                download_list.append((source, destination))
                source = os.path.join(wagasci_repository, record["name"],
                                      "{}_ecal_dif_{}_tree.root".format(record["name"], dif.index))
                download_list.append((source, destination))
                print("Copying DIF %s into location %s" % (source, destination))

    # Actual download
    with wagascianpy.utils.utils.Cd(download_folder):
        for source, destination in download_list:
            wagascianpy.utils.utils.mkdir_p(destination)
            rsync = wagascianpy.utils.utils.which("rsync")
            if rsync is None:
                raise RuntimeError("rsync program not found")

            if not batch_mode:
                download_label_text.set("Copying {} into the local directory {}".format(source, destination))

            if is_remote_repo:
                cmd_ending = '-essh {} {}'.format(source, destination)
            else:
                cmd_ending = '{} {}'.format(source, destination)

            cmd = 'rsync -avz --progress ' + cmd_ending
            try:
                wagascianpy.utils.utils.mkdir_p(destination)
                proc = subprocess.Popen(cmd,
                                        shell=True,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True
                                        )
            except subprocess.CalledProcessError as exception:
                error_message = "Error while copying the repository {} into the local " \
                                "directory {} : {}".format(source, destination, str(exception))
                _report_error(error_message=error_message, reporter=reporter)

            for line in iter(proc.stdout.readline, ''):
                print(line, end='')
                if '%' in line:
                    progress = re.findall(r'(\d+)%', line)[0]
                    if not batch_mode:
                        progress_bar['value'] = progress
                        # Update the window
                        download_window.update_idletasks()
                elif 'total size is' in line:
                    break

        if not batch_mode:
            progress_bar['value'] = 100
            download_label_text.set("Download complete (you may close this window now)")
            download_window.update_idletasks()
            del download_label_text
            del progress_bar


def _report_error(error_message, reporter=None):
    if reporter:
        reporter(exc=None, val=error_message, tb=None)
    else:
        print(error_message)
