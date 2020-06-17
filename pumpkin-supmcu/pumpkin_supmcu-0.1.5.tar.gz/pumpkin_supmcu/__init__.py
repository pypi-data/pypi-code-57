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
The `pumpkin_supmcu` package has the following functionality:

* Discover all telemetry items on a module, and put into telemetry definitions.
* Parse any telemetry item on a module given a module telemetry definition.
* Provide a universal I2C interface so we can integrate multiple I2C Masters.
* Request telemetry from any SupMCU module via I2C interface.
* Write commands to SupMCU modules via I2C interface.

The `pumpkin_supmcu.i2c` package provides :class:`~pumpkin_supmcu.I2CMaster` implementations for the
`I2CDriver Board <https://i2cdriver.com/>`_ or `(support coming soon)`
`Total Phase Aardvark Adaptor <https://www.totalphase.com/products/aardvark-i2cspi/>`_.

Users are encouraged to contribute more implementations of other I2CMaster devices as
`pumpkin_supmcu` provides a :class:`~pumpkin_supmcu.I2CMaster` :class:`~typing.Protocol` to implement
(see `PEP 544 <https://www.python.org/dev/peps/pep-0544/>`_)
"""
from .i2c import I2CDriverMaster, I2CMaster, I2CBusSpeed
from .supmcu import TelemetryType, SupMCUMaster, request_module_definition, request_telemetry_definition, Parsers, \
    DataItemParser, parse_header, parse_telemetry, TelemetryDataItem, SupMCUHDR, SupMCUTelemetry, sizeof_supmcu_type, \
    DataType, typeof_supmcu_fmt_char, SupMCUTelemetryDefinition, SupMCUModuleDefinition, datatype_to_supmcu_fmt_char
