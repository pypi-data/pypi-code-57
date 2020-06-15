"""Main entry point for CLI application"""
import argparse
import re

from scruf import compare, execute, parse, run as scruf_run
from scruf.observers import tap


def run(argv):
    """Run scruf with options over some files

    Returns
    -------
    int
        0 if all tests pass, otherwise 1, suitable for sys.exit
    """
    options = _get_options(argv[1:])
    filenames = options.pop("files")
    observer = _build_observer()

    exit_code = 0 if run_files(filenames, options, observer) else 1
    return exit_code


def run_files(filenames, options, observer):
    success = True
    for filename in filenames:
        success &= run_file(filename, options, observer)
    return success


def run_file(filename, options, observer):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except (OSError, IOError) as file_error:
        observer.notify_file_open_error(filename, file_error)
        return False
    observer.notify_before_testing_file(filename)

    parser = parse.Parser(options["indent"])
    try:
        tests = parser.parse(lines)
    except parse.ProgressionError as e:
        observer.notify_test_progression_error(filename, e)
        return False

    try:
        executor = execute.Executor(shell=options["shell"], cleanup=options["cleanup"])
    except execute.FailedToCreateTestDirError as e:
        observer.notify_execute_setup_error(filename, e)
        return False

    return run_tests(tests, executor, observer)


def run_tests(tests, executor, observer=None):
    success = True
    observer.notify_before_tests_run(tests)

    for i, test in enumerate(tests):
        test_number = i + 1
        observer.notify_before_test_run(test, test_number)

        if not _run_setup_commands(test, test_number, executor, observer):
            success = False
            continue

        exec_result = executor.execute(test.command)
        try:
            compare_output = scruf_run.run_test(test, exec_result)
        except (compare.RegexError, execute.OutOfLinesError) as e:
            observer.notify_test_error(test, test_number, e)
            success = False
            continue

        failed_tests = [r for r in compare_output if not r["comparison_result"]]
        if len(failed_tests) == 0:
            observer.notify_test_success(test, test_number)
        else:
            observer.notify_test_failure(test, test_number, failed_tests)
            success = False
    return success


def _run_setup_commands(test, test_number, executor, observer):
    for setup_command in test.setup_commands:
        setup_result = executor.execute(setup_command)

        if setup_result.returncode != 0:
            observer.notify_setup_command_failure(
                test, test_number, setup_command, setup_result
            )
            return False
    return True


def _get_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="FILE", nargs="+", help="File(s) to be tested")
    parser.add_argument(
        "--no-cleanup",
        action="store_false",
        dest="cleanup",
        help="Avoid cleaning up temporary test directory",
    )
    parser.add_argument(
        "-s",
        "--shell",
        type=str,
        help="Path to shell to be used to run tests with. Default is '/bin/sh'",
        default="/bin/sh",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=_indent_arg_type,
        default="    ",
        help="String to be used for detecting indentation when parsing tests. Default \
            is 4 spaces, use a literal '\\t' to denote a tab character",
    )

    return vars(parser.parse_args(args))


def _indent_arg_type(string):
    # Convert literal "\t" to tab characters, e.g. for "--indent '\t'"
    string = re.sub(r"\\t", "\t", string)

    if not string.isspace():
        import sys

        print("You gave me: '{}'".format(string), file=sys.stderr)
        msg = "{} is not entirely whitespace".format(string)
        raise argparse.ArgumentTypeError(msg)
    return string


def _build_observer():
    # TODO: once more than one observer exists this should take an option to decide
    # which to use
    return tap.TapObserver()
