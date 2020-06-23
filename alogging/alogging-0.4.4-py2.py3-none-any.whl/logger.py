
import functools
import inspect
import logging
import os
import sys

from alogging.pp import pf
from alogging.echo import echo_format
# import prettyprinter

HAS_COLOR_BUCKET = False
try:
    # https://github.com/alikins/color_bucket_logger
    import color_bucket_logger
    HAS_COLOR_BUCKET = True
except ImportError:
    pass

# set to True if on py3 and you want stack_info log record populated
# WARNING: STACK_INFO=True is not compatible with py2 and will break
STACK_INFO = False

DEFAULT_FMT_STRING = """%(asctime)s %(relativeCreated)d %(levelname)-0.1s %(name)s %(process)d %(funcName)s:%(lineno)d - %(message)s"""

# for use with datefmt="%H:%M:%S" if you still want the ',123' msec info
NO_DATE_FMT_STRING = """%(asctime)s,%(msecs)03d %(levelname)-0.1s %(name)s %(processName)s:%(process)d %(funcName)s:%(lineno)d - %(message)s"""
STACK_INFO_FMT_STRING = """ %(stack_info)s"""

COLON_FMT_STRING = '%(asctime)s processName:%(processName)s process:%(process)d threadName ' + \
    '%(threadName)-2s level: %(levelname)s module: %(module)s name: %(name)s ' + \
    'funcName: %(funcName)s lineno: %(lineno)d %(message)s'

EVERYTHING_FMT_STRING = '%(asctime)s %(levelname)-0.1s %(levelno)-0.1d %(processName)-0.1s ' + \
    '%(process)d %(threadName)s %(thread)d %(name)s %(module)s %(filename)s %(funcName)s %(lineno)d - %(message)s'

DEFAULT_FILE_FMT_STRING = DEFAULT_FMT_STRING
DEFAULT_STREAM_FMT_STRING = NO_DATE_FMT_STRING
DEFAULT_FILE_DATEFMT_STRING = DEFAULT_STREAM_DATEFMT_STRING = DEFAULT_DATEFMT_STRING = None

# TODO: add a stack depth indicator filter?
#       filter would expect 'extra' to have a 'stack_depth' int attribute
#       The filter would replace value of 'stack_depth' with a string that
#       is basically '.' * stack_depth.
#       That adds a visual indicator to log lines about the stack depth

# TODO: method for setting a logger level by env var
# loglevel.ansible.inventory.manager.Manager=DEBUG ansible-playbook -v


def env_var(var_name):
    '''See if 'Var_Name', 'VAR_NAME', or 'var_name' is an enviroment variable'''

    # be liberal in log env var name cap
    for env_var_candidates in (var_name, var_name.upper(), var_name.lower()):
        # print(env_var_candidates)
        env_var_value = os.environ.get(var_name, None)
        if env_var_value is not None:
            continue

    # print('%s=%s' % (var_name, env_var_value))

    if not env_var_value:
        return None

    env_var_value = env_var_value.strip()

    return env_var_value


def env_log_level(var_name):
    env_var_value = env_var(var_name)

    if env_var_value is None:
        return None

    log_level = getattr(logging, env_var_value, env_var_value)

    try:
        log_level = int(log_level)
    except ValueError:
        raise Exception('the log level %s is not known' % env_var_value)

    return log_level


def get_logger_name(depth=None):
    depth = depth or 1
    called_from = inspect.stack()[depth]
    called_from_module = inspect.getmodule(called_from[0])
    return called_from_module.__name__


def get_class_logger_name(obj, depth=None):
    '''Use to get a logger name equiv to module.Class'''
    depth = depth or 1
    # pprint.pprint(inspect.stack())
    called_from = inspect.stack()[depth]
    called_from_module = inspect.getmodule(called_from[0])
    called_from_module_name = called_from_module.__name__
    # if obj has a name, use it, else check it's class name
    # This supports being pass a cls like in a meta class __new__ or a classmethor
    #  of being passed self as used in a class init
    obj_name = getattr(obj, '__name__', obj.__class__.__name__)
    return '%s.%s' % (called_from_module_name, obj_name)


# dont really need this, a log record has funcName
def get_method_logger_name(depth=None):
    depth = depth or 1
    called_from = inspect.stack()[depth]
    called_from_method = called_from[3]
    # called_from_module = inspect.getmodule(called_from[0])
    return called_from_method


def get_logger(name=None, depth=2):
    '''Use to get a logger with name of callers __name__

    Can be used in place of:

        import logging
        log = logging.getLogger(__name__)

    That can be replaced with

        import alogging
        log = alogging.get_logger()

    Args:
        name (str): Optional logger name to use to override the
            default one chosen automatically.
        depth (int): Optional depth of stack to influence where
            get_logger looks to automatically choose a logger name.
            Default is 2.

    Returns:
        logging.Logger: A logger
    '''
    name = name or get_logger_name(depth=depth)

    # TODO: if we want to setup filters on each logger created,
    #       we could do it here.
    #       Or, set a default level/prop/.
    #       Or just returning a custom logging.Logger subclass.
    return logging.getLogger(name)


