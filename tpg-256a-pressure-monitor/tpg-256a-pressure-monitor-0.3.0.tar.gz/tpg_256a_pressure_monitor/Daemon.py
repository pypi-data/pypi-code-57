""" Daemon TCP server. The server will run indefinitely
listening on the specified TCP (see the
:class:`~lab_utils.socket_comm.Server` documentation).
When a client connects and sends a message string, the
message parser will call the appropriate method. The
following commands are supported by the parser (options
must be used with a double dash \\- \\-):

+-----------+-----------------------+---------------------------------------------------------------------------+
| quit      |                       | Stops the daemon and cleans up database and serial port                   |
+-----------+-----------------------+---------------------------------------------------------------------------+
| status    |                       | TODO: Not implemented yet                                                 |
+-----------+-----------------------+---------------------------------------------------------------------------+
| tpg_256a  | on/off/restart        | Connects / disconnects / restarts the TPG 256A device                     |
+           +-----------------------+---------------------------------------------------------------------------+
|           | test                  | Performs a serial port test and returns the device firmware               |
+           +-----------------------+---------------------------------------------------------------------------+
|           | config {file}         | Reloads the default (or given) config file (logging is stopped)           |
+           +-----------------------+---------------------------------------------------------------------------+
|           | gauge-info            | Returns gauge type, status and latest value                               |
+           +-----------------------+---------------------------------------------------------------------------+
|           | single-readout        | Performs a single read-out to the device (logging is stopped)             |
+-----------+-----------------------+---------------------------------------------------------------------------+
| logging   | start / stop          | Launches or stops the separate device monitoring thread                   |
+           +-----------------------+---------------------------------------------------------------------------+
|           | terminal              | Prints output to the terminal with *info* level                           |
+           +-----------------------+---------------------------------------------------------------------------+
|           | use-database          | Enables data saving to a PostgreSQL database                              |
+-----------+-----------------------+---------------------------------------------------------------------------+

"""

# Imports
from serial import SerialException
import argparse
import configparser
from psycopg2 import DatabaseError
from configparser import Error as ConfigError

# Third party
from lab_utils.socket_comm import Server

# Local
from .TPG_256A import TPG_256A, StateError
from .Monitor import Monitor
from .__project__ import (
    __documentation__ as docs_url,
    __description__ as prog_desc,
    __module_name__ as mod_name,
)


