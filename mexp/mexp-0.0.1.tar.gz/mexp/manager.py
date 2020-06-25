from pathlib import Path
from operator import attrgetter

def find_any(list_of_object, **kwargs):
    """ Find any element that match properties values
        Args:
            list_of_object: provide a list of objects you want to filter
            kwargs: properties with values you want to use as filter
        Returns:
            A filtered list of objects that match any of the filter properties
    """
    filtered_object = list_of_object
    result = set()
    if kwargs:
        for key, val in kwargs.items():
            func = attrgetter(key)
            if type(val) == bool:
                filter_func = func if val else lambda e: not func(e)
            else:
                filter_func = lambda obj: func(obj) == val            
            result.update(filter(filter_func, filtered_object))
    else:
        result = filtered_object
    return result

def find(list_of_object, **kwargs):
    """ Find elements that match properties values
        Args:
            list_of_object: provide a list of objects you want to filter
            kwargs: properties with values you want to use as filter
        Returns:
            A filtered list of objects that match the filter properties
    """    
    filtered_object = list_of_object
    if kwargs:
        for key, val in kwargs.items():
            func = attrgetter(key)
            if type(val) == bool:
                filter_func = func if val else lambda e: not func(e)
            else:
                filter_func = lambda obj: func(obj) == val
            filtered_object = list(filter(filter_func, filtered_object))
    return filtered_object