def get_class_logger(obj, depth=2):
    '''Use to get a logger with name equiv to module.Class

    in a regular class __init__, use like:

        self.log = alogging.get_class_logger(self)


    In a metaclass __new__, use like:

        log = alogging.get_class_logger(cls)
    '''

    return logging.getLogger(get_class_logger_name(obj, depth=depth))


def get_method_logger(depth=2):
    return logging.getLogger(get_method_logger_name(depth=depth))


def a(*args):
    '''
    Log the args of 'a' and returns the args.

    Basically, log info about whatever it wraps, but returns it so
    it can continue to be callled.

    Args:
       args (tuple): The args to pass through to whatever is wrapped

    Returns: (tuple): The args that were passed in.
    '''
    log_name = get_logger_name(depth=2)
    log = logging.getLogger(log_name)
    if STACK_INFO:
        log._log(logging.DEBUG, 'd args=%s', repr(args), stack_info=True)
    else:
        log._log(logging.DEBUG, 'd args=%s echo_format:%s', (repr(args), echo_format(args[0])))

    # walk up the stack to find the first named logger?
    return args and args[0]


def t(func):
    '''Decorate a callable (class or method) and log it's args and return values

    The loggers created and used should reflect where the object is defined/used.

    ie, 'mycode.utils.math.Summer.total' for calling 'total' method on an instance of mycode.utils.math.Summer
    '''
    log_name = get_method_logger_name(depth=2)
    # _log = logging.getLogger(log_name)
    # log.debug('log_name=%s', log_name)
    # mlog.debug('depth0=%s depth1=%s', get_method_logger_name(depth=0), get_method_logger_name(depth=1))
    log_name1 = get_logger_name(depth=2)
    # _log1 = logging.getLogger(log_name1)
    # log1.debug('log_name_1=%s', log_name1)

    # log_name = get_class_logger_name(func, depth=2)
    # log_name = get_class_logger_name(func, depth=2)
    # log = logging.getLogger(log_name)
    # log.debug('cccccccc, log_name=%s', log_name)

    # log2_name = '%s.%s' % (log_name1, log_name)
    # log.debug('log2_name: %s', log2_name)

    # log2 = logging.getLogger(log2_name)
    # log2.debug('xxxxxxxxxxxxxxxx, log2=%s, log2_name=%s', log2, log2_name)

    # log_name = get_logger_name(depth=2)
    # log_name = get_logger_name(depth=1)
    def wrapper(*args, **kwargs):
        # log_name = get_method_logger_name(depth=1)
        # print(get_logger_name())
        # print(get_logger_name(depth=2))
        # print('ga: %s' % getattr(wrapper, "__name__", None))
        qual_name = getattr(func, "__qualname__", None)
        func_name = qual_name or func.__name__
        # full_func_name = getattr(func, "__qualname__", '%s.%s' % (log_name, func.__name__))
        full_func_name = func_name or '%s.%s' % (log_name, func.__name__)

        log = logging.getLogger(log_name)
        # log.debug('-- log_name=%s, log_name1=%s, log2_name=%s, qual_name=%s, func_name=%s, full_func_name=%s',
        #          log_name, log_name1, log2_name, qual_name, func_name, full_func_name)

        log4_name = '%s.%s.%s' % (log_name1, log_name, func.__name__)
        _log4 = get_logger(log4_name)

        _log4.debug('%s() called with args: %s, kwargs: %s', full_func_name, pf(args), pf(kwargs))
        # _log4.debug('%s called with kwargs: %s', full_func_name, pf(kwargs))
        # _log4.debug('%s(%s, %s)', full_func_name,
        #            ', '.join([arg for arg in args if not isinstance(arg, func.__class__)]),
        #            ', '.join(['%s=%s' % (x, y) for x, y in kwargs.items()]))
        # log4.debug('log4=%s', log4_name)
        # log.debug('t locals()=%s args=%s kwargs=%s', repr(locals()), repr(args), repr(kwargs))

        # _log4.debug('t locals()=%s args=%s kwargs=%s', pf(locals()), pf(args), pf(kwargs))

        # _log2 = get_class_logger(func, depth=1)
        # log2.debug('wrapper? %s', func_name)

        # _log3 = get_logger(func_name)
        # log3.debug('log_name=%s, log_name1=%s, log2_name=%s, logfunc_name=%s', log_name, log_name1, log2_name, func_name)

        try:
            ret = func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            raise

        # _log.debug('t_log ret=%s', repr(ret))
        # _log1.debug('t_log1 ret=%s', repr(ret))
        # _log2.debug('t_log2 ret=%s', repr(ret))
        # _log3.debug('t_log3 ret=%s', repr(ret))
        _log4.debug('%s() returned: %s', full_func_name, repr(ret))

        return ret

    return functools.update_wrapper(wrapper, func)


