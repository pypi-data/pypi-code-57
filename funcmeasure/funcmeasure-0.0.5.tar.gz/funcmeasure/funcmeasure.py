# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Callable, Union, Tuple, Dict, Optional
import time

# Local
from .measurement import Measurement

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def measure(
    funcs: Union[List[Union[Callable, Tuple[Callable, str]]], Dict[Callable, Optional[str]]],
    times: int = 1000,
    print_benchmark: bool = True
) -> List[Measurement]:
    """Measure and compare execution times of functions

    Args:
        funcs (Union[List[Union[Callable, Tuple[Callable, str]]], Dict[Callable, Optional[str]]]):
            The functions that will be measured.
            This can be a list or a dictionary.
            If dictionary is passed, the name of the function will be 
                overwritten with the name of the specified value.
            If a list is passed, the values can be either a Callable
                or a Tuple of Callable and string(custom function name)

            Example values:
                - List: [f1, (f2, 'second'), f3]
                - Dict: {
                      f1: 'first',
                      f2: 'second',
                      f3: None
                  }

    Kwargs:
        times (int, optional): How many times will each function be measured. Defaults to 1000.

        print_benchmark (bool, optional): Print results or no. Defaults to True.

    Returns:
        List[Measurement]: List of Measurement objects
    """
    measurements = []

    if isinstance(funcs, list):
        _funcs = {}

        for func in funcs:
            if isinstance(func, tuple):
                _funcs[func[0]] = func[1]
            else:
                _funcs[func] = func.__name__
        
        funcs = _funcs

    for func, func_name in funcs.items():
        total_duration = 0

        for _ in range(0, times):
            start = time.time()
            func()
            total_duration += time.time() - start

        measurements.append(
            Measurement(
                func_name or func.__name__,
                total_duration,
                times
            )
        )

    measurements = sorted(measurements, key=lambda k: k.avg_duration)

    if print_benchmark:
        __print(measurements, times)

    return measurements

def partial(func: Callable, *args, **kwargs):
    from functools import partial as _partial

    return _partial(func, *args, **kwargs)


# ----------------------------------------------------------- Private methods ------------------------------------------------------------ #

def __print(measurements: List[Measurement], times: int) -> None:
    fastest = measurements[0].avg_duration

    val_table_on_columns = [
        ['rank'],
        ['name'],
        ['duration'],
        ['benchmark']
    ]

    rank=0
    for measurement in measurements:
        rank+=1
        val_table_on_columns[0].append(str(rank))
        val_table_on_columns[1].append(measurement.func_name)

        val_table_on_columns[2].append("%.8f" % measurement.avg_duration + 's')

        multi = measurement.avg_duration / fastest
        multi_str = "%.2f" % multi + 'x'

        if multi == 1:
            multi_str = ''
        elif multi == int(multi):
            multi_str = "%.0f" % multi + 'x'
        
        val_table_on_columns[3].append(multi_str)
    
    longest_lens = []

    for column_vals in val_table_on_columns:
        longest_len = 0

        for val in column_vals:
            val_len =len(val)

            if val_len > longest_len:
                longest_len = val_len

        longest_lens.append(longest_len)

    val_table_on_rows = []
    for _ in range(0, len(val_table_on_columns[0])):
        val_table_on_rows.append([])

    for i in range(0, len(val_table_on_columns)):
        longest_len = longest_lens[i]
        column_vals = val_table_on_columns[i]

        for j in range(0, len(column_vals)):
            column_val = column_vals[j]

            val_table_on_rows[j].append(
                __fixed_len_str(
                    column_val,
                    longest_len,
                    filling_char = ' ',
                    center = j == 0
                )
            )

    header = __line(val_table_on_rows[0])
    divider = '-' * len(header)

    print('\nRan', times, 'times\n')
    print(divider)
    print(header)
    print(divider)

    for i in range(1, len(val_table_on_rows)):
        print(__line(val_table_on_rows[i]))

    print(divider)

def __line(elements: List[str], divider_char: str = '|') -> str:
    return divider_char + ' ' + (' ' + divider_char + ' ').join(elements) + ' ' + divider_char

def __fixed_len_str(
    string: str,
    preferred_length: int = 8,
    filling_char: str = ' ',
    center: bool = False
) -> str:
    last_side = 0

    while len(string) < preferred_length:
        if center:
            if last_side == 0:
                last_side = 1
                string = filling_char + string
            else:
                last_side = 0
                string += filling_char
        else:
            string = filling_char + string
    
    if len(string) > preferred_length:
        string = string[:preferred_length-1] + '.'
    
    return string


# ---------------------------------------------------------------------------------------------------------------------------------------- #