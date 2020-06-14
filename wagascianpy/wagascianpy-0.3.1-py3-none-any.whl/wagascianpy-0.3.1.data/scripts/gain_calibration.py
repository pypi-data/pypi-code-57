#!python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

"""Script to calibration the gain of the high gain preamp the SPIROC2D ASIC

"""

# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-function-args
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=eval-used
# pylint: disable-msg=bare-except

# Python modules
import json
import argparse
import os
import collections
from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis.analysis import WagasciAnalysis
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils.utils import limit_threads, join_threads

PEU_LEVEL = 1
MAX_NB_THREAD_CHAINS = 8


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def _gain_decoder(process, run_root_dir, input_dac, peu,
                  acq_name, dif, n_chips):
    """ wgDecoder for the gain_run.py script """
    peu = int(peu)
    dif = int(dif)
    n_chips = int(n_chips)
    input_raw_file = "%s/iDAC%s/PEU%s/RawData/%s_ecal_dif_%s.raw" \
                     % (run_root_dir, input_dac, peu, acq_name, dif)
    output_dir = "%s/iDAC%s/PEU%s/wgDecoder" % (run_root_dir, input_dac, peu)
    overwrite_flag = True
    compatibility_mode = False
    disable_calibration_variables = False
    return process.spawn("decoder", input_raw_file, "", output_dir,
                         overwrite_flag, compatibility_mode,
                         disable_calibration_variables, dif, n_chips)


def _gain_make_hist(process, run_root_dir, input_dac, peu, acq_name,
                    acq_config_xml, dif):
    """ wgMakeHist for the gain_run.py script """
    peu = int(peu)
    dif = int(dif)
    input_tree_file = "%s/iDAC%s/PEU%s/wgDecoder/%s_ecal_dif_%s_tree.root" \
                      % (run_root_dir, input_dac, peu, acq_name, dif)
    output_dir = "%s/iDAC%s/PEU%s/wgMakeHist" \
                 % (run_root_dir, input_dac, peu)
    flags = bitarray('0' * 9, endian='big')
    flags[7] = True  # dark noise
    flags[4] = True  # charge hit HG
    flags[0] = True  # overwrite
    ul_flags = int(flags.to01(), 2)
    return process.make_hist(input_tree_file, acq_config_xml,
                             output_dir, ul_flags, dif)


def _gain_gain_calib(process, run_root_dir, acq_config_xml,
                     only_wallmrd, only_wagasci):
    """ wgGainCalib for the gain_run.py script """
    output_xml_dir = run_root_dir + "/wgGainCalib/Xml"
    output_img_dir = run_root_dir + "/wgGainCalib/Images"
    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
    return process.gain_calib(run_root_dir, acq_config_xml, output_xml_dir,
                              output_img_dir, only_wallmrd, only_wagasci)


# ============================================================================ #
#                                                                              #
#                                gain_analysis                                 #
#                                                                              #
# ============================================================================ #

