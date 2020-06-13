#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc

import wagascianpy.program.program
import wagascianpy.program.program_builder

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class DecoderBuilder(wagascianpy.program.program_builder.ProgramBuilder, ABC):
    """ Decode raw data """

    def __init__(self, overwrite_flag=False,
                 enable_calib_mapping_variables=False,
                 compatibility_mode=False):
        super(DecoderBuilder, self).__init__()
        self._program = wagascianpy.program.program.Program()
        self._add_decoder(overwrite_flag=overwrite_flag,
                          enable_calib_mapping_variables=enable_calib_mapping_variables,
                          compatibility_mode=compatibility_mode)

    def reset(self):
        self._program = wagascianpy.program.program.Program()

    @property
    def program(self):
        my_program = self._program
        self.reset()
        return my_program
