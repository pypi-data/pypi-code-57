import time

from servicemapper.ioc import Core

current_millisecond_time = lambda: int(round(time.time() * 1000))

def trace(function):
    def inner_function(*args, **kwargs):
        logger = Core.logger()
        logger.debug(f"BEGIN: {function.__name__}")
        begin = current_millisecond_time()
        retval = function(*args, **kwargs)
        end = current_millisecond_time()
        ms = (end - begin)
        logger.debug(f"END: {function.__name__} duration = {ms}ms")
        return retval
    return inner_function
