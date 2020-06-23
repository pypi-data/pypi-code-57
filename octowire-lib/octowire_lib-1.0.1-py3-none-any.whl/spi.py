# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire


class SPI(Octowire):
    """
    SPI protocol class.
    """
    OPCODE = b"\x0b"
    OPERATION_CONFIGURE = b"\x01"
    OPERATION_TRANSMIT = b"\x02"
    OPERATION_RECEIVE = b"\x03"
    OPERATION_TRANSMIT_RECEIVE = b"\x04"

    BUS_0 = 0
    BUS_1 = 1

    def __init__(self, serial_instance, bus_id):
        """
        Init function.
        :param serial_instance: Octowire Serial instance.
        :param bus_id: SPI bus number.
        """
        self.serial_instance = serial_instance
        self.bus_id = bus_id
        super().__init__(serial_instance=self.serial_instance)
        if not bus_id and bus_id not in [0, 1]:
            raise ValueError('bus_id parameter should be 0 or 1.')
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")

    def configure(self, baudrate=1000000, clock_polarity=0, clock_phase=0):
        """
        Configure the SPI bus (baudrate, clock phase and clock polarity).
        """
        baudrate = struct.pack("<L", baudrate)
        args_size = struct.pack("<H", 8)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.bus_id]) + self.OPERATION_CONFIGURE +
                                   baudrate + bytes([clock_polarity]) + bytes([clock_phase]))
        self._read_response_code(operation_name="SPI configuration")

    def transmit(self, data):
        """
        Transmit data over the SPI interface.
        :param data: the payload sent over the SPI interface.
        """
        if not isinstance(data, bytes):
            raise ValueError("'data' parameter is not a bytes instance.")
        data_length = len(data)
        args_size = struct.pack("<H", 2 + data_length)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.bus_id]) + self.OPERATION_TRANSMIT + data)
        self._read_response_code(operation_name="SPI transmit")

    def receive(self, size):
        """
        This function receives the number bytes from the SPI interface.
        :param size: the number of bytes to receive.
        :return: the read bytes.
        :rtype: bytes
        """
        if not isinstance(size, int):
            raise ValueError("'size' parameter is not an integer.")
        args_size = struct.pack("<H", 4)
        size_b = struct.pack("<H", size)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.bus_id]) + self.OPERATION_RECEIVE + size_b)
        self._read_response_code(operation_name="SPI receive")
        return self._read_data(expected_size=size, operation_name="SPI receive")

    def transmit_receive(self, data):
        """
        This function transmits and receives data simultaneously.
        :param data: the payload sent over the SPI interface.
        :return: the read bytes.
        :rtype: bytes
        """
        if not isinstance(data, bytes):
            raise ValueError("'data' parameter is not a bytes instance.")
        data_length = len(data)
        args_size = struct.pack("<H", 2 + data_length)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.bus_id]) +
                                   self.OPERATION_TRANSMIT_RECEIVE + data)
        self._read_response_code(operation_name="SPI transmit&receive")
        return self._read_data(operation_name="SPI transmit&receive")
