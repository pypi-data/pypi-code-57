#
# Copyright (c), 2016-2020, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
"""
Subpackage with unittest extensions for xmlschema.

Includes common classes and helpers for building test scripts for xmlschema. The main
part is a test factory for creating test cases from lists of paths to XSD or XML files.
The list of cases can be defined within files named "testfiles". These are text files
that contain a list of relative paths to XSD or XML files, that are used to dinamically
build a set of test classes. Each path is followed by a list of options that defines a
custom setting for each test.
"""
import platform
from urllib.request import urlopen
from urllib.error import URLError

import xmlschema

from .case_class import XsdValidatorTestCase
from .builders import make_schema_test_class, make_validation_test_class
from .factory import get_test_args, xsd_version_number, defuse_data, \
    get_test_program_args_parser, get_test_line_args_parser, tests_factory
from .observers import SchemaObserver, ObservedXMLSchema10, ObservedXMLSchema11


def has_network_access(*locations):
    for url in locations:
        try:
            urlopen(url, timeout=5)
        except (URLError, OSError):
            pass
        else:
            return True
    return False


SKIP_REMOTE_TESTS = not has_network_access(
    'https://github.com/', 'https://www.w3.org/', 'https://www.sissa.it/'
)


def print_test_header():
    """Print an header thar displays Python version and platform used for test session."""
    header1 = "Test %r" % xmlschema
    header2 = "with Python {} on platform {}".format(platform.python_version(), platform.platform())
    print('{0}\n{1}\n{2}\n{0}'.format("*" * max(len(header1), len(header2)), header1, header2))


__all__ = [
    'XsdValidatorTestCase', 'make_schema_test_class', 'make_validation_test_class',
    'get_test_args', 'xsd_version_number', 'defuse_data', 'get_test_program_args_parser',
    'get_test_line_args_parser', 'tests_factory', 'SchemaObserver', 'ObservedXMLSchema10',
    'ObservedXMLSchema11', 'has_network_access', 'SKIP_REMOTE_TESTS', 'print_test_header',
]
