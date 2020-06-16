import re
from typing import List, Union, Callable, Any

def value_set(values):
    return lambda value: value in values

def matches(pattern: str):
    regex = re.compile(pattern)
    return lambda value: regex.fullmatch(value) is not None

def min_length(min_length: int):
    return lambda value: len(value) >= min_length

def max_length(max_length: int):
    return lambda value: len(value) <= max_length

def multiple_of(multiple_of: Union[int, float]):
    return lambda value: value % multiple_of == 0

def minimum(minimum: Union[int, float], exclusive_minimum: bool):
    if exclusive_minimum:
        return lambda value: value > minimum
    else:
        return lambda value: value >= minimum

def maximum(maximum: Union[int, float], exclusive_maximum: bool):
    if exclusive_maximum:
        return lambda value: value < maximum
    else:
        return lambda value: value <= maximum

def listitem_validator(*validators: Callable[[Any], bool]):
    return lambda value: all([
            all([validator(item) for validator in validators]) 
            for item in value
        ])

def min_items(min_items: int):
    return min_length(min_items)

def max_items(max_items: int):
    return max_length(max_items)

def unique_items():
    return lambda value: len(set(value)) == len(value)
