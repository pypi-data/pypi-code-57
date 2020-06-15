"""average.py
"""
import functools
from functools import reduce

import numpy as np
import torch
from numpy.core import overrides
from .result_type import result_type

__all__ = [
    'average'
]

array_function_dispatch = functools.partial(
    overrides.array_function_dispatch, module='pytorch_math')

def _average_dispatcher(a, axis=None, weights=None, returned=None):
    return (a, weights)


@array_function_dispatch(_average_dispatcher)
def average(a, axis=None, weights=None, returned=False):
    """
    Compute the weighted average along the specified axis.
    Parameters
    ----------
    a : array_like
        Array containing data to be averaged. If `a` is not an array, a
        conversion is attempted.
    axis : None or int or tuple of ints, optional
        Axis or axes along which to average `a`.  The default,
        axis=None, will average over all of the elements of the input array.
        If axis is negative it counts from the last to the first axis.
        .. versionadded:: 1.7.0
        If axis is a tuple of ints, averaging is performed on all of the axes
        specified in the tuple instead of a single axis or all the axes as
        before.
    weights : array_like, optional
        An array of weights associated with the values in `a`. Each value in
        `a` contributes to the average according to its associated weight.
        The weights array can either be 1-D (in which case its length must be
        the size of `a` along the given axis) or of the same shape as `a`.
        If `weights=None`, then all data in `a` are assumed to have a
        weight equal to one.  The 1-D calculation is::
            avg = sum(a * weights) / sum(weights)
        The only constraint on `weights` is that `sum(weights)` must not be 0.
    returned : bool, optional
        Default is `False`. If `True`, the tuple (`average`, `sum_of_weights`)
        is returned, otherwise only the average is returned.
        If `weights=None`, `sum_of_weights` is equivalent to the number of
        elements over which the average is taken.
    Returns
    -------
    retval, [sum_of_weights] : array_type or double
        Return the average along the specified axis. When `returned` is `True`,
        return a tuple with the average as the first element and the sum
        of the weights as the second element. `sum_of_weights` is of the
        same type as `retval`. The result dtype follows a genereal pattern.
        If `weights` is None, the result dtype will be that of `a` , or ``float64``
        if `a` is integral. Otherwise, if `weights` is not None and `a` is non-
        integral, the result type will be the type of lowest precision capable of
        representing values of both `a` and `weights`. If `a` happens to be
        integral, the previous rules still applies but the result dtype will
        at least be ``float64``.
    Raises
    ------
    ZeroDivisionError
        When all weights along axis are zero. See `numpy.ma.average` for a
        version robust to this type of error.
    TypeError
        When the length of 1D `weights` is not the same as the shape of `a`
        along axis.
    See Also
    --------
    mean
    ma.average : average for masked arrays -- useful if your data contains
                 "missing" values
    numpy.result_type : Returns the type that results from applying the
                        numpy type promotion rules to the arguments.
    Examples
    --------
    >>> data = np.arange(1, 5)
    >>> data
    array([1, 2, 3, 4])
    >>> np.average(data)
    2.5
    >>> np.average(np.arange(1, 11), weights=np.arange(10, 0, -1))
    4.0
    >>> data = np.arange(6).reshape((3,2))
    >>> data
    array([[0, 1],
           [2, 3],
           [4, 5]])
    >>> np.average(data, axis=1, weights=[1./4, 3./4])
    array([0.75, 2.75, 4.75])
    >>> np.average(data, weights=[1./4, 3./4])
    Traceback (most recent call last):
        ...
    TypeError: Axis must be specified when shapes of a and weights differ.
    >>> a = np.ones(5, dtype=np.float128)
    >>> w = np.ones(5, dtype=np.complex64)
    >>> avg = np.average(a, weights=w)
    >>> print(avg.dtype)
    complex256
    """
    # a = np.asanyarray(a)

    if weights is None:
        # avg = a.mean(axis)
        kwargs = {}
        if axis is not None:
            kwargs['dim'] = axis
        if not a.dtype.is_floating_point:
            kwargs['dtype'] = torch.float32
        avg = a.mean(**kwargs)
        # scl = avg.dtype.type(a.size/avg.size)
        # pylint: disable=not-callable
        scl = torch.tensor(a.numpy().size/avg.numpy().size, dtype=avg.dtype)
    else:
        # wgt = np.asanyarray(weights)
        wgt = weights

        # if issubclass(a.dtype.type, (np.integer, np.bool_)):
        # TODO isn't there a better way to perform this check?
        if issubclass(a.numpy().dtype.type, (np.integer, np.bool_)):
            # result_dtype = np.result_type(a.dtype, wgt.dtype, 'f8')
            type_examples = [a, wgt, torch.Tensor([0]).type(torch.float64)]
            result_dtype = result_type(type_examples)
            # result_dtype = get_result_type_2_by_2(type_examples)
        else:
            # result_dtype = np.result_type(a.dtype, wgt.dtype)
            result_dtype = torch.result_type(a, wgt)

        # Sanity checks
        if a.shape != wgt.shape:
            if axis is None:
                raise TypeError(
                    "Axis must be specified when shapes of a and weights "
                    "differ.")
            if wgt.ndim != 1:
                raise TypeError(
                    "1D weights expected when shapes of a and weights differ.")
            if wgt.shape[0] != a.shape[axis]:
                raise ValueError(
                    "Length of weights not compatible with specified axis.")

            # setup wgt to broadcast along axis
            # wgt = np.broadcast_to(wgt, (a.ndim-1)*(1,) + wgt.shape)
            wgt = wgt.reshape((a.ndim-1)*(1,) + wgt.shape)
            # wgt = wgt.swapaxes(-1, axis)
            wgt = wgt.reshape(-1, axis+1)

        # scl = wgt.sum(axis=axis, dtype=result_dtype)
        kwargs = {}
        if axis is not None:
            kwargs['dim'] = axis
        base_kwargs = kwargs
        kwargs['dtype'] = result_dtype

        scl = wgt.sum(**kwargs)
        if torch.any(scl == 0.0):
            raise ZeroDivisionError(
                "Weights sum to zero, can't be normalized")

        # avg = np.multiply(a, wgt, dtype=result_dtype).sum(axis)/scl
        avg = a.type(result_dtype).mul(wgt).sum(**base_kwargs)/scl

    if returned:
        if scl.shape != avg.shape:
            # scl = np.broadcast_to(scl, avg.shape).copy()
            raise ValueError("feature not implemented yet")
        return avg, scl
    return avg


