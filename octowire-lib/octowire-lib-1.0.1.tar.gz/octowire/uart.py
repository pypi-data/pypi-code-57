# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire


class UART(Octowire):
    """
    UART protocol class.
    """
    OPCODE = b"\x0a"
    OPERATION_CONFIGURE = b"\x01"
    OPERATION_TRANSMIT = b"\x02"
    OPERATION_RECEIVE = b"\x03"
    OPERATION_GET_AVAILABLE_SIZE = b"\x04"
    OPERATION_PASSTHROUGH = b"\x05"

    INTERFACE_0 = 0
    INTERFACE_1 = 1

    def __init__(self, serial_instance, interface_id):
        """
        Init function.
        :param serial_instance: Octowire Serial instance.
        :param interface_id: UART interface number.
        """
        self.serial_instance = serial_instance
        self.interface_id = interface_id
        super().__init__(serial_instance=self.serial_instance)
        if not interface_id and interface_id not in [0, 1]:
            raise ValueError('interface_id parameter should be 0 or 1.')
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")

    def configure(self, baudrate=115200):
        """
        Configure the UART interface baudrate.
        """
        baudrate = struct.pack("<L", baudrate)
        args_size = struct.pack("<H", 6)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.interface_id]) + self.OPERATION_CONFIGURE +
                                   baudrate)
        self._read_response_code(operation_name="UART configuration")

    def transmit(self, data):
        """
        This function transmits data over the UART interface.
        :param data: the payload sent over the UART interface.
        """
        if not isinstance(data, bytes):
            raise ValueError("'data' parameter is not a bytes instance.")
        data_length = len(data)
        args_size = struct.pack("<H", 2 + data_length)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.interface_id]) + self.OPERATION_TRANSMIT + data)
        self._read_response_code(operation_name="UART transmit")

    def receive(self, size):
        """
        This function receives a number of bytes from the UART interface.
        :param size: the number of bytes to receive.
        :return: the received bytes.
        :rtype: bytes
        """
        if not isinstance(size, int):
            raise ValueError("'size' parameter is not an integer.")
        args_size = struct.pack("<H", 4)
        b_size = struct.pack("<H", size)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.interface_id]) +
                                   self.OPERATION_RECEIVE + b_size)
        self._read_response_code(operation_name="UART receive read response code", disable_timeout=True)
        return self._read_data(expected_size=size, operation_name="UART receive data")

    def _get_available_size(self):
        """
        This function receives the 2 bytes data size to receive from the Octowire and returns it.
        :return: Available size.
        :rtype: int
        """
        resp = self.serial_instance.read(2)
        if not resp:
            raise Exception("Unable to get the size of the data to"
                            " receive from the Octowire (Operation: {}).".format("UART in_waiting"))
        return struct.unpack("<H", resp)[0]

    def in_waiting(self):
        """
        Get available size (waiting to be read).
        :return: the size waiting to be read on the UART interface.
        :rtype: int
        """
        args_size = struct.pack("<H", 2)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.interface_id]) +
                                   self.OPERATION_GET_AVAILABLE_SIZE)
        self._read_response_code(operation_name="UART receive")
        return self._get_available_size()

    def passthrough(self):
        """
        Enter passthrough mode (bridge mode).
        """
        args_size = struct.pack("<H", 2)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.interface_id]) + self.OPERATION_PASSTHROUGH)
        self._read_response_code(operation_name="UART passthrough")
        self.logger.handle("Please press the User Button to exit passthrough mode", self.logger.USER_INTERACT)
