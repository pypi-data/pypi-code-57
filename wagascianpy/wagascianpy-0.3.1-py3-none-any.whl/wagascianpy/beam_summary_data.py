#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

# Python modules
import operator
import os
import re
from collections import namedtuple
from itertools import islice

# ROOT
import ROOT

# user
import wagascianpy.utils
import wagascianpy.spill
import wagascianpy.database.bsddb
import wagascianpy.database.db_record
import wagascianpy.database.wagascidb

BSD_ERROR_CODE = 1000

_CONVERTION_FACTOR = 0x7FFF
_OFFSET = 1


def _open_wagasci_tree(input_file, mode="READ"):
    tfile = ROOT.TFile.Open(input_file, mode)
    if not tfile:
        raise IOError("ROOT file %s does not exist or is not valid" % input_file)

    raw_tree = getattr(tfile, wagascianpy.utils.extract_raw_tree_name(tfile))

    if raw_tree.GetEntries() == 0:
        raise IOError("Raw data TTree is empty in file %s" % input_file)

    raw_tree.SetBranchStatus("*", 0)
    raw_tree.SetBranchStatus("spill_count", 1)
    raw_tree.SetBranchStatus("spill_mode", 1)
    raw_tree.SetBranchStatus("fixed_spill_number", 1)
    raw_tree.SetBranchStatus("good_spill_flag", 1)
    return raw_tree, tfile


def _set_wagasci_spills(input_file, matched_spills):
    raw_tree, tfile = _open_wagasci_tree(input_file, "UPDATE")
    if tfile.GetListOfKeys().Contains("bsd"):
        for key in tfile.GetListOfKeys():
            if key.GetName() == "bsd":
                tfile.Delete("bsd;{}".format(key.GetCycle()))

    friend_tree = ROOT.TTree("bsd", "BSD information")
    friend_tree.SetDirectory(tfile)
    raw_tree.AddFriend(friend_tree)

    empty_bsd_spill = wagascianpy.spill.SpillFactory.get_spill("bsd")
    array_list = empty_bsd_spill.get_array_list()
    for array_info in array_list:
        friend_tree.Branch(array_info.name, array_info.array, array_info.type_str)

    for event in raw_tree:
        current_spill_number = event.fixed_spill_number
        current_spill_count = event.spill_count
        current_spill_mode = event.spill_mode
        if current_spill_mode != wagascianpy.spill.WAGASCI_SPILL_BEAM_MODE:
            matched_spill = None
        else:
            matched_spill = next((matched_spill for matched_spill in matched_spills
                                  if matched_spill.WagasciSpill.spill_number == current_spill_number and
                                  matched_spill.WagasciSpill.spill_count == current_spill_count), None)
        if matched_spill is None:
            bsd_spill = wagascianpy.spill.SpillFactory.get_spill("bsd")
        else:
            bsd_spill = matched_spill.BsdSpill
        bsd_spill.set_array_list(array_list)
        friend_tree.Fill()

    raw_tree.SetBranchStatus("*", 1)
    friend_tree.Write("", ROOT.TObject.kWriteDelete)
    tfile.Write("", ROOT.TObject.kWriteDelete)
    tfile.Close()


def _get_wagasci_spills(input_file):
    raw_tree, tfile = _open_wagasci_tree(input_file)

    assert (raw_tree.GetUserInfo().FindObject("start_time") not in [ROOT.nullptr, None, 0]), \
        "Start time not found in {} TTree of file {}".format(raw_tree.GetName(), input_file)
    start_time = raw_tree.GetUserInfo().FindObject("start_time").GetVal()
    assert (raw_tree.GetUserInfo().FindObject("stop_time") not in [ROOT.nullptr, None, 0]), \
        "stop time not found in {} TTree of file {}".format(raw_tree.GetName(), input_file)
    stop_time = raw_tree.GetUserInfo().FindObject("stop_time").GetVal()
    dif_id = raw_tree.GetUserInfo().FindObject("dif_id").GetVal()
    print("Run start time %s" % wagascianpy.database.db_record.DBRecord.timestamp2str(start_time))
    print("Run stop time %s" % wagascianpy.database.db_record.DBRecord.timestamp2str(stop_time))
    print("DIF %s" % dif_id)

    wagasci_spills = []
    for event in raw_tree:
        if event.spill_mode != wagascianpy.spill.WAGASCI_SPILL_BEAM_MODE:
            continue
        wagasci_spill = wagascianpy.spill.SpillFactory.get_spill("wagasci")
        wagasci_spill.spill_number = event.fixed_spill_number
        wagasci_spill.spill_count = event.spill_count
        wagasci_spill.converted_spill_number = wagasci_spill.spill_number & _CONVERTION_FACTOR
        wagasci_spill.spill_mode = event.spill_mode
        wagasci_spill.good_spill_flag = event.good_spill_flag
        if wagasci_spill.are_all_defined():
            wagasci_spills.append(wagasci_spill)

    tfile.Close()
    return wagasci_spills, start_time, stop_time


