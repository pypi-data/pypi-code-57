# --------------------------------------------------------------------------------------
# File: "TimerFunctions.py"
# Dir: "C:\Users\ldsan\Downloads\Github_Projects\SandsPythonFunctions\src\SandsPythonFunctions"
# Created: 2020-05-25
# --------------------------------------------------------------------------------------
"""
this file contains functions related to the timing of functions

TESTCODE: designates code used in testing the script
make sure to comment out that line so that it does not impact the production code
"""


def function_timer(func):
    """This is a timer decorator when defining a function if you want that function to
    be timed then add `@function_timer` before the `def` statement and it'll time the
    function

    Arguments:
        func {function} -- it takes a function for this decorator to work

    Returns:
        this will print out the time taken and the time the function started and
        completed
    """
    from datetime import datetime
    import functools
    import time

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()
        start_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        # print(f"The function {func.__name__} started at {start_date}")
        value = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        stop_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        if elapsed_time > 60:
            print(
                f"The function {func.__name__} took: {round(elapsed_time/60, 3)} minutes at {stop_date}"
            )
        elif elapsed_time > 3600:
            print(
                f"The function {func.__name__} took: {round((elapsed_time/60)/60, 3)} hours at {stop_date}"
            )
        else:
            print(
                f"The function {func.__name__} took: {round(elapsed_time, 3)} seconds"
            )
        return value

    return wrapper_timer
