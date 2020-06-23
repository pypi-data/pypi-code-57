# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:39:06 2020

@author: hansp
"""

def nice_poly(p,x):
    """  
    This function takes a sympy function p, tries to interpret it as
    a polynomial in x, and re-writes it by using .factor() on all
    polynomial coefficients.
    """
    c = p.as_poly(x).all_coeffs()[::-1]
    return sum( [ x**i*(y.factor()) for y,i in zip(c,np.arange(np.size(c))) ] )
