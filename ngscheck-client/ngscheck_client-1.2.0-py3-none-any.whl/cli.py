"""
Client to submit jobs to and retrieve results from a remote ngscheck service.
"""
import argparse
import logging
import sys

from getpass import getpass 
from os.path import basename

from . import api, util


LOGGER = logging.getLogger(__name__)


def main():
    """
    Top-level control flow.
    """
    parser = get_parser()
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    exit_code = 0
    try:
        # auth stuff common to API actions
        if hasattr(args, 'email'):
            password = (args.password_file.readline().strip()
                        if args.password_file else getpass('Password: '))
            token = api.get_access_token(args.email, password)
            userid = api.get_userid(token)

        action = args.action
        if action == 'validate':
            invalid = [f.name for f in args.files if not util.validate(f)]
            if invalid:
                LOGGER.error("invalid files: %s", invalid)
                exit_code = 2
            else:
                LOGGER.info("all files are valid")
        elif action == 'submit':
            api.submit(args.files, args.manifest_file, userid, token)
        elif action == 'get_status':
            api.get_status(args.manifest_file, userid, token)
        elif action == 'get_results':
            # get_status first to get latest status
            api.get_status(args.manifest_file, userid, token)
            api.get_results(args.manifest_file, args.include_logs,
                            userid, token)
        elif action == 'get_userid':
            print(userid)
        else:
            raise NotImplementedError(action)

    except Exception as ex:
        LOGGER.exception(ex)
        exit_code = 1
    LOGGER.info("exit_code: %s", exit_code)
    sys.exit(exit_code)


def get_parser():
    """
    Return a configured ArgumentParser for command-line use.
    """
    my_name = basename(sys.argv[0])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        default=logging.WARNING,
        help="output more logging (INFO level)")

    subparsers = parser.add_subparsers(
        dest="action",
        title="actions",
        required=True,
        help=f"{my_name} ACTION -h for help on individual actions")

    validate = subparsers.add_parser(
        "validate",
        help="validate qprofiler2 outputs")
    validate.add_argument(
        "files",
        metavar="QPXML",
        type=argparse.FileType('rb'),
        nargs='+')

    # all API actions require auth
    api_actions = argparse.ArgumentParser(add_help=False)
    api_actions.add_argument(
        "--email",
        required=True,
        help="email used to sign up to the service")
    api_actions.add_argument(
        "--password-file",
        type=argparse.FileType('r'),
        help="if --password-file is not supplied a password will be prompted "
        "for interactively")

    submit_p = subparsers.add_parser(
        "submit",
        parents=[api_actions],
        help="submit qprofiler2 outputs to be analyzed and generate job "
        "manifest file")
    submit_p.add_argument(
        "files",
        metavar="QPXML",
        type=argparse.FileType('rb'),
        nargs='+')
    submit_p.add_argument(
        "--manifest-file",
        required=True,
        # exclusive new write (fail if exists)
        type=argparse.FileType('x'),
        help="name of the job manifest file that will be created")

    get_status_p = subparsers.add_parser(
        "get_status",
        parents=[api_actions],
        help="check and update status of jobs listed in a manifest file")
    get_status_p.add_argument(
        "--manifest-file",
        required=True,
        type=argparse.FileType('r'))

    get_results_p = subparsers.add_parser(
        "get_results",
        parents=[api_actions],
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
        parents=[api_actions],
        help="return user identifier associated with this account (FYI only)")

    return parser


if __name__ == "__main__":
    main()
