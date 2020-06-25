import time
import logging


class Profiler(object):
    """
    A profile which can profile the speed and memory usage
    for each decorated function line by line
    """

    def __init__(self, output=None):
        self.output = output

    def profile_speed(self, func):
        # TODO
        # make it profile line by line
        def wrap(*args, **kwargs):
            started_at = time.time()
            result = func(*args, **kwargs)
            logging.info(time.time() - started_at)
            return result

        return wrap

    def warn_slow(self):
        raise Exception("Not implemented yet")

    def warn_memory(self):
        raise Exception("Not implemented yet")
