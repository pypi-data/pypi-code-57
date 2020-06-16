"""
Client to submit jobs to and retrieve results from a remote ngscheck service.
"""
import argparse
import getpass
import logging
import sys

from . import api


LOGGER = logging.getLogger(__name__)


def main():
    """
    Top-level control flow.
    """
    args = get_args(sys.argv[1:])
    logging.basicConfig(level=args.loglevel)
    exit_code = 0
    try:
        if args.password_file:
            password = args.password_file.read().strip()
            args.password_file.close()
        else:
            password = args.password or getpass.getpass("Password: ")
        token = api.get_access_token(args.email, password)
        userid = api.get_userid(token)
        command = args.subcommand
        if command == 'submit':
            api.submit(args.files, args.manifest_file, userid, token)
        elif command == 'get_status':
            api.get_status(args.manifest_file, userid, token)
        elif command == 'get_results':
            # get_status first to get latest status
            api.get_status(args.manifest_file, userid, token)
            api.get_results(args.manifest_file, args.include_logs,
                            userid, token)
        elif command == 'get_userid':
            print(userid)
        else:
            raise NotImplementedError(command)

    except Exception as ex:
        LOGGER.exception(ex)
        exit_code = 1
    LOGGER.info("exit_code: %s", exit_code)
    sys.exit(exit_code)


def get_args(args):
    """
    Parse arguments from the command line.

    Args:
        args: options & arguments from the command line, e.g. sys.argv[1:]

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(description=__doc__)

    common_args = parser.add_argument_group('common arguments')
    common_args.add_argument(
        "--email",
        required=True,
        help="email used to sign up to the service")
    password_group = common_args.add_mutually_exclusive_group()
    password_group.add_argument(
        "--password",
        help="using --password-file or interactive use is safer")
    password_group.add_argument(
        "--password-file",
        type=argparse.FileType('r'),
        help="if neither --password nor --password-file is supplied a "
        "password will be prompted for interactively")
    common_args.add_argument(
        "--verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        default=logging.WARNING,
        help="output more logging (INFO level)")

    subparsers = parser.add_subparsers(
        dest="subcommand",
        required=True,
        help="SUBCOMMAND -h for subcommand help")

    submit_p = subparsers.add_parser(
        "submit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="submit qprofiler outputs to be analyzed and generate job "
        "manifest file")
    submit_p.add_argument(
        "files",
        metavar="QPXML",
        type=argparse.FileType('rb'),
        nargs='+')
    submit_p.add_argument(
        "--manifest-file",
        # exclusive new write (fail if exists)
        type=argparse.FileType('x'),
        default="manifest.json",
        help="name of the job manifest file that will be created")

    get_status_p = subparsers.add_parser(
        "get_status",
        help="check and update status of jobs listed in a manifest file")
    get_status_p.add_argument(
        "--manifest-file",
        required=True,
        type=argparse.FileType('r'))

    get_results_p = subparsers.add_parser(
        "get_results",
        help="get results of completed jobs listed in a manifest file")
    get_results_p.add_argument(
        "--manifest-file",
        required=True,
        type=argparse.FileType('r'))
    get_results_p.add_argument(
        "--include-logs",
        action='store_true',
        help="also get log files, may be useful to troubleshoot failed jobs")

    subparsers.add_parser(
        "get_userid",
        help="return user identifier associated with this account (FYI only)")

    return parser.parse_args(args)


if __name__ == "__main__":
    main()
