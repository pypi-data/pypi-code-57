# -*- coding: utf-8 -*-
"""A library to interface with a Hayward/Goldline AquaLogic/ProLogic
pool controller."""

from enum import IntEnum, unique
from threading import Timer
import binascii
import logging
import queue
import socket
import time
import serial

_LOGGER = logging.getLogger(__name__)


@unique
class States(IntEnum):
    """States reported by the unit"""
    # These correspond to the LEDs on the unit
    HEATER_1 = 1 << 0
    VALVE_3 = 1 << 1
    CHECK_SYSTEM = 1 << 2
    POOL = 1 << 3
    SPA = 1 << 4
    FILTER = 1 << 5
    LIGHTS = 1 << 6
    AUX_1 = 1 << 7
    AUX_2 = 1 << 8
    SERVICE = 1 << 9
    AUX_3 = 1 << 10
    AUX_4 = 1 << 11
    AUX_5 = 1 << 12
    AUX_6 = 1 << 13
    VALVE_4 = 1 << 14
    SPILLOVER = 1 << 15
    SYSTEM_OFF = 1 << 16
    AUX_7 = 1 << 17
    AUX_8 = 1 << 18
    AUX_9 = 1 << 19
    AUX_10 = 1 << 20
    AUX_11 = 1 << 21
    AUX_12 = 1 << 22
    AUX_13 = 1 << 23
    AUX_14 = 1 << 24
    SUPER_CHLORINATE = 1 << 25
    HEATER_AUTO_MODE = 1 << 30  # This is a kludge for the heater auto mode
    FILTER_LOW_SPEED = 1 << 31  # This is a kludge for the low-speed filter


@unique
class Keys(IntEnum):
    """Key events which can be sent to the unit"""
    # Second word is the same on first down, 0000 every 100ms while holding
    # Note WIRED_KEY_EVENTs only use the first 16-bits
    LIGHTS = 0x00010000
    AUX_1 = 0x00020000
    AUX_2 = 0x00040000
    AUX_3 = 0x00080000
    AUX_4 = 0x00100000
    AUX_5 = 0x00200000
    AUX_6 = 0x00400000
    AUX_7 = 0x00800000
    RIGHT = 0x01000000
    MENU = 0x02000000
    LEFT = 0x04000000
    SERVICE = 0x08000000
    MINUS = 0x10000000
    PLUS = 0x20000000
    POOL_SPA = 0x40000000
    FILTER = 0x80000000
    # These are only valid for WIRELESS_KEY_EVENTs
    VALVE_3 = 0x00000100
    VALVE_4 = 0x00000200
    HEATER_1 = 0x00000400
    AUX_8 = 0x00000800
    AUX_9 = 0x00001000
    AUX_10 = 0x00002000
    AUX_11 = 0x00004000
    AUX_12 = 0x00008000
    AUX_13 = 0x00000001
    AUX_14 = 0x00000002


