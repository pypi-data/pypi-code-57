#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

# pylint: disable=broad-except, too-many-instance-attributes, too-many-locals
# pylint: disable=no-self-use, too-many-branches, too-many-statements
# pylint: disable=singleton-comparison, too-many-nested-blocks, arguments-differ

"""WAGASCI simple run database"""
import os
import re
import subprocess
from enum import IntEnum

import wagascianpy.database.db_record
import wagascianpy.database.my_tinydb
import wagascianpy.utils.utils

try:
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError as err:
    if "ROOT" in repr(err):
        ROOT = None
    else:
        raise

###############################################################################
#                                  Constants                                  #
###############################################################################

_NON_PHYSICAL_VALUE = -1


class TriggerTime(IntEnum):
    """ Spill time stamp in second for Epoch (UNIX time) """
    GPS1 = 0
    GPS2 = 1
    RubidiumClock = 2


class GoodSpillFlag(IntEnum):
    """
    =0:Bad
    =1:Good@horn250kA
    =-1:Good@horn-250kA
    =2:Good@horn200kA<
    =100:Good@horn0kA)
    """
    Bad = 0
    GoodHornPlus250kA = 1
    GoodHornMinus250kA = -1
    GoodHornLess200kA = 2
    GoodHorn0kA = 100


class NeutrinosType(IntEnum):
    """ Type of neutrinos in the beam """
    Neutrinos = GoodSpillFlag.GoodHornPlus250kA
    AntiNeutrinos = GoodSpillFlag.GoodHornMinus250kA
    Unknown = GoodSpillFlag.Bad


class RunType(IntEnum):
    """ run type (=1:physic run) """
    PhysicsRun = 1


class HornNumber(IntEnum):
    """ Horn number """
    FirstHorn = 0
    SecondHorn = 1
    ThirdHorn = 2


class HornCurrent(IntEnum):
    """ Horn power supply channel """
    TotalCurrent = 0
    Channel1 = 1
    Channel2 = 2
    Channel3 = 3
    Channel4 = 4


class CTNumber(IntEnum):
    """ CT monitor number """
    First = 0
    Second = 1
    Third = 2
    Fourth = 3
    Fifth = 4


class BunchNumber(IntEnum):
    """ Bunch number """
    TotalCurrent = 0
    First = 1
    Second = 2
    Third = 3
    Fourth = 4
    Fifth = 5
    Sixth = 6
    Seventh = 7
    Eighth = 8


###########################################################################
#                                BsdRecord                                #
###########################################################################

