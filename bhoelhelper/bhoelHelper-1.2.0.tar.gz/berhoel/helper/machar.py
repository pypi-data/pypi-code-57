#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Determine machine-specific parameters affecting floating-point
arithmetic.

Function to determine machine-specific parameters affecting
floating-point arithmetic.

* This is build after "NUMERICAL RECIPES in C", second edition,
  Reprinted 1996, pp.  889.
"""

from __future__ import division, print_function, absolute_import, unicode_literals

# Standard libraries.
import math

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

__date__ = "2020/06/13 17:49:10 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 1999, 2000,2018 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "bhoel@starship.python.net"


def machar():
    """
Determines and returns machine-specific parameters affecting
floating-point arithmetic. Returned values include:

    ``ibeta``  -- The radix in which numbers are represented, almost
                  always 2, but occasionally 16, or even 10

    ``it``     -- The number of base-``ibeta`` digits in the floating point
                  mantissa

    ``machep`` -- Is the exponent of the smallest (mos negative) power if
                  ``ibeta`` that, added to 1.0 gives something different
                  from 1.0.

    ``eps``    -- Is the floating-point number ``ibeta`` ** ``machdep``, loosly
                  referred to as the *floating-point precision*.

    ``negep``  -- Is the exponenet of the smalles power of ``ibeta`` that,
                subtracted from 1.0, gives something different from 1.0.

    ``epsneg`` -- Is ``ibeta`` ** ``negep``, another way of defining
                floating-point precision. Not infrequently ``epsneg`` is
                0.5 times ``eps``; occasionally ``eps`` and ``epsneg`` are
                equal.

    ``iexp``   -- Is the number of bits in the exponent (including its
                sign or bias)

    ``minexp`` -- Is the smallest (most negative) power if ``ibeta``
                consistent with there no leading zeros in the mantissa.

    ``xmin``   -- Is the floating-point number ``ibeta`` ** ``minexp``, generally
                the smallest (in magnitude) usable floating value

    ``maxexp`` -- Is the smallest (positive) power of ``ibeta`` that causes
                overflow.

    ``xmax``   -- Is (1 - ``epsneg``) x ``ibeta`` ** ``maxexp``, generally the largest
                (in magnitude) usable floating value.

    ``irnd``   -- Returns a code in the range 0...5, giving information on
                what kind of rounding is done in addition, and on how
                underflow is handled.

                If ``irnd`` returns 2 or 5, then your computer is
                compilant with the IEEE standard for rounding. If it
                returns 1 or 4, then it is doing some kind of rounding,
                but not the IEEE standard. If ``irnd`` returns 0 or 3,
                then it is truncating the result, not rounding it.

    ``ngrd``   -- Is the number of *guard digits* used when truncating
                the ploduct of two mantissas to fit the representation

