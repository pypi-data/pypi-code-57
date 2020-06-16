import numpy as np
from .AbstractRegression import AbstractRegression
from typing import Tuple
from .utilities import MatMul, MatInv, MatDiag, MatFlip, getOrder

class Linear(AbstractRegression):
    """
    Used to perform multivariate linear regressions. 

    Typical use involves:
        a matrix of independant variables X[...,F, P]
        a matrix of dependant variable Y[...,F, 1]
        where F is the number of points in the Fit Dimension (FitDim)
        and P is the number of parameters in the Parameters Dimension (ParmDim)

        For example, one could have a 2D X matrix with columns: age, height
        and another 2D matrix (but only one column) for Y: weight

        Note that this package allows the FitDim and ParmDim to be elsewhere than at the
        end, in which case the user must specify which dimensions fill that purpose. 

        L = Linear(X, Y)
        L.Fit()

        Fitted constants and their errors are found in
        Beta
        BetaFitError
        BetaPredictionError

        Evaluating the function using given input matrix X' is done using
        Eval(X)
        EvalFitError(X)
        EvalPredictionError(X)

    """
    _Xt:np.ndarray
    _XtXinv:np.ndarray
    _ParmDim:int

    @property
    def ParmDim(self) -> int:
        """
        The dimension containing the parameters. 
        """
        return self._ParmDim

    @ParmDim.setter
    def ParmDim(self, value:int):
        assert not self._initialized, "Can't change this property after instanciation"
        assert -self._X.ndim <= value < self._X.ndim, "Specified dimension must respect -X.ndim <= ParmDim < X.ndim"
        assert value % self._X.ndim != self.FitDim, "Cannot use the same dimension for both ParmDim and FitDim"
        self._ParmDim = value % self._X.ndim
        
    @property
    def Axis(self) -> Tuple[int,int]:
        """
        Returns a tuple containing (FitDim, ParmDim)
        """
        return (self.FitDim, self.ParmDim)

    def __init__(self, x:np.ndarray, y:np.ndarray, fitDim:int=-2, confidenceInterval:float=0.95, simult:bool=False, parmDim:int=-1):
        
        # Instanciate using superclass constructor
        super(Linear, self).__init__(x, y, x.shape[parmDim], fitDim, confidenceInterval, simult)
        
        # Unlock modifying properties
        self._initialized = False

        # The add the missing properties
        self.ParmDim = parmDim

        # Re-lock modifying properties
        self._initialized = True

    def _computeXtXinv(self):
        """
        Computes the most useful intermediate matrices
        used in a Linear regression. 
        """
        order = [x for x in range(self._X.ndim)]
        order[self.FitDim] = self.ParmDim
        order[self.ParmDim] = self.FitDim
        self._Xt = self._X.transpose(order)
        self._XtXinv = MatInv(MatMul(self._Xt, self._X, self.Axis), self.Axis)

    def Fit(self):
        self._computeXtXinv()
        self._Beta = MatMul( MatMul(self._XtXinv, self._Xt, self.Axis), self._Y, self.Axis )
        self._computeFitStats()

        # self._BetaFitError = self.Student * np.sqrt( MatDiag(self._XtXinv, self.Axis) * self.MSE )
        # self._BetaPredictionError = self.Student * np.sqrt( 1 + MatDiag(self._XtXinv, self.Axis) * self.MSE )
        # This swap seems to work nicely at putting the fit dim at the end, which comes in handy for removing it once in the Polynomial
        self._BetaFitError = self.Student * np.sqrt( MatDiag(self._XtXinv, tuple(reversed(self.Axis))) * self.MSE )

        

    def Eval(self, x:np.ndarray):
        """
        Evaluates the fitted function using the values of the
        input array x. 
        """
        assert x.ndim == self._X.ndim, "Must match the number of dimensions of the training data"
        assert all([x.shape[i] == self._X.shape[i] for i in range(self._X.ndim) if i != self.FitDim]), "All dimensions other than the fit dimension must match"
        return MatMul(x, self._Beta, self.Axis)

    def EvalFitError(self, x:np.ndarray):
        """
        The error on the fit. This one is smaller
        and represents where the real curve likely sits, within the
        current confidence interval. 
        """
        # return self.Student * np.sqrt( MatDiag( MatMul( MatMul(x, self._XtXinv, self.Axis), MatFlip(x, self.Axis), self.Axis ), tuple(reversed(self.Axis)) ) * self.MSE )
        return self.Student * np.sqrt( MatDiag( MatMul( MatMul(x, self._XtXinv, self.Axis), MatFlip(x, self.Axis), self.Axis ), self.Axis ) * self.MSE )

    def EvalPredictionError(self, x:np.ndarray):
        """
        The prediction interval. This one is bigger and represents
        where a new data point is likely to be found, within the 
        current confidence interval. 
        """
        # return self.Student * np.sqrt( MatDiag( 1 + MatMul( MatMul(x, self._XtXinv, self.Axis), MatFlip(x, self.Axis), self.Axis ), tuple(reversed(self.Axis)) ) * self.MSE )
        return self.Student * np.sqrt( MatDiag( 1 + MatMul( MatMul(x, self._XtXinv, self.Axis), MatFlip(x, self.Axis), self.Axis ), self.Axis ) * self.MSE )