# @array_function_dispatch(_average_dispatcher)
# def average(a, axis=None, weights=None, returned=False):
#     """
#     Compute the weighted average along the specified axis.
#     Parameters
#     ----------
#     a : array_like
#         Array containing data to be averaged. If `a` is not an array, a
#         conversion is attempted.
#     axis : None or int or tuple of ints, optional
#         Axis or axes along which to average `a`.  The default,
#         axis=None, will average over all of the elements of the input array.
#         If axis is negative it counts from the last to the first axis.
#         .. versionadded:: 1.7.0
#         If axis is a tuple of ints, averaging is performed on all of the axes
#         specified in the tuple instead of a single axis or all the axes as
#         before.
#     weights : array_like, optional
#         An array of weights associated with the values in `a`. Each value in
#         `a` contributes to the average according to its associated weight.
#         The weights array can either be 1-D (in which case its length must be
#         the size of `a` along the given axis) or of the same shape as `a`.
#         If `weights=None`, then all data in `a` are assumed to have a
#         weight equal to one.  The 1-D calculation is::
#             avg = sum(a * weights) / sum(weights)
#         The only constraint on `weights` is that `sum(weights)` must not be 0.
#     returned : bool, optional
#         Default is `False`. If `True`, the tuple (`average`, `sum_of_weights`)
#         is returned, otherwise only the average is returned.
#         If `weights=None`, `sum_of_weights` is equivalent to the number of
#         elements over which the average is taken.
#     Returns
#     -------
#     retval, [sum_of_weights] : array_type or double
#         Return the average along the specified axis. When `returned` is `True`,
#         return a tuple with the average as the first element and the sum
#         of the weights as the second element. `sum_of_weights` is of the
#         same type as `retval`. The result dtype follows a genereal pattern.
#         If `weights` is None, the result dtype will be that of `a` , or ``float64``
#         if `a` is integral. Otherwise, if `weights` is not None and `a` is non-
#         integral, the result type will be the type of lowest precision capable of
#         representing values of both `a` and `weights`. If `a` happens to be
#         integral, the previous rules still applies but the result dtype will
#         at least be ``float64``.
#     Raises
#     ------
#     ZeroDivisionError
#         When all weights along axis are zero. See `numpy.ma.average` for a
#         version robust to this type of error.
#     TypeError
#         When the length of 1D `weights` is not the same as the shape of `a`
#         along axis.
#     See Also
#     --------
#     mean
#     ma.average : average for masked arrays -- useful if your data contains
#                  "missing" values
#     numpy.result_type : Returns the type that results from applying the
#                         numpy type promotion rules to the arguments.
#     Examples
#     --------
#     >>> data = np.arange(1, 5)
#     >>> data
#     array([1, 2, 3, 4])
#     >>> np.average(data)
#     2.5
#     >>> np.average(np.arange(1, 11), weights=np.arange(10, 0, -1))
#     4.0
#     >>> data = np.arange(6).reshape((3,2))
#     >>> data
#     array([[0, 1],
#            [2, 3],
#            [4, 5]])
#     >>> np.average(data, axis=1, weights=[1./4, 3./4])
#     array([0.75, 2.75, 4.75])
#     >>> np.average(data, weights=[1./4, 3./4])
#     Traceback (most recent call last):
#         ...
#     TypeError: Axis must be specified when shapes of a and weights differ.
#     >>> a = np.ones(5, dtype=np.float128)
#     >>> w = np.ones(5, dtype=np.complex64)
#     >>> avg = np.average(a, weights=w)
#     >>> print(avg.dtype)
#     complex256
#     """
#     a = np.asanyarray(a)

