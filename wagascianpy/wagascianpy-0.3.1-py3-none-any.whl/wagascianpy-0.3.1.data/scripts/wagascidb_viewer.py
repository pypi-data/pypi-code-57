#!python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#
import sys
from typing import Optional, Type

from wagascianpy.utils.configuration import Configuration, RepositoryType

try:
    # for Python2
    # noinspection PyPep8Naming
    import Tkinter as tkinter
except ImportError:
    # for Python3
    import tkinter
from tkinter import messagebox

import pygubu

import wagascianpy.database.bsddb
import wagascianpy.database.db_record
import wagascianpy.database.wagascidb
import wagascianpy.program.program_builder
import wagascianpy.utils.environment
import wagascianpy.utils.utils

import wagascianpy.viewer.downloader
import wagascianpy.viewer.show_run_info
import wagascianpy.viewer.topology
import wagascianpy.viewer.utils
import wagascianpy.viewer.parse_args
import wagascianpy.viewer.configuration


class Application(object):
    """Main GUI application
    """

    def __init__(self, config):
        # type: (Type[Configuration]) -> None

        # private attributes
        self._config = config
        self._batch_mode = self._config.viewer_configuration.batch_mode()
        self._records = None
        self._topology = wagascianpy.viewer.topology.Topology()

        if not self._batch_mode:
            self._build_gui()

    def _build_gui(self):
        # 1: Create a builder
        self._builder = pygubu.Builder()

        # 2: Load an gui.ui file
        self._builder.add_from_file(wagascianpy.viewer.utils.gui_file_finder())

        # 3: Create the widget using a master as parent
        self._mainwindow = self._builder.get_object('mainwindow')

        # 4: Connect method callbacks
        self._builder.connect_callbacks(self)

        # 5: override report_callback_exception method
        # tkinter.Tk.report_callback_exception = self._report_callback_exception

        # 6: set default values
        self._builder.get_object('wallmrd_top_north').invoke()
        self._builder.get_object('wallmrd_bottom_north').invoke()
        self._builder.get_object('wallmrd_top_south').invoke()
        self._builder.get_object('wallmrd_bottom_south').invoke()
        self._builder.get_object('wagasci_top_upstream').invoke()
        self._builder.get_object('wagasci_side_upstream').invoke()
        self._builder.get_object('wagasci_top_downstream').invoke()
        self._builder.get_object('wagasci_side_downstream').invoke()

        # WAGASCI database configuration
        self._builder.get_object('wagasci_repository').set(
            self._config.wagasci_database_configuration.wagasci_repository())
        self._builder.get_object('wagasci_database').set(
            self._config.wagasci_database_configuration.wagasci_database())
        self._builder.get_object('wagasci_download_location').set(
            self._config.wagasci_database_configuration.wagasci_download_location())
        self._builder.get_object('wagasci_decoded_location').set(
            self._config.wagasci_database_configuration.wagasci_decoded_location())
        if self._config.wagasci_database_configuration.repository_type() == RepositoryType.Simple:
            self._builder.get_object('simple_repository').invoke()
        elif self._config.wagasci_database_configuration.repository_type() == RepositoryType.Borg:
            self._builder.get_object('borg_repository').invoke()
        else:
            print("Repository type not recognized : %s" % self._config.wagasci_database_configuration.repository_type())

        # BSD database configuration
        self._builder.get_object('bsd_repository').set(
            self._config.bsd_database_configuration.bsd_repository())
        self._builder.get_object('bsd_database').set(
            self._config.bsd_database_configuration.bsd_database())
        self._builder.get_object('bsd_download_location').set(
            self._config.bsd_database_configuration.bsd_download_location())

        # Global configuration
        self._builder.get_object('t2krun').set(self._config.global_configuration.t2krun())
        self._builder.get_object('data_quality_location').set(
            self._config.global_configuration.data_quality_location())

        # Temperature configuration
        self._builder.get_object('temperature_sqlite_database').set(
            self._config.temperature_configuration.temperature_sqlite_database())

        # Viewer configuration
        self._builder.get_object('only_good_runs').invoke()
        self._builder.get_object('include_overlapping').invoke()

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def _report_callback_exception(self, exc, val, tb):
        """Report exceptions to the user
        """
        messagebox.showerror('Exception', message=str(val))

    def _get_generic_members(self):
        """Read each member
        """
        # WAGASCI database configuration
        wagasci_repository = self._builder.get_object('wagasci_repository').get()
        wagasci_database = self._builder.get_object('wagasci_database').get()
        wagasci_download_location = self._builder.get_object('wagasci_download_location').get()
        wagasci_decoded_location = self._builder.get_object('wagasci_decoded_location').get()
        if self._builder.tkvariables.__getitem__('is_borg_repo').get():
            repository_type = RepositoryType.Borg
        else:
            repository_type = RepositoryType.Simple

        self._config.wagasci_database_configuration.override({
            'wagasci_repository': wagasci_repository,
            'wagasci_database': wagasci_database,
            'wagasci_download_location': wagasci_download_location,
            'wagasci_decoded_location': wagasci_decoded_location,
            'repository_type': repository_type
        })

        # BSD database configuration
        bsd_repository = self._builder.get_object('bsd_repository').get()
        bsd_database = self._builder.get_object('bsd_database').get()
        bsd_download_location = self._builder.get_object('bsd_download_location').get()

        self._config.bsd_database_configuration.override({
            'bsd_repository': bsd_repository,
            'bsd_database': bsd_database,
            'bsd_download_location': bsd_download_location
        })

        # Temperature configuration
        temperature_sqlite_database = self._builder.get_object('temperature_sqlite_database').get()
        self._config.temperature_configuration.override({
            'temperature_sqlite_database': temperature_sqlite_database
        })

        # Viewer configuration
        wagasci_update_database = self._builder.tkvariables.__getitem__('wagasci_update_database').get()
        wagasci_rebuild_database = self._builder.tkvariables.__getitem__('wagasci_rebuild_database').get()
        bsd_update_database = self._builder.tkvariables.__getitem__('bsd_update_database').get()
        bsd_rebuild_database = self._builder.tkvariables.__getitem__('bsd_rebuild_database').get()
        wagasci_libdir = self._builder.get_object('wagasci_libdir').get()
        only_good_runs = self._builder.tkvariables.__getitem__('only_good_runs').get()
        include_overlapping = self._builder.tkvariables.__getitem__('include_overlapping').get()
        self._config.viewer_configuration.override({
            'wagasci_update_database': wagasci_update_database,
            'wagasci_rebuild_database': wagasci_rebuild_database,
            'bsd_update_database': bsd_update_database,
            'bsd_rebuild_database': bsd_rebuild_database,
            'wagasci_libdir': wagasci_libdir,
            'only_good_runs': only_good_runs,
            'include_overlapping': include_overlapping,
        })

        # Global configuration
        t2krun = int(self._builder.get_object('t2krun').get())
        data_quality_location = self._builder.get_object('data_quality_location').get()
        self._config.global_configuration.override({
            't2krun': t2krun,
            'data_quality_location': data_quality_location
        })

    def _get_topology(self):
        self._topology.read_topology(self._builder)

    def _get_analyzers(self):
        decoder = self._builder.tkvariables.__getitem__('decoder').get()
        spill_number_fixer = self._builder.tkvariables.__getitem__('spill_number_fixer').get()
        beam_summary_data = self._builder.tkvariables.__getitem__('beam_summary_data').get()
        temperature = self._builder.tkvariables.__getitem__('temperature').get()
        data_quality = self._builder.tkvariables.__getitem__('data_quality').get()
        Configuration.analyzer_configuration.override({
            'decoder': decoder,
            'spill_number_fixer': spill_number_fixer,
            'beam_summary_data': beam_summary_data,
            'temperature': temperature,
            'data_quality': data_quality
        })

    def _check_members(self):
        wagascianpy.viewer.utils.check_repository_and_database_sanity(
            repository=self._config.wagasci_database_configuration.wagasci_repository(),
            database=self._config.wagasci_database_configuration.wagasci_database(),
        )
        wagascianpy.viewer.utils.check_repository_and_database_sanity(
            repository=self._config.bsd_database_configuration.bsd_repository(),
            database=self._config.bsd_database_configuration.bsd_database(),
        )
        self._wagasci_libdir = wagascianpy.viewer.utils.check_wagasci_libdir(
            self._config.viewer_configuration.wagasci_libdir())

    def download(self, overwrite=True, builtin_reporter=True):
        # type: (bool, bool) -> None
        # Read the topology checkboxes
        if not self._batch_mode:
            self._get_topology()

        if builtin_reporter:
            reporter = self._report_callback_exception
        else:
            reporter = None

        # Download the runs
        wagascianpy.viewer.downloader.downloader(
            config=self._config,
            records=self._records,
            topology=self._topology,
            reporter=reporter,
            overwrite=overwrite,
            batch_mode=self._batch_mode)

    def analyze(self, overwrite_flag=False):
        # type: (bool) -> None

        # 1 : update members
        if not self._batch_mode:
            self._get_generic_members()
            self._get_analyzers()

        # 2 : Check the input folder (you need to have downloaded the raw data before decoding)
        if self._config.analyzer_configuration.decoder():
            run_dic = wagascianpy.viewer.utils.check_input_folder(
                input_folder=self._config.wagasci_database_configuration.wagasci_download_location(),
                records=self._records, batch_mode=self._batch_mode)
        else:
            run_dic = wagascianpy.viewer.utils.check_input_folder(
                input_folder=self._config.wagasci_database_configuration.wagasci_decoded_location(),
                records=self._records, batch_mode=self._batch_mode)

        # 3 : create builder
        builder = wagascianpy.program.program_builder.ProgramBuilder()

        # 4 : set run dictionary
        builder.run_location = run_dic

        # 5 : set save location
        if self._config.analyzer_configuration.decoder() and \
                self._config.wagasci_database_configuration.wagasci_decoded_location():
            builder.save_location = self._config.wagasci_database_configuration.wagasci_decoded_location()
        else:
            builder.output_dir_same_as_input()

        # 6 : add decoder
        if self._config.analyzer_configuration.decoder():
            builder.enforce_dependencies()
            builder.add_decoder(overwrite_flag=overwrite_flag,
                                enable_tdc_variables=False,
                                compatibility_mode=False)
        else:
            builder.do_not_enforce_dependencies()

        # 7 : add spill number fixer
        if self._config.analyzer_configuration.spill_number_fixer():
            builder.add_spill_number_fixer(enable_graphics=False)

        # 8 : add beam summary data
        if self._config.analyzer_configuration.beam_summary_data():
            builder.add_beam_summary_data(
                bsd_database_location=self._config.bsd_database_configuration.bsd_database(),
                bsd_repository_location=self._config.bsd_database_configuration.bsd_repository(),
                download_bsd_database_location='/tmp/bsddb.db',
                download_bsd_repository_location=self._config.bsd_database_configuration.bsd_download_location(),
                t2krun=self._config.global_configuration.t2krun(),
                recursive=True)

        # 9 : add temperature
        if self._config.analyzer_configuration.temperature():
            builder.add_temperature(
                sqlite_database=self._config.temperature_configuration.temperature_sqlite_database())

        # 10 : add data quality
        if self._config.analyzer_configuration.data_quality():
            builder.multiple_runs_analyzer_save_location = self._config.global_configuration.data_quality_location()
            builder.add_data_quality()

        # 11 : start program
        builder.program.start()

    def get_time_interval(self, start_time=None, stop_time=None, only_good_runs=True, include_overlapping=True):
        # type: (Optional[str], Optional[str], bool, bool) -> None
        """Get runs in an interval of time
        """

        if not self._batch_mode:
            self._get_generic_members()
            only_good_runs = self._builder.tkvariables.__getitem__('only_good_runs').get()
            include_overlapping = self._builder.tkvariables.__getitem__('include_overlapping').get()
            start_time, stop_time = wagascianpy.viewer.utils.get_time_interval_members(self._builder)
        self._check_members()

        wagascianpy.database.wagascidb.WagasciDataBase.wagasci_lib = self._wagasci_libdir
        with wagascianpy.database.wagascidb.WagasciDataBase(
                repo_location=self._config.wagasci_database_configuration.wagasci_repository(),
                db_location=self._config.wagasci_database_configuration.wagasci_database(),
                is_borg_repo=self._config.wagasci_database_configuration.repository_type() == RepositoryType.Borg,
                update_db=Configuration.viewer_configuration.wagasci_update_database(),
                rebuild_db=Configuration.viewer_configuration.wagasci_rebuild_database()) as database:
            self._records = database.get_time_interval(datetime_start=start_time,
                                                       datetime_stop=stop_time,
                                                       only_good=only_good_runs,
                                                       include_overlapping=include_overlapping)

            if not self._batch_mode:
                wagascianpy.viewer.show_run_info.make_records_table(config=self._config,
                                                                    builder=self._builder,
                                                                    records=self._records)
            else:
                for record in self._records:
                    wagascianpy.database.wagascidb.WagasciRunRecord(record).pretty_print()

    def get_run_interval(self, start_run=None, stop_run=None, only_good_runs=True):
        # type: (Optional[int], Optional[int], bool) -> None
        """Get runs in an between two runs
        """
        if not self._batch_mode:
            self._get_generic_members()
            only_good_runs = self._builder.tkvariables.__getitem__('only_good_runs').get()
            start_run = self._builder.tkvariables.__getitem__('start_run').get()
            stop_run = self._builder.tkvariables.__getitem__('stop_run').get()
        assert start_run is not None and stop_run is not None, "Please specify start run and stop run"
        self._check_members()

        wagascianpy.database.wagascidb.WagasciDataBase.wagasci_lib = self._wagasci_libdir
        with wagascianpy.database.wagascidb.WagasciDataBase(
                repo_location=self._config.wagasci_database_configuration.wagasci_repository(),
                db_location=self._config.wagasci_database_configuration.wagasci_database(),
                is_borg_repo=self._config.wagasci_database_configuration.repository_type() == RepositoryType.Borg,
                update_db=Configuration.viewer_configuration.wagasci_update_database(),
                rebuild_db=Configuration.viewer_configuration.wagasci_rebuild_database()) as database:
            self._records = database.get_run_interval(run_number_start=start_run,
                                                      run_number_stop=stop_run,
                                                      only_good=only_good_runs)

            if not self._batch_mode:
                wagascianpy.viewer.show_run_info.make_records_table(config=self._config,
                                                                    builder=self._builder,
                                                                    records=self._records)
            else:
                for record in self._records:
                    wagascianpy.database.wagascidb.WagasciRunRecord(record).pretty_print()

    def get_all(self, only_good_runs=True):
        # type: (bool) -> None
        """Get all WAGASCI runs
        """
        if not self._batch_mode:
            self._get_generic_members()
            only_good_runs = self._builder.tkvariables.__getitem__('only_good_runs').get()
        self._check_members()

        wagascianpy.database.wagascidb.WagasciDataBase.wagasci_lib = Configuration.viewer_configuration.wagasci_libdir()
        with wagascianpy.database.wagascidb.WagasciDataBase(
                repo_location=self._config.wagasci_database_configuration.wagasci_repository(),
                db_location=self._config.wagasci_database_configuration.wagasci_database(),
                is_borg_repo=self._config.wagasci_database_configuration.repository_type() == RepositoryType.Borg,
                update_db=self._config.viewer_configuration.wagasci_update_database(),
                rebuild_db=self._config.viewer_configuration.wagasci_rebuild_database()) as database:
            self._records = database.get_all(only_good=only_good_runs)

            if not self._batch_mode:
                wagascianpy.viewer.show_run_info.make_records_table(config=self._config,
                                                                    builder=self._builder,
                                                                    records=self._records)
            else:
                for record in self._records:
                    wagascianpy.database.wagascidb.WagasciRunRecord(record).pretty_print()

    def run(self):
        """Run the application
        """
        if not self._batch_mode:
            self._mainwindow.mainloop()


