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
"""
The :class:`~pumpkin_supmcu.I2CMaster` :class:`~typing.Protocol` is for creating I2C Bus Master implementations
such as the :class:`~pumpkin_supmcu.I2CDriverMaster`. Any implementation of the :class:`~pumpkin_supmcu.I2CMaster`
can be used with functions/classes defined in the :py:mod:`~pumpkin_supmcu.supmcu` module.
"""
import sys
from abc import abstractmethod
from enum import IntEnum

if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
    from typing import Protocol
else:
    from typing_extensions import Protocol


class I2CBusSpeed(IntEnum):
    """The possible I2C Bus speeds that are supported by the I2CMaster Protocol."""
    Standard = 100
    """100 kHz bus speed"""
    Fast = 400
    """400 kHz bus speed"""


class I2CMaster(Protocol):
    """
    The :class:`~typing.Protocol` to use for implementing a I2C Master device such as the I2CDriver or
    the Aardvark. Note the package
    """

    @property
    @abstractmethod
    def device_name(self) -> str:
        """Returns the name of the I2C Master device."""

    @property
    @abstractmethod
    def device_speed(self) -> I2CBusSpeed:
        """Returns the I2C bus speed currently used."""

    @device_speed.setter
    @abstractmethod
    def device_speed(self, speed: I2CBusSpeed):
        """Sets the I2C bus speed to use."""

    @property
    @abstractmethod
    def device_pullups(self) -> bool:
        """Returns if the I2C pullups are ON or OFF."""

    @device_pullups.setter
    @abstractmethod
    def device_pullups(self, is_on: bool):
        """Sets if the I2C pullups are ON or OFF."""

    @abstractmethod
    def write(self, addr: int, b: bytes):
        """Writes the bytes `b` to the I2C address `addr`."""

    @abstractmethod
    def read(self, addr: int, amount: int) -> bytes:
        """Reads `amount` bytes from the I2C address `addr`."""