def gain_analysis(run_name, idac_range=range(1, 242, 30),
                  only_wallmrd=False, only_wagasci=False,
                  decoder=True, makehist=True, overwrite=False):
    """ Analyze gain calibration data """

    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
    decoder = bool(decoder)
    makehist = bool(makehist)

    # Environmental variables
    env = WagasciEnvironment()
    wagasci_ana = env['WAGASCI_MAINDIR']
    calibdata_dir = env['WAGASCI_CALIBDATADIR']
    wagasci_lib = wagasci_ana + "/lib64"

    run_root_dir = calibdata_dir + "/" + run_name
    acq_config_path = run_root_dir + "/" + os.path.basename(env['WAGASCI_ACQCONFIGDIR'])
    acq_config_xml = acq_config_path + "/" + env['WAGASCI_ACQCONFIGXML']
    if not os.path.exists(acq_config_xml):
        print("Acquisition configuration XML file not found : %s"
              % acq_config_xml)
        exit(-1)

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

        for input_dac in idac_range:
            acq_name = "%s_iDAC%s_PEU%s" % (run_name, input_dac, PEU_LEVEL)
            for dif in dif_topology:
                if only_wagasci and int(dif) < 4:
                    continue
                if only_wallmrd and int(dif) >= 4:
                    continue
                decoded_file = "%s/iDAC%s/PEU%s/wgDecoder/%s_ecal_dif_%s_tree.root" \
                               % (run_root_dir, input_dac, PEU_LEVEL, acq_name, dif)
                if not overwrite and os.path.exists(decoded_file):
                    print("Skipping %s" % decoded_file)
                    continue
                limit_threads(threads, MAX_NB_THREAD_CHAINS)
                process = WagasciAnalysis(wagasci_lib)
                n_chips = len(dif_topology[dif])
                threads.append(_gain_decoder(process, run_root_dir, input_dac,
                                             PEU_LEVEL, acq_name, dif, n_chips))
                del process
            # dif loop
        # input_dac loop

        # Wait until all the threads have returned
        join_threads(threads)

    ###########################################################################
    #                                make_hist                                #
    ###########################################################################

    if makehist:

        for input_dac in idac_range:
            acq_name = "%s_iDAC%s_PEU%s" % (run_name, input_dac, PEU_LEVEL)
            actual_acq_config_xml = "%s/iDAC%s/PEU%s/RawData/%s.xml" \
                                    % (run_root_dir, input_dac, PEU_LEVEL, acq_name)
            for dif in dif_topology:
                if only_wagasci and int(dif) < 4:
                    continue
                if only_wallmrd and int(dif) >= 4:
                    continue
                makehist_file = "%s/iDAC%s/PEU%s/wgMakeHist/%s_ecal_dif_%s_hist.root" \
                                % (run_root_dir, input_dac, PEU_LEVEL, acq_name, dif)
                if not overwrite and os.path.exists(makehist_file):
                    print("Skipping %s" % makehist_file)
                    continue
                process = WagasciAnalysis(wagasci_lib)
                result = _gain_make_hist(process, run_root_dir, input_dac, PEU_LEVEL,
                                         acq_name, actual_acq_config_xml, dif)
                if result != 0:
                    print("wgMakeHist returned error code %s" % result)
                    exit(result)
                del process
            # dif loop
        # input_dac loop

    ###########################################################################
    #                             gain_calib                                 #
    ###########################################################################

    process = WagasciAnalysis(wagasci_lib)
    result = _gain_gain_calib(process, run_root_dir, acq_config_xml,
                              only_wallmrd, only_wagasci)
    del process
    if result != 0:
        print("wgGainCalib returned error code %s" % result)
        exit(result)


###############################################################################
#                                     MAIN                                    #
###############################################################################

# noinspection PyPep8,PyBroadException
def _is_evaluable(string):
    try:
        tmp = eval(string)
        if not isinstance(tmp, collections.Iterable):
            return False
        return True
    except:
        return False


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Analyze gain calibration data')

    PARSER.add_argument('run_name', metavar='N', type=str, nargs='+',
                        help='Name of the run to analyze')
    PARSER.add_argument('idac_range', metavar='R', type=str, nargs='+',
                        help='Range of Input 8-bit DAC (python code)')
    PARSER.add_argument('--only-wallmrd', dest='only_wallmrd', action='store_true')
    PARSER.add_argument('--only-wagasci', dest='only_wagasci', action='store_true')
    PARSER.add_argument('--disable-decoder', dest='decoder', action='store_false')
    PARSER.add_argument('--disable-makehist', dest='makehist', action='store_false')
    PARSER.add_argument('--overwrite', dest='overwrite', action='store_true')

    PARSER.set_defaults(ignore_wagasci=False)

    ARGS = PARSER.parse_args()
    RUN_NAME = ARGS.run_name[0]
    IDAC_RANGE = ARGS.idac_range[0]
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

    if (IDAC_RANGE is not None or IDAC_RANGE != "") and _is_evaluable(IDAC_RANGE):
        IDAC_RANGE = eval(IDAC_RANGE)
    else:
        raise ValueError("IDAC_RANGE string not recognized")

    gain_analysis(RUN_NAME, IDAC_RANGE, ONLY_WALLMRD, ONLY_WAGASCI,
                  DECODER, MAKEHIST, OVERWRITE)