if __name__ == '__main__':

    # Parse shell arguments
    ARGS = wagascianpy.viewer.parse_args.parse_args(sys.argv[1:])

    # Edit the initial configuration
    wagascianpy.viewer.configuration.fill_configuration(ARGS)

    # Create application
    APP = Application(config=Configuration)

    if Configuration.viewer_configuration.batch_mode():
        # select runs
        if Configuration.run_select_configuration.get_time_interval():
            APP.get_time_interval(start_time=Configuration.run_select_configuration.start_time(),
                                  stop_time=Configuration.run_select_configuration.stop_time(),
                                  only_good_runs=Configuration.viewer_configuration.only_good_runs(),
                                  include_overlapping=Configuration.viewer_configuration.include_overlapping())
        if Configuration.run_select_configuration.get_run_interval():
            APP.get_run_interval(start_run=Configuration.run_select_configuration.start_run(),
                                 stop_run=Configuration.run_select_configuration.stop_run(),
                                 only_good_runs=Configuration.viewer_configuration.only_good_runs())
        if Configuration.run_select_configuration.get_all():
            APP.get_all(only_good_runs=Configuration.viewer_configuration.only_good_runs())

        # download
        if Configuration.analyzer_configuration.download():
            APP.download(builtin_reporter=False)

        # analysis
        APP.analyze(overwrite_flag=Configuration.analyzer_configuration.overwrite_flag())

    else:
        APP.run()
