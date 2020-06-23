# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import serial
import struct
import time
from octowire.utils.Logger import Logger


class Octowire:
    """
    Octowire superclass.
    Each protocol should inherit from it.
    It implements basic functionality.
    """
    def __init__(self, serial_instance=None):
        """
        Init function.
        :param serial_instance: Octowire USB CDC Serial (pyserial) instance.
        """
        self.serial_instance = serial_instance
        self.logger = Logger()

    def is_connected(self):
        """
        Check octowire serial port connection status.
        :return: Bool
        """
        if self._is_serial_instance():
            if self.serial_instance.is_open:
                return True
            else:
                self.logger.handle("Serial port is a valid serial instance but no connection was detected.",
                                   self.logger.ERROR)
                return False
        else:
            self.logger.handle("{}{}".format(type(self.serial_instance), " is not a Serial instance."),
                               self.logger.ERROR)
            return False

    def _is_serial_instance(self):
        """
        Check whether serial_port is a valid Serial instance.
        :return:
        """
        return isinstance(self.serial_instance, serial.Serial)

    def ensure_binary_mode(self):
        """
        Ensure that the Octowire is in binary mode. Otherwise enter it.
        :return: bool
        """
        if self.is_connected():
            current_mode = self.mode
            if current_mode == 't':
                binmode_opcode = b"binmode\n"
                self.serial_instance.write(binmode_opcode)
                time.sleep(1)
                # read local echo
                self.serial_instance.read(self.serial_instance.in_waiting)
                if self.mode == 'b':
                    return True
                else:
                    self.logger.handle("Unable to switch the Octowire to binary mode.", self.logger.ERROR)
                    return False
            elif current_mode == 'b':
                return True
            else:
                return False

    def ensure_text_mode(self):
        """
        Ensure that the Octowire is in text mode. Otherwise enter it.
        :return: bool
        """
        if self.is_connected():
            current_mode = self.mode
            if current_mode == 'b':
                mode_opcode = b"\x00\x00\x01"
                self.serial_instance.write(mode_opcode)
                time.sleep(1)
                # read local echo
                self.serial_instance.read(self.serial_instance.in_waiting)
                if self.mode == 't':
                    return True
                else:
                    self.logger.handle("Unable to switch the Octowire to text mode.", self.logger.ERROR)
                    return False
            elif current_mode == 't':
                return True
            else:
                return False

    def octowire_status_is_valid(self):
        """
        Determine whether Octowire is in a valid mode (b or t).
        :return: Bool
        """
        if self._is_serial_instance():
            octowire_mode = self.mode
            if octowire_mode in ["t", "b"]:
                return True
            else:
                self.logger.handle("Invalid string mode received", self.logger.ERROR)
                return False
        else:
            self.logger.handle("The serial_instance parameter is not a valid Serial instance.", self.logger.ERROR)
            return False

    def get_octowire_version(self):
        """
        Return the Octowire version.
        :return: string (Octowire version).
        """
        if self.octowire_status_is_valid():
            version_opcode = b"\x00\x00\x02"
            mode = self.mode
            # If the Octowire is in text mode, enter in binary mode
            if mode == "t":
                self.ensure_binary_mode()
            # Get Octowire version
            self.serial_instance.write(version_opcode)
            # First, read the command status
            status = self.serial_instance.read(1)
            if status == b"\x00":
                # Then, read 4 bytes to get the response size sent by the Octowire
                size = self.serial_instance.read(4)
                if int.from_bytes(size, byteorder='little') > 0:
                    # Finally, read the Octowire version string
                    version = self.serial_instance.read(struct.unpack("<L", size)[0])
                    return version.decode()
                else:
                    self.logger.handle("Invalid version size returned by the Octowire.", self.logger.ERROR)
                    return None
            else:
                self.logger.handle("Error while trying to get Octowire version.", self.logger.ERROR)
                return None
        else:
            return None

    def _read_response_code(self, operation_name=None, disable_timeout=False):
        """
        This function handles reading the response code.
        :param operation_name: String Octowire operation name.
        :param disable_timeout: If true, disable the Serial instance timeout.
        :return: Nothing
        """
        timeout = self.serial_instance.timeout
        if disable_timeout:
            self.serial_instance.timeout = None
        status = self.serial_instance.read(1)
        self.serial_instance.timeout = timeout
        if status != b"\x00":
            raise Exception("Operation '{}' returned an error.".format(operation_name))

    def _get_size_read_data(self, operation_name=None):
        """
        This function receives the 4 bytes data size to receive from the Octowire and returns it.
        :param operation_name: String Octowire operation name.
        :return: Size of the next data chunk to read.
        :rtype: int
        """
        resp = self.serial_instance.read(4)
        if not resp:
            raise Exception("Unable to get the size of the data to"
                            " receive from the Octowire (Operation: {}).".format(operation_name))
        return struct.unpack("<L", resp)[0]

    def _read_chunk(self, chunk_size, operation_name=None):
        """
        This function reads a chunk of data.
        :param chunk_size: The data length to read (bytes).
        :param operation_name: Octowire operation name.
        :return: the data chunk that was read.
        :rtype: bytes
        """
        chunk = self.serial_instance.read(chunk_size)
        if not chunk:
            raise Exception("No data received from the Octowire (Operation: {}).".format(operation_name))
        return chunk

    def _read_data(self, expected_size=None, operation_name=None):
        """
        This function handles data reception.
        :param operation_name: Octowire operation name.
        :param expected_size: The expected size to read.
        :return: Data read from the Octowire.
        :rtype: bytes
        """
        data = bytearray()
        if expected_size is not None:
            while expected_size > 0:
                chunk_size = self._get_size_read_data(operation_name)
                data.extend(self._read_chunk(chunk_size, operation_name=operation_name))
                expected_size = expected_size - chunk_size
        # When the size of data to receive is not known, for get Octowire version for example, read only the first chunk
        else:
            chunk_size = self._get_size_read_data(operation_name)
            data.extend(self._read_chunk(chunk_size, operation_name=operation_name))
        return data

    @property
    def mode(self):
        """
        This function sends the 0x0a character to detect the current mode (binary or text).
        :return: 'b' or 't'.
        :rtype: string
        """
        self.serial_instance.write(b"\x0a")
        time.sleep(0.1)
        if self.serial_instance.in_waiting:
            self.serial_instance.read(self.serial_instance.in_waiting)
            return "t"
        else:
            # If in bin mode, we have to terminate the command (args size + version opcode + empty arguments)
            self.serial_instance.write(b"\x00\x02" + 10 * b"\x00")
            self._read_response_code(operation_name="Get current Octowire's mode")
            self._read_data(operation_name="Detect current Octowire's mode")
            return "b"

    @mode.setter
    def mode(self, value):
        """
        Allow to switch between the binary and text mode.
        :param value: 'b' for binary, 't' for text.
        """
        if value in ["t", "b"]:
            if value == "t":
                if not self.ensure_text_mode():
                    raise Exception("Unable to switch the Octowire to text mode.")
            else:
                if not self.ensure_binary_mode():
                    raise Exception("Unable to switch the Octowire to binary mode.")
        else:
            raise ValueError("Invalid mode selector. 'b' or 't' is waiting.")
