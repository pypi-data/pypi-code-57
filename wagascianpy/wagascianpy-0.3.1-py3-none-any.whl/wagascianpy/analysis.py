#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio, Eguchi Aoi

# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=too-many-branches

"""
WAGASCI Analysis Python module

This module is just a wrapping around some of the WAGASCI Analysis C++ libraries.
The libraries are wrapped using Ctypes.

You can call the analysis methods directly as blocking functions or
you can spawn a thread and concatenate how many analysis methods as
you want. When chained, each method is not executed until the previous
one has returned. If there is an error or an exception in any link of
the chain all the successive methods are not executed. If you want,
you can wait for the last method in the chain to return and check its
return value by explicitly using the join() method.

Usage examples:

    # Call analysis methods as blocking functions

    process = WagasciAnalysis("lib_dir")
    process.function1("argument1")
    process.function2("argument2")
    del process # optional

    # Execute function1, function2 and function3 in sequence without blocking
    # the main process and then wait for function3 to return

    process = WagasciAnalysis("lib_dir")
    process.spawn("function1","argument1")
    process.spawn("function2","argument2")
    thread = process.spawn("function3","argument3")
    del process # optional
    # Do other stuff
    result = thread.join()
    if result not 0 :
        print "Error number : %d" %(result)

"""

import os
import ctypes as ct
import sys
import threading
from bitarray import bitarray

import wagascianpy.utils
import wagascianpy.beam_summary_data

OPTIMIZE_THRESHOLD_MODE = 0
OPTIMIZE_INPUTDAC_MODE = 1
SPIROC2D_NCHANNELS = 36


def _wrap_function(lib, funcname, restype, argtypes):
    """Simplify wrapping ctypes functions"""
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


# noinspection PyUnresolvedReferences
class ThreadWithReturnValue(threading.Thread):
    """Thread subclass where the join() method returns the return value of the
    called function.

    This class inherits from the threading.Thread class and the only difference
    is that its join() method returns the return value of the called
    function. The return value is always zero, a positive integer or minus
    one. Zero means the the called function returned successfully. A positive
    integer means that there was an error in the called function. Minus one
    means that there was an error in one of the chained functions.

    """

    # noinspection PyArgumentList
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, daemon=None):
        if sys.version_info.major >= 3:
            threading.Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        else:
            threading.Thread.__init__(self, group, target, name, args, kwargs, verbose=False)
        self._return = None

    def run(self):
        if sys.version_info.major >= 3:
            if self._target is not None:
                self._return = self._target(*self._args, **self._kwargs)
        else:
            if self._Thread__target is not None:
                self._return = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)

    def join(self, timeout=None):
        threading.Thread.join(self, timeout)
        return self._return