class AquaLogic():
    """Hayward/Goldline AquaLogic/ProLogic pool controller."""

    # pylint: disable=too-many-instance-attributes
    FRAME_DLE = 0x10
    FRAME_STX = 0x02
    FRAME_ETX = 0x03

    FRAME_TYPE_WIRED_KEY_EVENT = b'\x00\x03'
    FRAME_TYPE_WIRELESS_KEY_EVENT = b'\x00\x83'
    FRAME_TYPE_ON_OFF_EVENT = b'\x00\x05'   # Seems to only work for some keys

    FRAME_TYPE_KEEP_ALIVE = b'\x01\x01'
    FRAME_TYPE_LEDS = b'\x01\x02'
    FRAME_TYPE_DISPLAY_UPDATE = b'\x01\x03'
    FRAME_TYPE_LONG_DISPLAY_UPDATE = b'\x04\x0a'
    FRAME_TYPE_PUMP_SPEED_REQUEST = b'\x0c\x01'
    FRAME_TYPE_PUMP_STATUS = b'\x00\x0c'

    def __init__(self, reader=None, writer=None):
        self._reader = reader
        self._writer = writer
        self._is_metric = False
        self._air_temp = None
        self._pool_temp = None
        self._spa_temp = None
        self._pool_chlorinator = None
        self._spa_chlorinator = None
        self._salt_level = None
        self._check_system_msg = None
        self._pump_speed = None
        self._pump_power = None
        self._states = 0
        self._flashing_states = 0
        self._send_queue = queue.Queue()
        self._multi_speed_pump = False
        self._heater_auto_mode = True # Assume the heater is in auto mode


    def connect(self, host, port):
        self.connect_socket(host, port)


    def connect_socket(self, host, port):
        """Connects via a RS-485 to Ethernet adapter."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        self._reader = sock.makefile(mode='rb')
        self._writer = sock.makefile(mode='wb')

    
    def connect_serial(self, serial_port_name):
        s = serial.Serial(port=serial_port_name, baudrate=19200, 
                               stopbits=serial.STOPBITS_TWO)
        self._reader = s
        self._writer = s


    def _check_state(self, data):
        desired_states = data['desired_states']
        for desired_state in desired_states:
            if (self.get_state(desired_state['state']) !=
                    desired_state['enabled']):
                # The state hasn't changed
                data['retries'] -= 1
                if data['retries'] != 0:
                    # Re-queue the request
                    _LOGGER.info('requeue')
                    self._send_queue.put(data)
                    return
            else:
                _LOGGER.debug('state change successful')



    def _send_frame(self):
        if not self._send_queue.empty():
            data = self._send_queue.get(block=False)
            self._writer.write(data['frame'])
            self._writer.flush()
            _LOGGER.info('%3.3f: Sent: %s', time.monotonic(), 
                    binascii.hexlify(data['frame']))

            try:
                if data['desired_states'] is not None:
                    # Set a timer to verify the state changes
                    # Wait 2 seconds as it can take a while for
                    # the state to change.
                    Timer(2.0, self._check_state, [data]).start()
            except KeyError:
                pass


    def process(self, data_changed_callback):
        """Process data; returns when the reader signals EOF.
        Callback is notified when any data changes."""
        # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        while True:
            # Data framing (from the AQ-CO-SERIAL manual):
            #
            # Each frame begins with a DLE (10H) and STX (02H) character start
            # sequence, followed by a 2 to 61 byte long Command/Data field, a
            # 2-byte Checksum and a DLE (10H) and ETX (03H) character end sequence.
            #
            # The DLE, STX and Command/Data fields are added together to provide the
            # 2-byte Checksum. If any of the bytes of the Command/Data Field or
            # Checksum are equal to the DLE character (10H), a NULL character (00H)
            # is inserted into the transmitted data stream immediately after that byte.
            # That NULL character must then be removed by the receiver.

            byte = self._reader.read(1)
            frame_start_time = None

            while True:
                # Search for FRAME_DLE + FRAME_STX
                if not byte:
                    return
                if byte[0] == self.FRAME_DLE:
                    frame_start_time = time.monotonic()
                    next_byte = self._reader.read(1)
                    if not next_byte:
                        return
                    if next_byte[0] == self.FRAME_STX:
                        break
                    else:
                        continue
                byte = self._reader.read(1)

            frame = bytearray()
            byte = self._reader.read(1)

            while True:
                if not byte:
                    return
                if byte[0] == self.FRAME_DLE:
                    # Should be FRAME_ETX or 0 according to
                    # the AQ-CO-SERIAL manual
                    next_byte = self._reader.read(1)
                    if not next_byte:
                        return
                    if next_byte[0] == self.FRAME_ETX:
                        break
                    elif next_byte[0] != 0:
                        # Error?
                        pass

                frame.append(byte[0])
                byte = self._reader.read(1)

            # Verify CRC
            frame_crc = int.from_bytes(frame[-2:], byteorder='big')
            frame = frame[:-2]

            calculated_crc = self.FRAME_DLE + self.FRAME_STX
            for byte in frame:
                calculated_crc += byte

            if frame_crc != calculated_crc:
                _LOGGER.warning('Bad CRC')
                continue

            frame_type = frame[0:2]
            frame = frame[2:]

            if frame_type == self.FRAME_TYPE_KEEP_ALIVE:
                # Keep alive
                #_LOGGER.debug('%3.3f: KA', frame_start_time)

                # If a frame has been queued for transmit, send it.
                if not self._send_queue.empty():
                    self._send_frame()

                continue
            elif frame_type == self.FRAME_TYPE_WIRED_KEY_EVENT:
                _LOGGER.debug('%3.3f: Wired Key: %s', 
                             frame_start_time, binascii.hexlify(frame))
            elif frame_type == self.FRAME_TYPE_WIRELESS_KEY_EVENT:
                _LOGGER.debug('%3.3f: Wireless Key: %s', 
                             frame_start_time, binascii.hexlify(frame))
            elif frame_type == self.FRAME_TYPE_LEDS:
                #_LOGGER.debug('%3.3f: LEDs: %s', 
                #              frame_start_time, binascii.hexlify(frame))
                # First 4 bytes are the LEDs that are on;
                # second 4 bytes_ are the LEDs that are flashing
                states = int.from_bytes(frame[0:4], byteorder='little')
                flashing_states = int.from_bytes(frame[4:8],
                                                 byteorder='little')
                states |= flashing_states
                if self._heater_auto_mode:
                    states |= States.HEATER_AUTO_MODE
                if (states != self._states
                        or flashing_states != self._flashing_states):
                    self._states = states
                    self._flashing_states = flashing_states
                    data_changed_callback(self)
            elif frame_type == self.FRAME_TYPE_PUMP_SPEED_REQUEST:
                value = int.from_bytes(frame[0:2], byteorder='big')
                _LOGGER.debug('%3.3f: Pump speed request: %d%%', 
                              frame_start_time, value)
                if self._pump_speed != value:
                    self._pump_speed = value
                    data_changed_callback(self)
            elif (frame_type == self.FRAME_TYPE_PUMP_STATUS) & (len(frame) >= 5):
                # Pump status messages sent out by Hayward VSP pumps
                self._multi_speed_pump = True
                speed = frame[2]
                # Power is in BCD
                power = ((((frame[3] & 0xf0) >> 4) * 1000)
                         + (((frame[3] & 0x0f)) * 100)
                         + (((frame[4] & 0xf0) >> 4) * 10)
                         + (((frame[4] & 0x0f))))
                _LOGGER.debug('%3.3f; Pump speed: %d%%, power: %d watts',
                              frame_start_time, speed, power)
                if self._pump_power != power:
                    self._pump_power = power
                    data_changed_callback(self)
            elif frame_type == self.FRAME_TYPE_DISPLAY_UPDATE:
                parts = frame.decode('latin-1').split()
                _LOGGER.debug('%3.3f: Display update: %s', 
                              frame_start_time, parts)

                try:
                    if parts[0] == 'Pool' and parts[1] == 'Temp':
                        # Pool Temp <temp>°[C|F]
                        value = int(parts[2][:-2])
                        if self._pool_temp != value:
                            self._pool_temp = value
                            self._is_metric = parts[2][-1:] == 'C'
                            data_changed_callback(self)
                    elif parts[0] == 'Spa' and parts[1] == 'Temp':
                        # Spa Temp <temp>°[C|F]
                        value = int(parts[2][:-2])
                        if self._spa_temp != value:
                            self._spa_temp = value
                            self._is_metric = parts[2][-1:] == 'C'
                            data_changed_callback(self)
                    elif parts[0] == 'Air' and parts[1] == 'Temp':
                        # Air Temp <temp>°[C|F]
                        value = int(parts[2][:-2])
                        if self._air_temp != value:
                            self._air_temp = value
                            self._is_metric = parts[2][-1:] == 'C'
                            data_changed_callback(self)
                    elif parts[0] == 'Pool' and parts[1] == 'Chlorinator':
                        # Pool Chlorinator <value>%
                        value = int(parts[2][:-1])
                        if self._pool_chlorinator != value:
                            self._pool_chlorinator = value
                            data_changed_callback(self)
                    elif parts[0] == 'Spa' and parts[1] == 'Chlorinator':
                        # Spa Chlorinator <value>%
                        value = int(parts[2][:-1])
                        if self._spa_chlorinator != value:
                            self._spa_chlorinator = value
                            data_changed_callback(self)
                    elif parts[0] == 'Salt' and parts[1] == 'Level':
                        # Salt Level <value> [g/L|PPM|
                        value = float(parts[2])
                        if self._salt_level != value:
                            self._salt_level = value
                            self._is_metric = parts[3] == 'g/L'
                            data_changed_callback(self)
                    elif parts[0] == 'Check' and parts[1] == 'System':
                        # Check System <msg>
                        value = ' '.join(parts[2:])
                        if self._check_system_msg != value:
                            self._check_system_msg = value
                            data_changed_callback(self)
                    elif parts[0] == 'Heater1':
                        self._heater_auto_mode = parts[1] == 'Auto'
                except ValueError:
                    pass
            elif frame_type == self.FRAME_TYPE_LONG_DISPLAY_UPDATE:
                # Not currently parsed
                pass
            else:
                _LOGGER.info('%3.3f: Unknown frame: %s %s',
                             frame_start_time,
                             binascii.hexlify(frame_type),
                             binascii.hexlify(frame))

    def _append_data(self, frame, data):
        for byte in data:
            frame.append(byte)
            if byte == self.FRAME_DLE:
                frame.append(0)

    def _get_key_event_frame(self, key):
        frame = bytearray()
        frame.append(self.FRAME_DLE)
        frame.append(self.FRAME_STX)

        self._append_data(frame, self.FRAME_TYPE_WIRELESS_KEY_EVENT)
        self._append_data(frame, b'\x01')
        self._append_data(frame, key.value.to_bytes(4, byteorder='big'))
        self._append_data(frame, key.value.to_bytes(4, byteorder='big'))
        self._append_data(frame, b'\x00')

        crc = 0
        for byte in frame:
            crc += byte
        self._append_data(frame, crc.to_bytes(2, byteorder='big'))

        frame.append(self.FRAME_DLE)
        frame.append(self.FRAME_ETX)

        return frame

    def send_key(self, key):
        """Sends a key."""
        _LOGGER.info('Queueing key %s', key)
        frame = self._get_key_event_frame(key)

        # Queue it to send immediately following the reception
        # of a keep-alive packet in an attempt to avoid bus collisions.
        self._send_queue.put({'frame': frame})

    @property
    def air_temp(self):
        """Returns the current air temperature, or None if unknown."""
        return self._air_temp

    @property
    def pool_temp(self):
        """Returns the current pool temperature, or None if unknown."""
        return self._pool_temp

    @property
    def spa_temp(self):
        """Returns the current spa temperature, or None if unknown."""
        return self._spa_temp

    @property
    def pool_chlorinator(self):
        """Returns the current pool chlorinator level in %,
        or None if unknown."""
        return self._pool_chlorinator

    @property
    def spa_chlorinator(self):
        """Returns the current spa chlorinator level in %,
        or None if unknown."""
        return self._spa_chlorinator

    @property
    def salt_level(self):
        """Returns the current salt level, or None if unknown."""
        return self._salt_level

    @property
    def check_system_msg(self):
        """Returns the current 'Check System' message, or None if unknown."""
        if self.get_state(States.CHECK_SYSTEM):
            return self._check_system_msg
        return None

    @property
    def status(self):
        """Returns 'OK' or the current 'Check System' message."""
        if self.get_state(States.CHECK_SYSTEM):
            return self._check_system_msg
        return 'OK'

    @property
    def pump_speed(self):
        """Returns the current pump speed in percent, or None if unknown.
           Requires a Hayward VSP pump connected to the AquaLogic bus."""
        return self._pump_speed

    @property
    def pump_power(self):
        """Returns the current pump power in watts, or None if unknown.
           Requires a Hayward VSP pump connected to the AquaLogic bus."""
        return self._pump_power

    @property
    def is_metric(self):
        """Returns True if the temperature and salt level values
        are in Metric."""
        return self._is_metric

    def states(self):
        """Returns a set containing the enabled states."""
        state_list = []
        for state in States:
            if state.value & self._states != 0:
                state_list.append(state)

        if (self._flashing_states & States.FILTER) != 0:
            state_list.append(States.FILTER_LOW_SPEED)

        return state_list

    def get_state(self, state):
        """Returns True if the specified state is enabled."""
        # Check to see if we have a change request pending; if we do
        # return the value we expect it to change to.
        for data in list(self._send_queue.queue):
            desired_states = data['desired_states']
            for desired_state in desired_states:
                if desired_state['state'] == state:
                    return desired_state['enabled']
        if state == States.FILTER_LOW_SPEED:
            return (States.FILTER.value & self._flashing_states) != 0
        return (state.value & self._states) != 0

    def set_state(self, state, enable):
        """Set the state."""

        is_enabled = self.get_state(state)
        if is_enabled == enable:
            return True

        key = None

        if state == States.FILTER_LOW_SPEED:
            if not self._multi_speed_pump:
                return False
            # Send the FILTER key once.
            # If the pump is in high speed, it wil switch to low speed.
            # If the pump is off the retry mechanism will send an additional
            # FILTER key to switch into low speed.
            # If the pump is in low speed then we pretend the pump is off;
            # the retry mechanism will send an additional FILTER key
            # to switch into high speed.
            key = Keys.FILTER
            desired_states = [{'state': state, 'enabled': not is_enabled}]
            desired_states.append({'state': States.FILTER, 'enabled': True})
        elif state == States.HEATER_AUTO_MODE:
            key = Keys.HEATER_1
            # Flip the heater mode
            desired_states = [{'state': States.HEATER_AUTO_MODE, 'enabled': not self._heater_auto_mode}]
        elif state == States.POOL or state == States.SPA:
            key = Keys.POOL_SPA
            desired_states = [{'state': state, 'enabled': not is_enabled}]
        elif state == States.HEATER_1:
            # TODO: is there a way to force the heater on? Perhaps press & hold?
            return False
        else:
            # See if this state has a corresponding Key
            try:
                key = Keys[state.name]
            except KeyError:
                # TODO: send the appropriate combination of keys
                # to enable the state
                return False
            desired_states = [{'state': state, 'enabled': not is_enabled}]

        frame = self._get_key_event_frame(key)

        # Queue it to send immediately following the reception
        # of a keep-alive packet in an attempt to avoid bus collisions.
        self._send_queue.put({'frame': frame, 'desired_states': desired_states,
                              'retries': 10})

        return True

    def enable_multi_speed_pump(self, enable):
        """Enables multi-speed pump mode."""
        self._multi_speed_pump = enable
        return True
