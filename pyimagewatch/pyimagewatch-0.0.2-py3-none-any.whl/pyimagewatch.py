"""
Image processing debugger similar to Image Watch for Visual Studio.
"""

from functools import partial, wraps
from inspect import unwrap

import cv2 as cv

# * ------------------------------------------------------------------------------ # *
# * DECORATION HELPER * #


def decorate_functions(function_names, decorator):
    "Decorates a list of functions in the cv module with a decorator."
    for function_name in function_names:
        function = getattr(cv, function_name)
        setattr(cv, function_name, decorator(function))


# * ------------------------------------------------------------------------------ # *
# * COERCION * #


def is_even(value):
    is_even = not (value % 2)
    return is_even


def scale(range_in, range_out, value_in):
    """scale a value from an input range to an output range"""
    diff_in = range_in[1] - range_in[0]
    diff_value = value_in - range_in[0]
    diff_out = range_out[1] - range_out[0]
    scaling_factor = diff_out / diff_in
    value_out = range_out[0] + scaling_factor * diff_value
    return value_out


def coerce(track_range, arg_range, trackbar_pos):
    value = int(scale(track_range, arg_range, trackbar_pos))
    if is_even(value):
        value = value + 1
    return value


# * ------------------------------------------------------------------------------ # *
# * TRACKBAR DEFINITION * #

# trackbar-specific configuration
TRACK_MAX_VALUE = 1000
TRACK_RANGE = [0, TRACK_MAX_VALUE]


def trackbar(
    cv_function_name,
    args,
    track_arg,
    coerce_function,
    track_range,
    arg_range,
    trackbar_pos,
):
    """Converts a trackbar input to an argument range"""
    cv_function = getattr(cv, cv_function_name)
    value = coerce_function(track_range, arg_range, trackbar_pos)
    args[track_arg] = value
    result = unwrap(cv_function)(**args)
    cv.imshow(cv_function_name, result)
    return result


def track(
    cv_function_name,
    args,
    track_arg,
    coerce_function,
    track_range,
    arg_range,
    arg_init_value,
    f,
):
    """Decorator that adds a trackbar to a cv module function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        trackbar_specific = partial(
            trackbar,
            cv_function_name,
            kwargs,
            track_arg,
            coerce,
            track_range,
            arg_range,
        )
        track_init_value = int(scale(arg_range, track_range, arg_init_value))
        cv.createTrackbar(
            track_arg,
            cv_function_name,
            track_init_value,
            TRACK_MAX_VALUE,
            trackbar_specific,
        )
        result = trackbar_specific(track_init_value)
        cv.waitKey()
        return result

    return wrapper


# * ------------------------------------------------------------------------------ # *
# * DECORATORS * #


def show(f):
    """Decorator that shows the result of a cv module function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        cv.imshow(f.__name__, result)
        cv.waitKey()
        return result

    return wrapper
