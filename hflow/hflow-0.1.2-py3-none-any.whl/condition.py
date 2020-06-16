import json
import logging

logger = logging.getLogger(__name__)


class Condition():
    """
    Execution Condition Layer
    """
    def __init__(self, condition_fn, true_fn, false_fn):
        self.__name__ = true_fn.__name__
        self.condition_fn = condition_fn
        self.true_fn = true_fn
        self.false_fn = false_fn
        self.runned_fn = None
    
    def __call__(self, *args, **kwargs):
        satisfy = self.condition_fn(*args, **kwargs)
        logger.info(f"Condition {self.condition_fn.__name__} satisfy: {satisfy}")

        if satisfy:
            logger.info(f"Executing {self.true_fn.__name__}")
            args, kwargs = self.true_fn(*args, **kwargs)
            self.runned_fn = self.true_fn
        elif self.false_fn:
            logger.info(f"Executing {self.false_fn.__name__}")
            args, kwargs = self.false_fn(*args, **kwargs)
            self.runned_fn = self.false_fn
            
        return args, kwargs
