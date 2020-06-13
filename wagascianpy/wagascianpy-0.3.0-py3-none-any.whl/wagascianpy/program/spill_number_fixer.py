#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc

import wagascianpy.program.program
import wagascianpy.program.program_builder

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class SpillNumberFixerBuilder(wagascianpy.program.program_builder.ProgramBuilder, ABC):
    """ Fix spill number """

    def __init__(self):
        super(SpillNumberFixerBuilder, self).__init__()
        self._program = wagascianpy.program.program.Program()
        self.output_dir_same_as_input()
        self.do_not_enforce_dependencies()
        self._add_spill_number_fixer(enable_graphics=False)

    def reset(self):
        self._program = wagascianpy.program.program.Program()

    @property
    def program(self):
        my_program = self._program
        self.reset()
        return my_program
