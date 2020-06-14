#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

import json

try:
    # for Python2
    # noinspection PyPep8Naming
    import Tkinter as tkinter
except ImportError:
    # for Python3
    import tkinter

from typing import Type, List

import pygubu
import wagascianpy.database.bsddb
import wagascianpy.database.wagascidb
import wagascianpy.utils.configuration


# noinspection PyArgumentList, PyUnresolvedReferences
def _show_run_info(builder,  # type: Type[wagascianpy.utils.configuration.Configuration]
                   record,  # type: wagascianpy.database.wagascidb.WagasciRunRecord
                   bsd_database  # type: wagascianpy.database.bsddb.BsdDatabase
                   ):
    """Show info about a run record in the run_info frame
    """
    run_info = builder.get_object('run_info')
    for child in run_info.winfo_children():
        child.destroy()

    pot_upper_limit = 0
    pot_lower_limit = 0
    good_bsd_spills_upper_limit = 0
    good_bsd_spills_lower_limit = 0
    neutrino_global_type = wagascianpy.database.bsddb.NeutrinosType.Unknown.name
    if bsd_database:
        try:
            bsd_records = bsd_database.get_time_interval(record["start_time"], record["stop_time"], True, True)
            if bsd_records:
                for bsd_record in bsd_records:
                    pot_upper_limit += int(bsd_record["number_of_pot"])
                    good_bsd_spills_upper_limit += int(bsd_record["number_of_good_spills"])
            bsd_records = bsd_database.get_time_interval(record["start_time"], record["stop_time"], True, False)
            if bsd_records:
                for bsd_record in bsd_records:
                    neutrino_type = wagascianpy.database.bsddb.NeutrinosType(bsd_records[0]["neutrino_type"])
                    if neutrino_type != wagascianpy.database.bsddb.NeutrinosType.Unknown:
                        neutrino_global_type = neutrino_type.name
                    pot_lower_limit += int(bsd_record["number_of_pot"])
                    good_bsd_spills_lower_limit += int(bsd_record["number_of_good_spills"])
        except RuntimeWarning as exception:
            print(str(exception))

    # Run name
    label = tkinter.Label(run_info, text='Run name', padx=5)
    label.grid(row=0, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text=record['name'], padx=5)
    label.grid(row=0, column=1, sticky=tkinter.W)
    # Run number
    label = tkinter.Label(run_info, text='Run number', padx=5)
    label.grid(row=1, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text=record['run_number'], padx=5)
    label.grid(row=1, column=1, sticky=tkinter.W)
    # Run type
    label = tkinter.Label(run_info, text='Run type', padx=5)
    label.grid(row=2, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text=record['run_type'], padx=5)
    label.grid(row=2, column=1, sticky=tkinter.W)
    # Is bad
    label = tkinter.Label(run_info, text='Bad/good run', padx=5)
    label.grid(row=3, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text=record['is_bad'], padx=5)
    label.grid(row=3, column=1, sticky=tkinter.W)
    # Duration
    label = tkinter.Label(run_info, text='Duration (hours)', padx=5)
    label.grid(row=4, column=0, sticky=tkinter.W)
    duration_h = "{0:.2f}".format(float(record['duration_h']), padx=5)
    label = tkinter.Label(run_info, text=duration_h, padx=5)
    label.grid(row=4, column=1, sticky=tkinter.W)
    # Start time
    label = tkinter.Label(run_info, text='Start time', padx=5)
    label.grid(row=5, column=0, sticky=tkinter.W)
    start_time = wagascianpy.database.wagascidb.WagasciRunRecord(record). \
        get_start_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
    label = tkinter.Label(run_info, text=start_time, padx=5)
    label.grid(row=5, column=1, sticky=tkinter.W)
    # Stop time
    label = tkinter.Label(run_info, text='Stop time', padx=5)
    label.grid(row=6, column=0, sticky=tkinter.W)
    stop_time = wagascianpy.database.wagascidb.WagasciRunRecord(record). \
        get_stop_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
    label = tkinter.Label(run_info, text=stop_time, padx=5)
    label.grid(row=6, column=1, sticky=tkinter.W)
    # POTs upper limit
    label = tkinter.Label(run_info, text='POTs (upper limit)', padx=5)
    label.grid(row=7, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text="{:.2e}".format(pot_upper_limit), padx=5)
    label.grid(row=7, column=1, sticky=tkinter.W)
    # POTs lower limit
    label = tkinter.Label(run_info, text='POTs (lower limit)', padx=5)
    label.grid(row=8, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text="{:.2e}".format(pot_lower_limit), padx=5)
    label.grid(row=8, column=1, sticky=tkinter.W)
    # Good BSD spills upper limit
    label = tkinter.Label(run_info, text='Good BSD spills (upper limit)', padx=5)
    label.grid(row=9, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text=str(good_bsd_spills_upper_limit), padx=5)
    label.grid(row=9, column=1, sticky=tkinter.W)
    # Good BSD spills lower limit
    label = tkinter.Label(run_info, text='Good BSD spills (lower limit)', padx=5)
    label.grid(row=10, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text=str(good_bsd_spills_lower_limit), padx=5)
    label.grid(row=10, column=1, sticky=tkinter.W)
    # Neutrino Type
    label = tkinter.Label(run_info, text='Neutrino type', padx=5)
    label.grid(row=11, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text=neutrino_global_type, padx=5)
    label.grid(row=11, column=1, sticky=tkinter.W)
    # Run folder
    label = tkinter.Label(run_info, text='Run folder', padx=5)
    label.grid(row=12, column=0, sticky=tkinter.W)
    label = tkinter.Label(run_info, text=record["run_folder"], padx=5)
    label.grid(row=12, column=1, sticky=tkinter.W)
    # Topology
    label = tkinter.Label(run_info, text='Topology', padx=5)
    label.grid(row=13, column=0, sticky=tkinter.W)
    if record["topology"] in ["", "undef", None]:
        pass
    else:
        topology_dict = json.loads(record['topology'])
        topology_str = ""
        for detector_name, detector_topology in wagascianpy.database.wagascidb.DETECTORS.items():
            found = True
            for dif_id, dif_topology in detector_topology.items():
                if dif_id not in topology_dict or \
                        sorted(topology_dict[dif_id]) != sorted(dif_topology):
                    found = False
            if found:
                topology_str += detector_name + ", "
                label = tkinter.Label(run_info, text=topology_str.rstrip(", "), padx=5, wraplength=1000)
                label.grid(row=13, column=1, sticky=tkinter.W)
                # Raw files
    for i, (dif, raw_file) in enumerate(sorted(record['raw_files'].items()), 14):
        label = tkinter.Label(run_info, text="DIF %s" % dif, padx=5)
        label.grid(row=i, column=0, sticky=tkinter.W)
        label = tkinter.Label(run_info, text=raw_file, padx=5)
        label.grid(row=i, column=1, sticky=tkinter.W)