class Daemon(Server):
    """ Base class of the daemon, derived from
    :class:`~lab_utils.socket_comm.Server`. The daemon
    holds pointers to the :attr:`device` driver and the
    :attr:`monitor` thread, and communicates with them
    upon message reception. """

    # Attributes
    device: TPG_256A = None     #: Device handler.
    monitor: Monitor = None     #: Monitor thread.

    def __init__(self,
                 config_file: str = None,
                 pid_file_name: str = None,
                 host: str = None,
                 port: int = None,
                 autostart: bool = False,
                 device_config_file: str = None,
                 database_config_file: str = None,
                 ):
        """ Initializes the :class:`Daemon` object.
        The :attr:`device` constructor is called:
        serial connection is established and hardware
        information is retrieved from the controller.

        Parameters
        ----------
        config_file : str, optional
            See parent class :class:`~lab_utils.socket_comm.Server`.

        pid_file_name : str, optional
            See parent class :class:`~lab_utils.socket_comm.Server`.

        host : int, optional
            See parent class :class:`~lab_utils.socket_comm.Server`.

        port : int, optional
            See parent class :class:`~lab_utils.socket_comm.Server`.

        autostart : bool, optional
            Connect to the device and start monitoring.

        device_config_file : str, optional
            Configuration file for the TPG-256A :attr:`device`.

        database_config_file : str, optional
            Configuration file for the database. If given and
            :paramref:`~Daemon.__init__.autostart` is 'True',
            a :class:`Monitor` thread will be launched with
            database option active.

        Raises
        ------
        :class:`configparser.Error`
            Configuration file error

        :class:`LockError`
            The PID file could not be locked (see parent
            class :class:`~lab_utils.socket_comm.Server`).

        :class:`OSError`
            Socket errors (see parent class
            :class:`~lab_utils.socket_comm.Server`).

        :class:`~serial.SerialException`
            The connection to the :attr:`device` has failed

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            :attr:`device` was in the wrong state, e.g. already ON.

        """
        # Call the parent class initializer
        super().__init__(
            config_file=config_file,
            pid_file_name=pid_file_name,
            host=host,
            port=port,
        )

        # Add custom arguments to the message parser
        self.update_parser()

        # Initialize device
        self.device = TPG_256A(config_file=device_config_file)

        # Autostart?
        if not autostart:
            return
        else:
            self.logger.info('Launching auto-start sequence')

        # 1. Connect to the device and check access
        self.device.connect()
        firmware = self.device.program_number()
        self.logger.debug('Device firmware: {}'.format(firmware))

        # 2. Start background monitor thread
        self.monitor = Monitor(
            device=self.device,
            name='Daemon Thread',
            terminal_flag=False,    # the autostart option is meant to be used with supervisord, no terminal output
            database_flag=database_config_file is not None,
            database_config_file=database_config_file,
        )
        self.logger.info('Monitor thread launched!')

    def update_parser(self):
        """ Sets up the message
        :attr:`~lab_utils.socket_comm.Server.parser`. """

        self.logger.debug('Setting up custom message parser')

        # Set some properties of the base class argument parser
        self.parser.prog = mod_name
        self.parser.description = prog_desc
        self.parser.epilog = 'Check out the package documentation for more information:\n{}'.format(docs_url)

        # Subparsers for each acceptable command
        # 1. STATUS
        sp_status = self.sp.add_parser(
            name='status',
            description='checks the status of the daemon',
        )
        sp_status.set_defaults(
            func=self.status,
            which='status')

        # 2. TPG-256A
        sp_tpg_256a = self.sp.add_parser(
            name='tpg_256a',
            description='interface to the Pfeiffer TPG 256A device',
        )
        sp_tpg_256a.set_defaults(
            func=self.tpg_256a,
            which='tpg_256a'
        )
        sp_g1 = sp_tpg_256a.add_mutually_exclusive_group()
        sp_g1.add_argument(
            '--on',
            action='store_true',
            help='connects to the device',
            default=False,
            dest='turn_on',
        )
        sp_g1.add_argument(
            '--off',
            action='store_true',
            help='closes the connection',
            default=False,
            dest='turn_off',
        )
        sp_g1.add_argument(
            '--restart, -r',
            action='store_true',
            help='restarts the connection',
            default=False,
            dest='restart',
        )
        sp_tpg_256a.add_argument(
            '--test, -t',
            action='store_true',
            help='performs a connection check',
            default=False,
            dest='test',
        )
        sp_tpg_256a.add_argument(
            '--config,-c',
            default=argparse.SUPPRESS,      # If --config is not given,  it will not show up in the namespace
            nargs='?',                      # If --config is given, it may be used with or without an extra argument
            const=None,                     # If --config is given without an extra argument, 'dest' = None
            help='reloads the configuration file (and resets the file if given, absolute path only)',
            dest='config_file',
        )
        sp_tpg_256a.add_argument(
            '--gauge-info,-g',
            action='store_true',
            help='prints gauge status and information',
            default=False,
            dest='gauge_info',
        )
        sp_tpg_256a.add_argument(
            '--single-readout,-r',
            action='store_true',
            help='performs a single readout to the device',
            default=False,
            dest='single_readout',
        )

        # 3. Monitor
        sp_monitor = self.sp.add_parser(
            name='logging',
            description='manages the logging thread',
        )
        sp_monitor.set_defaults(
            func=self.logging,
            which='logging'
        )
        sp_g2 = sp_monitor.add_mutually_exclusive_group()
        sp_g2.add_argument(
            '--start',
            action='store_true',
            help='starts the monitor thread',
            default=False,
            dest='start',
        )
        sp_g2.add_argument(
            '--stop',
            action='store_true',
            help='stops the monitor thread',
            default=False,
            dest='stop',
        )
        sp_monitor.add_argument(
            '--terminal',
            action='store_true',
            help='prints the monitor output to the application logging sink',
            default=False,
            dest='terminal',
        )
        sp_monitor.add_argument(
            '--use-database',
            default=argparse.SUPPRESS,  # If --use-database is not given it will not show up in the namespace
            nargs='?',                  # If --use-database is given it may be used with or without an extra argument
            const=None,                 # If --use-database is given without an extra argument, 'dest' = None
            help='logs data to a PostgreSQL database using the given config file, or the default one',
            dest='database_config_file',
        )

    def quit(self):
        """ Stops the daemon, called with message 'quit'.
        The method overrides the original
        :meth:`~lab_utils.socket_comm.Server.quit` to do
        proper clean-up of the monitoring
        :attr:`thread<monitor>` and the :attr:`device`
        handler.
        """

        self.logger.info('Launching quitting sequence')

        # Monitor
        if self.monitor is not None and self.monitor.is_alive():
            if self.monitor.stop():
                self.reply += 'Monitor thread stopped\n'
            else:
                self.reply += 'Thread error! Monitor thread did not respond to the quit signal and is still running\n'

        # Serial connection
        if self.device.connected:
            try:
                self.device.disconnect()
            except (SerialException, StateError, IOError) as e:
                self.reply += 'Clean-up error! {}: {}'.format(type(e).__name__, e)
                self.logger.debug('Serial connection could not be closed')
            else:
                self.reply += 'Clean-up: device is now off\n'
                self.logger.info('Serial connection closed')

        self.logger.info('Stopping daemon TCP server now')
        self.reply += 'Stopping daemon TCP server now'

    def status(self):
        """ TODO
        """
        self.reply += 'Status: doing great!'

    def tpg_256a(self):
        """ Modifies or checks the status of the TPG 256A
        :attr:`device`. Provides functionality to:

        -  Connect and disconnect the controller.
        -  Retrieve hardware information.
        -  Reload device configuration.
        -  Perform a single read-out of the gauges
        """
        self.logger.debug('Method \'tpg_256a\' called by the message parser')

        # Turn ON
        if self.namespace.turn_on:
            # Check current status
            if self.device.connected:
                self.logger.info('Device already connected')
                self.reply += 'Device was already connected\n'
            else:
                try:
                    self.device.connect()
                except (SerialException, StateError, IOError) as e:
                    self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    self.reply += 'Connection successful\n'

        # Turn OFF
        if self.namespace.turn_off:
            # TODO: stop logging as well
            # Check current status
            if not self.device.connected:
                self.logger.info('Device already off')
                self.reply += 'Device was already off!\n'
            else:
                try:
                    self.device.disconnect()
                except (SerialException, StateError, IOError) as e:
                    self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    self.reply += 'Device is now off\n'

        # Restart device (if ON, turn OFF then ON; if OFF, turn ON)
        if self.namespace.restart:
            # Turn OFF if connected
            # TODO: stop logging as well
            if self.device.connected:
                try:
                    self.device.disconnect()
                except (SerialException, StateError, IOError) as e:
                    self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    self.reply += 'Device was shut down\n'

            # Turn ON
            try:
                self.device.connect()
            except SerialException as e:
                self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                return
            else:
                self.reply += 'Device was restarted\n'

        # Test serial connection and device access
        if self.namespace.test:
            # Check current status
            # TODO: check device is not running
            if not self.device.connected:
                self.reply += 'Device is not connected, cannot perform test'
            else:
                try:
                    # Read some device information
                    firmware = self.device.program_number()
                except (SerialException, StateError, IOError) as e:
                    self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    self.reply += 'Connection test successful, device firmware: {}'.format(firmware)
                    self.logger.debug('Device firmware: {}'.format(firmware))

        # Reset and load configuration file
        if "config_file" in self.namespace:
            self.logger.info('Reloading device configuration')
            device_was_on = self.device.connected

            try:
                # Stop the device if it is running
                # TODO: stop logging as well
                if self.device.connected:
                    self.reply += 'Turning off the device\n'
                    self.device.disconnect()

                # Apply configuration
                self.device.config(self.namespace.config_file)
                self.reply += 'Configuration file {} loaded\n'.format(self.device.config_file)

                # Turn on again?
                if device_was_on:
                    self.device.connect()
                    self.reply += 'Device was reconnected\n'

            except (SerialException, StateError, configparser.Error, IOError) as e:
                self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                return

        # Single readout
        if self.namespace.single_readout:
            # Check current status
            # TODO: check device is not running
            if not self.device.connected:
                self.reply += 'Device is not connected, cannot perform pressure readout'
            else:
                try:
                    self.device.pressure_gauges()
                except (SerialException, StateError, IOError) as e:
                    self.reply += 'Error! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    pass

        # Gauge status and information
        if self.namespace.gauge_info:
            # Check device is ON
            if not self.device.connected:
                self.reply += 'Gauge information: Device is not connected, information might be outdated'
            else:
                # Build nice table
                header = '{:15}{:25}{}\n'.format('Gauge', 'Status', 'Latest Value')
                self.reply += ''.join('-' for _ in range(len(header)))
                self.reply += '\n'
                self.reply += header
                self.reply += ''.join('-' for _ in range(len(header)))
                self.reply += '\n'
                for ch in self.device.channel_info:
                    if ch.label is None:
                        continue
                    status = 'Active, logging'
                    if not ch.active:
                        status = 'Inactive'
                    if ch.active and not ch.logging:
                        status = 'Active, not logging'
                    data = ch.data
                    if data is None:
                        data = 'None'
                    self.reply += '{:15}{:25}{:15}\n'.format(ch.label, status, str(data))
                self.reply += ''.join('-' for _ in range(len(header)))
                self.reply += '\n'
        self.reply += 'TPG-256A routine completed\n'

    def logging(self):
        """ Manages the :attr:`logging thread<monitor>`.
        Provides functionality to:

        -  Start and stop the thread.
        -  Enable or disable database usage.
        -  Enable or disable terminal output.

        """
        self.logger.debug('Method \'logging\' called by the message parser')

        # Start
        if self.namespace.start:
            # Check current status
            if not self.device.connected:
                self.logger.warning('Device is not connected')
                self.reply += 'Device is not connected\n'
            elif self.monitor is not None and self.monitor.is_alive():
                self.logger.warning('Monitor thread is already running')
                self.reply += 'Monitor thread is already running\n'
            else:
                self.logger.info('Launching logging thread')

                # Use database?
                db_config_file = None
                if "database_config_file" in self.namespace:
                    use_db = True
                    db_config_file = self.namespace.database_config_file
                else:
                    use_db = False

                try:
                    self.monitor = Monitor(
                        device=self.device,
                        name='Daemon Thread',
                        terminal_flag=self.namespace.terminal,
                        database_flag=use_db,
                        database_config_file=db_config_file,
                    )
                except (StateError, RuntimeError, DatabaseError, ConfigError) as e:
                    self.reply += 'Error launching Daemon Thread! {}: {}'.format(type(e).__name__, e)
                    return
                else:
                    self.reply += 'Daemon Thread launched\nYou can check its status with the \'status\' option\n'

        # Stop
        if self.namespace.stop:
            # Check current status
            if self.monitor is None or not self.monitor.is_alive():
                self.logger.info('Monitor thread is not running')
                self.reply += 'Monitor thread is not running\n'
            else:
                if self.monitor.stop():
                    self.reply += 'Daemon thread stopped\n'
                else:
                    self.reply += 'Daemon thread error, still running...\n'