#     if weights is None:
#         avg = a.mean(axis)
#         scl = avg.dtype.type(a.size/avg.size)
#     else:
#         wgt = np.asanyarray(weights)

#         if issubclass(a.dtype.type, (np.integer, np.bool_)):
#             result_dtype = np.result_type(a.dtype, wgt.dtype, 'f8')
#         else:
#             result_dtype = np.result_type(a.dtype, wgt.dtype)

#         # Sanity checks
#         if a.shape != wgt.shape:
#             if axis is None:
#                 raise TypeError(
#                     "Axis must be specified when shapes of a and weights "
#                     "differ.")
#             if wgt.ndim != 1:
#                 raise TypeError(
#                     "1D weights expected when shapes of a and weights differ.")
#             if wgt.shape[0] != a.shape[axis]:
#                 raise ValueError(
#                     "Length of weights not compatible with specified axis.")

#             # setup wgt to broadcast along axis
#             wgt = np.broadcast_to(wgt, (a.ndim-1)*(1,) + wgt.shape)
#             wgt = wgt.swapaxes(-1, axis)

#         scl = wgt.sum(axis=axis, dtype=result_dtype)
#         if np.any(scl == 0.0):
#             raise ZeroDivisionError(
#                 "Weights sum to zero, can't be normalized")

#         avg = np.multiply(a, wgt, dtype=result_dtype).sum(axis)/scl

#     if returned:
#         if scl.shape != avg.shape:
#             scl = np.broadcast_to(scl, avg.shape).copy()
#         return avg, scl
#     else:
#         return avg

    # type_examples = [a, wgt, torch.Tensor([0]).type(torch.float64)]
