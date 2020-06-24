from pprint import pprint
import sys
import os
import argparse
import multiprocessing

from smear.file_identifier import detect_mc_type, McFileTypes
from smear.uiterm import markup_print as mprint
from smear.smearing import print_detectors, detectors

help_text = '''
Simple command line interface to eic-smear and jleic-smear

usage: 
  ejana_smear <flags> [input file]   # smears the input file
  ejana_smear -l                     # list of available detectors

examples:
  ejana_smear beagle_eD.txt                     # smear the file with handbook detector
  ejana_smear beagle_eD.txt -o my_file.root     # smears the file and set output file name  
  ejana_smear -d beast -n 10000 beagle_eD.txt   # uses beast detector, smears only 10k events
   
main flags:    
  -l / --list           Show all detectors and versions    
  -d / --detector       Detector parametrisation. Handbook is default. 
                        Run with -l/--list flag to see all options
  -n / --nevents        Number of events to process
  -s / --nskip          Number of events to skip    
  -o / --output         Output file name    
  -j / --threads        Number of threads. Set 'auto' for max. Default is 1  
  -h / --help           Show help

advanced flags:
  -t / --input-type     Input file type. Select from: beagle, hepmc2, lund, eic_pythia6, g4e, auto
  -a / --analysis       Comma separated additional analysis list
  --explain             Explain all configurations, but don't run smearing

number of events:
  One can set a number of events by -n(--nevents) and -s(--nskip) flags. Flag -n also support ranges:
    -n 100        : process 100 events
    -s 100 -n 50  : skip first 100 events, and process 50 events
    -s 100        : skip first 100 events and process the rest

known file formats:
  Applies to -t / --input-type
    beagle, hepmc2, lund, eic_pythia6, g4e, auto
'''

type_to_plugin = {
    'beagle': 'beagle_reader',
    'hepmc2': 'hepmc_reader',
    'eic_pythia6': 'lund_reader',
    'lund': 'lund_reader',
    'g4e': 'g4e_reaer'
}

def _get_jana_args(params):
    """Get Jana constructor arguments from general paramters"""
    jana_args = {}
    if params.nevents:
        jana_args['nevents'] = params.nevents

    if params.nskip:
        jana_args['nskip'] = params.nskip

    jana_args['output'] = params.output
    jana_args['nthreads'] = params.threads
    return jana_args


def run_smearing(params):
    from pyjano.jana import Jana

    jana_args = _get_jana_args(params)

    jana = Jana(**jana_args)
    jana.plugin(type_to_plugin[params.input_type])
    jana.plugin('event_writer')
    jana.plugin('eic_smear', detector=params.detector)
    jana.source(params.input_file)

    if params.explain:
        mprint("<b><blue>run command  : </blue></b> ejana " + jana.get_run_command())
    else:
        jana.run()


def makeup_output_file_name(input_file):
    file_name = os.path.basename(input_file)
    base, ext = os.path.splitext(file_name)
    return base + ".root"


