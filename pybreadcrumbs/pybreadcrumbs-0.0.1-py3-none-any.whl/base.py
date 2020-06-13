"""Base.py."""
import asyncio
import datetime
from functools import wraps
import inspect
import logging
import time
import uuid

import pytz

from .configurations import breadcrumbs_config

logger = logging.getLogger(__name__)

# extract_configuration
ADDITIONAL_BREADCRUMBS_KEYS = breadcrumbs_config.get("additional_keys")
BREADCRUMBS_DATETIME_FORMAT = breadcrumbs_config.get("datetime_format")
BREADCRUMBS_EXTRACTION_FALLBACK_LEVEL = breadcrumbs_config.get("extraction_fallback_level")
BREADCRUMBS_KEY_PREFIX = breadcrumbs_config.get("key_prefix")
BREADCRUMBS_TRACE_ID_PREFIX = breadcrumbs_config.get("trace_id_prefix")
BREADCRUMBS_TZINFO = breadcrumbs_config.get("timezone")

# Base Keys
BREADCRUMBS_TRACE_KEY = "trace"
BREADCRUMBS_TRACE_ID_KEY = "trace_id"
BREADCRUMBS_TRACE_META_KEY = "trace_meta"
BREADCRUMBS_TRACE_TEXT_KEY = "trace_text"
BREADCRUMBS_TRACE_TIMESTAMP_KEY = "trace_timestamp"
BREADCRUMBS_ELASPED_TIME_KEY = "elapsed_time"
BREADCRUMBS_CURRENT_DATETIME_KEY = "current_datetime"
BREADCRUMBS_DECORATOR_INIT_TIME_KEY = "decorator_init_time"
BREADCRUMBS_IS_FUNCTION_CALL_KEY = "is_function_call"

# Prefixed Base Keys
FULL_BREADCRUMBS_TRACE_KEY = "trace"
FULL_BREADCRUMBS_TRACE_ID_KEY = BREADCRUMBS_KEY_PREFIX + "trace_id"
FULL_BREADCRUMBS_TRACE_META_KEY = BREADCRUMBS_KEY_PREFIX + "trace_meta"
FULL_BREADCRUMBS_TRACE_TEXT_KEY = BREADCRUMBS_KEY_PREFIX + "trace_text"
FULL_BREADCRUMBS_TRACE_TIMESTAMP_KEY = BREADCRUMBS_KEY_PREFIX + "trace_timestamp"
FULL_BREADCRUMBS_ELASPED_TIME_KEY = BREADCRUMBS_KEY_PREFIX + "elapsed_time"
FULL_BREADCRUMBS_CURRENT_DATETIME_KEY = BREADCRUMBS_KEY_PREFIX + "current_datetime"
FULL_BREADCRUMBS_DECORATOR_INIT_TIME_KEY = BREADCRUMBS_KEY_PREFIX + "decorator_init_time"
FULL_BREADCRUMBS_IS_FUNCTION_CALL_KEY = BREADCRUMBS_KEY_PREFIX + "is_function_call"

BREADCRUMBS_BOOLEAN_TRUE = "true"
BREADCRUMBS_BOWL_KEY = "breadcrumbs_bowl"
BREADCRUMBS_BOWL_CLASS_NAME = "BreadCrumbBowl"

ARGS_KEY = "args"
KWARGS_KEY = "kwargs"
DICT_CLASS_NAME = "dict"

EXTRACTOR_PIPE = "|"
EXTRACTOR_OPERATOR_KEY = "@"
EXTRACTOR_PARENTHESIS_START = "("
EXTRACTOR_PARENTHESIS_END = ")"

METHOD_INITIALISATION_TEXT = "{0} initialised"
INVALID_EXTRACTOR_KEY_MESSAGE = "Invalid extractor for key `{0}`"

FETCHABLE_BREADCRUMBS_KEYS = {BREADCRUMBS_TRACE_ID_KEY, BREADCRUMBS_TRACE_TEXT_KEY}.union(ADDITIONAL_BREADCRUMBS_KEYS)

BREADCRUMBS_TZ = pytz.timezone(BREADCRUMBS_TZINFO)