class BsdRecord(wagascianpy.database.db_record.DBRecord):
    """Bsd record"""

    def __init__(self, file_path=None, record=None):
        """Initialize BsdRecord from database record"""
        self.file_path = file_path
        self.name = None
        self.t2k_run = None
        self.main_ring_run = None
        self.main_ring_subrun = None
        self.neutrino_daq_run = None
        self.bsd_version = None

        self.start_time = None
        self.stop_time = None
        self.duration_s = None
        self.duration_h = None
        self.start_spill = None
        self.stop_spill = None
        self.number_of_spills = None
        self.number_of_good_spills = None
        self.number_of_pot = None
        self.mean_pot_per_spill = None
        self.mean_horn_current = None
        self.neutrino_type = None

        super(BsdRecord, self).__init__(record)

        if record is None:
            if not isinstance(self.file_path, str):
                raise RuntimeError("Run path is not a string")

            self.name = os.path.basename(self.file_path)

            try:
                match = re.search(r"\S+t2krun(\d+)/bsd_run(\d{3})(\d{4})_(\d{2})(\D\d{2}).root", self.file_path)
                if match is None or len(match.groups()) != 5:
                    raise ValueError("The BSD file path is not valid : %s" % str(self.file_path))
                self.t2k_run = int(match.group(1))
                self.main_ring_run = int(match.group(2))
                self.neutrino_daq_run = int(match.group(2) + match.group(3))
                self.main_ring_subrun = int(match.group(4))
                self.bsd_version = match.group(5)
            except (IndexError, AttributeError) as exception:
                raise RuntimeError("Failed to parse %s : %s" % (str(self.file_path), str(exception)))
            if ROOT:
                try:
                    self._read_tfile()
                except RuntimeError as exception:
                    print(str(exception))
                    self._set_defaults_if_error()
            else:
                self._set_defaults_if_error()

    def _set_defaults_if_error(self):
        self.start_time = int(_NON_PHYSICAL_VALUE)
        self.stop_time = int(_NON_PHYSICAL_VALUE)
        self.duration_h = float(_NON_PHYSICAL_VALUE)
        self.duration_s = float(_NON_PHYSICAL_VALUE)
        self.start_spill = int(_NON_PHYSICAL_VALUE)
        self.stop_spill = int(_NON_PHYSICAL_VALUE)
        self.number_of_spills = int(_NON_PHYSICAL_VALUE)
        self.number_of_good_spills = int(_NON_PHYSICAL_VALUE)
        self.number_of_pot = int(_NON_PHYSICAL_VALUE)
        self.mean_pot_per_spill = float(_NON_PHYSICAL_VALUE)
        self.mean_horn_current = float(_NON_PHYSICAL_VALUE)
        self.neutrino_type = NeutrinosType.Unknown

    def _read_tfile(self):
        bsd_file = ROOT.TFile.Open(self.file_path)
        if not bsd_file:
            raise RuntimeError("ROOT file %s does not exist or is not valid"
                               % self.file_path)
        bsd_tree = bsd_file.bsd
        if bsd_tree.GetEntries() == 0:
            raise RuntimeError("ROOT file %s is empty" % self.file_path)

        bsd_tree.SetBranchStatus("*", 0)
        bsd_tree.SetBranchStatus("nurun", 1)
        bsd_tree.SetBranchStatus("mrrun", 1)
        bsd_tree.SetBranchStatus("spillnum", 1)
        bsd_tree.SetBranchStatus("trg_sec", 1)
        bsd_tree.SetBranchStatus("ct_pot", 1)
        bsd_tree.SetBranchStatus("hct", 1)
        bsd_tree.SetBranchStatus("good_spill_flag", 1)
        bsd_tree.SetBranchStatus("run_type", 1)

        get_all = 0  # get only active branches
        if bsd_tree.GetEntry(0, get_all) <= 0:
            raise RuntimeError("Failed to read first entry")

        if bsd_tree.nurun != self.neutrino_daq_run:
            raise ValueError("Neutrino DAQ run from TTree ({}) different from one"
                             " from file name ({})".format(bsd_tree.nurun, self.neutrino_daq_run))
        if bsd_tree.mrrun != self.main_ring_run:
            raise ValueError("Main Ring run from TTree ({}) different from one"
                             " from file name ({})".format(bsd_tree.mrrun, self.main_ring_run))

        self.start_spill = bsd_tree.spillnum
        self.start_time = bsd_tree.trg_sec[TriggerTime.RubidiumClock]

        if bsd_tree.GetEntry(bsd_tree.GetEntries() - 1, get_all) <= 0:
            raise RuntimeError("Failed to read last entry")

        self.stop_spill = bsd_tree.spillnum
        self.stop_time = bsd_tree.trg_sec[TriggerTime.RubidiumClock]
        self._set_duration_s()
        self._set_duration_h()

        self.number_of_spills = 0
        self.number_of_good_spills = 0
        self.number_of_pot = 0.0
        self.mean_horn_current = 0.0
        self.mean_pot_per_spill = 0.0
        mean_neutrino_type = 0.0

        for event in bsd_tree:
            self.number_of_spills += 1
            if ((event.good_spill_flag == GoodSpillFlag.GoodHornMinus250kA or
                 event.good_spill_flag == GoodSpillFlag.GoodHornPlus250kA) and
                    event.run_type == RunType.PhysicsRun):
                self.number_of_good_spills += 1
                self.number_of_pot += event.ct_pot[BunchNumber.TotalCurrent]
                # noinspection PyTypeChecker
                self.mean_horn_current += event.hct[HornNumber.FirstHorn * len(HornNumber) + HornCurrent.TotalCurrent]
                mean_neutrino_type += event.good_spill_flag
        if self.number_of_good_spills > 0:
            self.mean_horn_current /= self.number_of_good_spills
            self.mean_pot_per_spill = self.number_of_pot / self.number_of_good_spills
            mean_neutrino_type /= self.number_of_good_spills

        if abs(mean_neutrino_type) < 0.1:
            self.neutrino_type = NeutrinosType.Unknown
        elif abs(mean_neutrino_type - float(NeutrinosType.Neutrinos)) < \
                abs(mean_neutrino_type - float(NeutrinosType.AntiNeutrinos)):
            self.neutrino_type = NeutrinosType.Neutrinos
        else:
            self.neutrino_type = NeutrinosType.AntiNeutrinos

    def _set_duration_s(self):
        """Set the run duration in seconds
        """
        if self.stop_time is None or self.start_time is None:
            raise ValueError("Set start time and stop time before duration")
        self.duration_s = float((self.stop_time - self.start_time))

    def _set_duration_h(self):
        """Set the run duration in hours
        """
        if self.stop_time is None or self.start_time is None:
            raise ValueError("Set start time and stop time before duration")
        self.duration_h = float((self.stop_time - self.start_time) / 3600.0)

    def get_start_datetime(self):
        """Get start datetime
        """
        if self.start_time is None:
            return None
        return self.timestamp2datetime(self.start_time)

    def get_stop_datetime(self):
        """Get stop datetime
        """
        if self.stop_time is None:
            return None
        return self.timestamp2datetime(self.stop_time)


