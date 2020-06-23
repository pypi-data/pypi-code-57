# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire


class I2C(Octowire):
    """
    I2C protocol class.
    """
    OPCODE = b"\x0c"
    OPERATION_CONFIGURE = b"\x01"
    OPERATION_TRANSMIT = b"\x02"
    OPERATION_RECEIVE = b"\x03"
    OPERATION_SCAN = b"\x04"

    BUS_0 = 0
    BUS_1 = 1

    def __init__(self, serial_instance, bus_id):
        """
        Init function.
        :param serial_instance: Octowire serial instance.
        :param bus_id: I2C bus number.
        """
        self.serial_instance = serial_instance
        self.bus_id = bus_id
        super().__init__(serial_instance=self.serial_instance)
        if not bus_id and bus_id not in [0, 1]:
            raise ValueError('bus_id parameter should be 0 or 1.')
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")

    def configure(self, baudrate=1000000):
        """
        Configure the I2C bus baudrate.
        """
        baudrate = struct.pack("<L", baudrate)
        args_size = struct.pack("<H", 6)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.bus_id]) + self.OPERATION_CONFIGURE +
                                   baudrate)
        self._read_response_code(operation_name="I2C configuration")

    def transmit(self, data, i2c_addr, int_addr, int_addr_length):
        """
        Transmit data over the I2C interface.
        :param data: the payload sent over the I2C interface.
        :param i2c_addr: The I2C address of the slave device with which to communicate.
        :param int_addr: The internal address (internal to the device) at which to read or write data.
        :param i2c_addr_length: The internal address length (byte).
        """
        if not isinstance(data, bytes):
            raise ValueError("'i2c.transmit: data' parameter is not a bytes instance.")
        if not isinstance(i2c_addr, int):
            raise ValueError("'i2c.transmit: i2c_addr' parameter is not an integer.")
        if not isinstance(int_addr, int):
            raise ValueError("'i2c.transmit: int_addr' parameter is not an integer.")
        if not isinstance(int_addr_length, int):
            raise ValueError("'i2c.transmit: i2c_addr_length' parameter is not an integer")
        data_length = len(data)
        args_size = struct.pack("<H", 8 + data_length)
        i2c_addr = struct.pack("<B", i2c_addr)
        int_addr = struct.pack("<L", int_addr)
        int_addr_length = struct.pack("<B", int_addr_length)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.bus_id]) + self.OPERATION_TRANSMIT
                                   + i2c_addr + int_addr + int_addr_length + data)
        self._read_response_code(operation_name="I2C transmit")

    def receive(self, size, i2c_addr, int_addr, int_addr_length):
        """
        This function receive a number bytes from the I2C interface.
        :param size: the number of bytes to receive.
        :param i2c_addr: The target chip I2C address.
        :param int_addr: The internal address of the target chip.
        :param int_addr_length: The internal address length (byte).
        :return: The read bytes.
        :rtype: bytes
        """
        if not isinstance(size, int):
            raise ValueError("'i2c.receive: size' parameter is not an integer.")
        if not isinstance(i2c_addr, int):
            raise ValueError("'i2c.receive: i2c_addr' parameter is not an integer.")
        if not isinstance(int_addr, int):
            raise ValueError("'i2c.receive: int_addr' parameter is not an integer.")
        if not isinstance(int_addr_length, int):
            raise ValueError("'i2c.receive: i2c_addr_length' parameter is not an integer")
        args_size = struct.pack("<H", 10)
        b_size = struct.pack("<H", size)
        i2c_addr = struct.pack("<B", i2c_addr)
        int_addr = struct.pack("<L", int_addr)
        int_addr_length = struct.pack("<B", int_addr_length)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.bus_id]) + self.OPERATION_RECEIVE
                                   + i2c_addr + int_addr + int_addr_length + b_size)
        self._read_response_code(operation_name="I2C receive")
        return self._read_data(expected_size=size, operation_name="I2C receive")

    def _get_size_scan_data(self):
        """
        This function receives the 2 bytes data size to receive from the Octowire and returns it.
        :return: Size of the list returned by the scan function.
        :rtype: int
        """
        resp = self.serial_instance.read(2)
        if not resp:
            raise Exception("Unable to get the size of the data to"
                            " receive from the Octowire (Operation: {}).".format("I2C scan"))
        return struct.unpack("<H", resp)[0]

    def scan(self):
        """
        Scan I2C bus and return detected slave device addresses.
        :return: bytearray of I2C addresses.
        """
        i2c_addresses = bytearray()
        args_size = struct.pack("<H", 2)
        self.serial_instance.write(args_size + self.OPCODE + bytes([self.bus_id]) + self.OPERATION_SCAN)
        self._read_response_code(operation_name="I2C scan")
        list_size = self._get_size_scan_data()
        i2c_addresses += self._read_chunk(list_size, operation_name="I2C scan")
        return i2c_addresses