class BreadCrumbBowl:
    """BreadCrumbBowlv3.

    A cutom dict like structure for breadcrumbs module.

    NOTE: this data structure is not JSON serializable, always pop this out before sending keyword arguments
    for serialization.
    """
    def __init__(self, **kwargs):
        """Init."""
        self.__data__ = {}
        if BREADCRUMBS_TRACE_ID_KEY in kwargs:
            self.__data__[FULL_BREADCRUMBS_TRACE_ID_KEY] = kwargs.pop(BREADCRUMBS_TRACE_ID_KEY)
        else:
            self.__data__[FULL_BREADCRUMBS_TRACE_ID_KEY] = "{0}{1}".format(
                BREADCRUMBS_TRACE_ID_PREFIX, uuid.uuid4().hex)
        if BREADCRUMBS_TRACE_TIMESTAMP_KEY in kwargs:
            self.trace_timestamp = kwargs.pop(BREADCRUMBS_TRACE_TIMESTAMP_KEY)
        else:
            self.trace_timestamp = time.perf_counter()

        if BREADCRUMBS_TRACE_META_KEY in kwargs:
            self.__data__[FULL_BREADCRUMBS_TRACE_META_KEY] = kwargs.pop(BREADCRUMBS_TRACE_META_KEY)
        else:
            self.__data__[FULL_BREADCRUMBS_TRACE_META_KEY] = dict()

        if BREADCRUMBS_TRACE_TEXT_KEY in kwargs:
            self.__data__[FULL_BREADCRUMBS_TRACE_TEXT_KEY] = kwargs.pop(BREADCRUMBS_TRACE_TEXT_KEY)

        for k, v in kwargs.items():
            self.__setitem__(k, v)

    def __setitem__(self, key, value):
        """__setitem__."""
        if key in ADDITIONAL_BREADCRUMBS_KEYS:
            self.__data__[BREADCRUMBS_KEY_PREFIX + key] = value
        else:
            raise Exception("Unconfigured key `{0}`, assignment allowed for configured keys only".format(key))

    def __getitem__(self, key):
        """__getitem__."""
        try:
            if key == BREADCRUMBS_TRACE_TIMESTAMP_KEY:
                return self.trace_timestamp
            else:
                return self.__data__[BREADCRUMBS_KEY_PREFIX + key]
        except KeyError:
            raise KeyError("{0}".format(key))

    def __contains__(self, key):
        """__contains__."""
        return BREADCRUMBS_KEY_PREFIX + key in self.__data__

    def update_trace_id(self, trace_id=None):
        """update_trace_id."""
        if not trace_id:
            trace_id = "{0}{1}".format(BREADCRUMBS_TRACE_ID_PREFIX, uuid.uuid4().hex)
        self.__data__[FULL_BREADCRUMBS_TRACE_ID_KEY] = trace_id

    def update_trace_timestamp(self, trace_timestamp=None):
        """update_trace_id."""
        if not trace_timestamp:
            trace_timestamp = time.perf_counter()
        self.trace_timestamp = trace_timestamp

    def add_trace_text(self, trace_text):
        """add_trace_text."""
        self.__data__[FULL_BREADCRUMBS_TRACE_TEXT_KEY] = str(trace_text)
        dt_object = datetime.datetime.now(BREADCRUMBS_TZ)
        self.__data__[FULL_BREADCRUMBS_ELASPED_TIME_KEY] = (
            time.perf_counter() - self.trace_timestamp
        )
        self.__data__[FULL_BREADCRUMBS_CURRENT_DATETIME_KEY] = (
            dt_object.strftime(BREADCRUMBS_DATETIME_FORMAT)
        )
        return self.__data__

    def add_trace_meta(self, **kwargs):
        """add_trace_meta."""
        for k, v in kwargs.items():
            self.__data__[FULL_BREADCRUMBS_TRACE_META_KEY][k] = str(v)

    @property
    def log_payload(self):
        """log_payload."""
        dt_object = datetime.datetime.now(BREADCRUMBS_TZ)
        self.__data__[FULL_BREADCRUMBS_ELASPED_TIME_KEY] = (
            time.perf_counter() - self.trace_timestamp
        )
        self.__data__[FULL_BREADCRUMBS_CURRENT_DATETIME_KEY] = (
            dt_object.strftime(BREADCRUMBS_DATETIME_FORMAT)
        )
        return self.__data__

    @property
    def meta(self):
        """meta."""
        return self.__data__[FULL_BREADCRUMBS_TRACE_META_KEY]