###########################################################################
#                               BsdDataBase                               #
###########################################################################

def _check_records(records):
    """check that all records are sane"""
    for record in records:
        if not isinstance(record, BsdRecord):
            raise ValueError("record is not of type BsdRecord")
        if not record.is_ready():
            raise ValueError("record is not ready to be inserted")


class BsdDataBase(wagascianpy.database.my_tinydb.MyTinyDB):
    """Virtual class to manage a database"""

    def __init__(self,
                 bsd_database_location,
                 bsd_repository_location=None,
                 bsd_repository_download_location=None,
                 t2kruns=10,
                 update_db=False,
                 rebuild_db=False):

        self._repository_location = bsd_repository_location
        if ':' in self._repository_location:
            self._is_remote_repository = True
        else:
            self._is_remote_repository = False
        self._repository_download_location = bsd_repository_download_location
        self._t2kruns = [t2kruns] if isinstance(t2kruns, int) else t2kruns
        super(BsdDataBase, self).__init__(bsd_database_location)
        if rebuild_db:
            self.clear_database()
            self._is_fresh_database = True
        if update_db or rebuild_db:
            self._update_bsd_db()

    def _rsync(self):
        rsync = wagascianpy.utils.utils.which("rsync")
        if rsync is None:
            raise RuntimeError("rsync program not found")
        remote = ""
        local = ""
        try:
            for t2krun in self._t2kruns:
                remote = "{}/t2krun{}/*".format(self._repository_location, t2krun)
                local = "{}/t2krun{}/".format(self._repository_download_location, t2krun)
                if self._is_remote_repository:
                    subprocess.check_output([rsync, "-a", "-essh", remote, local])
                else:
                    subprocess.check_output([rsync, "-a", remote, local])
        except subprocess.CalledProcessError as exception:
            raise RuntimeError("Error while copying the remote repository %s into the "
                               "local directory %s : %s" % (remote, local, str(exception)))

    def _update_bsd_db(self):
        if self._is_remote_repository and not self._repository_download_location:
            raise ValueError("If updating the remote repository you must specify a download path")
        if self._repository_download_location:
            download_location = self._repository_download_location
        else:
            download_location = self._repository_location
        with wagascianpy.utils.utils.Cd(download_location):
            if download_location != self._repository_location:
                # Copy all the remote BSD files into a local folder
                self._rsync()
            # List all the BSD files
            run_list = []
            for root, _, files in os.walk(download_location):
                for file in files:
                    if '.root' in file:
                        run_list.append(os.path.join(root, file))

            run_record_list = []
            # Loop over every BSD file
            for run_path in sorted(run_list):
                if self.has_record(os.path.basename(run_path)):
                    print("Skipping run %s" % run_path)
                    continue
                else:
                    print("Run %s not found in database" % run_path)
                    run_record_list.append(BsdRecord(run_path))

        _check_records(run_record_list)
        self.update_database(run_record_list)

    def get_time_interval(self, datetime_start, datetime_stop, *args, **kwargs):
        """ Get BSD records in an interval of time """
        if self.is_fresh_database():
            raise RuntimeWarning("BSD database is empty")
        timestamp_start = BsdRecord.datetime2timestamp(datetime_start)
        timestamp_stop = BsdRecord.datetime2timestamp(datetime_stop)
        return super(BsdDataBase, self).get_time_interval(timestamp_start, timestamp_stop, *args, **kwargs)

    def pretty_print(self, name):
        """ Print info about a run """
        BsdRecord(self.get_record(name)[0]).pretty_print()
