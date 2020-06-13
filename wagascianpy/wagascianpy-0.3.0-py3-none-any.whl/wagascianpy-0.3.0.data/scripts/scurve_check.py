#!python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

""" Run script to measure and check the pedestal of the SPIROC2D ASIC """

# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-function-args
# pylint: disable-msg=too-many-locals

# Python modules
import os
import time
import json
import argparse
from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis import WagasciAnalysis
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils import limit_threads, join_threads

RANGE_IDAC = [1, 121, 241]
RANGE_PEU = [1, 2]  # threshold set at 0.5 and 1.5 p.e.
MAX_NB_THREAD_CHAINS = 8


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def _scurve_check_decoder(process, run_root_dir, acq_name, dif, n_chips):
    """ wgDecoder for the scurve_check_run.py script """
    dif = int(dif)
    n_chips = int(n_chips)
    input_raw_file = "%s/RawData/%s_ecal_dif_%d.raw" % (run_root_dir, acq_name, dif)
    output_dir = "%s/wgDecoder" % run_root_dir
    overwrite_flag = True
    compatibility_mode = False
    disable_calibration_variables = True
    return process.spawn("decoder", input_raw_file, "", output_dir,
                         overwrite_flag, compatibility_mode,
                         disable_calibration_variables, dif, n_chips)


def _scurve_check_make_hist(process, run_root_dir, acq_name, acq_config_xml, dif):
    """ wgMakeHist for the scurve_check_run.py script """
    dif = int(dif)
    input_tree_file = "%s/wgDecoder/%s_ecal_dif_%d_tree.root" \
                      % (run_root_dir, acq_name, dif)
    output_dir = "%s/wgMakeHist" % run_root_dir
    flags = bitarray('0' * 9, endian='big')
    flags[7] = True  # dark noise
    flags[0] = True  # overwrite
    ul_flags = int(flags.to01(), 2)
    return process.make_hist(input_tree_file, acq_config_xml, output_dir,
                             ul_flags, dif)


