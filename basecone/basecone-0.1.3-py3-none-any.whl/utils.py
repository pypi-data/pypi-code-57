import time

def timeit(method):
    """
    Decorator to log time it took to execute method
    """
    def timed(self, *args, **kwargs):
        ts = time.time()
        result = method(self, *args, **kwargs)
        te = time.time()

        if 'log_time' in kwargs:
            name = kwargs.get('log_name', method.__name__.upper())
            kwargs['log_time'][name] = round((te - ts) * 1000, 2)
        else:
            # print(f">>> method '{self.__class__.__name__}.{method.__name__}{args}' took {round((te - ts) * 1000, 2)} ms to execute\n")
            print(f">>> method '{self.__class__.__name__}.{method.__name__}' took {round((te - ts) * 1000, 2)} ms to execute\n")
        return result

    return timed