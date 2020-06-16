import logging
import json

# create logger
logger = logging.getLogger(__name__)


class Sequence():
    """
    Execution Sequence Layer
    The input is a list of function of sequence
    The sequence object can be treat like a normal function

    Example:
    =======
    seq = Sequence([sum, print])
    seq([1, 2])
    """
    def __init__(self, funcs):
        self.funcs = funcs
    
    def __call__(self, *args, **kwargs):
        for func in self.funcs:
            logger.info(f"Executing {func.__name__}")
            logger.debug(f"Executing {func.__name__}( { args, kwargs} )")
            args, kwargs = func(*args, **kwargs)
        return args, kwargs
