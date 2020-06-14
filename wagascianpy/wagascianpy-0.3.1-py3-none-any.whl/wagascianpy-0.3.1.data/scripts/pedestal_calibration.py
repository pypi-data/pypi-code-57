#!python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

""" Run script to measure and check the pedestal of the SPIROC2D ASIC """

# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-function-args
# pylint: disable-msg=too-many-locals

import argparse
# Python modules
import json
import os
import re
import textwrap

from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis.analysis import WagasciAnalysis
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils.utils import limit_threads, join_threads

RANGE_PEU = [1, 2]
MAX_NB_THREAD_CHAINS = 8


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def pedestal_decoder(process, idac_dir, acq_name, peu, threshold_dir,
                     dif, n_chips):
    """ wgDecoder for the pedestal_run.py script """
    peu = int(peu)
    dif = int(dif)
    n_chips = int(n_chips)
    input_raw_file = "%s/PEU%s/%s/RawData/%s_ecal_dif_%s.raw" \
                     % (idac_dir, peu, threshold_dir, acq_name, dif)
    output_dir = "%s/PEU%s/%s/wgDecoder" % (idac_dir, peu, threshold_dir)
    overwrite_flag = True
    compatibility_mode = False
    enable_tdc_variables = False
    return process.spawn("decoder", input_raw_file, "", output_dir,
                         overwrite_flag, compatibility_mode,
                         enable_tdc_variables, dif, n_chips)


def pedestal_make_hist(process, idac_dir, acq_name, peu, threshold_dir,
                       dif, acq_config_xml):
    """ wgMakeHist for the pedestal_run.py script """
    peu = int(peu)
    dif = int(dif)
    input_tree_file = "%s/PEU%s/%s/wgDecoder/%s_ecal_dif_%s_tree.root" \
                      % (idac_dir, peu, threshold_dir, acq_name, dif)
    output_dir = "%s/PEU%s/%s/wgMakeHist" % (idac_dir, peu, threshold_dir)
    flags = bitarray('0' * 9, endian='big')
    flags[7] = True  # dark noise
    flags[5] = True  # charge nohit
    flags[4] = True  # charge hit HG
    flags[0] = True  # overwrite
    ul_flags = int(flags.to01(), 2)
    return process.make_hist(input_tree_file, acq_config_xml,
                             output_dir, ul_flags, dif)


