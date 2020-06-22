""" Driver for the Pfeiffer TPG 256A. The device is
a six-channel pressure readout and monitor controller.

The :class:`TPG_256A` main class manages the interface
to the device and implements some of the available
operations through RS-232 communication. The driver
implements an auxiliary :class:`Channel` class to hold
information about the available gauges. A custom
exception :class:`StateError` is used for internal
error management.

The driver has been adapted to Python3 from the
:obj:`PyExpLabSys<PyExpLabSys.drivers.pfeiffer>`
library. More information is also available in the
:download:`device documentation <../Pfeiffer_MultiGauge256A_OpInstructions.pdf>`
"""

# Imports
import time
from serial import Serial
from typing import List, Tuple
import configparser

# Third party
from lab_utils.custom_logging import getLogger


# Code translations constants
MEASUREMENT_STATUS = {
    0: 'Measurement data okay',
    1: 'Underrange',
    2: 'Overrange',
    3: 'Sensor error',
    4: 'Sensor off (IKR, PKR, IMR, PBR)',
    5: 'No sensor (output: 5,2.0000E-2 [mbar])',
    6: 'Identification error'
}
GAUGE_IDS = {
    'TPR':          'Pirani Gauge or Pirani Capacitive gauge',
    'IKR9':         'Cold Cathode Gauge 10E-9 ',
    'IKR11':        'Cold Cathode Gauge 10E-11 ',
    'PKR':          'FullRange CC Gauge',
    'PBR':          'FullRange BA Gauge',
    'IMR':          'Pirani / High Pressure Gauge',
    'CMR':          'Linear gauge',
    'noSEn':        'No Sensor',
    'no Sensor':    'No Sensor',
    'noid':         'No identifier'
}


class StateError(BaseException):
    """ Mock-up exception to deal with unexpected device status.
    It is used to signal for instance that the device should be
    connected but it is not at a certain execution point.
    """
    pass


class Channel:
    """ Simple container to hold channel information. The setup
    is read from the :attr:`configuration file<TPG_256A.config_file>`
    (e.g. :attr:`label`) or is retrieved from the controller
    directly (e.g. :attr:`gauge_id`).

    The following gauge types are supported:

    =========   ==========================================
    ID          Description
    =========   ==========================================
    TPR         Pirani Gauge or Pirani Capacitive gauge
    IKR9        Cold Cathode Gauge 10E-9
    IKR11       Cold Cathode Gauge 10E-11
    PKR         FullRange CC Gauge
    PBR         FullRange BA Gauge
    IMR         Pirani / High Pressure Gauge
    CMR         Linear gauge
    noSEn       No Sensor
    no Sensor   No Sensor
    noid        No identifier
    =========   ==========================================

    The measurement status can take the following values:

    =========   ==========================================
    Code        Status
    =========   ==========================================
    0           Measurement data okay
    1           Underrange
    2           Overrange
    3           Sensor error
    4           Sensor off (IKR, PKR, IMR, PBR)
    5           No sensor (output: 5,2.0000E-2 [mbar])
    6           Identification error
    =========   ==========================================

    """

    gauge_number: int = None    #: The channel ID number.
    connected: bool = False     #: The gauge was detected by the controller.
    active: bool = False        #: The gauge should be ON.
    logging: bool = False       #: Data from the gauge should be recorded.
    label: str = ''             #: Label of the gauge, to be used when logging to a database.
    gauge_id: str = None        #: Gauge type, retrieved from the controller.
    data: float = None          #: Latest pressure readout value.
    status_code: int = None     #: Measurement status code.
    status_str: str = None      #: Measurement status description.

    def __init__(self, gauge_number: int = None):
        self.gauge_number = gauge_number


