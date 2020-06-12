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
"""
The implementation of the :class:`~pumpkin_supmcu.I2CMaster` for the `I2CDriver Board <https://i2cdriver.com/>`_.
"""
from i2cdriver import I2CDriver

from .master import I2CMaster, I2CBusSpeed

SDA_SCL_4_7K_MASK = 0x24


class I2CDriverMaster(I2CMaster):
    def __init__(self, port: str):
        """
        Creates an I2CMaster using the I2CDriver as the I2CMaster device.

        :param port: The serial port the I2CDriver is on.
        """
        self.i2c_driver = I2CDriver(port)
        # Work-around windows bug where first read always fails on I2C Driver
        self.i2c_driver.getstatus()
        self.i2c_driver.scan(True)

    @property
    def device_speed(self) -> I2CBusSpeed:
        """The device speed the I2C Bus is currently at."""
        self.i2c_driver.getstatus()
        return I2CBusSpeed(self.i2c_driver.speed)

    @device_speed.setter
    def device_speed(self, bus_speed: I2CBusSpeed):
        """Sets the device speed of the I2C bus."""
        self.i2c_driver.setspeed(int(bus_speed))

    @property
    def device_pullups(self) -> bool:
        """If the I2C SDA/SCL pullups are ON or OFF."""
        self.i2c_driver.getstatus()
        return (self.i2c_driver.pullups & 0x3F) > 0

    @device_pullups.setter
    def device_pullups(self, is_on: bool):
        """Sets the state of the I2C SDA/SCL pullups ON or OFF."""
        self.i2c_driver.setpullups(SDA_SCL_4_7K_MASK)

    @property
    def device_name(self) -> str:
        """Returns `I2CDriver` as the name."""
        return "I2CDriver"

    def write(self, addr: int, b: bytes):
        """
        Starts an I2C transaction for the I2CDriver and writes out all
        of the bytes `b` to the address `addr`. Stops the I2C Transaction
        once the write has finished.

        :param addr:  The I2C Address to write to.
        :param b: The bytes `b` to write to the I2C Bus.
        """
        self.i2c_driver.start(addr, 0)
        self.i2c_driver.write(b)
        self.i2c_driver.stop()

    def read(self, addr: int, amount: int) -> bytes:
        """
        Starts an I2C transaction for the I2CDriver and reads `amount` bytes
        from the device at address `addr` on the I2C Bus. Stops the I2C Transaction
        after the read has finished.

        :param addr: The I2C Address to read from.
        :param amount: The amount of bytes to read from the bus.
        :return: The bytes read from the bus.
        """
        self.i2c_driver.start(addr, 1)
        b = self.i2c_driver.read(amount)
        self.i2c_driver.stop()
        return b
