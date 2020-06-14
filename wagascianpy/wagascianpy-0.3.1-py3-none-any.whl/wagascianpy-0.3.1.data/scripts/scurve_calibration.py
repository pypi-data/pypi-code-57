#!python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio, Eguchi Aoi

""" Script to analyze the S-curve data of the SPIROC2D ASIC """

# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-function-args
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=line-too-long

# Python modules
import json
import argparse
import os
from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis import WagasciAnalysis
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils import list_dir_with_integer, join_threads, limit_threads

MAX_NB_THREAD_CHAINS = 16


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def scurve_decoder(process, threshold_dir, acq_name, dif, n_chips):
    """ wgDecoder for the scurve_run.py script """
    dif = int(dif)
    n_chips = int(n_chips)
    input_raw_file = "%s/RawData/%s_ecal_dif_%d.raw" \
                     % (threshold_dir, acq_name, dif)
    output_dir = "%s/wgDecoder" % threshold_dir
    overwrite_flag = True
    compatibility_mode = False
    disable_calibration_variables = True
    return process.spawn("decoder", input_raw_file, "", output_dir,
                         overwrite_flag, compatibility_mode,
                         disable_calibration_variables, dif, n_chips)


def scurve_make_hist(process, threshold_dir, acq_name, dif, acq_config_xml):
    """ wgMakeHist for the pedestal_run.py script """
    dif = int(dif)
    input_tree_file = "%s/wgDecoder/%s_ecal_dif_%d_tree.root" \
                      % (threshold_dir, acq_name, dif)
    output_dir = "%s/wgMakeHist" % threshold_dir
    flags = bitarray('0' * 9, endian='big')
    flags[7] = True  # dark noise
    flags[0] = True  # overwrite
    ul_flags = int(flags.to01(), 2)
    return process.make_hist(input_tree_file, acq_config_xml, output_dir,
                             ul_flags, dif)


