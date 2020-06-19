import argparse
import os
from . import run_test
from .general.util import save_feedback_file
from .general.result_watchdog import ResultWatchdog
from .general.constants import WATCHDOG_TIMEOUT
from .builder import build
import time


parser = argparse.ArgumentParser(description="General purpose test evaluator", prog="feedback")
parser.add_argument('tested_file', type=str, help="file to be tested")
parser.add_argument('config_file', type=str, help="config for the test")
parser.add_argument('--verbose', '-v', action="store_true", help="Enable extra console logging")
parser.add_argument('--result_file', '-f', type=str, default="result.json", help="output file name")
parser.add_argument('--clear_cache', '-x', action="store_true", help="Remove all cached contents")
parser.add_argument('--copy_tmp', '-c', type=str, default=None, help="Copy tmp dir to specified location, before it's removed")
parser.add_argument('--enable_watchdog', '-w', action="store_true", help="Enable watchdog subprocess to ensure result file integrity [ONLY ENABLE ON EXAM ASSESSMENTS]")
parser.add_argument('--disable_result_validation', '-d', action="store_true", help="Disable validation checking on result files")

builder_parser = argparse.ArgumentParser(description="Create Autograder zip file", prog="feedback-builder")
builder_parser.add_argument('tested_file', type=str, help="file to be tested")
builder_parser.add_argument('config_file', type=str, help="config for the test")
builder_parser.add_argument('--verbose', '-v', action="store_true", help="Enable extra console logging")
builder_parser.add_argument('--output_zip', '-o', type=str, default="autograder.zip", help="Location of the generated zip")

def launch_watchdog(result_file):
    watchdog = ResultWatchdog(result_file, timeout=WATCHDOG_TIMEOUT)
    write_callback = watchdog.write_results_callback
    watchdog.launch()
    return write_callback

# Primary entry point, with argument processing
def main():
    args = parser.parse_args()

    write_callback = launch_watchdog(args.result_file) if args.enable_watchdog else None

    result = run_test(
        args.tested_file, 
        args.config_file, 
        {"clear_cache": args.clear_cache, "verbose": args.verbose, "check_validity": not args.disable_result_validation}, 
        args.copy_tmp)
    
    save_feedback_file(result, args.result_file, verbose=args.verbose, callback=write_callback)
    time.sleep(1)

def run_builder():
    args = builder_parser.parse_args()

    build(args.tested_file, args.config_file, args.output_zip, verbose=args.verbose)

if __name__ == "__main__":      # Run main if ran directly
    main()
    # run_builder()