# TODO: replace with loading a logging dict config from yaml config file
def setup(name=None, stream_handler=None,
          file_handler=None, use_root_logger=False):

    #    if name is None:
    #        name = 'alogging'

    log_level = env_log_level('%s_log_level' % name) or logging.DEBUG

    use_multiprocessing = False

    log = logging.getLogger(name)

    log.setLevel(log_level)

    handlers = []

    if file_handler:
        # log_file = log_file or os.path.expanduser('~/.alogging.log')
        file_handler.setLevel(log_level)
        handlers.append(file_handler)

    if stream_handler:
        stream_handler.setLevel(log_level)
        handlers.append(stream_handler)

    if not handlers:
        handlers = [logging.NullHandler()]

    # If 'name' is not provided, the default logger name with be '', ie, the root
    # logger. And the handlers will be attached to the root logger.
    #
    # If a 'name' is provided, then by default, the handlers will be attached to
    # that logger by default. If 'use_root_logger' True, then handlers are added
    # to root logger instead.
    if use_root_logger:
        setup_root_logger(root_level=logging.DEBUG, handlers=handlers)
    else:
        for handler in handlers:
            log.addHandler(handler)

    if use_multiprocessing:
        import multiprocessing
        mp_log = multiprocessing.get_logger()
        mp_log.setLevel(multiprocessing.SUBDEBUG)
        if stream_handler:
            stream_handler.setLevel(multiprocessing.SUBDEBUG)
            mp_log.addHandler(stream_handler)

    # import logging_tree
    # logging_tree.printout()

    return log


def setup_root_logger(root_level=None, handlers=None):
    # if not handlers:
    #    handlers = [logging.NullHandler()]

    root_log_level = root_level or env_log_level('ROOT_LOG_LEVEL') or logging.INFO

    root_logger = logging.getLogger()
    root_logger.setLevel(root_log_level)

    for handler in handlers:
        root_logger.addHandler(handler)


def get_stream_handler(name=None):

    # stream_fmt_string = """%(asctime)s %(name)s %(process)d %(funcName)s:%(lineno)d - %(message)s"""
    # stream_fmt_string = DEFAULT_STREAM_FMT_STRING
    stream_fmt_string = os.environ.get('%s_fmt_string' % name, None) or DEFAULT_STREAM_FMT_STRING
    # default_fmt_string = stream_fmt_string
    stream_datefmt_string = os.environ.get('%s_datefmt_string' % name, None) or DEFAULT_STREAM_DATEFMT_STRING
    stream_datefmt_string = "%H:%M:%S"
    stack_info = os.environ.get('ALOGGING_STACK_INFO', None) or STACK_INFO
    if stack_info:
        stream_fmt_string += STACK_INFO_FMT_STRING

    if HAS_COLOR_BUCKET:
        color_groups = [
            ('funcName', ['funcName', 'lineno']),
            ('levelname', ['levelno']),
            ('name', ['stack_info']),
            # ('name', ['filename', 'module',  'pathname']),
            ('process', ['processName'])
        ]
        stream_formatter = color_bucket_logger.color_debug.ColorFormatter(fmt=stream_fmt_string,
                                                                          default_color_by_attr='name',
                                                                          # default_color_by_attr='process',
                                                                          auto_color=True,
                                                                          color_groups=color_groups,
                                                                          datefmt=stream_datefmt_string)
    else:
        stream_formatter = logging.Formatter(fmt=stream_fmt_string,
                                             datefmt=stream_datefmt_string)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)

    return stream_handler


def get_file_handler(name):
    fmt_string = os.environ.get('%s_fmt_string' % name, None) or DEFAULT_FILE_FMT_STRING

    log_file = env_var('%s_log_file' % name) or env_var('alogging_log_file')

    if log_file is None:
        return None

    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter(fmt=fmt_string)
    file_handler.setFormatter(file_formatter)

    return file_handler


def app_setup(name=None):
    '''Call this to setup a default logging setup in a script or apps __main__

    This will create a root logger with some default handlers, as well as a logger
    for 'name' if provided.

    Args:
        name: (str): If provided, create a logging.Logger with this name

    '''
    stream_handler = get_stream_handler(name=name)

    file_handler = get_file_handler(name=name)

    return setup(name=name,
                 stream_handler=stream_handler,
                 file_handler=file_handler,
                 use_root_logger=True)


def module_setup(name=None, use_root_logger=False):
    '''Call this to setup a default log setup from a library or module.

    ie, where the app itself may be setting up handlers, root logger, etc'''
    stream_handler = get_stream_handler(name=name)

    file_handler = get_file_handler(name=name)

    return setup(name=name,
                 stream_handler=stream_handler,
                 file_handler=file_handler,
                 use_root_logger=use_root_logger)


# From https://stackoverflow.com/a/47956089
def get_stack_size():
    """Get stack size for caller's frame.
    """

    # %timeit len(inspect.stack())
    # 8.86 ms +/- 42.5 us per loop (mean +/- std. dev. of 7 runs, 100 loops each)
    # %timeit get_stack_size()
    # 4.17 us +/- 11.5 ns per loop (mean +/- std. dev. of 7 runs, 100000 loops each)

    size = 2  # current frame and caller's frame always exist
    while True:
        try:
            sys._getframe(size)
            size += 1
        except ValueError:
            return size - 1  # subtract current frame
