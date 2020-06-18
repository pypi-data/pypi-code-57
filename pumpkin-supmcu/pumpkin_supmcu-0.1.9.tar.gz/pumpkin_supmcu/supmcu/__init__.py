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
The :mod:`pumpkin_supmcu.supmcu` module contains the parsing, communication interface and module telemetry enumeration
definitions.
"""
from .discovery import request_telemetry_definition, request_module_definition
from .i2c import SupMCUMaster
from .parsing import parse_telemetry, parse_header, DataItemParser, Parsers
from .types import SupMCUModuleDefinition, SupMCUTelemetryDefinition, typeof_supmcu_fmt_char, DataType, \
    sizeof_supmcu_type, TelemetryType, SupMCUTelemetry, SupMCUHDR, TelemetryDataItem, datatype_to_supmcu_fmt_char
