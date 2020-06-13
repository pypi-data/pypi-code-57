#!python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

# pylint: disable-msg=too-many-arguments
# pylint: disable-msg=too-many-function-args
# pylint: disable-msg=too-many-locals

# Python modules
import os
import json
import argparse
import time
from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis import WagasciAnalysis
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils import join_threads, mkdir_p

# ROOT
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def _check_decoder(process, data_quality_dir, run_root_dir, run_name, dif, n_chips):
    dif = int(dif)
    n_chips = int(n_chips)
    input_raw_file = "%s/%s_ecal_dif_%s.raw" % (run_root_dir, run_name, dif)
    output_dir = "%s/wgDecoder" % data_quality_dir
    overwrite_flag = True
    compatibility_mode = False
    disable_calibration_variables = False
    return process.spawn("decoder", input_raw_file, "", output_dir,
                         overwrite_flag, compatibility_mode,
                         disable_calibration_variables, dif, n_chips)


def _check_make_hist(process, data_quality_dir, acq_name, acq_config_xml, dif):
    dif = int(dif)
    input_tree_file = "%s/wgDecoder/%s_ecal_dif_%s_tree.root" \
                      % (data_quality_dir, acq_name, dif)
    output_dir = "%s/wgMakeHist" % data_quality_dir
    flags = bitarray('0' * 9, endian='big')
    flags[8] = True  # non beam spills only
    flags[7] = True  # dark noise
    flags[5] = True  # charge nohit
    flags[4] = True  # charge hit HG
    flags[0] = True  # overwrite
    ul_flags = int(flags.to01(), 2)
    return process.make_hist(input_tree_file, acq_config_xml, output_dir,
                             ul_flags, dif)


