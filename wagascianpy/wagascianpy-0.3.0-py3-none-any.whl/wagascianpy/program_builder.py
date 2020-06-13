#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc
import os
import subprocess

from six import string_types

import wagascianpy.utils

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class ProgramBuilder(ABC):
    """
    The ProgramBuilder interface specifies methods for creating the different parts of
    a program
    """

    def __init__(self):
        self._program = None

    @property
    @abc.abstractmethod
    def program(self):
        pass

    def _add_decoder(self, **kwargs):
        self._program.add_step("decoder", **kwargs)

    def _add_spill_number_fixer(self, **kwargs):
        self._program.add_step("spill_number_fixer", **kwargs)

    def _add_beam_summary_data(self,
                               bsd_database_location,
                               bsd_repository_location,
                               download_bsd_database_location,
                               download_bsd_repository_location,
                               t2krun,
                               **kwargs):
        if ':' in bsd_database_location:
            if len(bsd_database_location.split(':', 1)) != 2:
                raise ValueError("Invalid database location : %s" % bsd_database_location)
            hostname = bsd_database_location.split(':', 1)[0]
            remote_db_path = bsd_database_location.split(':', 1)[-1]
            local_db_path = download_bsd_database_location
            print("Copying remote database %s into location %s" % (remote_db_path, local_db_path))
            wagascianpy.utils.scp_get(hostname, remote_db_path, local_db_path)
        else:
            local_db_path = bsd_database_location
        if not os.path.exists(local_db_path):
            raise EnvironmentError("Local BSD database not found at %s" % local_db_path)

        if ':' in bsd_repository_location:
            if len(bsd_repository_location.split(':', 1)) != 2:
                raise ValueError("Invalid repository location : %s" % bsd_repository_location)
            remote_repo_path = bsd_repository_location
            local_repo_path = download_bsd_repository_location
            print("Copying remote repository %s into location %s" % (remote_repo_path, local_repo_path))
            rsync = wagascianpy.utils.which("rsync")
            if rsync is None:
                raise RuntimeError("rsync program not found")
            try:
                remote = "{}/t2krun{}/*".format(remote_repo_path, t2krun)
                local = "{}/t2krun{}/".format(local_repo_path, t2krun)
                wagascianpy.utils.mkdir_p(local)
                subprocess.check_output([rsync, "-a", "-essh", remote, local])
            except subprocess.CalledProcessError as exception:
                raise RuntimeError("Error while copying the remote repository %s into the "
                                   "local directory %s : %s" % (remote_repo_path, local_repo_path, str(exception)))
        else:
            local_repo_path = bsd_repository_location
        if not os.path.exists(local_repo_path):
            raise EnvironmentError("Local BSD repository not found at %s" % local_repo_path)

        self._program.add_step("beam_summary_data",
                               bsd_database=local_db_path,
                               bsd_repository=local_repo_path,
                               **kwargs)

    def set_run_location(self, run_dict):
        self._program.set_run_location(run_dict)

    def get_run_location(self):
        return self._program.get_run_location()

    def set_save_location(self, save_location):
        if not save_location:
            raise ValueError("Save location cannot be empty")
        if not os.path.exists(save_location):
            raise OSError("Save location does not exist : %s" % save_location)
        save_dict = {}
        if isinstance(save_location, dict):
            save_dict = save_location
        elif isinstance(save_location, string_types):
            run_dict = self._program.get_run_location()
            for run_name in run_dict:
                save_dict[run_name] = os.path.join(save_location, run_name)
        self._program.set_save_location(save_dict)

    def get_save_location(self):
        return self._program.get_save_location()

    def output_dir_same_as_input(self):
        self._program.output_dir_same_as_input()

    def do_not_stop_on_exception(self):
        self._program._stop_on_exception = False

    def stop_on_exception(self):
        self._program._stop_on_exception = True

    def enforce_dependencies(self):
        self._program._enforce_dependencies = True

    def do_not_enforce_dependencies(self):
        self._program._enforce_dependencies = False
