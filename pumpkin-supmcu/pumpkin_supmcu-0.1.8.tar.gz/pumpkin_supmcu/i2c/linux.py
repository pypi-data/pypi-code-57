# coding: utf-8
# ##############################################################################
#  (C) Copyright 2019 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
import sys
from .master import I2CMaster, I2CBusSpeed
from plumbum import local
from socket import gethostname
from typing import List
if sys.platform.startswith("linux"):
    from smbus2 import SMBus, i2c_msg
else:
    SMBus = object
    i2c_msg = object


class I2CLinuxMaster(I2CMaster):
    def __init__(self, port: int):
        """
        Creates an :class:`~pumpkin_supmcu.I2CMaster` using linux's /dev/i2c-# interface

        :param port: the number of the i2c bus that is connected to the SupMCU
        """
        if not sys.platform.startswith("linux"):
            raise OSError("This class is only supported in linux")
        self.bus = SMBus(port)
        self.port = port

    @property
    def device_name(self) -> str:
        """Gets the device's hostname"""
        return gethostname()

    # FIXME this should return the current baudrate, not just the default
    @property
    def device_speed(self) -> I2CBusSpeed:
        """The default I2C baudrate"""
        return I2CBusSpeed(100)

    @device_speed.setter
    def device_speed(self, bus_speed: I2CBusSpeed):
        """"Supposed to set the baudrate of the I2C bus"""
        raise NotImplementedError("The I2C baud rate cannot be changed without rebooting")

    @property
    def device_pullups(self) -> bool:
        """If the I2C SDA/SCL pullups are ON or OFF."""
        return True

    @device_pullups.setter
    def device_pullups(self, is_on: bool):
        """Supposed to set the state of the I2C SDA/SCL pullups ON or OFF."""
        raise NotImplementedError("The pullups cannot be changed in software")

    def write(self, addr: int, b: bytes):
        """
        Writes all of `b` bytes to address `addr`

        :param addr:  The I2C Address to write to.
        :param b: The bytes `b` to write to the I2C Bus.
        """
        msg = i2c_msg.write(addr, b)
        self.bus.i2c_rdwr(msg)

    def read(self, addr: int, amount: int) -> bytes:
        """
        Reads `amount` bytes of data from address `addr`

        :param addr: The I2C Address to read from.
        :param amount: The amount of bytes to read from the bus.
        :return: The bytes read from the bus.
        """
        msg = i2c_msg.read(addr, amount)
        self.bus.i2c_rdwr(msg)
        return bytes(msg)

    def get_bus_devices(self) -> List[int]:
        """
        Gets the available I2C devices from the selected I2C bus and
        returns a list of device addresses

        :return: A list of device addresses
        """
        # plumbum.local will raise an import error if i2cdetect isn't found
        i2cdetect = local['i2cdetect']
        devices = i2cdetect["-y", str(self.port)]()
        # Parsing the output from the i2cdetect command for the device addresses
        devices = devices.split("\n")[1:]
        devices = [x.split(':')[-1].split() for x in devices]
        devices = [i for x in devices for i in x]
        return [int(i, 16) for i in devices if i != "--" and i != "UU"]