class BreadCrumbException(Exception):
    """BreadCrumbException."""

    def __init__(self, error_msg="", *args, **kwargs):
        """Init."""
        self.error_msg = error_msg

    def __str__(self):
        """Str."""
        return repr(self.error_msg)


def _generate_lambda_eval_function(key, func_text):
    return eval("lambda " + key + ": " + func_text)


def add_bowl(*args, **kwargs):
    """add_bowl.

    This is a decorator method which inserts a keyword argument `breadcrumbs_bowl` into the method on which
    it is applied.

    breadcrumbs_bowl : it is a dict which contains basic data of the method that needs to be logged in every
    log call. this payload needs to be passed to any other function call that may happen in the current method.
    If it is not passed , next trace tries to fetch it from stack frames.

    An Initiator trace copies meta, trace_id and action_timestamp from data passed from parent method and copies the
    rest of the keys and stores them into meta after renaming them.
    """
    CURRENT_ADDITIONAL_BREADCRUMBS = {
        i: kwargs.pop(i) for i in ADDITIONAL_BREADCRUMBS_KEYS if i in kwargs
    }
    PREVIOUS_ADDITIONAL_BREADCRUMBS_KEYS = ADDITIONAL_BREADCRUMBS_KEYS.difference(
        CURRENT_ADDITIONAL_BREADCRUMBS.keys())
    DEFAULT_BREADCRUMB_VALUE = kwargs.pop(BREADCRUMBS_TRACE_TEXT_KEY, None)
    BREADCRUMBS_TRACE_META = kwargs

    def inner(func):

        def extract_bowl():
            bowl = None
            if BREADCRUMBS_EXTRACTION_FALLBACK_LEVEL == 0:
                return bowl
            current_level = 1
            current_frame = inspect.currentframe().f_back.f_back
            while current_frame is not None:
                if BREADCRUMBS_BOWL_KEY in current_frame.f_locals:
                    bowl = current_frame.f_locals.get(BREADCRUMBS_BOWL_KEY)
                    break
                elif KWARGS_KEY in current_frame.f_locals:
                    kwargs = current_frame.f_locals.get(KWARGS_KEY)
                    if kwargs.__class__.__name__ == DICT_CLASS_NAME and BREADCRUMBS_BOWL_KEY in kwargs:
                        bowl = kwargs.get(BREADCRUMBS_BOWL_KEY)
                        break
                if current_level >= BREADCRUMBS_EXTRACTION_FALLBACK_LEVEL:
                    break
                current_level += 1
                current_frame = current_frame.f_back
            return bowl

        def get_breadcrumbs_bowl(previous_bowl, decorator_start_time):

            try:
                full_method_name = "{0}.{1}".format(func.__module__, func.__name__)
                BREADCRUMB_VALUE = DEFAULT_BREADCRUMB_VALUE or full_method_name

                if previous_bowl.__class__.__name__ == BREADCRUMBS_BOWL_CLASS_NAME:
                    breadcrumbs_bowl = BreadCrumbBowl(
                        **{
                            BREADCRUMBS_TRACE_TEXT_KEY: BREADCRUMB_VALUE,
                            BREADCRUMBS_TRACE_ID_KEY: previous_bowl[BREADCRUMBS_TRACE_ID_KEY],
                            BREADCRUMBS_TRACE_TIMESTAMP_KEY: previous_bowl[BREADCRUMBS_TRACE_TIMESTAMP_KEY],
                            BREADCRUMBS_TRACE_META_KEY: BREADCRUMBS_TRACE_META,
                            **{i: previous_bowl[i] for i in PREVIOUS_ADDITIONAL_BREADCRUMBS_KEYS if
                                i in previous_bowl},
                            **CURRENT_ADDITIONAL_BREADCRUMBS
                        }
                    )
                else:
                    breadcrumbs_bowl = BreadCrumbBowl(
                        **{
                            BREADCRUMBS_TRACE_TEXT_KEY: BREADCRUMB_VALUE,
                            BREADCRUMBS_TRACE_META_KEY: BREADCRUMBS_TRACE_META,
                            **CURRENT_ADDITIONAL_BREADCRUMBS
                        }
                    )

                log_payload = breadcrumbs_bowl.log_payload
                log_payload[FULL_BREADCRUMBS_DECORATOR_INIT_TIME_KEY] = time.perf_counter() - decorator_start_time
                log_payload[FULL_BREADCRUMBS_IS_FUNCTION_CALL_KEY] = BREADCRUMBS_BOOLEAN_TRUE
                logger.info(METHOD_INITIALISATION_TEXT.format(full_method_name), extra=log_payload)
                log_payload.pop(FULL_BREADCRUMBS_DECORATOR_INIT_TIME_KEY)
                log_payload.pop(FULL_BREADCRUMBS_IS_FUNCTION_CALL_KEY)
            except Exception as e:
                raise BreadCrumbException(error_msg=str(e))

            return breadcrumbs_bowl

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            breadcrumbs_bowl = {}
            decorator_start_time = time.perf_counter()
            previous_bowl = kwargs.pop(BREADCRUMBS_BOWL_KEY, {})
            if not previous_bowl:
                previous_bowl = extract_bowl()
            try:
                breadcrumbs_bowl = get_breadcrumbs_bowl(previous_bowl, decorator_start_time)
            except Exception as e:
                logger.error(e)
                breadcrumbs_bowl = BreadCrumbBowl()

            return func(*args, **kwargs, breadcrumbs_bowl=breadcrumbs_bowl)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            breadcrumbs_bowl = {}
            decorator_start_time = time.perf_counter()
            previous_bowl = kwargs.pop(BREADCRUMBS_BOWL_KEY, {})
            if not previous_bowl:
                previous_bowl = extract_bowl()

            try:
                breadcrumbs_bowl = get_breadcrumbs_bowl(previous_bowl, decorator_start_time)
            except Exception as e:
                logger.error(e)
                breadcrumbs_bowl = BreadCrumbBowl()

            return await func(*args, **kwargs, breadcrumbs_bowl=breadcrumbs_bowl)

        if asyncio.iscoroutinefunction(func) or asyncio.iscoroutine(func) or asyncio.isfuture(func):
            return async_wrapper
        else:
            return sync_wrapper

    return inner


