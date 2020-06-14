#!python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

"""Check the gain of the SPIROC2D ASIC (method 1)"""

# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-function-args
# pylint: disable-msg=too-many-locals

# Python modules
import json
import argparse
import os
from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis import WagasciAnalysis
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils import limit_threads, join_threads

MAX_NB_THREAD_CHAINS = 8
PEU_LEVEL = 1


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def _gain_decoder(process, run_root_dir, peu, run_name, dif, n_chips):
    """ wgDecoder for the gain_check.py script """
    dif = int(dif)
    n_chips = int(n_chips)
    input_raw_file = "%s/PEU%d/RawData/%s_ecal_dif_%d.raw" \
                     % (run_root_dir, peu, run_name, dif)
    output_dir = "%s/PEU%d/wgDecoder" % (run_root_dir, peu)
    overwrite_flag = True
    compatibility_mode = False
    disable_calibration_variables = True
    return process.spawn("decoder", input_raw_file, "", output_dir,
                         overwrite_flag, compatibility_mode,
                         disable_calibration_variables, dif, n_chips)


def _gain_make_hist(process, run_root_dir, peu, run_name, acq_config_xml, dif):
    """ wgMakeHist for the gain_check.py script """
    dif = int(dif)
    input_tree_file = "%s/PEU%d/wgDecoder/%s_ecal_dif_%d_tree.root" \
                      % (run_root_dir, peu, run_name, dif)
    output_dir = "%s/PEU%d/wgMakeHist" % (run_root_dir, peu)
    flags = bitarray('0' * 9, endian='big')
    flags[6] = True  # charge
    flags[0] = True  # overwrite
    ul_flags = int(flags.to01(), 2)
    return process.make_hist(input_tree_file, acq_config_xml,
                             output_dir, ul_flags, dif)


def _gain_gain_check(process, run_root_dir, peu, acq_config_xml,
                     only_wallmrd, only_wagasci):
    """ wgGainCalib for the gain_check.py script """
    input_dir = "%s/PEU%d/wgMakeHist" % (run_root_dir, peu)
    output_dir = run_root_dir + "/wgGainCheck"
    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
    return process.gain_check(input_dir, acq_config_xml, output_dir,
                              only_wallmrd, only_wagasci)


# ============================================================================ #
#                                                                              #
#                                gain_analysis                                 #
#                                                                              #
# ============================================================================ #

def gain_check_analysis(run_name,
                        only_wallmrd=False, only_wagasci=False,
                        decoder=True, makehist=True, overwrite=False):
    """ Analyze gain check data """

    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
    decoder = bool(decoder)
    makehist = bool(makehist)

    # Environmental variables
    env = WagasciEnvironment()
    calibdata_dir = env['WAGASCI_CALIBDATADIR']
    wagasci_lib = env["WAGASCI_LIBDIR"]

    run_root_dir = calibdata_dir + "/" + run_name
    acq_config_xml = "%s/PEU%d/RawData/%s.xml" % (run_root_dir, PEU_LEVEL, run_name)
    if not os.path.exists(acq_config_xml):
        print("Acquisition configuration XML file not found : %s" % acq_config_xml)

    # =========================================================== #
    #                        ANALYZE DATA                         #
    # =========================================================== #

    process = WagasciAnalysis(wagasci_lib)
    dif_topology = json.loads(process.get_dif_topology(acq_config_xml))
    process.enable_thread_safety()
    del process

    ###########################################################################
    #                                 decoder                                 #
    ###########################################################################

    # The decoder is completely multithread safe so we can spawn as many threads
    # as the amount of available memory allows

    if decoder:

        threads = []

        for dif in dif_topology:
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            if not overwrite and \
                    os.path.exists("%s/PEU%d/wgDecoder/%s_ecal_dif_%d_tree.root"
                                   % (run_root_dir, PEU_LEVEL, run_name, int(dif))):
                continue
            limit_threads(threads, MAX_NB_THREAD_CHAINS)
            process = WagasciAnalysis(wagasci_lib)
            n_chips = len(dif_topology[dif])
            threads.append(_gain_decoder(process, run_root_dir, PEU_LEVEL, run_name,
                                         dif, n_chips))
            del process
        # dif loop

        # Wait until all the threads have returned
        join_threads(threads)

    ###########################################################################
    #                                make_hist                                #
    ###########################################################################

    if makehist:

        for dif in dif_topology:
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            if not overwrite and \
                    os.path.exists("%s/PEU%d/wgMakeHist/%s_ecal_dif_%d_hist.root"
                                   % (run_root_dir, PEU_LEVEL, run_name, int(dif))):
                continue
            process = WagasciAnalysis(wagasci_lib)
            result = _gain_make_hist(process, run_root_dir, PEU_LEVEL, run_name,
                                     acq_config_xml, dif)
            if result != 0:
                print("wgMakeHist returned error code %d" % result)
                exit(result)
            del process
        # dif loop

    ###########################################################################
    #                             gain_calib1                                 #
    ###########################################################################

    process = WagasciAnalysis(wagasci_lib)
    result = _gain_gain_check(process, run_root_dir, PEU_LEVEL, acq_config_xml,
                              only_wallmrd, only_wagasci)
    del process
    if result != 0:
        print("wgGainCheck returned error code %d" % result)
        exit(result)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Check gain calibration')

    PARSER.add_argument('run_name', metavar='N', type=str, nargs='+',
                        help='Name of the run to analyze')
    PARSER.add_argument('--only-wallmrd', dest='only_wallmrd', action='store_true')
    PARSER.add_argument('--only-wagasci', dest='only_wagasci', action='store_true')
    PARSER.add_argument('--disable-decoder', dest='decoder', action='store_false')
    PARSER.add_argument('--disable-makehist', dest='makehist', action='store_false')
    PARSER.add_argument('--overwrite', dest='overwrite', action='store_true')

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
    OVERWRITE = False
    OVERWRITE = ARGS.overwrite

    gain_check_analysis(RUN_NAME, ONLY_WALLMRD, ONLY_WAGASCI,
                        DECODER, MAKEHIST, OVERWRITE)
