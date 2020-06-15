import numpy as np
from scipy.special import binom, factorial
#    term2 = np.sum([
#            for r in range(el - spin + 1)
#            ], axis=0)
#

def _fac(v):
    return factorial(v, exact=True)

theta = 1e-3
for spin in range(3):
    for el in range(50, 55):
        for em in range(0, el, 5):
#            for r in range(el - spin + 1):
#                print(binom(el - spin, r), binom(el + spin, r + spin - em))
#                print(el, em, spin, r, (1 / np.tan(theta / 2))**(2 * r + spin - em))
                #print(spin, el, em, _fac(el + em), _fac(el - em),  _fac(el + spin),  _fac(el - spin))
                print(spin, el, em, _fac(el + em) * _fac(el - em) /  _fac(el + spin) / _fac(el - spin))

#for 
#binom(el - spin, r) * binom(el + spin, r
#                            + spin - em) * (-1)**(el - r - spin)
#* np.exp(1j * em * phi) * (1 / np.tan(theta / 2))**(2 * r + spin - em)
