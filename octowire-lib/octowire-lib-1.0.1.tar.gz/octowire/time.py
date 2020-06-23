# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
import time
from octowire.octowire import Octowire


class Time(Octowire):
    """
    Octowire's time class.
    """
    OPCODE_GET_TIME = b"\x05"
    OPCODE_SET_TIME = b"\x06"

    def __init__(self, serial_instance):
        """
        Init function.
        :param serial_instance: Octowire Serial instance.
        """
        self.serial_instance = serial_instance
        super().__init__(serial_instance=self.serial_instance)
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter into binary mode.")

    def get_time(self):
        """
        This function returns the current internal time string of the Octowire.
        :return: The current internal time string (bytes).
        :rtype: bytes
        """
        args_size = struct.pack("<H", 0)
        self.serial_instance.write(args_size + self.OPCODE_GET_TIME)
        self._read_response_code(operation_name="Get time")
        return self._read_data(operation_name="Get time")

    def set_time(self, year, month, day, hour, minute, second):
        """
        This function sets the Octowire's internal time according to the current date and time arguments.
        """
        args_size = struct.pack("<H", 12)
        year = struct.pack("<H", year)
        month = struct.pack("<H", month)
        day = struct.pack("<H", day)
        hour = struct.pack("<H", hour)
        minute = struct.pack("<H", minute)
        second = struct.pack("<H", second)
        self.serial_instance.write(args_size + self.OPCODE_SET_TIME + year + month + day + hour + minute + second)
        self._read_response_code(operation_name="Set time", disable_timeout=True)
