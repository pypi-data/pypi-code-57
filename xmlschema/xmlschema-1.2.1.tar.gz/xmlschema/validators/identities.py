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
This module contains classes for other XML Schema identity constraints.
"""
import re
from collections import Counter
from elementpath import Selector, XPath2Parser, ElementPathError

from ..exceptions import XMLSchemaValueError
from ..qnames import XSD_ANNOTATION, XSD_QNAME, XSD_UNIQUE, XSD_KEY, XSD_KEYREF, \
    XSD_SELECTOR, XSD_FIELD, get_qname, qname_to_extended, is_not_xsd_annotation
from ..etree import etree_getpath
from ..regex import get_python_regex

from .exceptions import XMLSchemaValidationError
from .xsdbase import XsdComponent

QNAME_PATTERN = re.compile(
    r'(?:(?P<prefix>[^\d\W][\w\-.\u00B7\u0300-\u036F\u0387\u06DD\u06DE\u203F\u2040]*):)?'
    r'(?P<local>[^\d\W][\w\-.\u00B7\u0300-\u036F\u0387\u06DD\u06DE\u203F\u2040]*)',
)

XSD_IDENTITY_XPATH_SYMBOLS = {
    'processing-instruction', 'following-sibling', 'preceding-sibling',
    'ancestor-or-self', 'attribute', 'following', 'namespace', 'preceding',
    'ancestor', 'position', 'comment', 'parent', 'child', 'false', 'text', 'node',
    'true', 'last', 'not', 'and', 'mod', 'div', 'or', '..', '//', '!=', '<=', '>=', '(', ')',
    '[', ']', '.', '@', ',', '/', '|', '*', '-', '=', '+', '<', '>', ':', '(end)', '(name)',
    '(string)', '(float)', '(decimal)', '(integer)', '::'
}


class XsdIdentityXPathParser(XPath2Parser):
    symbol_table = {
        k: v for k, v in XPath2Parser.symbol_table.items() if k in XSD_IDENTITY_XPATH_SYMBOLS
    }
    SYMBOLS = XSD_IDENTITY_XPATH_SYMBOLS


XsdIdentityXPathParser.build_tokenizer()


class XsdSelector(XsdComponent):
    """Class for defining an XPath selector for an XSD identity constraint."""
    _ADMITTED_TAGS = {XSD_SELECTOR}
    xpath_default_namespace = ''
    pattern = re.compile(get_python_regex(
        r"(\.//)?(((child::)?((\i\c*:)?(\i\c*|\*)))|\.)(/(((child::)?"
        r"((\i\c*:)?(\i\c*|\*)))|\.))*(\|(\.//)?(((child::)?((\i\c*:)?"
        r"(\i\c*|\*)))|\.)(/(((child::)?((\i\c*:)?(\i\c*|\*)))|\.))*)*"
    ))

    def __init__(self, elem, schema, parent):
        super(XsdSelector, self).__init__(elem, schema, parent)

    def _parse(self):
        super(XsdSelector, self)._parse()
        try:
            self.path = self.elem.attrib['xpath']
        except KeyError:
            self.parse_error("'xpath' attribute required:", self.elem)
            self.path = '*'
        else:
            if not self.pattern.match(self.path.replace(' ', '')):
                self.parse_error("Wrong XPath expression for an xs:selector")

        # XSD 1.1 xpathDefaultNamespace attribute
        if self.schema.XSD_VERSION > '1.0':
            if 'xpathDefaultNamespace' in self.elem.attrib:
                self.xpath_default_namespace = self._parse_xpath_default_namespace(self.elem)
            else:
                self.xpath_default_namespace = self.schema.xpath_default_namespace

        try:
            self.xpath_selector = Selector(
                path=self.path,
                namespaces=self.namespaces,
                parser=XsdIdentityXPathParser,
                default_namespace=self.xpath_default_namespace,
                compatibility_mode=True,
                strict=False,
            )
        except ElementPathError as err:
            self.parse_error(err)
            self.xpath_selector = Selector('*', self.namespaces, XsdIdentityXPathParser)

    def __repr__(self):
        return '%s(path=%r)' % (self.__class__.__name__, self.path)

    @property
    def built(self):
        return True

    @property
    def target_namespace(self):
        if ':' in self.path:
            match = QNAME_PATTERN.findall(self.path)
            if match is not None:
                prefix = match[0][0]
                if prefix:
                    return self.namespaces[prefix]
                elif self.xpath_default_namespace:
                    return self.xpath_default_namespace

        return self.schema.target_namespace


class XsdFieldSelector(XsdSelector):
    """Class for defining an XPath field selector for an XSD identity constraint."""
    _ADMITTED_TAGS = {XSD_FIELD}
    pattern = re.compile(get_python_regex(
        r"(\.//)?((((child::)?((\i\c*:)?(\i\c*|\*)))|\.)/)*((((child::)?"
        r"((\i\c*:)?(\i\c*|\*)))|\.)|((attribute::|@)((\i\c*:)?(\i\c*|\*))))"
        r"(\|(\.//)?((((child::)?((\i\c*:)?(\i\c*|\*)))|\.)/)*"
        r"((((child::)?((\i\c*:)?(\i\c*|\*)))|\.)|"
        r"((attribute::|@)((\i\c*:)?(\i\c*|\*)))))*"
    ))


class XsdIdentity(XsdComponent):
    """
    Common class for XSD identity constraints.

    :ivar selector: the XPath selector of the identity constraint.
    :ivar fields: a list containing the XPath field selectors of the identity constraint.
    """
    selector = None
    elements = None  # XSD elements bound by selector (for speed-up and lazy mode)
    fields = ()

    def __init__(self, elem, schema, parent):
        super(XsdIdentity, self).__init__(elem, schema, parent)

    def _parse(self):
        super(XsdIdentity, self)._parse()
        elem = self.elem
        try:
            self.name = get_qname(self.target_namespace, elem.attrib['name'])
        except KeyError:
            self.parse_error("missing required attribute 'name'", elem)
            self.name = None

        for index, child in enumerate(elem):
            if child.tag == XSD_SELECTOR:
                self.selector = XsdSelector(child, self.schema, self)
                break
            elif child.tag != XSD_ANNOTATION:
                self.parse_error("'selector' declaration expected.", elem)
                break
        else:
            self.parse_error("missing 'selector' declaration.", elem)
            index = -1

        self.fields = []
        for child in filter(is_not_xsd_annotation, elem[index + 1:]):
            if child.tag == XSD_FIELD:
                self.fields.append(XsdFieldSelector(child, self.schema, self))
            else:
                self.parse_error("%r is not allowed here" % child, elem)

    def _parse_identity_reference(self):
        super(XsdIdentity, self)._parse()
        self.name = get_qname(self.target_namespace, self.elem.attrib['ref'])
        if 'name' in self.elem.attrib:
            self.parse_error("attributes 'name' and 'ref' are mutually exclusive")
        elif self._parse_child_component(self.elem) is not None:
            self.parse_error("a reference cannot has child definitions")

    def build(self):
        if self.ref is True:
            try:
                ref = self.maps.identities[self.name]
            except KeyError:
                self.parse_error("Unknown identity constraint {!r}".format(self.name))
                return
            else:
                if not isinstance(ref, self.__class__):
                    self.parse_error("attribute 'ref' points to a different kind constraint")
                self.selector = ref.selector
                self.fields = ref.fields
                self.ref = ref

        self.elements = {
            e for e in self.selector.xpath_selector.iter_select(self.parent) if e.name
        }

    @property
    def built(self):
        return self.elements is not None

    def get_fields(self, elem, namespaces=None, decoders=None):
        """
        Get fields for a schema or instance context element.

        :param elem: an Element or an XsdElement
        :param namespaces: is an optional mapping from namespace prefix to URI.
        :param decoders: context schema fields decoders.
        :return: a tuple with field values. An empty field is replaced by `None`.
        """
        fields = []
        for k, field in enumerate(self.fields):
            result = field.xpath_selector.select(elem)
            if not result:
                if decoders is not None and decoders[k] is not None:
                    value = decoders[k].value_constraint
                    if value is not None:
                        if decoders[k].type.root_type.name == XSD_QNAME:
                            value = qname_to_extended(value, namespaces)

                        if isinstance(value, list):
                            fields.append(tuple(value))
                        elif isinstance(value, (bool, float)):
                            fields.append(tuple([value, type(value)]))
                        else:
                            fields.append(value)

                        result.append(value)
                        continue

                if not isinstance(self, XsdKey) or 'ref' in elem.attrib and \
                        self.schema.meta_schema is None and self.schema.XSD_VERSION != '1.0':
                    fields.append(None)
                elif field.target_namespace not in self.maps.namespaces:
                    fields.append(None)
                else:
                    raise XMLSchemaValueError("%r key field must have a value!" % field)

            elif len(result) == 1:
                if decoders is None or decoders[k] is None:
                    fields.append(result[0])
                else:
                    value = decoders[k].data_value(result[0])
                    if decoders[k].type.root_type.name == XSD_QNAME:
                        value = qname_to_extended(value, namespaces)

                    if isinstance(value, list):
                        fields.append(tuple(value))
                    elif isinstance(value, (bool, float)):
                        fields.append(tuple([value, type(value)]))
                    else:
                        fields.append(value)
            else:
                raise XMLSchemaValueError("%r field selects multiple values!" % field)

        return tuple(fields)

    def iter_values(self, elem, namespaces=None):
        """
        Iterate field values, excluding empty values (tuples with all `None` values).

        :param elem: instance XML element.
        :param namespaces: XML document namespaces.
        :return: N-Tuple with value fields.
        """
        current_path = ''
        xsd_fields = None
        for e in self.selector.xpath_selector.iter_select(elem):
            path = etree_getpath(e, elem)
            if current_path != path:
                # Change the XSD context only if the path is changed
                current_path = path
                xsd_element = self.parent.find(path)
                if not hasattr(xsd_element, 'tag'):
                    yield XMLSchemaValidationError(
                        self, e, "{!r} is not an element".format(xsd_element)
                    )
                xsd_fields = self.get_fields(xsd_element)

            if not xsd_fields or all(fld is None for fld in xsd_fields):
                continue

            try:
                fields = self.get_fields(e, namespaces, decoders=xsd_fields)
            except XMLSchemaValueError as err:
                yield XMLSchemaValidationError(self, e, reason=str(err))
            else:
                if any(fld is not None for fld in fields):
                    yield fields

    def get_counter(self, enabled=True):
        return IdentityCounter(self, enabled)


class XsdUnique(XsdIdentity):
    _ADMITTED_TAGS = {XSD_UNIQUE}


class XsdKey(XsdIdentity):
    _ADMITTED_TAGS = {XSD_KEY}


class XsdKeyref(XsdIdentity):
    """
    Implementation of xs:keyref.

    :ivar refer: reference to a *xs:key* declaration that must be in the same element \
    or in a descendant element.
    """
    _ADMITTED_TAGS = {XSD_KEYREF}
    refer = None
    refer_path = '.'

    def _parse(self):
        super(XsdKeyref, self)._parse()
        try:
            self.refer = self.schema.resolve_qname(self.elem.attrib['refer'])
        except (KeyError, ValueError, RuntimeError) as err:
            if 'refer' not in self.elem.attrib:
                self.parse_error("missing required attribute 'refer'")
            else:
                self.parse_error(err)

    def build(self):
        super(XsdKeyref, self).build()

        if isinstance(self.refer, (XsdKey, XsdUnique)):
            return  # referenced key/unique identity constraint already set
        elif isinstance(self.ref, XsdKeyref):
            self.refer = self.ref.refer

        if self.refer is None:
            return  # attribute or key/unique identity constraint missing
        elif isinstance(self.refer, str):
            refer = self.parent.identities.get(self.refer)
            if refer is not None and refer.ref is None:
                self.refer = refer
            else:
                try:
                    self.refer = self.maps.identities[self.refer]
                except KeyError:
                    self.parse_error("key/unique identity constraint %r is missing" % self.refer)
                    return

        if not isinstance(self.refer, (XsdKey, XsdUnique)):
            self.parse_error("reference to a non key/unique identity constraint %r" % self.refer)
        elif len(self.refer.fields) != len(self.fields):
            self.parse_error("field cardinality mismatch between %r and %r" % (self, self.refer))
        elif self.parent is not self.refer.parent:
            refer_path = self.refer.parent.get_path(ancestor=self.parent)
            if refer_path is None:
                # From a note in par. 3.11.5 Part 1 of XSD 1.0 spec: "keyref
                # identity-constraints may be defined on domains distinct from
                # the embedded domain of the identity-constraint they reference,
                # or the domains may be the same but self-embedding at some depth.
                # In either case the node table for the referenced identity-constraint
                # needs to propagate upwards, with conflict resolution."
                refer_path = self.parent.get_path(ancestor=self.refer.parent, reverse=True)
                if refer_path is None:
                    refer_path = self.parent.get_path(reverse=True) + '/' + \
                        self.refer.parent.get_path()

            self.refer_path = refer_path

    @property
    def built(self):
        return self.elements is not None and isinstance(self.refer, XsdIdentity)

    def __call__(self, identities, elem, namespaces=None):
        if self.refer is None:
            return

        values = identities[self].counter
        refer_values = identities[self.refer].counter

        for v in values:
            if v not in refer_values:
                reason = "Value {!r} not found for key {} ({} times)" \
                    .format(v, self.refer.prefixed_name, values[v])
                yield XMLSchemaValidationError(validator=self, obj=elem, reason=reason)

    def get_counter(self, enabled=True):
        return KeyrefCounter(self, enabled)


class Xsd11Unique(XsdUnique):

    def _parse(self):
        if self._parse_reference():
            super(XsdIdentity, self)._parse()
            self.ref = True
        else:
            super(Xsd11Unique, self)._parse()


class Xsd11Key(XsdKey):

    def _parse(self):
        if self._parse_reference():
            super(XsdIdentity, self)._parse()
            self.ref = True
        else:
            super(Xsd11Key, self)._parse()


class Xsd11Keyref(XsdKeyref):

    def _parse(self):
        if self._parse_reference():
            super(XsdIdentity, self)._parse()
            self.ref = True
        else:
            super(Xsd11Keyref, self)._parse()


class IdentityCounter(object):

    def __init__(self, identity, enabled=True):
        self.counter = Counter()
        self.identity = identity
        self.enabled = enabled

    def __repr__(self):
        return "%s(counter=%r)" % (self.__class__.__name__, self.counter)

    def clear(self):
        self.counter.clear()
        self.enabled = True

    def increase(self, fields):
        self.counter[fields] += 1
        if self.counter[fields] == 2:
            msg = "duplicated value {!r} for {!r}"
            raise XMLSchemaValueError(msg.format(fields, self.identity))


class KeyrefCounter(IdentityCounter):

    def increase(self, fields):
        self.counter[fields] += 1

    def iter_errors(self, identities):
        try:
            refer_values = identities[self.identity.refer].counter
        except KeyError:
            if self.identity.refer is not None:
                raise
        else:
            for v in filter(lambda x: x not in refer_values, self.counter):
                if len(v) == 1 and v[0] in refer_values:
                    continue
                elif self.counter[v] > 1:
                    msg = "Value {} not found for {!r} ({} times)"
                    yield XMLSchemaValueError(msg.format(v, self.identity.refer, self.counter[v]))
                else:
                    msg = "Value {} not found for {!r}"
                    yield XMLSchemaValueError(msg.format(v, self.identity.refer))
