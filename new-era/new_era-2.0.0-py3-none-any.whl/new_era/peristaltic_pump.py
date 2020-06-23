import re
import time
import warnings

import serial

from new_era.utils import NewEraPumpHardwareError, NewEraPumpCommError, NewEraPumpError, NewEraPumpUnitError, convert

"""
A way to control a new era peristaltic pump 
So far tested with: NE-9000
Manual for the NE-9000: http://www.syringepump.com/download/NE-9000%20Peristaltic%20Pump%20User%20Manual.pdf

This module is based off the New Era Interface by Brad Buran:
https://bitbucket.org/bburan/new-era/src/default/
"""


class PeristalticPump(object):
    """
    Establish a connection with the New Era pump - specifically

    """

    #####################################################################
    # Basic information required for creating and parsing RS-232 commands
    #####################################################################

    # Hex command characters used to indicate state of data
    # transmission between pump and computer.
    ETX = '\x03'    # End of packet transmission
    STX = '\x02'    # Start of packet transmission
    CR  = '\x0D'    # Carriage return

    STANDARD_ENCODING = 'UTF-8'

    # These are actually the default parameters when calling the command
    # to init the serial port, but are also defined for clarity
    CONNECTION_SETTINGS = dict(
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        # timeout=1,
        # xonxoff=0,
        # rtscts=0,
        # writeTimeout=1,
        # dsrdtr=None,
        # interCharTimeout=None
    )

    STATUS = dict(
        I='dispensing',
        W='withdrawing',
        S='pumping program stopped',
        P='pumping program paused',
        T='timed pause phase',
        U='operational trigger wait',
        X='purging'
    )

    # Map of trigger modes.  Dictionary key is the value that must be provided
    # with the TRG command sent to the pump.  Value is a two-tuple indicating
    # the start and stop trigger for the pump (based on the TTL input).  The
    # trigger may be a rising/falling edge or None.  If you
    # set the trigger to 'falling', None', then a falling TTL will start the
    # pump's program with no stop condition.  A value of 'rising', 'falling'
    # will start the pump when the input goes high and stop it when the input
    # goes low.
    TRIG_MODE = {
        'FT':   ('falling', 'falling'),
        'FH':   ('falling', 'rising'),
        'F2':   ('rising',  'rising'),
        'LE':   ('rising',  'falling'),
        'ST':   ('falling', None),
        'T2':   ('rising',  None),
        'SP':   (None,      'falling'),
        'P2':   (None,      'rising'),
    }

    REV_TRIG_MODE = dict((v, k) for k, v in TRIG_MODE.items())

    DIR_MODE = {
        'INF':  'dispense',
        'WDR':  'withdraw',
        'REV':  'reverse',
    }

    REV_DIR_MODE = dict((v, k) for k, v in DIR_MODE.items())

    RATE_UNIT = {
        'OM':   'Oz/min',
        'MM':   'ml/min',
        'OS':   'Oz/sec',
        'MS':   'ml/sec',
    }

    # reversed dictionary of the rate unit dictionary, so that the keys become the values and vice versa
    REV_RATE_UNIT = dict((v, k) for k, v in RATE_UNIT.items())

    VOL_UNIT = {
        'OZ':   'Oz',
        'ML':   'ml',
    }

    # reversed dictionary of the vol unit dictionary, so that the keys become the values and vice versa
    REV_VOL_UNIT = dict((v, k) for k, v in VOL_UNIT.items())

    # The response from the pump always includes a status flag which indicates
    # the pump state (or error).  Response is in the format
    # <STX><response data><ETX> where <response data> is in the format <address><status>[<data>]
    # link to resource on understanding regex,compile() is https://docs.python.org/2/library/re.html#re.compile
    # the way that the regex is used
    # the (?P<name>...) means that the substring matched by the group is accessible via the symbolic group name
    # <name>; this means that later it is much easier and readable to access different parts of a match to a regex
    # expression by searching for the group defined by <name>
    # for regex, \d means any decimal digit; this is equivalent to the set [0-9], + means one or more
    # for regex, . means any character except new line, * means zero or more
    _basic_response = re.compile(STX +
                                 '(?P<address>\d+)' +
                                 '(?P<status>[IWSPTUX]|A\?)' +
                                 '(?P<data>.*)' +
                                 ETX)

    # Response for queries about volume dispensed.  Returns separate numbers for
    # dispense and withdraw.  Format is I<float>W<float><volume units>
    _dispensed = re.compile('I(?P<dispense>[\.0-9]+)' +
                            'W(?P<withdraw>[\.0-9]+)' +
                            '(?P<units>OZ|ML)')

    #####################################################################
    # Special functions for controlling pump
    #####################################################################

    def __init__(self,
                 port: str,
                 address: int = 0,
                 start_trigger='rising',
                 stop_trigger='falling',
                 volume_unit='ml',
                 rate_unit='ml/min',
                 ):
        """
        the pump by default sets the tubing inside diameter to 3/16 inches.

        :param str, port: port to connect to, for example, 'COM8'
        :param int, address: address of the pump/ Use 0 if only using 1 pump, but increase if connecting pumps to
            each other
        :param str, start_trigger: one of 'rising', 'falling', or None
        :param str, stop_trigger: one of 'rising', 'falling', or None
        :param str, volume_unit: one of VOL_UNIT values
        :param str, rate_unit: one of RATE_UNIT values
        """
        self.ser = None
        self._port = port
        self.connect()
        self._address = address

        # initialize rate and volume units on instantiation - these are the values in the RATE_UNIT and VOL_UNIT
        # dictionaries, as they are more readable
        self.rate_unit = rate_unit
        self.volume_unit = volume_unit
        # use the reversed versions or RATE and VOL_UNIT in order to get the command that the pump understands
        self.rate_unit_cmd = self.REV_RATE_UNIT[rate_unit]
        self.volume_unit_cmd = self.REV_VOL_UNIT[volume_unit]

        self._xmit(f'VOL {self.volume_unit_cmd}')  # set volume unit for pump
        self.set_trigger(start=start_trigger, stop=stop_trigger)
        pump_firmware_version = self._xmit('VER')
        print(f'Connected to pump {pump_firmware_version}')

        # attributes that have nothing to do with actual control of the new era pump but are used in for convenience
        # in other applications
        self.dead_volume_time_in_seconds = None

    @property
    def address(self) -> int:
        # todo check this works
        value = self._xmit('*ADR')
        # check if the address has 1 or 2 digits
        try:
            value = int(value[-2:])
        except Exception as e:
            value = int(value[-1:])
        return value

    @address.setter
    def address(self, value: int):
        """
        This is a special system command that will be accepted by the pump regardless of its current address.  Once
        set, the pump will only respond to commands with the set address and at the specified baud rate
        :param value:
        :return:
        """
        if value < 0 or value > 99:
            print('Can only set address between 0 and 99')
            return
        self._xmit(f'*ADR {str(value)}')

    def connect(self):
        try:
            if self.ser is None:
                cn = serial.Serial(port=self._port, **self.CONNECTION_SETTINGS)
                self.ser = cn
            if not self.ser.isOpen():
                self.ser.open()

            # Turn audible alarm on.  This will notify the user of any problems
            # with the pump.
            on = 1
            off = 0
            self._xmit(f'AL {on}')
            # Ensure that serial port is closed on system exit
            import atexit
            atexit.register(self.disconnect)
        except NewEraPumpHardwareError as e:
            # We want to trap and dispose of one very specific exception code,
            # 'R', which corresponds to a power interrupt.  This is almost
            # always returned when the pump is first powered on and initialized
            # so it really is not a concern to us.  The other error messages are
            # of concern so we reraise them.
            if e.code != 'R':
                raise
        except NameError as e:
            # Raised when it cannot find the global name 'SERIAL' (which
            # typically indicates a problem connecting to COM1).  Let's
            # translate this to a human-understandable error.
            print(e)
            raise NewEraPumpCommError('SER')

    def disconnect(self):
        """
        Stop pump and close serial port.  Automatically called when Python
        exits.
        """
        try:
            self.stop()
        finally:
            self.ser.close()
            return  # Don't reraise error conditions, just quit silently

    def set_address_and_baudrate(self, address: int, baudrate: int):
        """
        This is a special system command that will be accepted by the pump regardless of its current address.  Once
        set, the pump will only respond to commands with the set address and at the specified baud rate

        :param address:
        :param baudrate:
        :return:
        """
        if address < 0 or address > 99:
            print('Can only set address between 0 and 99')
            return
        acceptable_baudrates = [9200 | 9600 | 2400 | 1200 | 300]
        if baudrate not in acceptable_baudrates:
            print('Cannot set that baudrate')
            return
        self._xmit(f'*ADR {str(address)} B {str(baudrate)}')

    def set_baudrate(self, baudrate: int):
        """
        This is a special system command that will be accepted by the pump regardless of its current address.  Once
        set, the pump will only respond to commands with the set address and at the specified baud rate

        :param baudrate:
        :return:
        """
        acceptable_baudrates = [9200 | 9600 | 2400 | 1200 | 300]
        if baudrate not in acceptable_baudrates:
            print('Cannot set that baudrate')
            return
        address = self.address
        self._xmit(f'*ADR {str(address)} B {str(baudrate)}')

    def reset(self):
        """
        Clears program memory and resets communication parameters to Basic mode and address 0.
        This is a special system command that will be accepted by the pump regardless of its current address.
        :return:
        """
        self._xmit('*RESET')

    def run(self):
        """
        Start pump program
        """
        self.start()

    def run_if_TTL(self, value=True):
        """
        In contrast to `run`, the logical state of the TTL input is inspected
        (high=True, low=False).  If the TTL state is equal to value, the pump
        program is started.

        If value is True, start only if the TTL is high.  If value is False,
        start only if the TTL is low.
        """
        if self.get_TTL() == value:
            self.run()

    def reset_volume(self):
        """
        Reset the cumulative dispensed and withdrawn volume
        """
        self.reset_dispensed_volume()
        self.reset_withdrawn_volume()

    def reset_dispensed_volume(self):
        """
        Reset the cumulative dispensed volume
        """
        self._xmit('CLD INF')

    def reset_withdrawn_volume(self):
        """
        Reset the cumulative withdrawn volume
        """
        self._xmit('CLD WDR')

    def pause(self):
        self._trigger = self.get_trigger()
        self.set_trigger(None, 'falling')
        try:
            self.stop()
        except NewEraPumpError:
            pass

    def resume(self):
        self.set_trigger(*self._trigger)
        if self._trigger[0] in ('high', 'rising'):
            self.run_if_TTL(True)
        elif self._trigger[0] in ('low', 'falling'):
            self.run_if_TTL(False)

    def stop(self):
        """
        Stop the pump.  Raises NewEraPumpError if the pump is already stopped.
        """
        self._xmit('STP')

    def start(self):
        """
        Starts the pump.
        """
        self._xmit('RUN')

    def set_trigger(self, start, stop):
        """
        Set the start and stop trigger modes.  Valid modes are rising and falling.  Note that not all
        combinations of
        modes are supported (see TRIG_MODE for supported pairs).

        start=None, stop='falling': pump program stops on a falling edge (start
        manually or use the `run` method to start the pump)

        start='rising', stop='falling': pump program starts on a rising edge and
        stops on a falling edge
        """
        cmd = self.REV_TRIG_MODE[start, stop]
        self._xmit(f'TRG {cmd}')

    def get_trigger(self):
        """
        Get trigger mode.  Returns tuple of two values indicating start and stop
        condition.
        """
        value = self._xmit('TRG')
        return self.TRIG_MODE[value]

    def set_direction(self, direction):
        """
        Set direction of the pump.  Valid directions are 'dispense', 'withdraw'
        and 'reverse'.

        :param str, direction: one of 'dispense', 'withdraw', or 'reverse'
        """
        arg = self.REV_DIR_MODE[direction]
        self._xmit(f'DIR {arg}')

    def get_direction(self):
        """
        Get current direction of the pump.  Response will be either 'dispense' or
        'withdraw'.

        Query response: { INF | WDR }
        """
        value = self._xmit('DIR')
        return self.DIR_MODE[value]

    def get_rate(self, unit=None):
        """
        Get current rate of the pump, converting rate to requested unit.  If no
        unit is specified, value is in the units specified when the interface
        was created.

        Query response of RAT: <float><volume units>
        """
        value = self._xmit('RAT')
        # last two characters of the <data> from from the <response data> is the units
        if value[-2:] != self.rate_unit_cmd:
            raise NewEraPumpUnitError(self.volume_unit_cmd, value[-2:], 'RAT')
        # everything except the last two characters of the <data> from from the <response data> is the rate
        value = float(value[:-2])
        if unit is not None:
            value = convert(value, self.rate_unit, unit)
        return value

    def set_rate(self, rate, unit=None):
        """
        Set current rate of the pump, converting rate from specified unit to the
        unit the interface is set at
        """
        if unit is not None:
            rate = convert(rate, unit, self.rate_unit)
            rate = '%0.3g' % rate  # todo switch all string conversions to this instead
            self._xmit(f'RAT {rate} {self.rate_unit_cmd}')
        else:
            rate = '%0.3g' % rate
            self._xmit(f'RAT {rate}')

    def set_rate_unit(self,
                      rate_unit: str):
        """
        Set the rate unit of the pump
        :param str, rate_unit: one of RATE_UNIT values
        :return:
        """
        self.rate_unit = rate_unit
        self.rate_unit_cmd = self.REV_RATE_UNIT[rate_unit]
        self._xmit(f'RAT {self.rate_unit_cmd}')

    def set_volume(self, volume, unit=None):
        """
        Set current volume of the pump, converting volume from specified unit to the
        unit the interface is set to
        """

        if unit is not None:
            volume = convert(volume, unit, self.volume_unit)
            volume = '%0.3g' % volume
            self._xmit(f'VOL {volume} {self.volume_unit_cmd}')
        else:
            volume = '%0.3g' % volume
            self._xmit(f'VOL {volume}')

    def set_volume_unit(self,
                        volume_unit: str):
        """
        Set the volume unit of the pump
        :param str, volume_unit: one of VOL_UNIT values
        :return:
        """

        self.volume_unit = volume_unit
        self.volume_unit_cmd = self.REV_VOL_UNIT[volume_unit]
        self._xmit(f'VOL {self.volume_unit_cmd}')

    def get_volume(self, unit=None):
        """
        Get current volume of the pump, converting volume to requested unit.  If no
        unit is specified, value is in the units specified when the interface
        was created.

        Query response of VOL: <float><volume units>
        """
        value = self._xmit('VOL')
        if value[-2:] != self.volume_unit_cmd:
            raise NewEraPumpUnitError(self.volume_unit_cmd, value[-2:], 'VOL')
        value = float(value[:-2])
        if unit is not None:
            value = convert(value, unit, self.volume_unit)
        return value

    def _get_dispensed(self, direction, unit=None):
        """
        Helper method for _get_dispensed and _get_withdrawn

        Query response of DIS: I<float>W<float><volume units>

        :param str, direction: Valid directions are 'dispense' or 'withdraw'
        :param unit:
        :return:
        """
        result = self._xmit('DIS')
        match = self._dispensed.match(result)
        if match.group('units') != self.volume_unit_cmd:
            raise NewEraPumpUnitError(self.volume_unit_cmd, match.group('units'), 'DIS')
        else:
            value = float(match.group(direction))
            if unit is not None:
                value = convert(value, self.volume_unit, unit)
            return value

    def get_dispensed(self, unit=None):
        """
        Get current volume withdrawn, converting volume to requested unit.  If
        no unit is specified, value is in the units specified when the interface
        was created.
        """
        return self._get_dispensed('dispense', unit)

    def get_withdrawn(self, unit=None):
        """
        Get current volume dispensed, converting volume to requested unit.  If
        no unit is specified, value is in the units specified when the interface
        was created.
        """
        return self._get_dispensed('withdraw', unit)

    def set_diameter(self, diameter_numerator, diameter_denominator, unit=None):
        """
        Set tubing inside diameter (unit must be inches). e.g. 3/16
        Any diameter setting under 1 inch can be entered
        """
        if unit is not None and unit != 'inches':
            raise NewEraPumpUnitError('inches', unit, 'DIA')
        diameter = {diameter_numerator / diameter_denominator}
        self._xmit('DIA %.2f' % diameter)

    def get_diameter(self):
        """
        Get tubing inside diameter setting in inches
        """
        self._xmit('DIA')

    def get_TTL(self):
        """
        Get status of TTL trigger
        """
        data = self._xmit('IN 2')
        if data == '1':
            return True
        elif data == '0':
            return False
        else:
            raise NewEraPumpCommError('', 'IN 2')

    def get_status(self):
        return self.STATUS[self._get_raw_response('')['status']]

    #####################################################################
    # RS232 functions
    #####################################################################

    def _readline(self):
        bytesToRead = self.ser.inWaiting()
        response = self.ser.read(bytesToRead)
        response = response.decode(self.STANDARD_ENCODING)
        return response

    def _xmit_sequence(self, *commands):
        """
        Transmit sequence of commands to pump and return a dictionary containing all the named subgroups of the
        match, with the subgroup as the key and the matched string as the value; the responses to each of the
        commands are the values in this case
        """
        return [self._xmit(cmd) for cmd in commands]

    def _get_raw_response(self, command):
        self._send(command)
        time.sleep(1)  # need a small pause for the pump to actually have a response to send back
        result = self._readline()
        # I think that this result == '' check should be ignored because when setting parameters like VOL or DIR or
        # RAT, there won't be a <dada> in the <response data> sent back unless there was an actual error,
        # and when that happens the other catches should catch that
        # if result == '':
        #     raise NewEraPumpCommError('NR', command)
        match = self._basic_response.match(result)
        if match is None:
            raise NewEraPumpCommError('NR')
        if match.group('status') == 'A?':
            raise NewEraPumpHardwareError(match.group('data'), command)
        elif match.group('data').startswith('?'):
            raise NewEraPumpCommError(match.group('data')[1:], command)
        return match.groupdict()

    def _xmit(self, command):
        """
        Transmit command to pump and return response

        All necessary characters (e.g. the end transmission flag) are added to
        the command when transmitted, so you only need to provide the command
        string itself (e.g. "RAT 3.0 MM").

        The response packet is inspected to see if the pump has an error
        condition (e.g. a stall or power reset).  If so, the appropriate
        exception is raised. But if there is no error and the command sent was to query instead of set a parameter
        for the pump, then the response packet sent back will have the result of the query.
        """
        return self._get_raw_response(command)['data']

    def _send(self, command):
        formatted_command = command + ' ' + self.CR
        encoded_formatted_command = str.encode(formatted_command)
        print(f'send command {formatted_command}')
        self.ser.write(encoded_formatted_command)

    #####################################################################
    # Convenience functions and other functions
    #####################################################################

    def pump(self,
             pump_time,
             direction: str,
             wait_time: int = 0,
             rate: int = None,
             ):
        """
        Convenience method that has the same name as the pump method used in peristaltic pump control; likely
        that this
        method might be changed in the future/not used. Right  now it is just made in case there are scenarios where
        an application can be run either using Allan's pump or one of these new era pumps

        :param pump_time: how long to pump for
        :param rate: rate to pump at
        :param direction: one of 'dispense', 'withdraw', or 'reverse'
        :param wait_time: how long to wait for after dispensing or withdrawing
        :return:
        """
        if rate is not None:
            self.set_rate(rate=rate)
        self.set_direction(direction=direction)
        self.start()
        time.sleep(pump_time)
        self.stop()
        time.sleep(wait_time)

    def find_dead_volume_time(self):
        """
        method used to find the time to pump the dead volume. this is done by setting the pump to run and then
        letting
        the pump run until the user presses the enter button as input into the console, which will make the pump
        stop.
        the time since the pump started and when the user presses the enter button will be recorded as the dead
        volume time in seconds for the pump. by default the direction of the pump will be to 'dispense', and it will
        dispense at the rate the pump is currently set to

        :return the number of seconds required to pump the dead volume for the tubing set up for the pump

        """
        warnings.warn(
            'No longer implemented',
            DeprecationWarning,
            stacklevel=2,
        )
        return NotImplementedError
        # direction = 'dispense'
        # self.set_direction(direction=direction)
        # start_time = datetime.now()
        # self.start()
        # root = tkinter.Tk()
        # pump_time_reached = messagebox.showinfo("New era peristaltic pump", "Press OK when the dead volume for
        # the "
        #                                                                 "pump has been reached")
        # root.withdraw()
        # while pump_time_reached != 'ok':
        #     time.sleep(1)
        # root.destroy()
        # self.stop()
        # end_time = datetime.now()
        #
        # time_diff = end_time - start_time
        # seconds_elapsed = time_diff.total_seconds()  # number of seconds that have elapsed
        # minutes_elapsed = time_diff.total_seconds() / 60  # number of minutes that have elapsed
        # self.dead_volume_time_in_seconds = seconds_elapsed
        # print(f'For the dead volume in direction {direction}, you need to use a rate of {self.get_rate()} for '
        #       f'{seconds_elapsed} seconds == {minutes_elapsed} minutes')
        #
        # return self.dead_volume_time_in_seconds

    def find_dead_volume(self):
        """
        Method to find the dead volume in the pump
        :return: the dead volume in the pump for the volume unit that the pump is set at, so either Oz or mL
        """
        warnings.warn(
            'No longer implemented',
            DeprecationWarning,
            stacklevel=2,
        )
        return NotImplementedError
        # if self.dead_volume_time_in_seconds is None:
        #     self.find_dead_volume_time()
        #
        # dead_volume_time_in_seconds = self.dead_volume_time_in_seconds
        # dead_volume_time_in_minutes = dead_volume_time_in_seconds/60
        #
        # if self.rate_unit_cmd is 'OM':
        #     dead_volume = dead_volume_time_in_minutes * self.get_rate()
        # elif self.rate_unit_cmd is 'MM':
        #     dead_volume = dead_volume_time_in_minutes * self.get_rate()
        # if self.rate_unit_cmd is 'OM':
        #     dead_volume = dead_volume_time_in_seconds * self.get_rate()
        # elif self.rate_unit_cmd is 'MM':
        #     dead_volume = dead_volume_time_in_seconds * self.get_rate()
        #
        # print(f'dead volume is {dead_volume} {self.volume_unit}')
        # return dead_volume


class NewEraPeristalticPumpInterface(PeristalticPump):
    def __init__(self,
                 port: str,
                 address: int = 0,
                 start_trigger='rising',
                 stop_trigger='falling',
                 volume_unit='ml',
                 rate_unit='ml/min',
                 ):
        warnings.warn(
            'use PeristalticPump instead',
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(
            port=port,
            address=address,
            start_trigger=start_trigger,
            stop_trigger=stop_trigger,
            volume_unit=volume_unit,
            rate_unit=rate_unit,
        )
