import numpy as np
from typing import Tuple
from .GenericCurveFit import GenericCurveFit
from .utilities import FFTGuess

class Exponential(GenericCurveFit):
    
    def FitFunc(self, x:np.ndarray, a:float, b:float, c:float) -> np.ndarray:
        """
        An exponantial function that goes like
        $$ y = a e^{bx} + c $$
        """
        return a * np.exp(b*x) + c

    def Jacobian(self, x:np.ndarray, a:float, b:float, c:float) -> np.ndarray:
        """
        The jacobian of the exponential fit function. 
        Meant to return a matrix of shape [x.shape[0], 3], where
        every column contains the derivative of the function with 
        respect to the fit parameters in order. 
        """
        out = np.zeros((x.shape[0],3))
        out[:,0] = np.exp(b*x) # df/da
        out[:,1] = a*x*np.exp(b*x) # df/db
        out[:,2] = 1 # df/dc

        return out

    def __init__(self, x:np.ndarray, y:np.ndarray, p0:np.ndarray=None, bounds=(-np.inf, np.inf), confidenceInterval:float=0.95, simult:bool=False, **kwargs):
        super(Exponential, self).__init__(x, y, self.FitFunc, self.Jacobian, p0, bounds, confidenceInterval, simult, **kwargs )