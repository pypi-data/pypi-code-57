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
Tests subpackage module: common definitions for unittest scripts of the 'xmlschema' package.
"""
import unittest
import re
import os

from xmlschema import XMLSchema10
from xmlschema.exceptions import XMLSchemaValueError
from xmlschema.qnames import XSD_SCHEMA
from xmlschema.namespaces import XSD_NAMESPACE, get_namespace
from xmlschema.etree import etree_element, etree_register_namespace, etree_elements_assert_equal
from xmlschema.resources import fetch_namespaces
from xmlschema.helpers import is_etree_element


PROTECTED_PREFIX_PATTERN = re.compile(r'\bns\d:')
SCHEMA_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" version="{0}">
    {1}
</xs:schema>"""


class XsdValidatorTestCase(unittest.TestCase):
    """
    Base class for testing XSD validators.
    """
    TEST_CASES_DIR = None
    schema_class = XMLSchema10

    etree_register_namespace(prefix='xs', uri=XSD_NAMESPACE)
    etree_register_namespace(prefix='ns', uri="ns")

    @classmethod
    def setUpClass(cls):
        cls.errors = []
        cls.xsd_types = cls.schema_class.builtin_types()
        cls.content_pattern = re.compile(r'(<|<xs:)(sequence|choice|all)')

        cls.default_namespaces = {
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'tns': 'http://xmlschema.test/ns',
            'ns': 'ns',
        }

        if os.path.isfile(cls.casepath('testfiles')):
            cls.vh_dir = cls.casepath('examples/vehicles')
            cls.vh_xsd_file = cls.casepath('examples/vehicles/vehicles.xsd')
            cls.vh_xml_file = cls.casepath('examples/vehicles/vehicles.xml')
            cls.vh_json_file = cls.casepath('examples/vehicles/vehicles.json')
            cls.vh_schema = cls.schema_class(cls.vh_xsd_file)
            cls.vh_namespaces = fetch_namespaces(cls.vh_xml_file)

            cls.col_dir = cls.casepath('examples/collection')
            cls.col_xsd_file = cls.casepath('examples/collection/collection.xsd')
            cls.col_xml_file = cls.casepath('examples/collection/collection.xml')
            cls.col_json_file = cls.casepath('examples/collection/collection.json')
            cls.col_schema = cls.schema_class(cls.col_xsd_file)
            cls.col_namespaces = fetch_namespaces(cls.col_xml_file)

            cls.st_xsd_file = cls.casepath('features/decoder/simple-types.xsd')
            cls.st_schema = cls.schema_class(cls.st_xsd_file)

            cls.models_xsd_file = cls.casepath('features/models/models.xsd')
            cls.models_schema = cls.schema_class(cls.models_xsd_file)

    @classmethod
    def casepath(cls, relative_path):
        """
        Returns the absolute path from a relative path specified from the referenced TEST_CASES_DIR.
        """
        return os.path.join(cls.TEST_CASES_DIR or '', relative_path)

    def get_schema_source(self, source):
        """
        Returns a schema source that can be used to create an XMLSchema instance.

        :param source: A string or an ElementTree's Element.
        :return: An schema source string, an ElementTree's Element or a full pathname.
        """
        if is_etree_element(source):
            if source.tag in (XSD_SCHEMA, 'schema'):
                return source
            elif get_namespace(source.tag):
                raise XMLSchemaValueError("source %r namespace has to be empty." % source)
            elif source.tag not in {'element', 'attribute', 'simpleType', 'complexType',
                                    'group', 'attributeGroup', 'notation'}:
                raise XMLSchemaValueError("% is not an XSD global definition/declaration." % source)

            root = etree_element('schema', attrib={
                'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
                'elementFormDefault': "qualified",
                'version': self.schema_class.XSD_VERSION,
            })
            root.append(source)
            return root
        else:
            source = source.strip()
            if not source.startswith('<'):
                return self.casepath(source)
            elif source.startswith('<?xml ') or source.startswith('<xs:schema '):
                return source
            else:
                return SCHEMA_TEMPLATE.format(self.schema_class.XSD_VERSION, source)

    def get_schema(self, source, **kwargs):
        return self.schema_class(self.get_schema_source(source), **kwargs)

    def get_element(self, name, **attrib):
        source = '<xs:element name="{}" {}/>'.format(
            name, ' '.join('%s="%s"' % (k, v) for k, v in attrib.items())
        )
        schema = self.schema_class(self.get_schema_source(source))
        return schema.elements[name]

    def check_etree_elements(self, elem, other):
        """Checks if two ElementTree elements are equal."""
        try:
            self.assertIsNone(
                etree_elements_assert_equal(elem, other, strict=False, skip_comments=True)
            )
        except AssertionError as err:
            self.assertIsNone(err, None)

    def check_namespace_prefixes(self, s):
        """Checks that a string doesn't contain protected prefixes (ns0, ns1 ...)."""
        match = PROTECTED_PREFIX_PATTERN.search(s)
        if match:
            msg = "Protected prefix {!r} found:\n {}".format(match.group(0), s)
            self.assertIsNone(match, msg)

    def check_schema(self, source, expected=None, **kwargs):
        """
        Create a schema for a test case.

        :param source: A relative path or a root Element or a portion of schema for a template.
        :param expected: If it's an Exception class test the schema for raise an error. \
        Otherwise build the schema and test a condition if expected is a callable, or make \
        a substring test if it's not `None` (maybe a string). Then returns the schema instance.
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            self.assertRaises(expected, self.schema_class, self.get_schema_source(source), **kwargs)
        else:
            schema = self.schema_class(self.get_schema_source(source), **kwargs)
            if callable(expected):
                self.assertTrue(expected(schema))
            return schema

    def check_errors(self, path, expected):
        """
        Checks schema or validation errors, checking information completeness of the
        instances and those number against expected.

        :param path: the path of the test case.
        :param expected: the number of expected errors.
        """
        for e in self.errors:
            error_string = str(e)
            self.assertTrue(e.path, "Missing path for: %s" % error_string)
            self.assertTrue(e.namespaces, "Missing namespaces for: %s" % error_string)
            self.check_namespace_prefixes(error_string)

        if not self.errors and expected:
            raise ValueError("{!r}: found no errors when {} expected.".format(path, expected))
        elif len(self.errors) != expected:
            num_errors = len(self.errors)
            if num_errors == 1:
                msg = "{!r}: n.{} errors expected, found {}:\n\n{}"
            elif num_errors <= 5:
                msg = "{!r}: n.{} errors expected, found {}. Errors follow:\n\n{}"
            else:
                msg = "{!r}: n.{} errors expected, found {}. First five errors follow:\n\n{}"

            error_string = '\n++++++++++\n\n'.join([str(e) for e in self.errors[:5]])
            raise ValueError(msg.format(path, expected, len(self.errors), error_string))