def _check_ana_hist(process, data_quality_dir, acq_name, acq_config_xml, dif):
    dif = int(dif)
    input_hist_file = "%s/wgMakeHist/%s_ecal_dif_%s_hist.root" \
                      % (data_quality_dir, acq_name, dif)
    output_dir = "%s/wgAnaHist/Xml/dif_%s" % (data_quality_dir, dif)
    output_img_dir = "%s/wgAnaHist/Images/dif_%s" % (data_quality_dir, dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[6] = bool(acq_config_xml)
    flags[5] = False  # print
    flags[4] = True  # Dark noise
    flags[3] = True  # charge nohit
    flags[2] = True  # charge hit HG
    ul_flags = int(flags.to01(), 2)
    return process.spawn("ana_hist", input_hist_file, acq_config_xml, output_dir,
                         output_img_dir, ul_flags, dif)


def _check_ana_hist_summary(process, data_quality_dir, dif):
    dif = int(dif)
    input_dir = "%s/wgAnaHist/Xml/dif_%s" % (data_quality_dir, dif)
    output_dir = "%s/wgAnaHistSummary/Xml/dif_%s" % (data_quality_dir, dif)
    output_img_dir = "%s/wgAnaHistSummary/Images/dif_%s" % (data_quality_dir, dif)
    flags = bitarray('0' * 8, endian='big')
    flags[7] = True  # overwrite
    flags[5] = True  # print
    flags[4] = True  # Dark noise
    flags[3] = True  # charge nohit
    flags[2] = True  # charge hit HG
    ul_flags = int(flags.to01(), 2)
    return process.ana_hist_summary(input_dir, output_dir, output_img_dir, ul_flags)


def _bcid(decoded_filename, data_quality_dir, dif_id, n_chips, overwrite, hurry_up):
    decoded_file = ROOT.TFile.Open(decoded_filename, "READ")
    treename = "tree_dif_%s" % dif_id
    tree = getattr(decoded_file, treename)
    canvas = ROOT.TCanvas("BCID")
    canvas.cd()
    output_file = "%s/BunchStructure/dif%s/BCID_dif%s.png" \
                  % (data_quality_dir, dif_id, dif_id)
    if not overwrite and os.path.exists(output_file):
        print("Skipping %s" % output_file)
    else:
        tree.Draw("bcid>>(100,0,100)", "bcid != -1 && hit == 1 && spill_mode == 1 && charge > 750")
        canvas.Print(output_file)
    if not hurry_up:
        for chip_id in range(n_chips):
            output_file = "%s/BunchStructure/dif%s/BCID_dif%s_chip%s.png" \
                          % (data_quality_dir, dif_id, dif_id, chip_id)
            if not overwrite and os.path.exists(output_file):
                print("Skipping %s" % output_file)
                continue
            tree.Draw("bcid>>(100,0,100)", "bcid != -1 && hit == 1 && spill_mode == 1 && "
                                           "charge > 750 && chipid == %s" % chip_id)
            canvas.Print(output_file)
    decoded_file.Close()


def _time_ns(decoded_filename, data_quality_dir, dif_id, n_chips, overwrite, hurry_up):
    decoded_file = ROOT.TFile.Open(decoded_filename, "READ")
    treename = "tree_dif_%s" % dif_id
    tree = getattr(decoded_file, treename)
    canvas = ROOT.TCanvas("TDC")
    canvas.cd()
    output_file = "%s/BunchStructure/dif%s/TDC_dif%s.png" \
                  % (data_quality_dir, dif_id, dif_id)
    if not overwrite and os.path.exists(output_file):
        print("Skipping %s" % output_file)
    else:
        tree.Draw("time_ns>>(10000,10000,20000)", "time_ns != -1 && hit == 1 && "
                                                  "spill_mode == 1 && charge > 750")
        canvas.Print(output_file)
    if not hurry_up:
        for chip_id in range(n_chips):
            output_file = "%s/BunchStructure/dif%s/TDC_dif%s_chip%s.png" \
                          % (data_quality_dir, dif_id, dif_id, chip_id)
            if not overwrite and os.path.exists(output_file):
                print("Skipping %s" % output_file)
                continue
            tree.Draw("time_ns>>(10000,10000,20000)", "time_ns != -1 && hit == 1 && "
                                                      "spill_mode == 1 && charge > 750 && chipid == %s" % chip_id)
            canvas.Print(output_file)
    decoded_file.Close()


def _adc_by_channel(decoded_filename, data_quality_dir, dif_id, n_chips, overwrite):
    decoded_file = ROOT.TFile.Open(decoded_filename, "READ")
    treename = "tree_dif_%s" % dif_id
    tree = getattr(decoded_file, treename)
    canvas = ROOT.TCanvas("ADC")
    canvas.cd()
    for chip_id in range(n_chips):
        ichip = n_chips - chip_id - 1
        output_file = "%s/BunchStructure/dif%s/ADC_hit_dif%s_chip%s.png" \
                      % (data_quality_dir, dif_id, dif_id, chip_id)
        if not overwrite and os.path.exists(output_file):
            print("Skipping %s" % output_file)
            continue
        tree.Draw("charge[%d][][]:chanid[]>>(36,0,36,600,400,1000)" % ichip,
                  "hit[%d][][] == 1 && charge[%d][][] != -1" % (ichip, ichip), "colz")
        canvas.Print(output_file)
        output_file = "%s/BunchStructure/dif%s/ADC_nohit_dif%s_chip%s.png" \
                      % (data_quality_dir, dif_id, dif_id, chip_id)
        if not overwrite and os.path.exists(output_file):
            print("Skipping %s" % output_file)
            continue
        tree.Draw("charge[%d][][]:chanid[]>>(36,0,36,600,400,1000)" % ichip,
                  "hit[%d][][] == 0 && charge[%d][][] != -1" % (ichip, ichip), "colz")
        canvas.Print(output_file)
    decoded_file.Close()


# ============================================================================ #
#                                                                              #
#                                simple_data_quality                           #
#                                                                              #
# ============================================================================ #

def simple_data_quality(run_name, only_wallmrd=False, only_wagasci=False,
                        decoder=True, makehist=True, anahist=True,
                        anahistsummary=True, bunch_structure=True,
                        overwrite=False):
    """ Analyze pedestal calibration data """

    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
    decoder = bool(decoder)
    makehist = bool(makehist)
    anahist = bool(anahist)
    overwrite = bool(overwrite)

    # Environmental variables
    env = WagasciEnvironment()
    beamdata_dir = env['WAGASCI_BEAMDATADIR']
    data_quality_dir = env['WAGASCI_DQDIR']
    data_quality_dir += "/" + run_name
    wagasci_lib = env["WAGASCI_LIBDIR"]
    run_root_dir = beamdata_dir + "/" + run_name
    acq_config_xml = run_root_dir + "/" + run_name + ".xml"

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

        for dif in sorted(dif_topology):
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            decoded_file = "%s/wgDecoder/%s_ecal_dif_%s_tree.root" \
                           % (data_quality_dir, run_name, dif)
            if not overwrite and os.path.exists(decoded_file):
                print("Skipping %s" % decoded_file)
                continue
            process = WagasciAnalysis(wagasci_lib)
            n_chips = len(dif_topology[dif])
            threads.append(_check_decoder(process, data_quality_dir, run_root_dir,
                                          run_name, dif, n_chips))
            del process
        # dif loop

        # Wait until all the threads have returned
        join_threads(threads)
        time.sleep(5)

    #############################################################################
    #                                  make_hist                                #
    #############################################################################

    if makehist:

        for dif in sorted(dif_topology):
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            makehist_file = "%s/wgMakeHist/%s_ecal_dif_%s_hist.root" \
                            % (data_quality_dir, run_name, dif)
            if not overwrite and os.path.exists(makehist_file):
                print("Skipping %s" % makehist_file)
                continue
            process = WagasciAnalysis(wagasci_lib)
            result = _check_make_hist(process, data_quality_dir, run_name,
                                      acq_config_xml, dif)
            if result != 0:
                print("wgMakeHist returned error code %s" % result)
                exit(result)
            del process
        # dif loop

    #############################################################################
    #                                   ana_hist                                #
    #############################################################################

    if anahist:

        threads = []

        for dif in sorted(dif_topology):
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            anahist_dir = "%s/wgAnaHist/Xml/dif_%s" % (data_quality_dir, dif)
            if not overwrite and os.path.exists(anahist_dir):
                print("Skipping %s" % anahist_dir)
                continue
            process = WagasciAnalysis(wagasci_lib)
            threads.append(_check_ana_hist(process, data_quality_dir, run_name,
                                           acq_config_xml, dif))
            del process
        # dif loop

        # Wait until all the threads have returned
        join_threads(threads)
        time.sleep(5)

    #############################################################################
    #                             ana_hist_summary                              #
    #############################################################################

    if anahistsummary:

        for dif in sorted(dif_topology):
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            anahistsummary_dir = "%s/wgAnaHistSummary/Xml/dif_%s" % (data_quality_dir, dif)
            if not overwrite and os.path.exists(anahistsummary_dir):
                print("Skipping %s" % anahistsummary_dir)
                continue
            process = WagasciAnalysis(wagasci_lib)
            result = _check_ana_hist_summary(process, data_quality_dir, dif)
            if result != 0:
                print("wgAnaHistSummary returned error code %s" % result)
                exit(result)
            del process
        # dif loop

    ###########################################################################
    #                             Bunch structure                             #
    ###########################################################################

    if bunch_structure:

        for dif in sorted(dif_topology):
            if only_wagasci and int(dif) < 4:
                continue
            if only_wallmrd and int(dif) >= 4:
                continue
            n_chips = len(dif_topology[dif])
            decoded_filename = "%s/wgDecoder/%s_ecal_dif_%s_tree.root" \
                               % (data_quality_dir, run_name, dif)
            mkdir_p("%s/BunchStructure/dif%s" % (data_quality_dir, dif))
            if int(dif) < 4:
                hurry_up = False
            else:
                hurry_up = True
            _bcid(decoded_filename, data_quality_dir, dif, n_chips, overwrite, hurry_up)
            _time_ns(decoded_filename, data_quality_dir, dif, n_chips, overwrite, hurry_up)
            _adc_by_channel(decoded_filename, data_quality_dir, dif, n_chips, overwrite)
        # dif loop


###############################################################################
#                                  arguments                                  #
###############################################################################

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Simple data quality checks')

    PARSER.add_argument('run_name', metavar='N', type=str, nargs='+',
                        help='Name of the run to analyze')
    PARSER.add_argument('--only-wallmrd', dest='only_wallmrd', action='store_true')
    PARSER.add_argument('--only-wagasci', dest='only_wagasci', action='store_true')
    PARSER.add_argument('--disable-decoder', dest='decoder', action='store_false')
    PARSER.add_argument('--disable-makehist', dest='makehist', action='store_false')
    PARSER.add_argument('--disable-anahist', dest='anahist', action='store_false')
    PARSER.add_argument('--disable-anahistsummary', dest='anahistsummary',
                        action='store_false')
    PARSER.add_argument('--disable-bunch-structure', dest='bunch_structure',
                        action='store_false')
    PARSER.add_argument('--overwrite', dest='overwrite', action='store_true')

    PARSER.set_defaults(ignore_wagasci=False)
    ROOT.gROOT.SetBatch(True)

    ARGS = PARSER.parse_args()
    RUN_NAME = ARGS.run_name[0]
    ONLY_WAGASCI = False
    ONLY_WAGASCI = ARGS.only_wagasci
    ONLY_WALLMRD = False
    ONLY_WALLMRD = ARGS.only_wallmrd
    DECODER = True
    DECODER = ARGS.decoder
    BUNCH_STRUCTURE = True
    BUNCH_STRUCTURE = ARGS.bunch_structure
    MAKEHIST = True
    MAKEHIST = ARGS.makehist
    ANAHIST = True
    ANAHIST = ARGS.anahist
    ANAHISTSUMMARY = True
    ANAHISTSUMMARY = ARGS.anahistsummary
    OVERWRITE = False
    OVERWRITE = ARGS.overwrite

    simple_data_quality(RUN_NAME, ONLY_WALLMRD, ONLY_WAGASCI, DECODER, MAKEHIST,
                        ANAHIST, ANAHISTSUMMARY, BUNCH_STRUCTURE, OVERWRITE)