def scurve_ana_hist(process, threshold_dir, acq_name, dif, acq_config_xml):
    """ wgAnaHist for the pedestal_run.py script """
    dif = int(dif)
    input_hist_file = "%s/wgMakeHist/%s_ecal_dif_%d_hist.root" \
                      % (threshold_dir, acq_name, dif)
    output_dir = "%s/wgAnaHist/Xml/dif%d" % (threshold_dir, dif)
    output_img_dir = "%s/wgAnaHist/Images/dif%d" % (threshold_dir, dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[6] = bool(acq_config_xml)
    flags[5] = False  # print
    flags[4] = True  # Dark noise
    ul_flags = int(flags.to01(), 2)
    return process.ana_hist(input_hist_file, acq_config_xml,
                            output_dir, output_img_dir, ul_flags, dif)


def scurve_ana_hist_summary(process, threshold_dir, dif):
    """ wgAnaHistSummary for the pedestal_run.py script """
    dif = int(dif)
    input_dir = "%s/wgAnaHist/Xml/dif%d" % (threshold_dir, dif)
    output_xml_dir = "%s/wgAnaHistSummary/Xml/dif%d" % (threshold_dir, dif)
    output_img_dir = "%s/wgAnaHistSummary/Images/dif%d" % (threshold_dir, dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[5] = False  # print
    flags[4] = True  # Dark noise
    ul_flags = int(flags.to01(), 2)
    return process.ana_hist_summary(input_dir, output_xml_dir,
                                    output_img_dir, ul_flags)


def scurve_scurve(process, run_root_dir):
    """ wgScurve for the scurve_run.py script """
    output_dir = run_root_dir + "/wgScurve/Xml"
    output_img_dir = run_root_dir + "/wgScurve/Images"
    paranoid_mode = False
    return process.scurve(run_root_dir, output_dir, output_img_dir,
                          paranoid_mode)


# ================================================================ #
#                                                                  #
#                          scurve_analysis                         #
#                                                                  #
# ================================================================ #

def scurve_analysis(run_name, decoder=True, makehist=True, anahist=True,
                    overwrite=False):
    """ S-curve run """

    decoder = bool(decoder)
    makehist = bool(makehist)
    anahist = bool(anahist)
    overwrite = bool(overwrite)

    # Environmental variables
    env = WagasciEnvironment()
    calibdata_dir = env['WAGASCI_CALIBDATADIR']
    wagasci_lib = env["WAGASCI_LIBDIR"]

    run_root_dir = calibdata_dir + "/" + run_name
    acq_config_path = run_root_dir + "/" + os.path.basename(env['WAGASCI_ACQCONFIGDIR'])
    acq_config_xml = acq_config_path + "/" + env['WAGASCI_ACQCONFIGXML']
    if not os.path.exists(acq_config_xml):
        print("Acquisition configuration XML file not found : %s"
              % acq_config_xml)

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

    if decoder:

        threads = []

        idac_dirs = list_dir_with_integer(run_root_dir)

        for idac, idac_dir in idac_dirs:
            threshold_dirs = list_dir_with_integer(run_root_dir + "/" + idac_dir)
            for threshold, threshold_dir in threshold_dirs:
                threshold_dir = run_root_dir + "/" + idac_dir + "/" + threshold_dir
                acq_name = "%s_iDAC%s_threshold%s" % (run_name, idac, threshold)
                for dif in dif_topology:
                    decoded_filename = "%s/wgDecoder/%s_ecal_dif_%s_tree.root" \
                                       % (threshold_dir, acq_name, dif)
                    if not overwrite and os.path.exists(decoded_filename):
                        print("Skipping %s" % decoded_filename)
                        continue
                    limit_threads(threads, MAX_NB_THREAD_CHAINS)
                    n_chips = len(dif_topology[dif])
                    process = WagasciAnalysis(wagasci_lib)
                    threads.append(scurve_decoder(process, threshold_dir, acq_name, dif, n_chips))
                    del process
                # dif loop
            # threshold loop
        # idac loop

        # Wait until all the threads have returned
        join_threads(threads)

    ###########################################################################
    #                                make_hist                                #
    ###########################################################################

    if makehist:

        idac_dirs = list_dir_with_integer(run_root_dir)

        for idac, idac_dir in idac_dirs:
            threshold_dirs = list_dir_with_integer(run_root_dir + "/" + idac_dir)
            for threshold, threshold_dir in threshold_dirs:
                threshold_dir = run_root_dir + "/" + idac_dir + "/" + threshold_dir
                acq_name = "%s_iDAC%s_threshold%s" % (run_name, idac, threshold)
                actual_acq_config_xml = "%s/RawData/%s.xml" \
                                        % (threshold_dir, acq_name)
                for dif in dif_topology:
                    makehist_filename = "%s/wgMakeHist/%s_ecal_dif_%s_hist.root" \
                                        % (threshold_dir, acq_name, dif)
                    if not overwrite and os.path.exists(makehist_filename):
                        print("Skipping %s" % makehist_filename)
                        continue
                    process = WagasciAnalysis(wagasci_lib)
                    result = scurve_make_hist(process, threshold_dir, acq_name,
                                              dif, actual_acq_config_xml)
                    if result != 0:
                        print("wgMakeHist returned error code %d" % result)
                        exit(result)
                    del process
                # dif loop
            # threshold loop
        # idac loop

    #############################################################################
    #                                   ana_hist                                #
    #############################################################################

    if anahist:

        idac_dirs = list_dir_with_integer(run_root_dir)

        for idac, idac_dir in idac_dirs:
            threshold_dirs = list_dir_with_integer(run_root_dir + "/" + idac_dir)
            for threshold, threshold_dir in threshold_dirs:
                threshold_dir = run_root_dir + "/" + idac_dir + "/" + threshold_dir
                acq_name = "%s_iDAC%s_threshold%s" % (run_name, idac, threshold)
                actual_acq_config_xml = "%s/RawData/%s.xml" \
                                        % (threshold_dir, acq_name)
                for dif in dif_topology:
                    anahist_dirname = "%s/wgAnaHist/Xml/dif%s" % (threshold_dir, dif)
                    if not overwrite and os.path.exists(anahist_dirname):
                        print("Skipping %s" % anahist_dirname)
                        continue
                    process = WagasciAnalysis(wagasci_lib)
                    result = scurve_ana_hist(process, threshold_dir, acq_name, dif,
                                             actual_acq_config_xml)
                    if result != 0:
                        print("wgAnaHist returned error code %d" % result)
                        exit(result)
                    del process
                # dif loop
            # peu loop
        # input_dac loop

    #############################################################################
    #                               ana_hist_summary                            #
    #############################################################################

    if anahist:

        idac_dirs = list_dir_with_integer(run_root_dir)

        for idac, idac_dir in idac_dirs:
            threshold_dirs = list_dir_with_integer(run_root_dir + "/" + idac_dir)
            for threshold, threshold_dir in threshold_dirs:
                threshold_dir = run_root_dir + "/" + idac_dir + "/" + threshold_dir
                for dif in dif_topology:
                    anahist_dirname = "%s/wgAnaHistSummary/Xml/dif%s" % (threshold_dir, dif)
                    if not overwrite and os.path.exists(anahist_dirname):
                        print("Skipping %s" % anahist_dirname)
                        continue
                    process = WagasciAnalysis(wagasci_lib)
                    result = scurve_ana_hist_summary(process, threshold_dir, dif)
                    if result != 0:
                        print("wgAnaHistSummary returned error code %d" % result)
                        exit(result)
                    del process
                # dif loop
            # peu loop
        # input_dac loop

    #######################################################################
    #                           scurve analysis                           #
    #######################################################################

    process = WagasciAnalysis(wagasci_lib)
    result = scurve_scurve(process, run_root_dir)
    del process
    if result != 0:
        print("wgScurve returned error code %d" % result)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Analyze Scurve data')

    PARSER.add_argument('run_name', metavar='N', type=str, nargs='+',
                        help='Name of the run to analyze')
    PARSER.add_argument('--disable-decoder', dest='decoder', action='store_false')
    PARSER.add_argument('--disable-makehist', dest='makehist', action='store_false')
    PARSER.add_argument('--disable-anahist', dest='anahist', action='store_false')
    PARSER.add_argument('--overwrite', dest='overwrite', action='store_true')

    PARSER.set_defaults(ignore_wagasci=False)

    ARGS = PARSER.parse_args()
    RUN_NAME = ARGS.run_name[0]
    DECODER = True
    DECODER = ARGS.decoder
    MAKEHIST = True
    MAKEHIST = ARGS.makehist
    ANAHIST = True
    ANAHIST = ARGS.anahist
    OVERWRITE = False
    OVERWRITE = ARGS.overwrite

    scurve_analysis(RUN_NAME, DECODER, MAKEHIST, ANAHIST, OVERWRITE)
