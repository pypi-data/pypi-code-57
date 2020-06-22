from multiprocessing import Lock
from functools import wraps


class ThreadSafeContainer(object):
    
    '''The fundemantal data container that gurantees threading safety'''
    
    def __init__(self):
        self._thread_lock = None

    def __enter__(self):
        self.set_thread_lock(True)

    def __exit__(self, err_type, val, trace):
        self.set_thread_lock(False)
        if isinstance(val, TypeError):
            return False
        return True

    def __setstate__(self, load):
        self._thread_lock = load['_thread_lock']

    @property
    def ThreadLock(self):
        return self._thread_lock

    @property
    def isLocked(self):
        return self._thread_lock.locked()

    def set_thread_lock(self, mode=True):
        assert mode in (True, False), 'setting `ThreadLock` with True or False'
        if mode is True:
            if self._thread_lock is None:
                self._thread_lock = Lock()
        else:
            with self.ThreadLock:
                self._thread_lock = None

    def has_thread_lock(self):
        return bool(self._thread_lock)
        

def check_thread_locked(func):
    @wraps(func)
    def locked_func(self, *args, **kwrds):
        if self.has_thread_lock():
            with self._thread:
                return func(self, *args, **kwrds)
        return func(self, *args, **kwrds)
    return locked_func