def get_bsd_spills(bsd_database, bsd_repository, t2krun, start_time, stop_time):
    bsd_tree = ROOT.TChain("bsd")
    with wagascianpy.database.bsddb.BsdDataBase(bsd_database, bsd_repository, None, t2krun) as db:
        bsd_records = db.get_time_interval(start_time, stop_time)
        if not bsd_records:
            RuntimeError("Please specify a valid BSD database")
        for bsd_record in sorted(bsd_records, key=operator.itemgetter("name")):
            file_path = bsd_record["file_path"]
            if not os.path.exists(file_path):
                if bsd_repository is None:
                    raise RuntimeError("Please specify a valid BSD local repository")
                file_path = wagascianpy.utils.find_first_match(bsd_record["name"], bsd_repository)
                if file_path is None:
                    raise RuntimeError("Please specify a valid BSD local repository")
            bsd_tree.Add(file_path)

    bsd_tree.SetBranchStatus("*", 0)
    bsd_tree.SetBranchStatus("spillnum", 1)
    bsd_tree.SetBranchStatus("trg_sec", 1)
    bsd_tree.SetBranchStatus("trg_nano", 1)
    bsd_tree.SetBranchStatus("ct_pot", 1)
    bsd_tree.SetBranchStatus("good_spill_flag", 1)

    bsd_spills = []

    for event in bsd_tree:
        # print("Spill number = %s" % event.spillnum)
        # print("POT = %s" % event.ct_pot[BunchNumber.TotalCurrent])
        # print("Is bad spill = %s" % event.good_spill_flag)
        # print("Timestamp = %s" % bsd_tree.trg_sec[TriggerTime.RubidiumClock]

        bsd_spill = wagascianpy.spill.SpillFactory.get_spill("bsd")
        bsd_spill.bsd_spill_number = int(event.spillnum)
        bsd_spill.converted_spill_number = (bsd_spill.bsd_spill_number + _OFFSET) & _CONVERTION_FACTOR
        bsd_spill.pot = float(event.ct_pot[wagascianpy.database.bsddb.BunchNumber.TotalCurrent])
        bsd_spill.timestamp = float(bsd_tree.trg_sec[wagascianpy.database.bsddb.TriggerTime.RubidiumClock])
        bsd_spill.timestamp += float(bsd_tree.trg_nano[wagascianpy.database.bsddb.TriggerTime.RubidiumClock]) / 1e9
        bsd_spill.bsd_good_spill_flag = event.good_spill_flag
        if bsd_spill.are_all_defined():
            bsd_spills.append(bsd_spill)

    return bsd_spills


def _match_spills(wagasci_spills, bsd_spills, start_time, stop_time):
    if not wagasci_spills:
        raise ValueError("WAGASCI spill list is empty")
    if not bsd_spills:
        raise ValueError("BSD spill list is empty")
    if bsd_spills[0].timestamp > start_time:
        ValueError("BSD spill start time %s is greater than WAGASCI one %s" % (bsd_spills[0].timestamp, start_time))
    if bsd_spills[-1].timestamp < stop_time:
        ValueError("BSD spill stop time %s is less than WAGASCI one %s" % (bsd_spills[-1].timestamp, stop_time))

    MatchedSpill = namedtuple('MatchedSpill', ['WagasciSpill', 'BsdSpill'])
    matched_spills = []

    good_spills = (wagasci_spill for wagasci_spill in wagasci_spills
                   if wagasci_spill.good_spill_flag == wagascianpy.spill.IS_GOOD_SPILL and
                   wagasci_spill.spill_mode == wagascianpy.spill.WAGASCI_SPILL_BEAM_MODE)
    starting_index = 0
    for wagasci_spill in good_spills:
        bsd_index = next((index for index, bsd_spill in enumerate(islice(bsd_spills, starting_index, None))
                          if bsd_spill.converted_spill_number == wagasci_spill.converted_spill_number), None)
        if bsd_index is None:
            continue
        bsd_index += starting_index
        matched_spill = MatchedSpill(wagasci_spill, bsd_spills[bsd_index])
        matched_spills.append(matched_spill)
        starting_index = bsd_index
    return matched_spills


###############################################################################
#                             beam_summary_data                               #
###############################################################################

def beam_summary_data(input_path, bsd_database, bsd_repository, t2krun, recursive):
    if not os.path.exists(input_path):
        raise IOError("Input file %s not found" % input_path)
    input_files = []
    if os.path.isfile(input_path):
        input_files.append(input_path)
    if os.path.isdir(input_path):
        if recursive:
            for root, dirs, files in os.walk(input_path):
                for file_name in files:
                    if re.search(r'_ecal_dif_([\d]+)_tree.root$', file_name) is not None:
                        input_files.append(os.path.join(root, file_name))
        else:
            for file_name in os.listdir(input_path):
                if re.search(r'_ecal_dif_([\d]+)_tree.root', file_name).groups() is not None:
                    input_files.append(os.path.join(input_path, file_name))

    if not os.path.exists(bsd_database):
        raise IOError("Beam summary data database %s not found" % bsd_database)

    for input_file in input_files:
        wagasci_spills, start_time, stop_time = _get_wagasci_spills(input_file)
        bsd_spills = get_bsd_spills(bsd_database, bsd_repository, t2krun, start_time, stop_time)
        matched_spills = _match_spills(wagasci_spills, bsd_spills, start_time, stop_time)
        _set_wagasci_spills(input_file, matched_spills)
