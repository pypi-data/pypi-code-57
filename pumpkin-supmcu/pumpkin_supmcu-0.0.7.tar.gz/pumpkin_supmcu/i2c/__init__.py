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
The `pumpkin_supmcu.i2c` module contains definitions for creating I2CMaster devices, with a universal I2C Protocol.
The `pumpkin_supmcu.i2c` module contains an implementations of the :class:`~pumpkin_supmcu.I2CMaster` for the following
devices:

* The `I2CDriver Board <https://i2cdriver.com/>`_ as :class:`~pumpkin_supmcu.I2CDriverMaster`.
* (Coming soon) `Total Phase Aardvark Adaptor <https://www.totalphase.com/products/aardvark-i2cspi/>`_ as
  I2CAardvarkMaster.

Users can create (and possibly contribute) additional :class:`~pumpkin_supmcu.I2CMaster` implementations of other
I2C Bus Adaptors.
"""
from .i2cdriver import I2CDriverMaster
from .master import I2CBusSpeed, I2CMaster
