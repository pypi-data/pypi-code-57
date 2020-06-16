import json
import logging

logger = logging.getLogger(__name__)

class Function():
    """
    Execution function abstraction
    """
    __name__ = "Function"
    
    def __call__(self, *args, **kwargs):
        raise Exception("Unimplemented exception")
