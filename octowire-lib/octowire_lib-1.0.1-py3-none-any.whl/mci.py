# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire
from math import ceil


class MCI(Octowire):
    """
    MCI protocol class.
    The MCI protocol allows access to the Octowire's Memory Card interface.
    """
    OPCODE = b"\x0d"
    OPERATION_DETECT = b"\x01"
    OPERATION_TRANSMIT = b"\x02"
    OPERATION_RECEIVE = b"\x03"

    def __init__(self, serial_instance):
        """
        Init function.
        :param serial_instance: Octowire Serial instance.
        """
        self.serial_instance = serial_instance
        super().__init__(serial_instance=self.serial_instance)
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")

    def detect(self):
        """
        Detect MCI interface and return 4 Bytes containing Status, Type, Version and Capacity in KB information.
        return: Dictionary containing the status, type, version and capacity
        """
        valid_status = ["OK", "Initializing", "Error", "No media present"]
        valid_type = ["SD (Secure Digital)", "MMC (MultiMedia Card)", "SDHC (Secure Digital high Capacity)",
                      "MMCHC (MultiMedia Card High Capacity)", "SDIO (Secure Digital I/O)", "Combo (SD + SDIO)",
                      "Combo HC (SDHC + SDIO)", "Unknown"]
        args_size = struct.pack("<H", 1)
        self.serial_instance.write(args_size + self.OPCODE + self.OPERATION_DETECT)
        self._read_response_code(operation_name="MCI Detect response code")
        # Read values
        status = struct.unpack("<B", self.serial_instance.read(1))
        mem_type = struct.unpack("<B", self.serial_instance.read(1))
        version = struct.unpack("<B", self.serial_instance.read(1))
        capacity = struct.unpack("<L", self.serial_instance.read(4))
        # Data interpretation
        try:
            status_str = valid_status[status[0]]
        except KeyError:
            status_str = "Invalid status"
        try:
            type_str = valid_type[mem_type[0]]
        except KeyError:
            type_str = "Invalid type"
        return {
            "status": status[0],
            "status_str": status_str,
            "type": mem_type[0],
            "type_str": type_str,
            "minor_version": version[0] >> 0 & 0b1111,
            "major_version": version[0] >> 4 & 0b1111,
            "version_str": "{}.{}".format(version[0] >> 4 & 0b1111, version[0] >> 0 & 0b1111),
            "capacity": capacity[0],
        }

    def transmit(self, data, start_block):
        """
        Transmit data through the MCI interface.
        :param data: the data (bytes) to send through the MCI interface.
        :param start_block: The index of the first block to write.
        :return: Nothing
        """
        if not isinstance(data, bytes):
            raise ValueError("'data' parameter is not a bytes instance.")
        # One block = 512 bytes
        block_count = ceil(len(data) / 512)
        current_block = 0
        while block_count > 0:
            # Write 8 blocks maximum per transmission
            blocks = 8 if block_count > 8 else block_count
            data_chunk = data[current_block * 512:(current_block + blocks) * 512]
            args_size = struct.pack("<H", 5 + len(data_chunk))
            self.serial_instance.write(args_size + self.OPCODE + self.OPERATION_TRANSMIT +
                                       struct.pack("<L", current_block + start_block) + data_chunk)
            self._read_response_code(operation_name="MCI transmit response code")
            # Update current block
            current_block = current_block + blocks
            # Decrement number of block
            block_count = block_count - blocks

    def receive(self, size, start_block):
        """
        This function receives the number of bytes from the MCI interface.
        :param size: the number of bytes to receive.
        :param start_block: The index of the first block to receive.
        :return: the read bytes.
        :rtype: bytes
        """
        data = bytearray()
        if not isinstance(size, int):
            raise ValueError("'size' parameter is not an integer.")
        args_size = struct.pack("<H", 6)
        # 1 block = 512 Bytes
        block_count = ceil(size / 512)
        current_block = start_block
        while block_count > 0:
            # Read by block of 8 maximum
            blocks = block_count if block_count < 8 else 8
            self.serial_instance.write(args_size + self.OPCODE + self.OPERATION_RECEIVE +
                                       struct.pack("<L", current_block) + struct.pack("<B", blocks))
            self._read_response_code(operation_name="MCI receive response code")
            data.extend(self._read_data(operation_name="MCI receive data"))
            # Update the index of the first block
            current_block = current_block + blocks
            # Decrement the size
            block_count = block_count - blocks
        return data[:size]