This is taken from "NUMERICAL RECIPES in C", second edition,
Reprinted 1996.
"""
    one = float(1)
    two = one + one
    zero = one - one
    # Determine ``ibeta`` and ``beta`` by the method of M. Malcom.
    a = temp1 = one
    while temp1 - one == zero:
        a += a
        temp = a + one
        temp1 = temp - a
    b = one
    itemp = 0
    while itemp == 0:
        b += b
        temp = a + b
        itemp = int(temp - a)
    ibeta = itemp
    beta = float(ibeta)
    # Determine ``it`` and ``irnd``.
    it = 0
    b = temp1 = one
    while temp1 - one == zero:
        it = it + 1
        b = beta * b
        temp = b + one
        temp1 = temp - b
    irnd = 0
    betah = beta / two
    temp = a + betah
    if temp - a != zero:
        irnd = 1
    tempa = a + beta
    temp = tempa + betah
    if irnd == 0 and temp - tempa != zero:
        irnd = 2
    # Determine ``negep`` und ``epsneg``.
    negep = it + 3
    betain = one / beta
    a = one
    i = 1
    while i <= negep:
        i = i + 1
        a = betain * a
    b = a
    while 1:
        temp = one - a
        if temp - one != zero:
            break
        a = beta * a
        negep = negep - 1
    negep = -negep
    epsneg = a
    # Determine ``machdep`` and ``eps``.
    machdep = -it - 3
    a = b
    while 1:
        temp = one + a
        if temp - one != zero:
            break
        a = a * beta
        machdep = machdep + 1
    eps = a
    # Deterrmine ``ngrd``.
    ngrd = 0
    temp = one + eps
    if irnd == 0 and temp * one - one != zero:
        ngrd = 1
    # Determine ``iexp``.
    i = 0
    k = 1
    z = betain
    t = one + eps
    nxres = 0
    while 1:  # Loop until underflow ocurs, then exit.
        y = z
        z = y * y
        a = z * one  # check for underflow
        temp = z * t
        if a + a == zero or math.fabs(z) >= y:
            break
        temp1 = temp * betain
        if temp1 * beta == z:
            break
        i = i + 1
        k = k + k
    if ibeta != 10:
        iexp = i + 1
        mx = k + k
    else:  # For decimal machines only
        iexp = i + i
        iz = ibeta
        while k >= iz:
            iz = ibeta * iz
            iexp = iexp + 1
        mx = iz + iz - 1
    # To determine ``minexp`` and ``xmin``, loop until an underflow
    # occurs, then exit.
    while 1:
        xmin = y
        y = betain * y
        a = y * one  # Check here for the underflow
        temp = y * t
        if a + a != zero or fabs(y) < xmin:
            k = k + 1
            temp1 = temp * betain
            if temp1 * beta == y and temp != y:
                nxres = 3
                xmin = y
                break
        else:
            break
    minexp = -k
    # Determine maxexp, xmax.
    if mx <= k + k + 3 and ibeta != 10:
        mx = mx + mx
        iexp = iexp + 1
    maxexp = mx + minexp
    irnd = nxres + irnd  # Adjust ``irnd`` to reflect partial underflow
    if irnd >= 2:
        maxexp = maxexp - 2  # Adjust for IEEE-stype machines
    i = maxexp + minexp
    # Adjust for machines with implicit leading bit in binary mantissa,
    # and machines with radix point at extreme right of mantissa.
    if ibeta == 2 and not i:
        maxexp = maxexp - 1
    if i > 20:
        maxexp = maxexp - 1
    if a != y:
        maxexp = maxexp - 2
    xmax = one - epsneg
    if xmax * one != xmax:
        xmax = one - beta * epsneg
    xmax = xmax / (xmin * beta * beta * beta)
    i = maxexp + minexp + 3
    j = 1
    while j <= i:
        j = j + 1
        if ibeta == 2:
            xmax = xmax + xmax
        else:
            xmax = xmax * beta
    return {
        "ibeta": ibeta,
        "it": it,
        "irnd": irnd,
        "ngrd": ngrd,
        "machdep": machdep,
        "negep": negep,
        "iexp": iexp,
        "minexp": minexp,
        "maxexp": maxexp,
        "eps": eps,
        "epsneg": epsneg,
        "xmin": xmin,
        "xmax": xmax,
    }


__tmp = machar()

# ``ibeta`` is the radix in which numbers are represented, almost always
# 2, but occasionally 16, or even 10
ibeta = __tmp["ibeta"]

# ``it`` is The number of base-``ibeta`` digits in the floating point
# mantissa
it = __tmp["it"]

# ``machep`` is the exponent of the smallest (mos negative) power if
# ``ibeta`` that, added to 1.0 gives something different from 1.0.
machdep = __tmp["machdep"]

# ``eps`` is the floating-point number ``ibeta`` ** ``machdep``, loosly
# referred to as the *floating-point precision*.
eps = __tmp["eps"]

# ``negep`` is the exponenet of the smalles power of ``ibeta`` that,
# subtracted from 1.0, gives something different from 1.0.
negep = __tmp["negep"]

# ``epsneg`` is ``ibeta`` ** ``negep``, another way of defining floating-point
# precision. Not infrequently ``epsneg`` is 0.5 times ``eps``;
# occasionally ``eps`` and ``epsneg`` are equal.
epsneg = __tmp["epsneg"]

# ``iexp`` is the number of bits in the exponent (including its sign or
# bias)
iexp = __tmp["iexp"]

# ``minexp`` is the smallest (most negative) power if ``ibeta`` consistent
# with there no leading zeros in the mantissa.
minexp = __tmp["minexp"]

# ``xmin`` is the floating-point number ``ibeta`` ** ``minexp``, generally the
# smallest (in magnitude) usable floating value
xmin = __tmp["xmin"]

# ``maxexp`` is the smallest (positive) power of ``ibeta`` that causes
# overflow.
maxexp = __tmp["maxexp"]

# ``xmax`` Is (1-``epsneg``) x ``ibeta`` ** ``maxexp``, generally the largest (in
# magnitude) usable floating value.
xmax = __tmp["xmax"]

# Returns a code in the range 0...5, giving information on what kind
# of rounding is done in addition, and on how underflow is handled.
#
# If ``irnd`` returns 2 or 5, then your computer is compilant with the
# IEEE standard for rounding. If it returns 1 or 4, then it is doing
# some kind of rounding, but not the IEEE standard. If ``irnd`` returns
# 0 or 3, then it is truncating the result, not rounding it.
irnd = __tmp["irnd"]

# ``ngrd`` is the number of *guard digits* used when truncating the
# ploduct of two mantissas to fit the representation
ngrd = __tmp["ngrd"]


# Local Variables:
# mode: python
# compile-command: "python ../../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
