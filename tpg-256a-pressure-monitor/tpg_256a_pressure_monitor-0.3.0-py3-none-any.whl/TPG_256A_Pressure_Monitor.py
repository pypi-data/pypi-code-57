""" Logging module for the TPG 256A Pressure
Monitor. The module manages a :class:`~Daemon.Daemon`
object over TCP communication.
"""

# Imports
from sys import argv
from configparser import Error as ConfigError
from argparse import ArgumentParser, Namespace

# Third party
from zc.lockfile import LockError
from lab_utils.socket_comm import Client
from lab_utils.custom_logging import configure_logging, getLogger

# Local packages
from tpg_256a_pressure_monitor.Daemon import Daemon
from tpg_256a_pressure_monitor.__project__ import (
    __documentation__ as docs_url,
    __module_name__ as module,
    __description__ as prog_desc,
)


def tpg_256a_pressure_monitor():
    """The main routine. It parses the input argument and acts accordingly."""

    # The argument parser
    ap = ArgumentParser(
        prog=module,
        description=prog_desc,
        add_help=True,
        epilog='Check out the package documentation for more information:\n{}'.format(docs_url)
    )

    # Optional arguments
    ap.add_argument(
        '-l',
        '--logging-config-file',
        help='configuration file with the logging options',
        default=None,
        dest='logging_config_file',
        type=str,
    )
    ap.add_argument(
        '-s',
        '--server-config-file',
        help='configuration file with the Alarm Manager options',
        default=None,
        dest='server_config_file',
        type=str,
    )
    ap.add_argument(
        '-d',
        '--device-config-file',
        help='configuration file with the device options',
        default=None,
        dest='device_config_file',
        type=str,
    )
    ap.add_argument(
        '-db',
        '--database-config-file',
        help='configuration file with the Database options',
        default=None,
        dest='database_config_file',
        type=str,
    )
    ap.add_argument(
        '-a',
        '--address',
        help='host address',
        default=None,
        dest='host',
        type=str
    )
    ap.add_argument(
        '-p',
        '--port',
        help='host port',
        default=None,
        dest='port',
        type=int
    )

    # Mutually exclusive positional arguments
    pos_arg = ap.add_mutually_exclusive_group()
    pos_arg.add_argument(
        '--run',
        action='store_true',
        help='starts the TPG-256A daemon',
        default=False,
    )
    pos_arg.add_argument(
        '--control',
        type=str,
        help='send a control command to the running TPG-256A daemon',
        nargs='?',
    )

    # Parse the arguments
    args, extra = ap.parse_known_args(args=argv[1:])
    if extra is not None and args.control is not None:
        args.control += ' ' + ' '.join(extra)

    # Setup logging
    configure_logging(
        config_file=args.logging_config_file,
        logger_name='TPG-256A'
    )

    # Call appropriate function
    if args.run:
        run(args)
    else:
        send_message(args)


def send_message(args: Namespace):
    """ Sends a string message to a running TPG-256A
    :class:`Daemon` object over TCP."""

    try:
        # Start a client
        c = Client(
            config_file=args.server_config_file,
            host=args.host,
            port=args.port,
        )
        getLogger().info('Opening connection to the TPG-256A server on {h}:{p}'.format(
            h=c.host,
            p=c.port
        ))

        # Send message and get reply
        getLogger().info('Sending message: %s', args.control)
        reply = c.send_message(args.control)
        getLogger().info(reply)

    except ConfigError as e:
        getLogger().error('Did you provide a valid configuration file?')

    except OSError as e:
        getLogger().error('Maybe the TPG-256A server is not running, or running elsewhere')

    except BaseException as e:
        # Undefined exception, full traceback to be printed
        getLogger().exception("{}: {}".format(type(e).__name__, e))

    else:
        exit(0)

    # Something went wrong...
    exit(1)


def run(args: Namespace):
    """ Launches a TPG-256A
    :class:`Daemon` object."""

    try:
        # Start the daemon
        getLogger().info('Starting the TPG-256A server...')
        the_daemon = Daemon(
            config_file=args.server_config_file,
            pid_file_name='/tmp/tpg_256a.pid',
            host=args.host,
            port=args.port,
            device_config_file=args.device_config_file,
        )

        # the_daemon.db.config(resource_filename(__name__, 'conf/database.ini'))
        the_daemon.start_daemon()
        getLogger().info('TPG-256A server stopped, bye!')

    except ConfigError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Did you provide a valid configuration file?')

    except OSError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Possible socket error, do you have permissions to the socket?')

    except LockError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('TPG-256A daemon is probably running elsewhere.')

    except BaseException as e:
        # Undefined exception, full traceback to be printed
        getLogger().exception("{}: {}".format(type(e).__name__, e))

    else:
        exit(0)

    # Something went wrong...
    exit(1)
