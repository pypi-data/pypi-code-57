# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Various utils
"""
import datetime
import json
import sys
import types
from collections import deque
from inspect import isclass
from itertools import islice
from logging import getLogger
from operator import methodcaller

from ._vendors.ipaddress import (  # type: ignore
    ip_address as _ip_address,
    ip_network as _ip_network,
)

if sys.version_info >= (3, 5):
    from typing import (
        Any,
        Callable,
        Dict,
        Iterable,
        List,
        Mapping,
        Optional,
        Set,
        Tuple,
    )

    HAS_TYPING = True

    ConvertFunc = Callable[[Any], Optional[str]]

else:
    from collections import Iterable, Mapping

    HAS_TYPING = False

LOGGER = getLogger(__name__)

HAS_ASYNCIO = sys.version_info >= (3, 4)

NONE_TYPE = type(None)

ZERO_TD = datetime.timedelta(0)

if sys.version_info[0] < 3:
    ALL_STRING_CLASS = basestring  # noqa
    STRING_CLASS = str
    UNICODE_CLASS = unicode  # noqa

    def iterkeys(d, **kwargs):
        return d.iterkeys(**kwargs)

    def itervalues(d, **kwargs):
        return d.itervalues(**kwargs)

    def create_bound_method(func, obj):
        return types.MethodType(func, obj, obj.__class__)

    class UTCTZ(datetime.tzinfo):
        """Basic UTC timezone"""

        def utcoffset(self, dt):
            return ZERO_TD

        def tzname(self, dt):
            return "UTC"

        def dst(self, dt):
            return ZERO_TD

    UTC = UTCTZ()

else:
    ALL_STRING_CLASS = str
    STRING_CLASS = str
    UNICODE_CLASS = str

    def iterkeys(d, **kwargs):
        return d.keys(**kwargs)

    def itervalues(d, **kwargs):
        return d.values(**kwargs)

    create_bound_method = types.MethodType

    UTC = datetime.timezone.utc


def is_string(value):  # type: (Any) -> bool
    """ Check if a value is a valid string, compatible with python 2 and python 3

    >>> is_string('foo')
    True
    >>> is_string(u'✌')
    True
    >>> is_string(42)
    False
    >>> is_string(('abc',))
    False
    """
    return isinstance(value, ALL_STRING_CLASS)


def is_unicode(value):  # type: (Any) -> bool
    """ Check if a value is a valid unicode string, compatible with python 2 and python 3

    >>> is_unicode(u'foo')
    True
    >>> is_unicode(u'✌')
    True
    >>> is_unicode(b'foo')
    False
    >>> is_unicode(42)
    False
    >>> is_unicode(('abc',))
    False
    """
    return isinstance(value, UNICODE_CLASS)


def to_latin_1(value):  # type: (str) -> bytes
    """ Return the input string encoded in latin1 with replace mode for errors
    """
    return value.encode("latin-1", "replace")


def is_json_serializable(value):  # type: (Any) -> bool
    """ Check that a single value is json serializable
    """
    return isinstance(value, (ALL_STRING_CLASS, NONE_TYPE, bool, int, float))  # type: ignore


def to_unicode_safe(value):  # type: (Any) -> Optional[str]
    """ Safely convert a value to a unicode string.
    """
    if value is None:
        return value
    # If value is a byte string (string without encoding)
    # Try to decode it as unicode, this operation will
    # always succeed because non UTF-8 characters will
    # get replaced by the UTF-8 replacement character.
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    # If the value is not already a unicode string
    # Try to convert it to a string
    # by calling the standard Python __str__ method on
    # the value.
    elif not is_unicode(value):
        value = STRING_CLASS(value)
        # In Python 2.7, the returned value has no encoding
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
    # Value is already a unicode string
    return value


###
# Raven configuration
###


def _raven_ignoring_handler(logger, *args, **kwargs):
    """ Ignore all logging messages from sqreen.* loggers, effectively
    disabling raven to log sqreen log messages as breadcrumbs
    """
    try:
        if logger.name.startswith("sqreen"):
            return True
    except Exception:
        LOGGER.warning("Error in raven ignore handler", exc_info=True)


def configure_raven_breadcrumbs():
    """ Configure raven breadcrumbs logging integration if raven is present
    """
    try:
        from raven import breadcrumbs  # type: ignore
    except ImportError:
        return

    # Register our logging handler to stop logging sqreen log messages
    # as breadcrumbs
    try:
        breadcrumbs.register_logging_handler(_raven_ignoring_handler)
    except Exception:
        LOGGER.warning("Error while configuring breadcrumbs", exc_info=True)


###
# NewRelics
###

def configure_newrelics_ignore_exception():
    """ Check if newrelics package is here, and disable Sqreen Exception
    """

    try:
        import newrelic.agent  # type: ignore
    except ImportError:
        return

    try:
        newrelic.agent.global_settings().error_collector.ignore_errors.extend(['sqreen.exceptions:RequestBlocked',
                                                                               'sqreen.exceptions:AttackBlocked',
                                                                               'sqreen.exceptions:ActionBlock',
                                                                               'sqreen.exceptions:ActionRedirect'])
    except Exception:
        LOGGER.warning("Error while configuring newrelics", exc_info=True)


###
# JSON Encoder
###


def qualified_class_name(obj):  # type: (Any) -> str
    """ Return the full qualified name of the class name of obj in form of
    `full_qualified_module.class_name`
    """
    if isclass(obj):
        instance_class = obj
    else:
        instance_class = obj.__class__

    return ".".join([instance_class.__module__, instance_class.__name__])


def django_user_conversion(obj):  # type: (Any) -> Optional[str]
    """ Convert a Django user either by returning USERNAME_FIELD or convert
    it to str.
    """
    if hasattr(obj, "USERNAME_FIELD"):
        return to_unicode_safe(getattr(obj, getattr(obj, "USERNAME_FIELD"), None))
    else:
        return UNICODE_CLASS(obj)


def psycopg_composable_conversion(obj, max_depth=64):  # type: (Any, int) -> str
    """ Best effort psycopg2 Composable string convertion.
    """
    if max_depth == 0:
        raise ValueError("Max depth reached while converting a psycopg2.sql.Composable")
    if hasattr(obj, "strings"):  # psycopg2.sql.Identifier
        # escaping is explained on https://www.postgresql.org/docs/current/sql-syntax-lexical.html#
        return ".".join(json.dumps(i).replace('\\"', '""') for i in obj.strings if isinstance(i, str))
    if hasattr(obj, "wrapped"):  # psycopg2.sql.Literal
        if isinstance(obj.wrapped, str):
            return "'{}'".format(obj.wrapped.replace("'", "''"))
        return repr(obj.wrapped)
    elif hasattr(obj, "__iter__"):  # psycopg2.sql.Composed
        return "".join(psycopg_composable_conversion(i, max_depth=max_depth - 1) for i in obj)
    return obj.as_string(None)


OBJECT_STRING_MAPPING = {
    "bson.objectid.ObjectId": UNICODE_CLASS,
    # Convert datetime to isoformat, compatible with Node Date()
    "datetime.datetime": methodcaller("isoformat"),
    "django.contrib.auth.models.AbstractUser": django_user_conversion,
    "os.PathLike": methodcaller("__fspath__"),
    "pathlib.PurePath": UNICODE_CLASS,
    "psycopg2.sql.Composable": psycopg_composable_conversion,
    "sqlalchemy.sql.elements.ClauseElement": UNICODE_CLASS,
    "sqreen._vendors.ipaddress.IPv4Address": UNICODE_CLASS,
    "sqreen._vendors.ipaddress.IPv6Address": UNICODE_CLASS,
}  # type: Dict[str, ConvertFunc]


def convert_to_string(obj, object_string_mapping=OBJECT_STRING_MAPPING):
    # type: (Any, Mapping[str, ConvertFunc]) -> Optional[str]
    """ Return a string representation for objects that are known to safely convert to string.
    """
    if type(obj) == type:
        instance_class = obj
    else:
        instance_class = obj.__class__

    # Manually do isinstance without needed to have a reference to the class
    for klass in instance_class.__mro__:
        qualified_name = qualified_class_name(klass)
        func = object_string_mapping.get(qualified_name)
        if func is not None:
            try:
                return func(obj)
            except Exception:
                LOGGER.warning("Error converting an instance of type %r", obj.__class__, exc_info=True)
    raise ValueError("cannot convert safely {} to string".format(instance_class))


class CustomJSONEncoder(json.JSONEncoder):
    MAPPING = OBJECT_STRING_MAPPING

    def default(self, obj):  # type: (Any) -> Optional[str]
        """ Return the repr of unkown objects
        """
        try:
            return convert_to_string(obj, object_string_mapping=self.MAPPING)
        except ValueError:
            # If we don't, or if we except, fallback on repr
            return repr(obj)


def ip_address(address):
    return _ip_address(UNICODE_CLASS(address))


def ip_network(address, strict=True):
    return _ip_network(UNICODE_CLASS(address), strict=strict)


def truncate_time(dt=None, round_to=60):  # type: (Optional[datetime.datetime], int) -> datetime.datetime
    """Return a datetime rounded to the previous given second interval."""
    if dt is None:
        dt = now()
    dt = dt.replace(microsecond=0)
    if dt.tzinfo is None:
        naive_dt = dt
    else:
        offset = dt.utcoffset()
        if offset is None:
            offset = ZERO_TD
        naive_dt = dt.replace(tzinfo=None) - offset
    seconds = (naive_dt - naive_dt.min).total_seconds()
    return dt - datetime.timedelta(seconds=seconds % round_to)


def flatten(iterable, max_iterations=1000):
    # type: (Iterable, int) -> Tuple[List, List]
    """Return the list of keys and values of iterable and nested iterables."""
    iteration = 0
    keys = []  # type: List[Any]
    values = []  # type: List[Any]
    remaining_iterables = deque([iterable], maxlen=max_iterations)
    seen_iterables = set()  # type: Set[int]

    while remaining_iterables:

        iteration += 1
        # If we have a very big or nested iterable, returns False.
        if iteration >= max_iterations:
            break

        iterable = remaining_iterables.popleft()
        id_iterable = id(iterable)
        # Protection against recursive objects
        if id_iterable in seen_iterables:
            continue
        seen_iterables.add(id_iterable)

        # If we get an iterable, add it to the list of remaining iterables.
        if isinstance(iterable, Mapping):
            keys.extend(islice(iterkeys(iterable), max_iterations))
            remaining_iterables.extend(islice(itervalues(iterable), max_iterations))
        elif isinstance(iterable, (list, tuple)):
            remaining_iterables.extend(islice(iter(iterable), max_iterations))
        else:
            values.append(iterable)

    return keys, values


def naive_dt_to_utc(dt):  # type: (datetime.datetime) -> datetime.datetime
    """Convert naive datetime to timezone aware datetime.
    By default, we consider all naive datetime to be in UTC.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


def now():  # type: () -> datetime.datetime
    """ Return the current UTC time.
    """
    return datetime.datetime.now(UTC)
