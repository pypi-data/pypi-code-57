# -*- coding: utf-8 -*-
"""
This file contains tricks to manipulate symbolic expressions
"""

import sympy as sy
import numpy as np

def ht_nicepoly(p,x):
    """  
    This function takes a sympy function p, tries to interpret it as
    a polynomial in x, and re-writes it by using .factor() on all
    polynomial coefficients.
    """
    c = p.as_poly(x).all_coeffs()[::-1]
    return sum( [ x**i*(y.factor()) for y,i in zip(c,np.arange(np.size(c))) ] )
