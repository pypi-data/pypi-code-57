#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio


import wagascianpy.program.program
import wagascianpy.program.program_builder
import wagascianpy.utils.environment


class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing products according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self):
        self._builder = None

    @property
    def builder(self):
        # type: (...) -> wagascianpy.program.program_builder.ProgramBuilder
        return self._builder

    @builder.setter
    def builder(self, builder):
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled product.
        """
        self._builder = builder

    """
    The Director can construct several product variations using the same
    building steps.
    """

    def build_decoder(self,
                      overwrite_flag=False,
                      enable_tdc_variables=False,
                      compatibility_mode=False):
        self.builder.enforce_dependencies()
        self.builder.add_decoder(overwrite_flag=overwrite_flag,
                                 enable_tdc_variables=enable_tdc_variables,
                                 compatibility_mode=compatibility_mode)

    def build_spill_number_fixer(self):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_spill_number_fixer(enable_graphics=False)

    def build_beam_summary_data(self,
                                bsd_database_location,
                                bsd_repository_location,
                                download_bsd_database_location="/tmp/bsd/bsddb.db",
                                download_bsd_repository_location="/tmp/bsd",
                                t2krun=10):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_beam_summary_data(bsd_database_location=bsd_database_location,
                                           bsd_repository_location=bsd_repository_location,
                                           download_bsd_database_location=download_bsd_database_location,
                                           download_bsd_repository_location=download_bsd_repository_location,
                                           t2krun=t2krun,
                                           recursive=True)

    def build_temperature(self, sqlite_database):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_temperature(sqlite_database=sqlite_database)

    def build_data_quality(self, data_quality_location=None):
        self.builder.do_not_enforce_dependencies()
        if not data_quality_location:
            env = wagascianpy.utils.environment.WagasciEnvironment()
            data_quality_location = env["WAGASCI_DQDIR"]
        self.builder.multiple_runs_analyzer_save_location = data_quality_location
        self.builder.add_data_quality()

    def all_analyzers(self,
                      bsd_database_location,
                      bsd_repository_location,
                      data_quality_location,
                      sqlite_database,
                      download_bsd_database_location="/tmp/bsd/bsddb.db",
                      download_bsd_repository_location="/tmp/bsd",
                      t2krun=10,
                      overwrite_flag=False,
                      enable_tdc_variables=False,
                      compatibility_mode=False
                      ):
        self.build_decoder(overwrite_flag=overwrite_flag,
                           enable_tdc_variables=enable_tdc_variables,
                           compatibility_mode=compatibility_mode)
        self.build_spill_number_fixer()
        self.build_beam_summary_data(bsd_database_location=bsd_database_location,
                                     bsd_repository_location=bsd_repository_location,
                                     download_bsd_database_location=download_bsd_database_location,
                                     download_bsd_repository_location=download_bsd_repository_location,
                                     t2krun=t2krun)
        self.build_temperature(sqlite_database=sqlite_database)
        self.build_data_quality(data_quality_location=data_quality_location)
        self.builder.enforce_dependencies()
