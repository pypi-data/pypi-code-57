import numpy as np
from scipy.stats import t
from typing import Tuple

class AbstractRegression:

    _initialized:bool
    _X:np.ndarray
    _Y:np.ndarray
    _CI:float
    _FitDim:int
    _Simult:bool
    _NbParms:int
    _Beta:np.ndarray
    _BetaFitError:np.ndarray
    
    _Residuals:np.ndarray
    _SSE:np.ndarray
    _MSE:np.ndarray

    @property
    def X(self) -> np.ndarray:
        """
        The independant variable. 
        """
        return self._X
    
    @X.setter
    def X(self, value:np.ndarray):
        assert not self._initialized, "Can't change this property after instanciation"
        assert isinstance(value, np.ndarray), "X must be of type np.ndarray"
        self._X = value

    @property
    def Y(self) -> np.ndarray:
        """
        The dependant variable. 
        """
        return self._Y
    
    @Y.setter
    def Y(self, value:np.ndarray):
        assert not self._initialized, "Can't change this property after instanciation"
        assert isinstance(value, np.ndarray), "Y must be of type np.ndarray"
        self._Y = value

    @property
    def CI(self) -> float:
        """
        The Confidence Interval used for computing the error bars. 
        """
        return self._CI

    @CI.setter
    def CI(self, value:float):
        assert isinstance(value, float) and 0 < value < 1, 'CI must be a float and respect 0 < CI < 1'
        self._CI = value

    @property
    def FitDim(self) -> int:
        return self._FitDim

    @FitDim.setter
    def FitDim(self, value:int):
        assert not self._initialized, "Can't change this property after instanciation"
        assert isinstance(value, int), "FitDim must be an integer"
        assert -self.X.ndim <= value < self.X.ndim, "Specified dimension must respect -X.ndim <= ParmDim < X.ndim"
        self._FitDim = value % self.X.ndim

    @property
    def Simult(self) -> bool:
        return self._Simult

    @Simult.setter
    def Simult(self, value:bool):
        assert isinstance(value, bool), "Simult must be a boolean value"
        self._Simult = value
    
    @property
    def NbParms(self) -> int:
        """
        The number of fit parameters used in the model. 
        This is useful when computing the degrees of freedom
        of the fit, the errorbars and the adjusted R2. 
        """
        return self._NbParms

    @NbParms.setter
    def NbParms(self, value:int):
        assert not self._initialized, "Can't change this property after instanciation"
        assert isinstance(value, int) and value >= 1, "Value must be an integer >= 1"
        self._NbParms = value

    @property
    def Nb(self) -> int:
        """
        Number of data points along the fitting axis. 
        """
        return self.X.shape[self.FitDim]

    @property
    def DoF(self) -> int:
        """
        The Degrees of Freedom of the problem. 

        """
        return self.Nb - self.NbParms
    
    @property
    def Student(self) -> float:
        """
        Returns the Student coefficient corresponding to
        the chosen Confidence Interval CI. 
        """
        if self.Simult:
            return t.ppf(1-(1-self.CI)/2/self.Nb,self.DoF)
        else:
            return t.ppf(1-(1-self.CI)/2,self.DoF)

    @property
    def SSE(self) -> np.ndarray:
        """
        The Sum of Squared Errors. 
        """
        return self._SSE

    @property
    def SST(self) -> np.ndarray:
        """
        The Sum of Squared Totals. 
        """
        return self._SST

    @property
    def MSE(self) -> np.ndarray:
        return self._MSE

    @property
    def R2(self) -> np.ndarray:
        """
        The coefficient of determination. 
        https://en.wikipedia.org/wiki/Coefficient_of_determination
        """
        return self._R2

    @property
    def AdjR2(self) -> np.ndarray:
        """
        The R2 adjusted for the degrees of freedom of the fit. 
        https://en.wikipedia.org/wiki/Coefficient_of_determination
        """
        return self._AdjR2

    @property
    def Beta(self) -> np.ndarray:
        """
        The fitted parameters. 
        """
        return self._Beta

    @property
    def BetaFitError(self) -> np.ndarray:
        """
        The error on the fit parameters. This one is smaller
        and represents where the real estimators likely sits, within the
        current confidence interval. 
        """
        return self._BetaFitError

    def _computeFitStats(self):
        """
        Computes various useful fit stats:
            Residuals:  The raw difference between the model and the data
            SSE:        Sum of squared errors
            SST:        Sum of Squared totals
            MSE:        Mean squared error
            R2:         Coefficient of determination
            AdjR2:      Adjusted coefficient of determination
            
        """
        self._Residuals = self.Y - self.Eval(self.X)
        self._SSE = np.sum(self._Residuals**2, axis=self.FitDim, keepdims=True)
        self._SST = np.sum((self.Y - np.mean(self.Y, axis=self.FitDim, keepdims=True)**2), axis=self.FitDim, keepdims=True)
        self._MSE = self.SSE / self.DoF
        self._R2 = 1 - self.SSE / self.SST
        self._AdjR2 = 1 - (1-self.R2) * (self.Nb - 1)/self.DoF

    def __init__(self, x:np.ndarray, y:np.ndarray, nbParms:int, fitDim:int=0, confidenceInterval:float=0.95, simult:bool=False):
        
        self._initialized = False

        self.X = x
        self.Y = y
        self.CI = confidenceInterval
        self.FitDim = fitDim
        self.Simult = simult
        self.Simult = simult
        self.NbParms = nbParms

        self._initialized = True # Once this is true, some parameters can't be modified

    def Fit(self):
        """
        Performs the fitting. Once this has been successfully ran, 
        you will have access to all the results via the properties
        * Beta
        * BetaFitError
        * BetaPredictionError
        * MSE
        * SSE
        * R2 and AdjR2

        And will be able to evaluate the model for a given input (that matches the 
        size of the fitted data in every dimension except the FitDim) using
        * Eval(X)
        * EvalFitError(X)
        * EvalPredictionError(X)
        """
        raise NotImplementedError("This function must be overriden in the child class!")

    def Eval(self, x:np.ndarray) -> np.ndarray:
        """
        Evaluates the fitted function using the values of the
        input array x. 
        """
        raise NotImplementedError("This function must be overriden in the child class!")

    def EvalFitError(self, x:np.ndarray):
        """
        The error on the fit. This one is smaller
        and represents where the real curve likely sits, within the
        current confidence interval. 
        """
        raise NotImplementedError("This function must be overriden in the child class!")

    def EvalPredictionError(self, x:np.ndarray):
        """
        The prediction interval. This one is bigger and represents
        where a new data point is likely to be found, within the 
        current confidence interval. 
        """
        raise NotImplementedError("This function must be overriden in the child class!")
    