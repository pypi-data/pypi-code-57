# -*- coding: utf-8 -*-

from enum import Enum


class ErrorCodes(Enum):
    XMLLINT_NOT_FOUND = 1
    INVALID_XML = 3
    INVALID_WITH_XSD = 2
    UNKNOWN = 999
