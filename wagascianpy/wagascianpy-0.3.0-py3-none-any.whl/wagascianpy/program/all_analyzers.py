#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc

import wagascianpy.program.program
import wagascianpy.program.program_builder

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class AllAnalyzersBuilder(wagascianpy.program.program_builder.ProgramBuilder, ABC):
    """ Decoded multiple runs in batch """

    def __init__(self,
                 bsd_database_location=None,
                 bsd_repository_location=None,
                 download_bsd_database_location="/tmp/bsd/bsddb.db",
                 download_bsd_repository_location="/tmp/bsd",
                 t2krun=None,
                 sqlite_database=None):
        super(AllAnalyzersBuilder, self).__init__()
        self._program = wagascianpy.program.program.Program()
        self._program.do_not_stop_on_exception()
        self._program.enforce_dependencies()
        self._add_decoder(overwrite_flag=True,
                          enable_calib_mapping_variables=False,
                          compatibility_mode=False)
        self._add_spill_number_fixer(enable_graphics=False)
        if bsd_database_location is not None and bsd_repository_location is not None and t2krun is not None:
            self._add_beam_summary_data(bsd_database_location=bsd_database_location,
                                        bsd_repository_location=bsd_repository_location,
                                        download_bsd_database_location=download_bsd_database_location,
                                        download_bsd_repository_location=download_bsd_repository_location,
                                        t2krun=t2krun,
                                        recursive=True)
        else:
            print("BSD info integration disabled because the BSD properties paths were not provided")
            print("BSD database : {}\nBSD repository : {}\nT2K run : {}\n".format(bsd_database_location,
                                                                                  bsd_repository_location, t2krun))
        if sqlite_database is not None:
            self._add_temperature(sqlite_database=sqlite_database)

    def reset(self):
        self._program = wagascianpy.program.program.Program()

    @property
    def program(self):
        my_program = self._program
        self.reset()
        return my_program