def process_arguments(args):

    # First, we parse arguments using argparse
    params = parse_arguments(args)

    # Result will be argparse.Namespace or int with suggested return code
    if isinstance(params, int):
        return params

    # print input file
    mprint("<b><blue>input  file  : </blue></b>" + params.input_file)
    # Test the file exists
    if not os.path.isfile(params.input_file):
        mprint("<red>(!) Error (!)</red> File does not exist or there is no permission to read it. "
               "File name is '{}' \n", params.input_file)
        return 1

    # Validate the detector
    if params.detector:
        if params.detector not in detectors.keys():
            mprint("<red>(!) Error (!)</red> Detector '{}' is not a known detector name/version. "
                   "Please run with -l flag to see the list of all available detectors".format(params.detector))
            return 1

    # determine file type
    if not params.input_type or params.input_type == 'auto':
        params.input_type = detect_mc_type(params.input_file).value
        if params.input_type == 'unknown':
            mprint("<red>(!) Error (!)</red> Cannot automatically determine file type. "
                   "Use -t/--input-type flag to set file type manually. Known types are: " + McFileTypes.list())
            return 1

        mprint("<b><blue>input  type  : </blue></b>" + params.input_type + " <green>(auto)</green>")
    else:
        mprint("<b><blue>input  type  : </blue></b>" + params.input_type)

    # makeup output file name
    if not params.output:
        params.output = makeup_output_file_name(params.input_file)
        mprint("<b><blue>output file  : </blue></b>" + params.output + " <green>(auto)</green>")
    else:
        mprint("<b><blue>output file  : </blue></b>" + params.output)

    # Number of events to skip
    if params.nskip:
        mprint("<b><blue>skip events  : </blue></b> " + str(params.nskip))
    else:
        mprint("<b><blue>skip events  : </blue></b>don't skip")

    # Number of events to process
    if params.nevents:
        mprint("<b><blue>proc events  : </blue></b>" + str(params.nevents))
    else:
        mprint("<b><blue>proc events  : </blue></b>until the end of file")

    # Number of threads
    available_threads = multiprocessing.cpu_count()
    if not params.threads:
        params.threads = 1
        mprint("<b><blue>num threads  : </blue></b>{} out of {} <green>(default)</green>",
               params.threads, available_threads)
    else:
        if params.threads == 'auto':
            params.threads = available_threads
            mprint("<b><blue>num threads  : </blue></b>{} <green>(auto)</green>", params.threads)
        else:
            params.threads = int(params.threads)
            mprint("<b><blue>num threads  : </blue></b>{}", params.threads)

    # detector
    if not params.detector:
        params.detector = 'matrix'
        mprint("<b><blue>detector     : </blue></b>" + params.detector + " latest <green>(default)</green>")
    else:
        mprint("<b><blue>detector     : </blue></b>" + params.detector)

    return params


def parse_arguments(args):
    """
    Parses program arguments


    :param args: sys.argv or test arguments
    :return: Returns either integer with the exist code or parse result
    """


    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False)

    parser.add_argument('input_files', nargs='*', default=None)

    # "List detectors"
    parser.add_argument("-l", "--list", action="store_true", help=argparse.SUPPRESS)    # List all available detectors
    parser.add_argument("-a", "--analysis", type=str, help=argparse.SUPPRESS)           # Comma separated additional analysis list
    parser.add_argument("-d", "--detector", type=str, help=argparse.SUPPRESS)           # Detector parametrisation. Handbook is default. Run -l/--list flag to see all options
    parser.add_argument("-t", "--input-type", default='auto', help=argparse.SUPPRESS)   # Input file type. Select from: beagle, hepmc2, lund, g4e
    parser.add_argument("-o", "--output", help=argparse.SUPPRESS)                       # Output file name
    parser.add_argument("-n", "--nevents", type=int, help=argparse.SUPPRESS)            # Number of events to process
    parser.add_argument("-s", "--nskip", type=int, help=argparse.SUPPRESS)              # Number of events to skip. See details for ranges
    parser.add_argument("-j", "--threads", help=argparse.SUPPRESS)                      # Number of threads
    parser.add_argument("-h", "--help", action="store_true", dest='show_help')          # Show help
    parser.add_argument("--explain", action="store_true")                               # Just explain the setup but don't run enything

    result = parser.parse_args(args)

    if len(sys.argv) == 0:
        print("(!) Provide at least one file to process. Run with --help flag")
        print(help_text)
        return 1

    if result.show_help:
        print(help_text)
        return 0

    if result.list:
        print_detectors()
        return 0

    # Validate input files
    if not result.input_files:
        mprint("<red>(!) Error (!)</red> Please provide at least one input file")
        print(help_text)
        return 1

    if len(result.input_files) > 1:
        mprint("<red>(!) Error (!)</red> Unfortunately, only a single file can be processed at a time. "
               "It will be updated in further versions")
        return 1

    result.input_file = result.input_files[0]

    return result


def smear_cli(args=None):
    """Run smearing according to user arguments"""
    # Print the setup and auto-identify missing params
    program_params = process_arguments(args if args is not None else sys.argv[1:])

    # Result will be argparse.Namespace or int with suggested return code
    if isinstance(program_params, int):
        exit(program_params)
    run_smearing(program_params)

    return program_params


if __name__ == "__main__":
    pp = smear_cli()
    pprint(pp)

