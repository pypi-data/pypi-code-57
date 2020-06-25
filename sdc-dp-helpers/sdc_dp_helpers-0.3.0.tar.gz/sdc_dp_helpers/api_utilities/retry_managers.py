"""
    Retry Managers:
        - retry decorators
        - failure mode handlers
"""
import time
from functools import wraps


def retry_handler(exceptions: Exception, total_tries:int = 4, initial_wait: float = 0.5, backoff_factor: int = 2):
    """
        Decorator - managing API failures

        args:
            exceptions (Exception): Exception instance or list of Exception instances to catch & retry
            total_tries (int): Total retry attempts
            initial_wait (float): initial delay between retry attempts in seconds
            backoff_factor (int): multiplier used to further randomize back off
        
        return:
            wrapped function's response
    """
    def retry_decorator(f):
        @wraps(f)
        def func_with_retries(*args, **kwargs):
            """wrapper function to decorate function with retry functionality"""
            _tries, _delay = total_tries, initial_wait
            while _tries > 1:
                try:
                    print(f'Attempt {total_tries + 1 - _tries}')
                    return f(*args, **kwargs)
                except exceptions as e:
                    # get logger message
                    if _tries == 1:
                        msg = str(f'Function: {f.__name__}\n'
                                f'Failed despite best efforts after {total_tries} tries')
                    else:
                        msg = str(f'Function: {f.__name__}\n'
                                    f'Exception {e}.\n'
                                    f'Retrying in {_delay} seconds!')
                    # log with print
                    print(msg)
                    # decrement _tries
                    _tries = _tries -1
                    # pause
                    time.sleep(_delay)
                    # increase delay by backoff factor
                    _delay = _delay * backoff_factor

        return func_with_retries

    return retry_decorator