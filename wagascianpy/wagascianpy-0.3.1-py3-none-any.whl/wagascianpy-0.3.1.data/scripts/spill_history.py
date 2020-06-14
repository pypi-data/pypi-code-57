#!python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import argparse
import os
import textwrap

import wagascianpy.plotting.detector
import wagascianpy.plotting.marker
import wagascianpy.plotting.plotter
import wagascianpy.plotting.topology
import wagascianpy.utils.utils


def spill_history(plotter):
    plotter.template_plotter()


if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description=textwrap.dedent('''\
                                     Produce spill history plots. If the stop time or stop run is not provided
                                      the present time or the last run are assumed. If both time and run number
                                      are provided the run number is preferred.'''))

    PARSER.add_argument('-n', '--output-string', metavar='<output string>', dest='output_string',
                        type=str, nargs=1, required=False, help=textwrap.dedent('''\
                        Output string to prepend to the file names
                        '''))

    PARSER.add_argument('-o', '--output-path', metavar='<output path>', dest='output_file_path',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Directory where to save the output plots
                        '''))

    PARSER.add_argument('-f', '--wagasci-runs-dir', metavar='<WAGASCI runs directory>', dest='wagasci_runs_dir',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the directory containing all the WAGASCI decoded runs.
                        '''))

    PARSER.add_argument('-d', '--wagasci-database', metavar='<WAGASCI run database>', dest='wagasci_database',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the WAGASCI run database file. This file is created by the 
                        Wagasci Database Viewer (wagascidb_viewer.py) program and is usually called wagascidb.db.
                        '''))

    PARSER.add_argument('-b', '--bsd-database', metavar='<BSD database>', dest='bsd_database',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the BSD database file. This file is created by the Wagasci Database Viewer
                         (wagascidb_viewer.py) program and is usually called bsddb.db.
                        '''))

    PARSER.add_argument('-g', '--bsd-files-dir', metavar='<BSD files directory>', dest='bsd_files_dir',
                        type=str, nargs=1, required=True, help=textwrap.dedent('''\
                        Path to the directory containing all the BSD root files.
                        '''))

    PARSER.add_argument('-at', '--start-time', metavar='<start time>', dest='start_time', type=str,
                        nargs=1, help='Start date and time in the format "%%Y/%%m/%%d %%H:%%M:%%S"', default=None,
                        required=False)

    PARSER.add_argument('-ot', '--stop-time', metavar='<stop time>', dest='stop_time', type=str,
                        nargs=1, help='Stop date and time in the format "%%Y/%%m/%%d %%H:%%M:%%S"', default=None,
                        required=False)

    PARSER.add_argument('-ar', '--start-run', metavar='<start run>', dest='start_run', type=int,
                        nargs=1, help='start run number', default=None, required=False)

    PARSER.add_argument('-or', '--stop-run', metavar='<stop run>', dest='stop_run', type=int,
                        nargs=1, help='Stop run number', default=None, required=False)

    PARSER.add_argument('-t', '--t2krun', metavar='<T2K run>', dest='t2krun', type=int,
                        nargs=1, help='T2K run number (default is 10)', default=10, required=False)

    PARSER.add_argument('-dp', '--delivered-pot', dest='delivered_pot', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the POT delivered by the beam line in the selected interval of time (or runs)'''))

    PARSER.add_argument('-ap', '--accumulated-pot', dest='accumulated_pot', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the POT accumulated by the WAGASCI detectors in the selected interval of time (or 
                        runs)'''))

    PARSER.add_argument('-bs', '--bsd-spill', dest='bsd_spill', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the BSD spill number in the selected interval of time (or runs)'''))

    PARSER.add_argument('-wsh', '--wagasci-spill-history', dest='wagasci_spill_history', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the WAGASCI spill number history in time for the selected interval of time (or 
                        runs)'''))

    PARSER.add_argument('-wsn', '--wagasci-spill-number', dest='wagasci_spill_number', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the WAGASCI spill number for the selected interval of time (or runs)'''))

    PARSER.add_argument('-wfs', '--wagasci-fixed-spill', dest='wagasci_fixed_spill', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the WAGASCI fixed spill number in the selected interval of time (or runs)'''))

    PARSER.add_argument('-th', '--temperature', dest='temperature', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the WAGASCI and WallMRD temperature in the selected interval of time (or runs)'''))

    PARSER.add_argument('-hh', '--humidity', dest='humidity', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot the WAGASCI and WallMRD humidity in the selected interval of time (or runs)'''))

    PARSER.add_argument('-all', '--all', dest='all', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''\
                        If set plot all available plots are produced for the selected interval of time (or runs)'''))

    PARSER.add_argument('-mr', '--run-markers', dest='run_markers', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''If set the WAGASCI runs are marked'''))

    PARSER.add_argument('-mm', '--maintenance-markers', dest='maintenance_markers', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''If set the maintenance days are marked'''))

    PARSER.add_argument('-mt', '--trouble-markers', dest='trouble_markers', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''If set the electronics and DAQ trouble events are 
                        marked'''))

    PARSER.add_argument('-tf', '--save-tfile', dest='save_tfile', required=False, default=False,
                        action='store_true', help=textwrap.dedent('''If set save the TCanvas inside a ROOT file'''))

    ARGS = PARSER.parse_args()

    if isinstance(ARGS.output_string, list):
        ARGS.output_string = ARGS.output_string[0]
    OUTPUT_STRING = ARGS.output_string + '_' if ARGS.output_string else None

    if isinstance(ARGS.output_file_path, list):
        ARGS.output_file_path = ARGS.output_file_path[0]
    OUTPUT_PATH = ARGS.output_file_path

    if isinstance(ARGS.wagasci_runs_dir, list):
        ARGS.wagasci_runs_dir = ARGS.wagasci_runs_dir[0]
    WAGASCI_RUNS_DIR = ARGS.wagasci_runs_dir

    if isinstance(ARGS.wagasci_database, list):
        ARGS.wagasci_database = ARGS.wagasci_database[0]
    WAGASCI_DATABASE = ARGS.wagasci_database

    if isinstance(ARGS.bsd_database, list):
        ARGS.bsd_database = ARGS.bsd_database[0]
    BSD_DATABASE = ARGS.bsd_database

    if isinstance(ARGS.bsd_files_dir, list):
        ARGS.bsd_files_dir = ARGS.bsd_files_dir[0]
    BSD_FILES_DIR = ARGS.bsd_files_dir

    if isinstance(ARGS.start_time, list):
        ARGS.start_time = ARGS.start_time[0]
    START_TIME = ARGS.start_time

    if isinstance(ARGS.stop_time, list):
        ARGS.stop_time = ARGS.stop_time[0]
    STOP_TIME = ARGS.stop_time

    if isinstance(ARGS.start_run, list):
        ARGS.start_run = ARGS.start_run[0]
    START_RUN = ARGS.start_run

    if isinstance(ARGS.stop_run, list):
        ARGS.stop_run = ARGS.stop_run[0]
    STOP_RUN = ARGS.stop_run

    if isinstance(ARGS.t2krun, list):
        ARGS.t2krun = ARGS.t2krun[0]
    T2KRUN = ARGS.t2krun

    START = START_RUN if START_RUN else START_TIME
    STOP = STOP_RUN if STOP_RUN else STOP_TIME

    DELIVERED_POT = ARGS.delivered_pot
    ACCUMULATED_POT = ARGS.accumulated_pot
    BSD_SPILL = ARGS.bsd_spill
    WAGASCI_SPILL_HISTORY = ARGS.wagasci_spill_history
    WAGASCI_SPILL_NUMBER = ARGS.wagasci_spill_number
    WAGASCI_FIXED_SPILL = ARGS.wagasci_fixed_spill
    TEMPERATURE = ARGS.temperature
    HUMIDITY = ARGS.humidity
    ALL = ARGS.all

    RUN_MARKERS = ARGS.run_markers
    MAINTENANCE_MARKERS = ARGS.maintenance_markers
    TROUBLE_MARKERS = ARGS.trouble_markers

    MARKERS = wagascianpy.plotting.marker.MarkerTuple(
        run=RUN_MARKERS,
        maintenance=MAINTENANCE_MARKERS,
        trouble=TROUBLE_MARKERS)

    SAVE_TFILE = ARGS.save_tfile

    print(ARGS)

    if not os.path.exists(OUTPUT_PATH):
        wagascianpy.utils.utils.mkdir_p(OUTPUT_PATH)

    if DELIVERED_POT or ALL:
        spill_history(wagascianpy.plotting.plotter.BsdPotPlotter(
            output_file_path=os.path.join(OUTPUT_PATH, "{}bsd_pot_history.pdf".format(OUTPUT_STRING)),
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            t2krun=T2KRUN,
            start=START,
            stop=STOP,
            enabled_markers=MARKERS,
            save_tfile=SAVE_TFILE))

    if ACCUMULATED_POT or ALL:
        spill_history(wagascianpy.plotting.plotter.WagasciPotPlotter(
            output_file_path=os.path.join(OUTPUT_PATH, "{}wagasci_pot_history.pdf".format(OUTPUT_STRING)),
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            wagasci_repository=WAGASCI_RUNS_DIR,
            t2krun=T2KRUN,
            start=START,
            stop=STOP,
            enabled_markers=MARKERS,
            save_tfile=SAVE_TFILE))

    if BSD_SPILL or ALL:
        spill_history(wagascianpy.plotting.plotter.BsdSpillPlotter(
            output_file_path=os.path.join(OUTPUT_PATH, "{}bsd_spill_history.pdf".format(OUTPUT_STRING)),
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            t2krun=T2KRUN,
            start=START,
            stop=STOP,
            enabled_markers=MARKERS,
            save_tfile=SAVE_TFILE))

    if WAGASCI_SPILL_HISTORY or ALL:
        for detector in wagascianpy.plotting.topology.Topology():
            topology = wagascianpy.plotting.topology.Topology()
            topology.disable_all_but(detector.name)
            detector_name = detector.name.lower().replace(' ', '_')
            spill_history(wagascianpy.plotting.plotter.WagasciSpillHistoryPlotter(
                output_file_path=os.path.join(OUTPUT_PATH, "{}wagasci_spill_history_{}.pdf".format(OUTPUT_STRING,
                                                                                                   detector_name)),
                bsd_database=BSD_DATABASE,
                bsd_repository=BSD_FILES_DIR,
                wagasci_database=WAGASCI_DATABASE,
                wagasci_repository=WAGASCI_RUNS_DIR,
                t2krun=T2KRUN,
                start=START,
                stop=STOP,
                enabled_markers=MARKERS,
                topology=topology,
                save_tfile=SAVE_TFILE))

    if WAGASCI_FIXED_SPILL or ALL:
        for detector in wagascianpy.plotting.topology.Topology():
            topology = wagascianpy.plotting.topology.Topology()
            topology.disable_all_but(detector.name)
            detector_name = detector.name.lower().replace(' ', '_')
            spill_history(wagascianpy.plotting.plotter.WagasciFixedSpillPlotter(
                output_file_path=os.path.join(
                    OUTPUT_PATH, "{}wagasci_fixed_spill_history_{}.pdf".format(OUTPUT_STRING, detector_name)),
                bsd_database=BSD_DATABASE,
                bsd_repository=BSD_FILES_DIR,
                wagasci_database=WAGASCI_DATABASE,
                wagasci_repository=WAGASCI_RUNS_DIR,
                t2krun=T2KRUN,
                start=START,
                stop=STOP,
                enabled_markers=MARKERS,
                topology=topology,
                save_tfile=SAVE_TFILE))

    if WAGASCI_SPILL_NUMBER or ALL:
        for detector in wagascianpy.plotting.topology.Topology():
            topology = wagascianpy.plotting.topology.Topology()
            topology.disable_all_but(detector.name)
            detector_name = detector.name.lower().replace(' ', '_')
            spill_history(wagascianpy.plotting.plotter.WagasciSpillNumberPlotter(
                output_file_path=os.path.join(OUTPUT_PATH, "{}wagasci_spill_number_{}.pdf".format(OUTPUT_STRING,
                                                                                                  detector_name)),
                bsd_database=BSD_DATABASE,
                bsd_repository=BSD_FILES_DIR,
                wagasci_database=WAGASCI_DATABASE,
                wagasci_repository=WAGASCI_RUNS_DIR,
                t2krun=T2KRUN,
                start=START,
                stop=STOP,
                enabled_markers=MARKERS,
                topology=topology,
                save_tfile=SAVE_TFILE))

    if TEMPERATURE or ALL:
        spill_history(wagascianpy.plotting.plotter.TemperaturePlotter(
            output_file_path=os.path.join(
                OUTPUT_PATH, "{}wagasci_temperature_history.pdf".format(OUTPUT_STRING)),
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            wagasci_repository=WAGASCI_RUNS_DIR,
            t2krun=T2KRUN,
            start=START,
            stop=STOP,
            enabled_markers=MARKERS,
            topology=wagascianpy.plotting.topology.Topology(iterate_by_dif=True),
            save_tfile=SAVE_TFILE))

    if HUMIDITY or ALL:
        spill_history(wagascianpy.plotting.plotter.HumidityPlotter(
            output_file_path=os.path.join(
                OUTPUT_PATH, "{}wagasci_humidity_history.pdf".format(OUTPUT_STRING)),
            bsd_database=BSD_DATABASE,
            bsd_repository=BSD_FILES_DIR,
            wagasci_database=WAGASCI_DATABASE,
            wagasci_repository=WAGASCI_RUNS_DIR,
            t2krun=T2KRUN,
            start=START,
            stop=STOP,
            enabled_markers=MARKERS,
            topology=wagascianpy.plotting.topology.Topology(iterate_by_dif=True),
            save_tfile=SAVE_TFILE))
