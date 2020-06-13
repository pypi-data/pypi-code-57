#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc

import wagascianpy.program.program
import wagascianpy.program.program_builder

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class TemperatureBuilder(wagascianpy.program.program_builder.ProgramBuilder, ABC):
    """ Add temperature and humidity reading to decoded data """

    def __init__(self, sqlite_database):
        super(TemperatureBuilder, self).__init__()
        self._program = wagascianpy.program.program.Program()
        self._program.stop_on_exception()
        self._program.do_not_enforce_dependencies()
        self._add_temperature(sqlite_database=sqlite_database)

    def reset(self):
        self._program = wagascianpy.program.program.Program()

    @property
    def program(self):
        my_program = self._program
        self.reset()
        return my_program