def add_bowlv2(*args, **kwargs):
    """add_bowlv2.

    This is a decorator method which inserts a keyword argument `breadcrumbs_bowl` into the method on which
    it is applied.

    breadcrumbs_bowl : it is a dict which contains basic data of the method that needs to be logged in every
    log call. this payload needs to be passed to any other function call that may happen in the current method.
    If it is not passed , next trace tries to fetch it from stack frames.

    An Initiator trace copies meta, trace_id and action_timestamp from data passed from parent method and copies the
    rest of the keys and stores them into meta after renaming them.
    """
    def process_token(token, key):
        args_token = kwargs_token = cons_token = ""

        if token[0] == EXTRACTOR_PARENTHESIS_START:
            end_parenthesis = token.find(EXTRACTOR_PARENTHESIS_END)
            if end_parenthesis == -1:
                raise BreadCrumbException(error_msg=INVALID_EXTRACTOR_KEY_MESSAGE.format(key))
            args_prefix, kwargs_prefix, cons_prefix = process_token(token[1:end_parenthesis], key)
            suffix = token[end_parenthesis + 1:]
            args_token = args_prefix + suffix
            kwargs_token = kwargs_prefix + suffix
            cons_token = cons_prefix + suffix
        else:
            pipe_operator = token.find(EXTRACTOR_PIPE)
            if pipe_operator == -1:
                if token.startswith(ARGS_KEY):
                    args_token = token
                elif token.startswith(KWARGS_KEY):
                    kwargs_token = token
                else:
                    cons_token = token
            else:
                args_prefix, kwargs_prefix, cons_prefix = process_token(token[:pipe_operator], key)
                args_token = args_token + args_prefix
                kwargs_token = kwargs_token + kwargs_prefix
                cons_token = cons_token + cons_prefix
                args_prefix, kwargs_prefix, cons_prefix = process_token(token[pipe_operator + 1:], key)
                args_token = args_token + args_prefix
                kwargs_token = kwargs_token + kwargs_prefix
                cons_token = cons_token + cons_prefix
        return args_token, kwargs_token, cons_token

    DEFAULT_BREADCRUMB_VALUE = None
    ADDITIONAL_BREADCRUMBS_ARGS_FUNCTIONS = {BREADCRUMBS_TRACE_META_KEY: {}, BREADCRUMBS_TRACE_KEY: {}}
    ADDITIONAL_BREADCRUMBS_KWARGS_FUNCTIONS = {BREADCRUMBS_TRACE_META_KEY: {}, BREADCRUMBS_TRACE_KEY: {}}
    CURRENT_ADDITIONAL_BREADCRUMBS = {BREADCRUMBS_TRACE_META_KEY: {}, BREADCRUMBS_TRACE_KEY: {}}
    CURRENT_ADDITIONAL_BREADCRUMBS_KEYS = set()

    for key, value in kwargs.items():
        if value[0] == EXTRACTOR_OPERATOR_KEY:
            args_fun, kwargs_func, cons_func = process_token(value[1:], key)
            if args_fun:
                if key in FETCHABLE_BREADCRUMBS_KEYS:
                    ADDITIONAL_BREADCRUMBS_ARGS_FUNCTIONS[BREADCRUMBS_TRACE_KEY][key] = (
                        _generate_lambda_eval_function(ARGS_KEY, args_fun)
                    )
                    CURRENT_ADDITIONAL_BREADCRUMBS_KEYS.add(key)
                else:
                    ADDITIONAL_BREADCRUMBS_ARGS_FUNCTIONS[BREADCRUMBS_TRACE_META_KEY][key] = (
                        _generate_lambda_eval_function(ARGS_KEY, args_fun)
                    )
            if kwargs_func:
                if key in FETCHABLE_BREADCRUMBS_KEYS:
                    ADDITIONAL_BREADCRUMBS_KWARGS_FUNCTIONS[BREADCRUMBS_TRACE_KEY][key] = (
                        _generate_lambda_eval_function(KWARGS_KEY, kwargs_func)
                    )
                    CURRENT_ADDITIONAL_BREADCRUMBS_KEYS.add(key)
                else:
                    ADDITIONAL_BREADCRUMBS_KWARGS_FUNCTIONS[BREADCRUMBS_TRACE_META_KEY][key] = (
                        _generate_lambda_eval_function(KWARGS_KEY, kwargs_func)
                    )
        elif key in FETCHABLE_BREADCRUMBS_KEYS:
            CURRENT_ADDITIONAL_BREADCRUMBS[BREADCRUMBS_TRACE_KEY][key] = value
            CURRENT_ADDITIONAL_BREADCRUMBS_KEYS.add(key)
        elif key == BREADCRUMBS_TRACE_TEXT_KEY:
            DEFAULT_BREADCRUMB_VALUE = value
        else:
            CURRENT_ADDITIONAL_BREADCRUMBS[BREADCRUMBS_TRACE_META_KEY][key] = value

    PREVIOUS_ADDITIONAL_BREADCRUMBS_KEYS = ADDITIONAL_BREADCRUMBS_KEYS.difference(
        CURRENT_ADDITIONAL_BREADCRUMBS_KEYS)

    def inner(func):

        def extract_bowl():
            bowl = {}
            if BREADCRUMBS_EXTRACTION_FALLBACK_LEVEL == 0:
                return bowl
            current_level = 1
            current_frame = inspect.currentframe().f_back.f_back
            while current_frame is not None:
                if BREADCRUMBS_BOWL_KEY in current_frame.f_locals:
                    bowl = current_frame.f_locals.get(BREADCRUMBS_BOWL_KEY)
                    break
                elif KWARGS_KEY in current_frame.f_locals:
                    kwargs = current_frame.f_locals.get(KWARGS_KEY)
                    if kwargs.__class__.__name__ == DICT_CLASS_NAME and BREADCRUMBS_BOWL_KEY in kwargs:
                        bowl = kwargs.get(BREADCRUMBS_BOWL_KEY)
                        break
                if current_level >= BREADCRUMBS_EXTRACTION_FALLBACK_LEVEL:
                    break
                current_level += 1
                current_frame = current_frame.f_back
            return bowl

        def get_breadcrumbs_bowl(previous_bowl, decorator_start_time, *args, **kwargs):

            try:
                full_method_name = "{0}.{1}".format(func.__module__, func.__name__)
                BREADCRUMB_VALUE = DEFAULT_BREADCRUMB_VALUE or full_method_name

                for key_type, key_values in ADDITIONAL_BREADCRUMBS_ARGS_FUNCTIONS.items():
                    for key, value in key_values.items():
                        try:
                            CURRENT_ADDITIONAL_BREADCRUMBS[key_type][key] = value(args)
                            ADDITIONAL_BREADCRUMBS_KWARGS_FUNCTIONS[key_type].pop(key, None)
                        except Exception:
                            pass

                for key_type, key_values in ADDITIONAL_BREADCRUMBS_KWARGS_FUNCTIONS.items():
                    for key, value in key_values.items():
                        try:
                            CURRENT_ADDITIONAL_BREADCRUMBS[key_type][key] = value(kwargs)
                        except Exception:
                            pass

                if previous_bowl.__class__.__name__ == BREADCRUMBS_BOWL_CLASS_NAME:
                    BREADCRUMBS_TRACE_TIMESTAMP_VALUE = previous_bowl[BREADCRUMBS_TRACE_TIMESTAMP_KEY]
                    breadcrumbs_bowl = BreadCrumbBowl(
                        **{
                            BREADCRUMBS_TRACE_TEXT_KEY: BREADCRUMB_VALUE,
                            BREADCRUMBS_TRACE_ID_KEY: previous_bowl[BREADCRUMBS_TRACE_ID_KEY],
                            BREADCRUMBS_TRACE_TIMESTAMP_KEY: BREADCRUMBS_TRACE_TIMESTAMP_VALUE,
                            BREADCRUMBS_TRACE_META_KEY: CURRENT_ADDITIONAL_BREADCRUMBS[BREADCRUMBS_TRACE_META_KEY],
                            **{i: previous_bowl[i] for i in PREVIOUS_ADDITIONAL_BREADCRUMBS_KEYS if
                                i in previous_bowl},
                            **CURRENT_ADDITIONAL_BREADCRUMBS[BREADCRUMBS_TRACE_KEY]
                        }
                    )
                else:
                    breadcrumbs_bowl = BreadCrumbBowl(
                        **{
                            BREADCRUMBS_TRACE_TEXT_KEY: BREADCRUMB_VALUE,
                            BREADCRUMBS_TRACE_META_KEY: CURRENT_ADDITIONAL_BREADCRUMBS[BREADCRUMBS_TRACE_META_KEY],
                            **CURRENT_ADDITIONAL_BREADCRUMBS[BREADCRUMBS_TRACE_KEY]
                        }
                    )
                log_payload = breadcrumbs_bowl.log_payload
                log_payload[FULL_BREADCRUMBS_DECORATOR_INIT_TIME_KEY] = time.perf_counter() - decorator_start_time
                log_payload[FULL_BREADCRUMBS_IS_FUNCTION_CALL_KEY] = BREADCRUMBS_BOOLEAN_TRUE
                logger.info(METHOD_INITIALISATION_TEXT.format(full_method_name), extra=log_payload)
                log_payload.pop(FULL_BREADCRUMBS_DECORATOR_INIT_TIME_KEY)
                log_payload.pop(FULL_BREADCRUMBS_IS_FUNCTION_CALL_KEY)
            except Exception as e:
                raise BreadCrumbException(error_msg=str(e))

            return breadcrumbs_bowl

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            breadcrumbs_bowl = {}
            decorator_start_time = time.perf_counter()
            previous_bowl = kwargs.pop(BREADCRUMBS_BOWL_KEY, {})
            if not previous_bowl:
                previous_bowl = extract_bowl()
            try:
                breadcrumbs_bowl = get_breadcrumbs_bowl(previous_bowl, decorator_start_time, *args, **kwargs)
            except Exception as e:
                logger.error(e)
                breadcrumbs_bowl = BreadCrumbBowl()

            return func(*args, **kwargs, breadcrumbs_bowl=breadcrumbs_bowl)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            breadcrumbs_bowl = {}
            decorator_start_time = time.perf_counter()
            previous_bowl = kwargs.pop(BREADCRUMBS_BOWL_KEY, {})
            if not previous_bowl:
                previous_bowl = extract_bowl()

            try:
                breadcrumbs_bowl = get_breadcrumbs_bowl(previous_bowl, decorator_start_time, *args, **kwargs)
            except Exception as e:
                logger.error(e)
                breadcrumbs_bowl = BreadCrumbBowl()

            return await func(*args, **kwargs, breadcrumbs_bowl=breadcrumbs_bowl)

        if asyncio.iscoroutinefunction(func) or asyncio.iscoroutine(func) or asyncio.isfuture(func):
            return async_wrapper
        else:
            return sync_wrapper

    return inner