# noinspection PyUnresolvedReferences
def make_records_table(config,  # type: Type[wagascianpy.utils.configuration.Configuration]
                       builder,  # type: pygubu.Builder
                       records  # type: List[wagascianpy.database.wagascidb.WagasciRunRecord]
                       ):
    # type: (...) -> None
    run_list = builder.get_object('run_list')
    for child in run_list.innerframe.winfo_children():
        child.destroy()
    run_info = builder.get_object('run_info')
    for run_child in run_info.winfo_children():
        run_child.destroy()

    label = tkinter.Label(run_list.innerframe, text='Run name')
    label.grid(row=0, column=0)
    label = tkinter.Label(run_list.innerframe, text='Run number')
    label.grid(row=0, column=1)
    label = tkinter.Label(run_list.innerframe, text='Run type')
    label.grid(row=0, column=2)
    label = tkinter.Label(run_list.innerframe, text='Duration (hours)')
    label.grid(row=0, column=3)
    label = tkinter.Label(run_list.innerframe, text='Start time')
    label.grid(row=0, column=4)
    label = tkinter.Label(run_list.innerframe, text='Stop time')
    label.grid(row=0, column=5)

    try:
        bsd_database = wagascianpy.database.bsddb.BsdDataBase(
            bsd_database_location=config.bsd_database_configuration.bsd_database(),
            bsd_repository_location=config.bsd_database_configuration.bsd_repository(),
            bsd_repository_download_location=config.bsd_database_configuration.bsd_download_location(),
            t2kruns=config.global_configuration.t2krun(),
            update_db=config.viewer_configuration.bsd_update_database(),
            rebuild_db=config.viewer_configuration.bsd_rebuild_database())
    except RuntimeWarning as exception:
        bsd_database = None
        print(str(exception))

    records.sort(key=lambda x: int(x['run_number']))
    for i, record in enumerate(records, 1):
        button = tkinter.Button(run_list.innerframe, text=record['name'],
                                command=lambda rec=record, db=bsd_database: _show_run_info(builder, rec, db))
        button.grid(row=i, column=0)
        label = tkinter.Label(run_list.innerframe, text=record['run_number'])
        label.grid(row=i, column=1)
        label = tkinter.Label(run_list.innerframe, text=record['run_type'])
        label.grid(row=i, column=2)
        duration_h = "{0:.2f}".format(float(record['duration_h']))
        label = tkinter.Label(run_list.innerframe, text=duration_h)
        label.grid(row=i, column=3)
        start_time = wagascianpy.database.wagascidb.WagasciRunRecord(record). \
            get_start_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
        label = tkinter.Label(run_list.innerframe, text=start_time)
        label.grid(row=i, column=4, padx=5)
        stop_time = wagascianpy.database.wagascidb.WagasciRunRecord(record). \
            get_stop_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
        label = tkinter.Label(run_list.innerframe, text=stop_time)
        label.grid(row=i, column=5, padx=5)

    run_list.reposition()
