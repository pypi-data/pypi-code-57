#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

""" Module to manage a database created with tinydb """
import operator
import os
from datetime import datetime
from random import seed, randint
import abc

from scp import SCPException
import tinydb

import wagascianpy.utils.utils

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

_TMP_DIR = "/tmp"


###############################################################################
#                                   MyTinyDB                                  #
###############################################################################

# noinspection PyPep8
class MyTinyDB(ABC):
    """Wrapper class around the tinyDB database"""

    _tmp_dir = _TMP_DIR

    def __init__(self, db_location):

        # If the database resides in a remote location, copy it locally for ease
        # and speed of handling

        self._is_remote_db = False
        self._hostname = None
        self._remote_db_path = None
        self._local_db_path = None
        self._database = None
        self._is_fresh_database = False
        self._write_to_remote = False

        seed(datetime.now())
        if ':' in db_location:
            self._is_remote_db = True
            if len(db_location.split(':', 1)) != 2:
                raise ValueError("Invalid database location : %s" % db_location)
            self._hostname = db_location.split(':', 1)[0]
            self._remote_db_path = db_location.split(':', 1)[-1]
            self._local_db_path = os.path.join(
                self._tmp_dir, str(randint(10000, 99999)) + ".db")
            try:
                print("Copying remote database %s into location %s"
                      % (self._remote_db_path, self._local_db_path))
                wagascianpy.utils.utils.scp_get(self._hostname, self._remote_db_path,
                                                self._local_db_path)
                print("Database found in remote location")
                print("Remote database copied to local location : "
                      "{}".format(self._local_db_path))
                print("Database size is %d kB" % int(os.path.getsize(self._local_db_path) / 1024))
            except SCPException as error:
                print("Creating a new database because not found in remote location : %s" % str(error))
                self._is_fresh_database = True
        else:
            self._local_db_path = db_location
            if not os.path.exists(self._local_db_path):
                print("Creating a new database because not found in local location")
                self._is_fresh_database = True
            print("using local database : %s" % self._local_db_path)

        # Open the tinydb database
        print("Opening database %s" % self._local_db_path)
        self._database = tinydb.TinyDB(self._local_db_path)

    def is_fresh_database(self):
        """ Return true if the database is empty """
        return self._is_fresh_database

    def update_database(self, run_record_list):
        """ Update the tinydb database """
        for run_record in run_record_list:
            if not self.has_record(run_record.name):
                print("Inserting run %s into database" % run_record.name)
                self.insert(run_record.make_record())
        self._is_fresh_database = False
        if self._is_remote_db:
            self._write_to_remote = True

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.__del__()

    def __del__(self):
        if hasattr(self, "_database") and self._database is not None:
            self._database.close()
            self._database = None

        if hasattr(self, "_is_remote_db") and self._is_remote_db:
            if None in [self._hostname, self._remote_db_path, self._local_db_path]:
                print("Remote database location is not properly set up.")
            else:
                try:
                    if hasattr(self, "_write_to_remote") and self._write_to_remote \
                            and os.path.exists(self._local_db_path):
                        print("Writing local database %s to remote location %s"
                              % (self._local_db_path, self._remote_db_path))
                        wagascianpy.utils.utils.scp_put(self._hostname, self._local_db_path,
                                                        self._remote_db_path)
                except SCPException as error:
                    print("Could not push the database to the remote "
                          "location : {}".format(str(error)))
                    print("Temporary local database is saved here : "
                          "%s" % self._local_db_path)
                else:
                    if os.path.exists(self._local_db_path):
                        os.remove(self._local_db_path)

    def insert(self, record):
        """Insert record into database"""
        self._database.insert(record)

    def remove(self, record):
        """Remove a record from the database
        """
        run = tinydb.Query()
        self._database.remove(run.name == record['name'])

    def has_record(self, name):
        """Return True if the run name is in the database
        """
        run = tinydb.Query()
        return len(self._database.search(run.name == name)) > 0

    def _check_field(self, field_name):
        run = tinydb.Query()
        if not self._database.search(run[field_name].exists()):
            raise ValueError("Field with name %s does not exist" % field_name)

    def _has_field(self, field_name):
        run = tinydb.Query()
        if not self._database.search(run[field_name].exists()):
            return False
        return True

    def get_duration_less_than(self, duration_h, only_good=True):
        """Return all the records with duration less than duration_h"""
        duration_h = float(duration_h)
        run = tinydb.Query()
        self._check_field("duration_h")
        if only_good and self._has_field("is_bad"):
            return self._database.search((run.duration_h <= duration_h) &
                                         (run.is_bad == False))
        return self._database.search(run.duration_h <= duration_h)

    def get_duration_greater_than(self, duration_h, only_good=True):
        """Return all the records with duration greater than duration_h"""
        self._check_field("duration_h")
        duration_h = float(duration_h)
        run = tinydb.Query()
        if only_good and self._has_field("is_bad"):
            return self._database.search((run.duration_h >= duration_h) &
                                         (run.is_bad == False))
        return self._database.search(run.duration_h >= duration_h)

    def get_all(self, only_good=True):
        """Return all records
        """
        if only_good and self._has_field("is_bad"):
            run = tinydb.Query()
            return self._database.search(run.is_bad == False)
        return self._database.all()

    def get_record(self, name):
        """Print info about run with name
        """
        run = tinydb.Query()
        return self._database.search(run.name == name)

    def get_time_interval(self, timestamp_start, timestamp_stop,
                          only_good=True, include_overlapping=True):
        """ Get records in a certain interval of time """
        self._check_field("start_time")
        self._check_field("stop_time")
        run = tinydb.Query()
        if only_good and self._has_field("is_bad") and not include_overlapping:
            matched_records = self._database.search((run.start_time >= timestamp_start) &
                                                    (run.stop_time <= timestamp_stop) &
                                                    (run.is_bad == False))
        elif only_good and self._has_field("is_bad") and include_overlapping:
            matched_records = self._database.search((run.start_time <= timestamp_stop) &
                                                    (run.stop_time >= timestamp_start) &
                                                    (run.is_bad == False))
        elif include_overlapping:
            matched_records = self._database.search((run.start_time <= timestamp_stop) &
                                                    (run.stop_time >= timestamp_start))
        else:
            matched_records = self._database.search((run.start_time >= timestamp_start) &
                                                    (run.stop_time <= timestamp_stop))
        return sorted(matched_records, key=operator.itemgetter("start_time"))

    def get_run_interval(self, run_number_start, run_number_stop, only_good=True):
        """ Get records in a certain interval of run numbers """
        self._check_field("run_number")
        run = tinydb.Query()
        if only_good and self._has_field("is_bad"):
            matched_records = self._database.search((run.run_number >= run_number_start) &
                                                    (run.run_number <= run_number_stop) &
                                                    (run.is_bad == False))
        else:
            matched_records = self._database.search((run.run_number >= run_number_start) &
                                                    (run.run_number <= run_number_stop))
        return sorted(matched_records, key=operator.itemgetter("start_time"))

    def set_tmp_dir(self, path):
        """Set temporary directory path"""
        self._tmp_dir = path

    def get_last_run_number(self, only_good=True):
        self._check_field("run_number")
        run = tinydb.Query()
        if only_good and self._has_field("is_bad"):
            records = self._database.search((run.run_number.exists()) & (run.is_bad == False))
        else:
            records = self._database.search(run.run_number.exists())
        if records is None:
            return None
        seq = [int(record["run_number"]) for record in records]
        return max(seq)

    def clear_database(self):
        if hasattr(self._database, "drop_tables"):
            self._database.drop_tables()
        elif hasattr(self._database, "purge_tables"):
            self._database.purge_tables()
        else:
            raise NotImplementedError("Cannot clear the database")