def pedestal_ana_hist(process, idac_dir, acq_name, peu, threshold_dir,
                      dif, acq_config_xml):
    """ wgAnaHist for the pedestal_run.py script """
    peu = int(peu)
    dif = int(dif)
    input_hist_file = "%s/PEU%s/%s/wgMakeHist/%s_ecal_dif_%s_hist.root" \
                      % (idac_dir, peu, threshold_dir, acq_name, dif)
    output_dir = "%s/PEU%s/%s/wgAnaHist/Xml/dif%s" \
                 % (idac_dir, peu, threshold_dir, dif)
    output_img_dir = "%s/PEU%s/%s/wgAnaHist/Images/dif%s" \
                     % (idac_dir, peu, threshold_dir, dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[6] = bool(acq_config_xml)
    flags[5] = False  # print
    flags[4] = True  # Dark noise
    flags[3] = True  # charge nohit
    flags[2] = True  # charge hit HG
    ul_flags = int(flags.to01(), 2)
    return process.spawn("ana_hist", input_hist_file, acq_config_xml,
                         output_dir, output_img_dir, ul_flags, dif)


def pedestal_ana_hist_summary(process, idac_dir, peu, threshold_dir, dif):
    """ wgAnaHistSummary for the pedestal_run.py script """
    peu = int(peu)
    dif = int(dif)
    input_dir = "%s/PEU%s/%s/wgAnaHist/Xml/dif%s" \
                % (idac_dir, peu, threshold_dir, dif)
    output_dir = "%s/PEU%s/%s/wgAnaHistSummary/Xml/dif%s" \
                 % (idac_dir, peu, threshold_dir, dif)
    output_img_dir = "%s/PEU%s/%s/wgAnaHistSummary/Images/dif%s" \
                     % (idac_dir, peu, threshold_dir, dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[5] = False  # print
    flags[4] = True  # Dark noise
    flags[3] = True  # charge nohit
    flags[2] = True  # charge hit HG
    ul_flags = int(flags.to01(), 2)
    return process.ana_hist_summary(input_dir, output_dir, output_img_dir,
                                    ul_flags)


def pedestal_pedestal_calib(process, idac_dir):
    """ wgPedestalCalib for the pedestal_run.py script """
    output_dir = idac_dir + "/wgPedestalCalib/Xml"
    output_img_dir = idac_dir + "/wgPedestalCalib/Images"
    return process.pedestal_calib(idac_dir, output_dir, output_img_dir)


def _get_idac_dir(run_root_dir):
    dir_list = [name for name in os.listdir(run_root_dir)
                if os.path.isdir(os.path.join(run_root_dir, name))]
    for name in dir_list:
        if len(re.findall(r'\d+', name)) == 1:
            return int(re.findall(r'\d+', name)[0])
        if "OPTIMIZE" in name:
            return "OPTIMIZE"
    return None


def pedestal_analysis(run_name, decoder=True, makehist=True, anahist=True, overwrite=False, single_threshold=False):
    """ Analyze pedestal calibration data """

    decoder = bool(decoder)
    makehist = bool(makehist)
    anahist = bool(anahist)
    overwrite = bool(overwrite)
    single_threshold = bool(single_threshold)

    # Environmental variables
    env = WagasciEnvironment()
    calibdata_dir = env['WAGASCI_CALIBDATADIR']
    wagasci_lib = env["WAGASCI_LIBDIR"]

    run_root_dir = "%s/%s" % (calibdata_dir, run_name)
    input_dac = _get_idac_dir(run_root_dir)
    if input_dac is None:
        raise ValueError("Input DAC not recognized")
    idac_dir = "%s/iDAC%s" % (run_root_dir, input_dac)
    acq_config_base = os.path.basename(env['WAGASCI_ACQCONFIGDIR'])
    acq_config_xml = "%s/%s/%s" % (run_root_dir, acq_config_base,
                                   env['WAGASCI_ACQCONFIGXML'])
    if not os.path.exists(acq_config_xml):
        print("Acquisition configuration XML file not found : %s" % acq_config_xml)
    if single_threshold:
        threshold_dirs = ["SingleTh"]
    else:
        threshold_dirs = ["LowTh", "MiddleTh", "HighTh"]

    # =========================================================== #
    #                        ANALYZE DATA                         #
    # =========================================================== #

    process = WagasciAnalysis(wagasci_lib)
    dif_topology_string, dif_topology_pointer = process.get_dif_topology(acq_config_xml)
    dif_topology = json.loads(dif_topology_string)
    process.free_topology(dif_topology_pointer)
    process.enable_thread_safety()
    del process

    ###########################################################################
    #                                 decoder                                 #
    ###########################################################################

    if decoder:

        threads = []

        for peu in RANGE_PEU:
            for threshold_dir in threshold_dirs:
                acq_name = "%s_iDAC%s_PEU%s_%s" % (run_name, input_dac, peu, threshold_dir)
                for dif in dif_topology:
                    decoded_filename = "%s/PEU%s/%s/wgDecoder/%s_ecal_dif_%s_tree.root" \
                                       % (idac_dir, peu, threshold_dir, acq_name, dif)
                    if not overwrite and os.path.exists(decoded_filename):
                        print("Skipping %s" % decoded_filename)
                        continue
                    limit_threads(threads, MAX_NB_THREAD_CHAINS)
                    process = WagasciAnalysis(wagasci_lib)
                    n_chips = len(dif_topology[dif])
                    threads.append(pedestal_decoder(process, idac_dir, acq_name, peu,
                                                    threshold_dir, dif, n_chips))
                    del process
                # dif loop
            # threshold loop
        # peu loop

        # Wait until all the threads have returned
        join_threads(threads)

    ###########################################################################
    #                                make_hist                                #
    ###########################################################################

    if makehist:

        for peu in RANGE_PEU:
            for threshold_dir in threshold_dirs:
                acq_name = "%s_iDAC%s_PEU%s_%s" % (run_name, input_dac, peu, threshold_dir)
                actual_acq_config_xml = "%s/PEU%s/%s/RawData/%s.xml" \
                                        % (idac_dir, peu, threshold_dir, acq_name)

                for dif in dif_topology:
                    makehist_filename = "%s/PEU%s/%s/wgMakeHist/%s_ecal_dif_%s_hist.root" \
                                        % (idac_dir, peu, threshold_dir, acq_name, dif)
                    if not overwrite and os.path.exists(makehist_filename):
                        print("Skipping %s" % makehist_filename)
                        continue
                    process = WagasciAnalysis(wagasci_lib)
                    result = pedestal_make_hist(process, idac_dir, acq_name, peu,
                                                threshold_dir, dif, actual_acq_config_xml)
                    if result != 0:
                        print("wgMakeHist returned error code %s" % result)
                        exit(result)
                    del process
                # dif loop
            # threshold loop
        # peu loop

    ###########################################################################
    #                                 ana_hist                                #
    ###########################################################################

    if anahist:

        threads = []

        for peu in RANGE_PEU:
            for threshold_dir in threshold_dirs:
                acq_name = "%s_iDAC%s_PEU%s_%s" % (run_name, input_dac, peu, threshold_dir)
                actual_acq_config_xml = "%s/PEU%s/%s/RawData/%s.xml" \
                                        % (idac_dir, peu, threshold_dir, acq_name)

                for dif in dif_topology:
                    anahist_dirname = "%s/PEU%s/%s/wgAnaHist/Xml/dif%s" \
                                      % (idac_dir, peu, threshold_dir, dif)
                    if not overwrite and os.path.exists(anahist_dirname):
                        print("Skipping %s" % anahist_dirname)
                        continue
                    limit_threads(threads, MAX_NB_THREAD_CHAINS)
                    process = WagasciAnalysis(wagasci_lib)
                    threads.append(pedestal_ana_hist(process, idac_dir, acq_name, peu,
                                                     threshold_dir, dif, actual_acq_config_xml))
                    # result = pedestal_ana_hist(process, idac_dir, acq_name, peu,
                    #                            dif, actual_acq_config_xml)
                    # if result != 0:
                    #     print "wgAnaHist returned error code %s" %(result)
                    #     exit(result)
                    del process
                # dif loop
            # threshold dir
        # peu loop

        # Wait until all the threads have returned
        join_threads(threads)

    ###########################################################################
    #                             ana_hist_summary                            #
    ###########################################################################

    if anahist:

        for peu in RANGE_PEU:
            for threshold_dir in threshold_dirs:
                for dif in dif_topology:
                    anahist_dirname = "%s/PEU%s/%s/wgAnaHistSummary/Xml/dif%s" \
                                      % (idac_dir, peu, threshold_dir, dif)
                    if not overwrite and os.path.exists(anahist_dirname):
                        print("Skipping %s" % anahist_dirname)
                        continue
                    process = WagasciAnalysis(wagasci_lib)
                    result = pedestal_ana_hist_summary(process, idac_dir, peu, threshold_dir, dif)
                    if result != 0:
                        print("wgAnaHistSummary returned error code %s" % result)
                        exit(result)
                    del process
                # dif loop
            # threshold loop
        # peu loop

    process = WagasciAnalysis(wagasci_lib)
    result = pedestal_pedestal_calib(process, idac_dir)
    del process
    if result != 0:
        print("wgPedestalCalib returned error code %s" % result)
        exit(result)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description='Analyze the pedestal calibration data')

    PARSER.add_argument('-f', '--run_name', metavar='<run name>', type=str, nargs=1, required=True,
                        help='Name of the run to analyze. It must be inside the WAGASCI_CALIBDATADIR folder.')
    PARSER.add_argument('-d', '--disable-decoder', dest='decoder', action='store_false',
                        required=False, default=True, help="Disable the wgDecoder.")
    PARSER.add_argument('-m', '--disable-makehist', dest='makehist', action='store_false',
                        required=False, default=True, help="Disable the wgMakeHist.")
    PARSER.add_argument('-a', '--disable-anahist', dest='anahist', action='store_false',
                        required=False, default=True, help="Disable the wgAnaHist and wgAnaHistSummary.")
    PARSER.add_argument('-r', '--overwrite', dest='overwrite', action='store_true',
                        required=False, default=False, help="Overwrite flag.")
    PARSER.add_argument('-s', '--single-threshold', dest='single_threshold', action='store_true',
                        required=False, default=False, help=textwrap.dedent('''
                        If not set it is assumed that the low threshold LowTh, high threshold HighTh and middle
                        threshold MiddleTh folders are present. If set only the SingleTh folder is analyzed.
                        '''))

    ARGS = PARSER.parse_args()

    if isinstance(ARGS.run_name, list):
        ARGS.run_name = ARGS.run_name[0]
    RUN_NAME = ARGS.run_name

    DECODER = ARGS.decoder
    MAKEHIST = ARGS.makehist
    ANAHIST = ARGS.anahist
    OVERWRITE = ARGS.overwrite
    SINGLE_THRESHOLD = ARGS.single_threshold

    pedestal_analysis(RUN_NAME, DECODER, MAKEHIST, ANAHIST, OVERWRITE, SINGLE_THRESHOLD)
