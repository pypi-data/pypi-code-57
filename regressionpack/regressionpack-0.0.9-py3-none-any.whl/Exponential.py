import numpy as np
from . import Polynomial
from typing import Tuple

class Exponential(Polynomial):

    """
    Might not be worth it to do this one, as it is a trivial extension of a linear/polynomial regression of
    log(y) = a + bx

    Doing it might mean using a different approach for generating errorbars in the future, as these
    will be multiplicative errorbars instead of additive ones. 
    Might be worth it to have all the error functions give the lower and upper bounds directly, rather than just the delta. 
    """

    def __init__(self, x:np.ndarray, y:np.ndarray, fitDim:int=0, confidenceInterval:float=0.95, simult:bool=False):
        super(Exponential, self).__init__(x, np.log(y), 1, fitDim, confidenceInterval, simult)

    @property
    def Beta(self):
        temp = super(Exponential, self).Beta
        # Deal with the transpose and stuff to apply exp() on all the values in position 0 of the parameter axis. 
    @property
    def BetaFitError(self):
        temp = super(Exponential, self).BetaFitError

    def Eval(self, x:np.ndarray):
        return np.exp(super(Exponential, self).Eval(x))