def _scurve_check_ana_hist(process, run_root_dir, acq_name, acq_config_xml, dif):
    """ wgAnaHist for the scurve_check_run.py script """
    dif = int(dif)
    input_hist_file = "%s/wgMakeHist/%s_ecal_dif_%d_hist.root" \
                      % (run_root_dir, acq_name, dif)
    output_dir = "%s/wgAnaHist/Xml/dif_%d" % (run_root_dir, dif)
    output_img_dir = "%s/wgAnaHist/Images/dif_%d" % (run_root_dir, dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[6] = bool(acq_config_xml)
    flags[5] = False  # print
    flags[4] = True  # Dark noise
    ul_flags = int(flags.to01(), 2)
    return process.spawn("ana_hist", input_hist_file, acq_config_xml, output_dir,
                         output_img_dir, ul_flags, dif)
    # return process.ana_hist(input_hist_file, acq_config_xml, output_dir,
    #                         output_img_dir, ul_flags, dif)


def _scurve_check_ana_hist_summary(process, run_root_dir, dif):
    """ wgAnaHistSummary for the scurve_check_run.py script """
    dif = int(dif)
    input_dir = "%s/wgAnaHist/Xml/dif_%d" % (run_root_dir, dif)
    output_dir = "%s/wgAnaHistSummary/Xml/dif_%d" % (run_root_dir, dif)
    output_img_dir = "%s/wgAnaHistSummary/Images/dif_%d" % (run_root_dir, dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[5] = True  # print
    flags[4] = True  # Dark noise
    ul_flags = int(flags.to01(), 2)
    return process.ana_hist_summary(input_dir, output_dir, output_img_dir, ul_flags)


# ============================================================================ #
#                                                                              #
#                                scurve_check_analysis                                 #
#                                                                              #
# ============================================================================ #

def scurve_check_analysis(run_name, only_wallmrd=False, only_wagasci=False,
                          decoder=True, makehist=True, anahist=True):
    """ Analyze pedestal calibration data """

    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
    decoder = bool(decoder)
    makehist = bool(makehist)
    anahist = bool(anahist)

    # Environmental variables
    env = WagasciEnvironment()
    calibdata_dir = env['WAGASCI_CALIBDATADIR']
    wagasci_lib = env["WAGASCI_LIBDIR"]

    run_root_dir = calibdata_dir + "/" + run_name
    acq_config_xml = run_root_dir + "/AcqConfig/wagasci_config.xml"

    # =========================================================== #
    #                        ANALYZE DATA                         #
    # =========================================================== #

    process = WagasciAnalysis(wagasci_lib)
    if not os.path.exists(acq_config_xml):
        raise ValueError("Acquisition XML configuration file does not exists : " +
                         acq_config_xml)
    dif_topology = json.loads(process.get_dif_topology(acq_config_xml))
    process.enable_thread_safety()
    del process

    #############################################################################
    #                                   decoder                                 #
    #############################################################################

    # The decoder is completely multithread safe so we can spawn as many threads
    # as the amount of available memory allows

    if decoder:

        threads = []

        for dif in dif_topology:
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            limit_threads(threads, MAX_NB_THREAD_CHAINS)
            process = WagasciAnalysis(wagasci_lib)
            n_chips = len(dif_topology[dif])
            threads.append(_scurve_check_decoder(process, run_root_dir,
                                                 run_name, dif, n_chips))
            del process
        # dif loop

        # Wait until all the threads have returned
        join_threads(threads)
        time.sleep(5)

    #############################################################################
    #                                  make_hist                                #
    #############################################################################

    # wgMakeHist does not play nicely with threads. Because of the wacky ROOT
    # memory handling there are a lot of seg faults and deadlocks when running
    # in a multithread environment. Moreover the memory footprint of wgMakeHist
    # is quite big (~1 GB per thread), so only a few threads can run
    # simultaneuously anyway. So be warned.

    if makehist:

        actual_acq_config_xml = "%s/RawData/%s.xml" % (run_root_dir, run_name)
        for dif in dif_topology:
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            process = WagasciAnalysis(wagasci_lib)
            result = _scurve_check_make_hist(process, run_root_dir, run_name,
                                             actual_acq_config_xml, dif)
            if result != 0:
                print("wgMakeHist returned error code %d" % result)
                exit(result)
            del process
        # dif loop

    #############################################################################
    #                                   ana_hist                                #
    #############################################################################

    # wgAnaHist is thread safe if there is no drawing (no print image to file)

    if anahist:

        threads = []

        actual_acq_config_xml = "%s/RawData/%s.xml" % (run_root_dir, run_name)
        for dif in dif_topology:
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            limit_threads(threads, MAX_NB_THREAD_CHAINS)
            process = WagasciAnalysis(wagasci_lib)
            threads.append(_scurve_check_ana_hist(process, run_root_dir, run_name,
                                                  actual_acq_config_xml, dif))
            # result = _scurve_check_ana_hist(process, run_root_dir, input_dac,
            #                         peu, acq_name,
            #                         actual_acq_config_xml, dif)
            # if result != 0:
            #     print "wgAnaHist returned error code %d" %(result)
            #     exit(result)
            del process
        # dif loop

        # Wait until all the threads have returned
        join_threads(threads)
        time.sleep(5)

    #############################################################################
    #                             ana_hist_summary                              #
    #############################################################################

    # The wgAnaHistSummary code is not thread safe

    if anahist:

        for dif in dif_topology:
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            process = WagasciAnalysis(wagasci_lib)
            result = _scurve_check_ana_hist_summary(process, run_root_dir, dif)
            if result != 0:
                print("wgAnaHistSummary returned error code %d" % result)
                exit(result)
            del process
        # dif loop


###############################################################################
#                                  arguments                                  #
###############################################################################

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Analyze scurve calibration data')

    PARSER.add_argument('run_name', metavar='N', type=str, nargs='+',
                        help='Name of the run to analyze')
    PARSER.add_argument('--only-wallmrd', dest='only_wallmrd', action='store_true')
    PARSER.add_argument('--only-wagasci', dest='only_wagasci', action='store_true')
    PARSER.add_argument('--disable-decoder', dest='decoder', action='store_false')
    PARSER.add_argument('--disable-makehist', dest='makehist', action='store_false')
    PARSER.add_argument('--disable-anahist', dest='anahist', action='store_false')

    PARSER.set_defaults(ignore_wagasci=False)

    ARGS = PARSER.parse_args()
    RUN_NAME = ARGS.run_name[0]
    ONLY_WAGASCI = False
    ONLY_WAGASCI = ARGS.only_wagasci
    ONLY_WALLMRD = False
    ONLY_WALLMRD = ARGS.only_wallmrd
    DECODER = True
    DECODER = ARGS.decoder
    MAKEHIST = True
    MAKEHIST = ARGS.makehist
    ANAHIST = True
    ANAHIST = ARGS.anahist

    scurve_check_analysis(RUN_NAME, ONLY_WALLMRD, ONLY_WAGASCI,
                          DECODER, MAKEHIST, ANAHIST)
