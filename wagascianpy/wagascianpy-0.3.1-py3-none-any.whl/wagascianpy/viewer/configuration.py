#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright 2020 pintaudi giorgio
#

import argparse
import sys
import time

from wagascianpy.utils.configuration import *
import wagascianpy.utils.environment


def fill_configuration(args=None):
    # type: (Optional[[argparse.Namespace, Dict[str, Any]]]) -> None

    if args is None:
        args = {'batch_mode': False}

    if isinstance(args, argparse.Namespace):
        args = vars(args)

    batch_mode = args["batch_mode"]

    if batch_mode:
        # WAGASCI database configuration
        wagasci_database = args["wagasci_database"]
        wagasci_repository = args["wagasci_repository"]
        wagasci_download_location = args["wagasci_download_location"]
        wagasci_decoded_location = args["wagasci_decoded_location"]
        borg_wagasci_repository = args["borg_wagasci_repository"]
        simple_wagasci_repository = args["simple_wagasci_repository"]
        # BSD database configuration
        bsd_repository = args["bsd_repository"]
        bsd_database = args["bsd_database"]
        bsd_download_location = args["bsd_download_location"]
        # global configuration
        t2krun = args["t2krun"]
        data_quality_location = args["data_quality_location"]
        # temperature configuration
        temperature_sqlite_database = args["temperature_sqlite_database"]
        # viewer volatile configuration
        update_wagasci_database = args["update_wagasci_database"]
        rebuild_wagasci_database = args["rebuild_wagasci_database"]
        update_bsd_database = args["update_bsd_database"]
        rebuild_bsd_database = args["rebuild_bsd_database"]
        wagasci_libdir = args["wagasci_libdir"]
        only_good_runs = args["only_good_runs"]
        include_overlapping = args["include_overlapping"]
        # analyzers
        download = args["download"]
        decoder = args["decoder"]
        spill_number_fixer = args["spill_number_fixer"]
        beam_summary_data = args["beam_summary_data"]
        temperature = args["temperature"]
        data_quality = args["data_quality"]
        all_analyzers = args["all_analyzers"]
        overwrite_flag = args["overwrite_flag"]
        # run selectors
        start_time = args["start_time"]
        stop_time = args["stop_time"]
        start_run = args["start_run"]
        stop_run = args["stop_run"]
    else:
        # WAGASCI database configuration
        wagasci_database = None
        wagasci_repository = None
        wagasci_download_location = None
        wagasci_decoded_location = None
        borg_wagasci_repository = None
        simple_wagasci_repository = None
        # BSD database configuration
        bsd_repository = None
        bsd_database = None
        bsd_download_location = None
        # global configuration
        t2krun = None
        data_quality_location = None
        # temperature configuration
        temperature_sqlite_database = None
        # viewer volatile configuration
        update_wagasci_database = None
        rebuild_wagasci_database = None
        update_bsd_database = None
        rebuild_bsd_database = None
        wagasci_libdir = None
        only_good_runs = None
        include_overlapping = None
        # analyzers
        download = None
        decoder = None
        spill_number_fixer = None
        beam_summary_data = None
        temperature = None
        data_quality = None
        all_analyzers = None
        overwrite_flag = None
        # run selectors
        start_time = None
        stop_time = None
        start_run = None
        stop_run = None

    # sanity checks
    if int(bool(borg_wagasci_repository)) + int(bool(simple_wagasci_repository)) == 2:
        raise ValueError("cannot select both --borg-wagasci-repository and --simple-wagasci-repository")
    get_time_interval = False
    get_run_interval = False
    get_all = False
    if start_time:
        if not stop_time:
            raise ValueError("please select stop time using --stop-time")
        get_time_interval = True
    elif start_run:
        if not stop_run:
            stop_run = start_run
        get_run_interval = True
    else:
        get_all = True
    if all_analyzers:
        decoder = spill_number_fixer = beam_summary_data = temperature = data_quality = True

    # WAGASCI library directory
    if not wagasci_libdir:
        try:
            env = wagascianpy.utils.environment.WagasciEnvironment()
            wagasci_libdir = env["WAGASCI_LIBDIR"]
        except KeyError:
            pass

    # wagasci database configuration
    if not wagasci_database:
        wagasci_database = Configuration.wagasci_database_configuration.wagasci_database()
    if not wagasci_repository:
        wagasci_repository = Configuration.wagasci_database_configuration.wagasci_repository()
    if not wagasci_download_location:
        wagasci_download_location = Configuration.wagasci_database_configuration.wagasci_download_location()
    if not wagasci_decoded_location:
        wagasci_decoded_location = Configuration.wagasci_database_configuration.wagasci_decoded_location()
    if borg_wagasci_repository:
        repository_type = RepositoryType.Borg
    elif simple_wagasci_repository:
        repository_type = RepositoryType.Simple
    else:
        repository_type = Configuration.wagasci_database_configuration.repository_type()

    # bsd database configuration
    if not bsd_database:
        bsd_database = Configuration.bsd_database_configuration.bsd_database()
    if not bsd_repository:
        bsd_repository = Configuration.bsd_database_configuration.bsd_repository()
    if not bsd_download_location:
        bsd_download_location = Configuration.bsd_database_configuration.bsd_download_location()

    # global configuration
    if not t2krun:
        t2krun = Configuration.global_configuration.t2krun()
    if not data_quality_location:
        data_quality_location = Configuration.global_configuration.data_quality_location()

    # temperature configuration
    if not temperature_sqlite_database:
        temperature_sqlite_database = Configuration.temperature_configuration.temperature_sqlite_database()

    # WAGASCI database configuration
    Configuration.wagasci_database_configuration.override({
        'wagasci_database': wagasci_database,
        'wagasci_repository': wagasci_repository,
        'wagasci_download_location': wagasci_download_location,
        'wagasci_decoded_location': wagasci_decoded_location,
        'repository_type': repository_type
    })

    # BSD database configuration
    Configuration.bsd_database_configuration.override({
        'bsd_repository': bsd_repository,
        'bsd_database': bsd_database,
        'bsd_download_location': bsd_download_location
    })

    # global configuration
    Configuration.global_configuration.override({
        't2krun': t2krun,
        'data_quality_location': data_quality_location
    })

    # temperature configuration
    Configuration.temperature_configuration.override({
        'temperature_sqlite_database': temperature_sqlite_database
    })

    # viewer configuration
    Configuration.create_section('viewer_configuration')
    Configuration.viewer_configuration.override({
        'batch_mode': batch_mode,
        'update_wagasci_database': update_wagasci_database,
        'rebuild_wagasci_database': rebuild_wagasci_database,
        'update_bsd_database': update_bsd_database,
        'rebuild_bsd_database': rebuild_bsd_database,
        'wagasci_libdir': wagasci_libdir,
        'only_good_runs': only_good_runs,
        'include_overlapping': include_overlapping
    })

    # analyzers configuration
    Configuration.create_section('analyzer_configuration')
    Configuration.analyzer_configuration.override({
        'download': download,
        'decoder': decoder,
        'spill_number_fixer': spill_number_fixer,
        'beam_summary_data': beam_summary_data,
        'temperature': temperature,
        'data_quality': data_quality,
        'all_analyzers': all_analyzers,
        'overwrite_flag': overwrite_flag
    })

    # run selectors
    Configuration.create_section('run_select_configuration')
    Configuration.run_select_configuration.override({
        'get_time_interval': get_time_interval,
        'get_run_interval': get_run_interval,
        'get_all': get_all,
        'start_time': start_time,
        'stop_time': stop_time,
        'start_run': start_run,
        'stop_run': stop_run
    })

    print("CONFIGURATION\n")
    Configuration.dump()
    sys.stdout.flush()
    time.sleep(1)