class TPG_256A(object): # noqa (ignore CamelCase convention)
    """ Driver implementation for the Pfeiffer TPG-256A. The device
    is a six-channel pressure readout and monitor controller. The
    driver has been adapted to Python3 from the
    :obj:`PyExpLabSys<PyExpLabSys.drivers.pfeiffer>` library, and
    implements the following commands (see the
    :download:`device documentation <../../Pfeiffer_MultiGauge256A_OpInstructions.pdf>`
    for more information):

    +-------------------+-----------------------------------------------------------+
    | Mnemonic          | Description                                               |
    +===================+===========================================+===============+
    | PNR               | Program number (firmware version)                         |
    +-------------------+-----------------------------------------------------------+
    | PR[1 ... 6]       | Pressure measurement (measurement data) gauge [1 ... 6]   |
    +-------------------+-----------------------------------------------------------+
    | TID               | Transmitter identification (gauge identification)         |
    +-------------------+-----------------------------------------------------------+
    | SEN,0,0,0,0,0,0   | Gauge status                                              |
    +-------------------+-----------------------------------------------------------+
    """

    # Attributes
    ETX = chr(3)    #: End text (Ctrl-c), chr(3), \\x03
    CR = chr(13)    #: Carriage return, chr(13), \\r
    LF = chr(10)    #: Line feed, chr(10), \\n
    ENQ = chr(5)    #: Enquiry, chr(5), \\x05
    ACK = chr(6)    #: Acknowledge, chr(6), \\x06
    NAK = chr(21)   #: Negative acknowledge, chr(21), \\x15

    # Serial port configuration
    serial: Serial = None                           #: Serial port handler.
    baud_rate: int = 9600                           #: Baud rate for serial communication.
    serial_port: str = '/dev/PfeifferTPG256A'       #: Physical address of the device file.
    timeout: float = 1.0                            #: Time-out for serial connection error.

    # Device setup
    config_file: str = 'conf/tpg_256a.ini'  #: Device configuration file
    channel_info: List[Channel] = []        #: Channel information, loaded from the configuration file.

    # Others
    connected: bool = False         #: Status flag.

    def __init__(self,
                 serial_port: str = None,
                 baud_rate: int = None,
                 connect: bool = False,
                 timeout: float = None,
                 config_file: str = None,
                 ):
        """ Initializes the :class:`TPG_256A` object. It calls
        the :meth:`config` method to set up the device if a
        :paramref:`~TPG_256A.__init__.config_file` is given. If
        the :paramref:`~TPG_256A.__init__.connect` flag is set
        to `True`, attempts the connection to the device.

        Parameters
        ----------
        serial_port : str, optional
            Physical address of the device file, default is 'None'

        timeout : float, optional
            Serial communication time out, default is 'None'

        baud_rate: int, optional
            Baud rate for serial communication, default is 'None'

        connect: bool, optional
            If set, attempt connection to the device, default is `False`

        config_file : str, optional
            Configuration file, default is 'None'.

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error

        :class:`~serial.SerialException`
            The connection to the device has failed

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            Device was in the wrong state.
        """

        # Initialize variables
        self.connected = False
        for ch in range(6):
            self.channel_info.append(Channel(gauge_number=ch+1))

        # Load config file, if given
        if config_file is not None:
            self.config(config_file)

        # Assign attributes, if given
        # They override they configuration file
        if baud_rate is not None:
            self.baud_rate = baud_rate
        if serial_port is not None:
            self.serial_port = serial_port
        if timeout is not None:
            self.timeout = timeout

        # Connect to the device
        if connect:
            self.connect()

    def config(self, new_config_file: str = None):
        """ Loads the TPG-256A configuration from a file. If
        :paramref:`~TPG_256A.config.new_config_file` is not
        given, the latest :attr:`config_file` is re-loaded;
        if it is given and the file is successfully parsed,
        :attr:`config_file` is updated to the new value.

        Parameters
        ----------
        new_config_file : str, optional
            New configuration file to be loaded.

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error
        """

        # Update configuration file, if given
        if new_config_file is None:
            new_config_file = self.config_file

        # Initialize config parser and read file
        getLogger().info("Loading configuration file %s", new_config_file)
        config_parser = configparser.ConfigParser()
        config_parser.read(new_config_file)

        # Load serial port configuration
        self.serial_port = config_parser.get(section='Connection', option='device')
        self.baud_rate = config_parser.getint(section='Connection', option='baud_rate')
        self.timeout = config_parser.getfloat(section='Connection', option='timeout')

        # Load channel information
        for ch in range(6):
            sec_name = 'Sensor_{}'.format(ch+1)
            act = False
            log = False
            lab = None
            if config_parser.has_section(sec_name):
                act = config_parser.getboolean(sec_name, 'active')
                log = config_parser.getboolean(sec_name, 'logging')
                lab = config_parser.get(sec_name, 'label')
                if log and not act:
                    getLogger().warning('Sensor %d (%s) set to logging, but not active. Monitor disabled.', ch+1, lab)
                    log = False
                getLogger().debug('Found sensor %d: %s, %s, %s', ch+1, str(act), str(log), lab)
            else:
                getLogger().debug('%s not found', sec_name)
            self.channel_info[ch].active = act
            self.channel_info[ch].logging = log
            self.channel_info[ch].label = lab

        # If everything worked, update local config_file for future calls
        self.config_file = new_config_file

    def connect(self):
        """ Connects to the TPG-256A Controller. The methods
        :meth:`gauge_identification` and :meth:`gauge_status`
        are called to retrieve hardware information from the
        device.

        Raises
        ------
        :class:`~serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            Device was in the wrong state.
        """
        if self.connected:
            raise StateError('device was already ON')
        
        getLogger().info('Connecting to TPG-256A Controller on port %s', self.serial_port)

        self.serial = Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                timeout=self.timeout,
            )

        self.connected = True
        self.gauge_identification()
        self.gauge_status()
        getLogger().info('Connection successful')

    def disconnect(self):
        """ Closes the connection to the TPG-256A Controller.

        Raises
        ------
        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            Device was in the wrong state.
        """
        # Check the device is connected
        if not self.connected:
            getLogger().warning('Device is not ON')
            raise StateError('Device is not ON')

        getLogger().info('Closing connection to TPG-256A Controller on port %s', self.serial_port)
        self.connected = False
        self.serial.close()
        getLogger().info('Connection closed')

    def gauge_status(self):
        """ Reads the gauges status. Checks that gauges
        marked as :attr:`~Channel.active` in
        :attr:`channel_info` are available; sets them
        to inactive otherwise.

        Raises
        ------
        :class:`StateError`
            Device was in the wrong state.

        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.
        """

        # Check device is ON
        if not self.connected:
            getLogger().warning('Device is not ON')
            raise StateError('Device is not ON')

        # Check gauge status
        msg = ','.join('0' for _ in range(6))
        getLogger().debug('Checking gauge status')
        self._send_command('SEN,{}'.format(msg))
        reply = self._get_data()
        getLogger().debug('Reply from the device: %s', reply)
        status = reply.split(',')
        for (ch, st) in zip(self.channel_info, status):
            if ch.active and st != '2':
                getLogger().warning('Channel %s set to active but it is OFF, deactivating', ch.label)
                ch.active = False
                ch.logging = False

    def program_number(self) -> str:
        """ Returns the firmware version.

        Returns
        -------
        str:
            The firmware version.

        Raises
        ------
        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.
        """
        self._send_command('PNR')
        return self._get_data()

    def pressure_gauge(self, gauge_nr) -> Tuple[float, int]:
        """Reads the pressure measured by gauge number
        :paramref:`~TPG_256A.pressure_gauge.gauge`.

        Arguments
        ---------
        gauge_nr: int
            The gauge number, 1 to 6

        Returns
        -------
        [float, int]
            (value, status code)

        Raises
        ------
        :class:`StateError`
            Device was in the wrong state.

        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`ValueError`
            Invalid :paramref:`gauge_nr`, must be between 1 and 6.
        """

        # Check device is ON
        if not self.connected:
            getLogger().warning('Device is not ON')
            raise StateError('Device is not ON')

        # Check gauge number
        if gauge_nr-1 not in range(6):
            message = 'The input gauge number must be between 1 and 6'
            raise ValueError(message)

        # Perform request
        self._send_command('PR' + str(gauge_nr))
        reply = self._get_data()

        # Save data
        status_code = int(reply.split(',')[0])
        data = float(reply.split(',')[1])

        return data, status_code

    def pressure_gauges(self):
        """Reads the pressure measured by all active gauges.
        Saves the data into the :attr:`channel_info` list.

        Raises
        ------
        :class:`StateError`
            Device was in the wrong state.

        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.
        """
        # Check device is ON
        if not self.connected:
            getLogger().warning('Device is not ON')
            raise StateError('Device is not ON')

        getLogger().debug('Pressure readout:')
        for ch in self.channel_info:
            if ch.active:
                # Single readout
                value, code = self.pressure_gauge(ch.gauge_number)
                ch.data = value
                ch.status_code = code
                ch.status_str = MEASUREMENT_STATUS[code]
                getLogger().debug('{:4}{:10}{:8}   {}'.format(
                    ' ',
                    ch.label,
                    ch.data,
                    ch.status_str
                ))

    def gauge_identification(self):
        """Reads the gauges identification. Saves the
        information in :attr:`channel_info`. Checks that
        gauges marked as :attr:`~Channel.active` in
        :attr:`channel_info` are available; sets them
        to inactive otherwise and disables logging.

        Raises
        ------
        :class:`StateError`
            Device was in the wrong state.

        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.
        """

        # Check device is ON
        if not self.connected:
            getLogger().warning('Device is not ON')
            raise StateError('Device is not ON')

        getLogger().info('Retrieving Gauge Identification')
        self._send_command('TID')
        reply = self._get_data()
        getLogger().debug('Gauge Identification String: %s', reply)
        id_list = reply.split(',')
        for (ch, id_code) in zip(self.channel_info, id_list):
            ch.gauge_id = GAUGE_IDS[id_code]
            ch.connected = ch.gauge_id != 'No Sensor'
            if ch.active and not ch.connected:
                getLogger().warning('Sensor %s is set to active, but no sensor was found', ch.label)
                ch.active = False
                ch.logging = False

    def _cr_lf(self, string: str) -> str:
        """ Pads :attr:`carriage return<TPG_256A.CR>`
        and :attr:`line feed<TPG_256A.LF>` to a
        given :paramref:`string`.

        Parameters
        ----------
        string : str
            String to pad

        Returns
        -------
        str:
            The padded string.
        """
        return string + self.CR + self.LF

    def _send_command(self, command: str):
        """Sends a command and checks if it
        is positively acknowledged.

        Parameters
        ----------
        command : str, optional
            The command to send.

        Raises
        ------
        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.
        """
        self.serial.write(str.encode(self._cr_lf(command)))
        response = self.serial.readline().decode()
        if response == self._cr_lf(self.NAK):
            message = 'Serial communication returned negative acknowledge'
            getLogger().error(message)
            raise IOError(message)
        elif response != self._cr_lf(self.ACK):
            message = 'Serial communication returned unknown response:\n{}'\
                ''.format(repr(response))
            getLogger().error(message)
            raise IOError(message)

    def _get_data(self) -> str:
        """Gets the data that is ready on the device.

        Returns
        -------
        str:
            The raw data

        Raises
        ------
        :class:`serial.SerialException`
            The connection to the device has failed.
        """
        self.serial.write(str.encode(self.ENQ))
        data = self.serial.readline().decode()
        return data.rstrip(self.LF).rstrip(self.CR)

    def _clear_output_buffer(self) -> str:
        """ Clears the output buffer.

        Returns
        -------
        str:
            The data that was in the buffer.

        Raises
        ------
        :class:`serial.SerialException`
            The connection to the device has failed.
        """
        time.sleep(0.1)
        just_read = 'start value'
        out = ''
        while just_read != '':
            just_read = self.serial.read()
            out += just_read
        return out