class WagasciAnalysis(object):
    """Class to manage WAGASCI Analysis processes. Refer to the WAGASCI Analysis
    software documentation for further info.

    """

    def __init__(self, lib_dir, thread=None):
        if lib_dir is not None and os.path.isdir(lib_dir):
            self.m_lib_dir = lib_dir.rstrip('/')
        else:
            raise ValueError("WAGASCI library directory could not be found : %s"
                             % lib_dir)
        self._previous_thread = thread
        self._result = 0
        self._previous_process = ""
        self.lock = threading.Lock()

    # The _dispatcher method calls the method called "function". If the "thread"
    # argument is different from null, it waits until that thread is over before
    # calling the function.
    def _dispatcher(self, thread, function, *argv, **kwargs):
        # Acquire lock to access the resources _result and _previous_process
        self.lock.acquire()
        try:
            # Wait for the previous thread to finish
            if thread is not None:
                self._result = thread.join()
            # if the _result attribute has been already set to -1 it means that
            # a previous thread returned an error. We can therefore avoid
            # calling all the successive functions
            if self._result == -1:
                raise RuntimeWarning
            elif self._result != 0:
                if self._result is not None:
                    raise ValueError("[%s] Error number : %d"
                                     % (self._previous_process, self._result))
                raise ValueError("[%s] Unspecified error"
                                 % self._previous_process)
            # Call the method named "function" and pass all the arguments "argv"
            # to it
            else:
                print("%s : start function %s" % (id(self), function))
                self._result = getattr(self, function)(*argv, **kwargs)
                print("%s : end function %s" % (id(self), function))
        except ValueError as error:
            print(str(error))
            self._result = -1
        finally:
            self._previous_process = function
            self.lock.release()
        return self._result

    def spawn(self, function, *argv, **kwargs):
        """Spawn a new thread that calls "function" whose arguments are "argv".
        Multiple threads can be chained together by calling the spawn function
        multiple times for the same object. This is a non-blocking function.

        Arguments:
        function = name of method to call
        argv = arguments to pass to *function*

        Return:
        object of the class ThreadWithReturnValue

        """
        argv = list(argv)
        argv.insert(0, self._previous_thread)
        argv.insert(1, function)
        self._previous_thread = ThreadWithReturnValue(target=self._dispatcher, args=tuple(argv), kwargs=kwargs)
        self._previous_thread.start()
        return self._previous_thread

    @wagascianpy.utils.utf8_decorator
    def decoder(self, input_file, calibration_dir, output_dir, overwrite_flag,
                compatibility_mode, enable_calib_mapping_variables, dif, n_chips):
        """Wrapping for the wgDecoder process"""
        lib_decoder = ct.CDLL(self.m_lib_dir + '/libwgDecoder.so')
        wg_decoder = _wrap_function(lib_decoder, 'wgDecoder', ct.c_int,
                                    [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                     ct.c_bool, ct.c_bool, ct.c_bool,
                                     ct.c_int, ct.c_int])
        return wg_decoder(input_file, calibration_dir, output_dir, overwrite_flag,
                          compatibility_mode, enable_calib_mapping_variables, dif, n_chips)

    @wagascianpy.utils.utf8_decorator
    def change_config(self, input_file, output_file, overwrite_flag, edit_flag,
                      value, mode, channel=SPIROC2D_NCHANNELS):
        """Wrapping for the wgChangeConfig process"""
        flags = bitarray('0' * 2, endian='big')
        flags[1] = bool(edit_flag)
        flags[0] = bool(overwrite_flag)
        flags_ulong = int(flags.to01(), 2)
        lib_change_config = ct.CDLL(self.m_lib_dir + '/libwgChangeConfig.so')
        wg_change_config = _wrap_function(lib_change_config, 'wgChangeConfig',
                                          ct.c_int,
                                          [ct.c_char_p, ct.c_char_p, ct.c_ulong,
                                           ct.c_int, ct.c_uint, ct.c_uint])
        return wg_change_config(input_file, output_file, flags_ulong,
                                int(value), int(mode), int(channel))

    @wagascianpy.utils.utf8_decorator
    def optimize(self, threshold_card, gain_card, topology_source,
                 bitstream_config_dir, mode=OPTIMIZE_INPUTDAC_MODE,
                 photo_electrons=2, input_dac=255, adj_th=0):
        """Wrapping for the wgOptimize process"""
        lib_optimize = ct.CDLL(self.m_lib_dir + '/libwgOptimize.so')
        wg_optimize = _wrap_function(lib_optimize, 'wgOptimize', ct.c_int,
                                     [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                      ct.c_char_p, ct.c_uint, ct.c_uint, ct.c_uint,
                                      ct.c_uint])
        return wg_optimize(threshold_card, gain_card, topology_source,
                           bitstream_config_dir, mode, photo_electrons,
                           input_dac, adj_th)

    @wagascianpy.utils.utf8_decorator
    def make_hist(self, input_file, config_file, output_dir, ul_flags, dif):
        """Wrapping for the wgMakeHist process"""
        lib_make_hist = ct.CDLL(self.m_lib_dir + '/libwgMakeHist.so')
        wg_make_hist = _wrap_function(lib_make_hist, 'wgMakeHist', ct.c_int,
                                      [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                       ct.c_ulong, ct.c_uint])
        return wg_make_hist(input_file, config_file, output_dir, ul_flags, dif)

    @wagascianpy.utils.utf8_decorator
    def ana_hist(self, input_file, config_file, output_dir,
                 output_img_dir, ul_flags, dif):
        """Wrapping for the wgAnaHist process"""
        lib_ana_hist = ct.CDLL(self.m_lib_dir + '/libwgAnaHist.so')
        wg_ana_hist = _wrap_function(lib_ana_hist, 'wgAnaHist', ct.c_int,
                                     [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                      ct.c_char_p, ct.c_ulong, ct.c_uint])
        return wg_ana_hist(input_file, config_file, output_dir,
                           output_img_dir, ul_flags, dif)

    @wagascianpy.utils.utf8_decorator
    def ana_hist_summary(self, input_dir, output_xml_dir, output_img_dir, ul_flags):
        """Wrapping for the wgAnaHistSummary process"""
        lib_ana_hist_summary = ct.CDLL(self.m_lib_dir + '/libwgAnaHistSummary.so')
        wg_ana_hist_summary = _wrap_function(lib_ana_hist_summary, 'wgAnaHistSummary',
                                             ct.c_int,
                                             [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                              ct.c_ulong])
        return wg_ana_hist_summary(input_dir, output_xml_dir,
                                   output_img_dir, ul_flags)

    @wagascianpy.utils.utf8_decorator
    def pedestal_calib(self, input_dir, output_xml_dir, output_img_dir):
        """Wrapping for the wgPedestalCalib process"""
        lib_pedestal_calib = ct.CDLL(self.m_lib_dir + '/libwgPedestalCalib.so')
        wg_pedestal_calib = _wrap_function(lib_pedestal_calib, 'wgPedestalCalib',
                                           ct.c_int,
                                           [ct.c_char_p, ct.c_char_p, ct.c_char_p])
        return wg_pedestal_calib(input_dir, output_xml_dir, output_img_dir)

    @wagascianpy.utils.utf8_decorator
    def gain_calib(self, input_dir, xml_config_file, output_xml_dir,
                   output_img_dir, only_wallmrd, only_wagasci):
        """Wrapping for the wgGainCalib process"""
        lib_gain_calib = ct.CDLL(self.m_lib_dir + '/libwgGainCalib.so')
        wg_gain_calib = _wrap_function(lib_gain_calib, 'wgGainCalib', ct.c_int,
                                       [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                        ct.c_char_p, ct.c_bool, ct.c_bool])
        return wg_gain_calib(input_dir, xml_config_file, output_xml_dir,
                             output_img_dir, only_wallmrd, only_wagasci)

    @wagascianpy.utils.utf8_decorator
    def gain_check(self, input_dir, xml_config_file, output_img_dir,
                   only_wallmrd, only_wagasci):
        """Wrapping for the wgGainCheck process"""
        lib_gain_check = ct.CDLL(self.m_lib_dir + '/libwgGainCheck.so')
        wg_gain_check = _wrap_function(lib_gain_check, 'wgGainCheck', ct.c_int,
                                       [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                        ct.c_bool, ct.c_bool])
        return wg_gain_check(input_dir, xml_config_file, output_img_dir,
                             only_wallmrd, only_wagasci)

    @wagascianpy.utils.utf8_decorator
    def scurve(self, input_dir, output_xml_dir, output_img_dir,
               paranoid_mode):
        """Wrapping for the wgScurve process"""
        lib_scurve = ct.CDLL(self.m_lib_dir + '/libwgScurve.so')
        wg_scurve = _wrap_function(lib_scurve, 'wgScurve', ct.c_int,
                                   [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                    ct.c_bool])
        return wg_scurve(input_dir, output_xml_dir, output_img_dir,
                         paranoid_mode)

    @wagascianpy.utils.utf8_decorator
    def spill_number_fixer(self, input_dir, output_dir, flipped_bits, offset, enable_graphics):
        """Wrapping for the wgSpillNumberFixer process"""
        lib_scurve = ct.CDLL(self.m_lib_dir + '/libwgSpillNumberFixer.so')
        wg_scurve = _wrap_function(lib_scurve, 'wgSpillNumberFixer', ct.c_int,
                                   [ct.c_char_p, ct.c_char_p, ct.c_char_p,
                                    ct.c_int, ct.c_bool])
        return wg_scurve(input_dir, output_dir, flipped_bits, offset, enable_graphics)

    @staticmethod
    def beam_summary_data(*args, **kwargs):
        try:
            wagascianpy.beam_summary_data.beam_summary_data(*args, **kwargs)
        except Exception as exception:
            print("beam_summary_data terminated with exception : %s" % str(exception))
            return wagascianpy.beam_summary_data.BSD_ERROR_CODE
        return 0

    @wagascianpy.utils.utf8_decorator
    def get_dif_topology(self, acq_config_xml):
        """Get detector topology (map_dif) from the acquisition configuration xml
        file"""
        lib_wagasci = ct.CDLL(self.m_lib_dir + '/libwagasci.so')
        wg_get_dif_topology = _wrap_function(lib_wagasci, 'GetDifTopologyCtypes',
                                             ct.c_char_p, [ct.c_char_p])
        return wg_get_dif_topology(acq_config_xml)

    @wagascianpy.utils.utf8_decorator
    def get_gdcc_topology(self, acq_config_xml):
        """Get detector topology (map_gdcc) from the acquisition configuration xml
        file"""
        lib_wagasci = ct.CDLL(self.m_lib_dir + '/libwagasci.so')
        wg_get_gdcc_topology = _wrap_function(lib_wagasci, 'GetGdccTopologyCtypes',
                                              ct.c_char_p, [ct.c_char_p])
        return wg_get_gdcc_topology(acq_config_xml)

    @wagascianpy.utils.utf8_decorator
    def free_topology(self, topology_string):
        """Release memory for the topology string"""
        lib_wagasci = ct.CDLL(self.m_lib_dir + '/libwagasci.so')
        wg_free_topology = _wrap_function(lib_wagasci, 'FreeTopologyCtypes', None,
                                          [ct.c_char_p])
        wg_free_topology(topology_string)

    def enable_thread_safety(self):
        """Enable ROOT thread safety"""
        lib_wagasci = ct.CDLL(self.m_lib_dir + '/libwagasci.so')
        wg_enable_thread_safety = _wrap_function(lib_wagasci, 'wgEnableThreadSafety',
                                                 None, None)
        wg_enable_thread_safety()
