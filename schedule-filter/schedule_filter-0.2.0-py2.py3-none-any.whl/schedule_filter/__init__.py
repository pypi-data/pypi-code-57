import datetime
import calendar
import functools


def nth_day_yearly(n, job_func, *args, **kwargs):
    """
    addition to schedule.every().day.do() or
                schedule.every().day.at(time).do()
    with this function, its possible to define
    the day of the year, where the function works

    example:
        schedule.every().day.do(nth_day_yearly(1, job_func)) # do job_func() on first day of the year
        schedule.every().day.do(nth_day_yearly(-1, job_func)) # do job_func() on last day of the year


    :param n: number of day, can be 1 to 365, if leap year 366 or
                                   -1 to -365, if leap year -366
    :param job_func: function
    :param args: list of positional arguments
    :param kwargs: dict of keyworded arguments
    :return: result of job_func(*args, **kwargs)
    """

    year = datetime.datetime.today().year
    days_of_year = 366 if calendar.isleap(year) else 365

    assert n != 0, "The nth day cannot be 0 (Zero)"
    assert n < days_of_year, "The nth day cannot be bigger than 365, if leap year 366"
    assert n > -days_of_year, "The nth day cannot be smaller than -365, if leap year -366"

    day_of_month = datetime.datetime.today().day

    day_of_year = int(datetime.datetime.today().strftime("%j")) # %j = Day number of year 001-366

    if n > 0 and n == day_of_year or \
       n < 0 and days_of_year-n == day_of_year:
        return _execute(job_func, args, kwargs)
    else:
        return  # wrong day


def nth_month_yearly(n, job_func, *args, **kwargs):
    """
    addition to schedule.every().day.do() or
                schedule.every().day.at(time).do()
    with this function, its possible to define
    the month, where the function works

    example:
        schedule.every().monday.do(nth_month_yearly(1, job_func)) # do job_func() on every monday of the month=1 (january)
        schedule.every().day.do(nth_month_yearly(-1, job_func)) # do job_func() on every day of the month=12 (december)


    :param n: number of day, can be 1 to 28 or
                                   -1 to -28
              up to 28, because february, the shortest month, has 28 days
    :param job_func: function
    :param args: list of positional arguments
    :param kwargs: dict of keyworded arguments
    :return: result of job_func(*args, **kwargs)
    """

    assert n != 0, "The nth month cannot be 0 (Zero)"
    assert n < 12, "The nth month cannot be bigger than 12"
    assert n > -12, "The nth month cannot be smaller than -12"

    month = datetime.datetime.today().month

    if n > 0 and n == month or \
       n < 0 and 13-n == month:
        return _execute(job_func, args, kwargs)
    else:
        return  # wrong day


def nth_day_monthly(n, job_func, *args, **kwargs):
    """
    addition to schedule.every().day.do() or
                schedule.every().day.at(time).do()
    with this function, its possible to define
    the day of the month, where the function works

    example:
        schedule.every().day.do(nth_day_monthly(1, job_func)) # do job_func() on first day of the month
        schedule.every().day.do(nth_day_monthly(-1, job_func)) # do job_func() on last day of the month


    :param n: number of day, can be 1 to 28 or
                                   -1 to -28
              up to 28, because february, the shortest month, has 28 days
    :param job_func: function
    :param args: list of positional arguments
    :param kwargs: dict of keyworded arguments
    :return: result of job_func(*args, **kwargs)
    """
    _, num_days_of_month = calendar.monthrange(datetime.datetime.today().year,
                                               datetime.datetime.today().month)

    assert n != 0, "The nth day cannot be 0 (Zero)"
    assert n < 28, f"The nth day cannot be bigger than 28"
    assert n > -28, f"The nth day cannot be smaller than -28"

    day_of_month = datetime.datetime.today().day

    if n > 0 and day_of_month == n or \
       n < 0 and day_of_month+1 == num_days_of_month - n:
        return _execute(job_func, args, kwargs)
    else:
        return  # wrong day


def nth_week_monthly(n, job_func, *args, **kwargs):
    """
    addition to schedule.every().weekday.do() or
                schedule.every().day.at(time).do()
    with this function, its possible to define
    the number of the week, where the function works

    example:
        schedule.every().monday.do(nth_week_monthly(1, job_func)) # do job_func() on first monday of the month
        schedule.every().sunday.do(nth_week_monthly(-1, job_func)) # do job_func() on last sunday of the month


    :param n: number of week, can be 1 to 4 or
                                    -1 to -4
    :param job_func: function
    :param args: list of positional arguments
    :param kwargs: dict of keyworded arguments
    :return: result of job_func(*args, **kwargs)
    """

    assert n != 0, "The nth week cannot be 0 (Zero)"
    assert n < 4, "The nth week cannot be bigger than 4"
    assert n > -4, "The nth week cannot be smaller than -4"

    day_of_month = datetime.datetime.today().day

    if n > 0:
        week_n = lambda n: 7 * n

        if week_n(n - 1) < day_of_month <= week_n(n):
            return _execute(job_func, args, kwargs)
        else:
            return  # wrong week

    elif n < 0:
        _, num_days_of_month = calendar.monthrange(datetime.datetime.today().year,
                                                   datetime.datetime.today().month)

        reverse_week_n = lambda n: num_days_of_month + (n * 7)
        """
        reverse week subtracts n weeks from the numbers of days of a month
        reverse_week_n(0) == num_days_of_month (31, for example)
        reverse_week_n(-1) == num_days_of_month - 7
        reverse_week_n(-2) == num_days_of_month - 14
        """

        if reverse_week_n(n) < day_of_month <= reverse_week_n(n + 1):
            return _execute(job_func, args, kwargs)
        else:
            return  # wrong week


def nth_year_ever(n, job_func, *args, **kwargs):
    if datetime.datetime.today().year == n:
        return _execute(job_func, args, kwargs)


def _execute(job_func, args, kwargs):
    s_job_func = functools.partial(job_func, *args, **kwargs)
    try:
        functools.update_wrapper(s_job_func, job_func)
    except AttributeError:
        # job_funcs already wrapped by functools.partial won't have
        # __name__, __module__ or __doc__ and the update_wrapper()
        # call will fail.
        pass

    return s_job_func()
