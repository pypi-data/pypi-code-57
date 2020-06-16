"""
LogisticRegression.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from .generic import format_x, GenericModel
from ._utilities import _coerce_sample_weights

from izzy.misc import equal

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm
from sklearn.linear_model import LogisticRegression as _LogisticRegression


# LogisticRegression class
# TODO OVR vs. multiclass
# TODO devise LogisticRegression that does not penalize the intercept
class LogisticRegression(_LogisticRegression, GenericModel):
    """
    The class ``LogisticRegression`` fits a logistic regression model

    The general scope is to provide independent variables `x` with labels `y`, which will be used to fit the model.

    Then, `predict_proba` can be used to solve using the fitted coefficients for new samples.
    """

    # Initialize class instance
    def __init__(self, solver='lbfgs', **kwargs):
        """
        Initialize an instance of LogisticRegression
        """

        # Call parent class
        _LogisticRegression.__init__(self, solver=solver, **kwargs)

        # If solver is izzy, we need to trick sklearn
        # TODO at some point in time, we can do a more elegant solution. This way, we still initialize class from ext
        if solver == 'izzy':
            self.solver = 'izzy'

        # Class variables
        self.coefficients = None
        self.intercept = None
        self.is_fitted = False

    # Add intercept to x
    def _add_intercept_to_x(self, x):
        # If there's an intercept, add to x
        if self.fit_intercept:
            x = np.hstack((np.ones((self.n_obs, 1)), x))

        # Return x
        return x

    # Fit function for izzy solver
    def _fit(self, x, y):
        # Initialize coefficients for features (+ intercept)
        coefficients = np.ones(self.n_features + self.fit_intercept)

        # If necessary, add intercept to x
        x = self._add_intercept_to_x(x)

        # Minimize
        coefficients = minimize(_cost, coefficients, args=(x, y)).x

        # Set intercept
        if self.fit_intercept:
            self.intercept = coefficients[0]
            coefficients = np.delete(coefficients, 0)

        # Set coefficients
        self.coefficients = coefficients

    # Solve the logistic function
    def _function(self, x, y):
        return 1. / (1. + np.exp(-self.coefficients * x))

    # Degrees of freedom
    def degrees_of_freedom(self, sample_weights=None, axis=1):
        """
        Returns the degrees of freedom

        If axis = 0, this is the degrees of freedom :math:`D` of the samples.

        .. math:: D = N_{obs,weight > 0} - N_{features + intercept}

        If axis = 1, :math:`D` is computed   in feature space.

        .. math:: D = N_{features + intercept,coefficient>0}

        Parameters
        ----------
        sample_weights : ArrayLike
            Weights for each observation
        axis : int
            If 0, observations; if 1, features + intercept

        Returns
        -------
        int
            degrees of freedom
        """

        # Coerce sample_weights into correct form
        sample_weights = _coerce_sample_weights(sample_weights, n_samples=self.n_obs)

        # If axis = 0, DOF = # obs - # obs with 0 weight - # features (including intercept if present)
        if axis == 0:
            d = self.n_obs - np.sum(equal(sample_weights, 0)) - self.n_features - self.fit_intercept

        # If axis = 1, DOF = # features - # features with 0 coefficient + 1 (if intercept present)
        elif axis == 1:
            coefficients = self.coef_[0]
            d = self.n_features - np.sum(equal(self.coefficients, 0.)) + self.fit_intercept

        # If we get here, there's a problem
        else:
            raise AttributeError('axis can only be 0 or 1')

        # Return
        return d

    # Fit
    def fit(self, x, y, **kwargs):
        # Format x
        x = format_x(x)

        # Store number of observations / features
        self.n_obs = x.shape[0]
        self.n_features = x.shape[1]

        # Store classes
        self.classes = np.unique(y)
        self.n_classes = len(self.classes)

        # We don't know how to deal with multi_class = 'ovr' and n_classes > 2
        if self.multi_class == 'ovr' and self.n_classes > 2:
            raise AttributeError('multi_class must be set to multinomial')
        else:
            self.multi_class = 'multinomial'

        # Fit
        if self.solver == 'izzy':
            self._fit(x, y)

        else:
            _LogisticRegression.fit(self, x, y)
            self.coefficients = self.coef_[0]
            self.intercept = self.intercept_

        # Mark as fitted
        self.is_fitted = True

    # Feature importance
    def feature_importance(self, x, y):
        """
        Outputs coefficients of the model, their standard errors, and significance

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        pandas.DataFrame
            feature importance report
        """

        # Input check
        x = format_x(x)

        # Get feature names
        if isinstance(x, pd.DataFrame):
            features = x.columns.to_list()
        else:
            features = ['x' + str(i) for i in range(x.shape[1])]

        # Get coefficients
        coefficients = self.coefficients

        # Is there an intercept? If so, add to x, features, and coefficients
        if self.fit_intercept:
            # TODO with we use R method of standard errors, we need line below. Fix this!!
            # x = np.hstack((np.ones((x.shape[0], 1)), x))  # add 1s for intercept
            features = ['(intercept)'] + features
            coefficients = np.insert(coefficients, 0, self.intercept)

        # Compute standard errors
        # We need to add 1s to x for the intercept, but the Hessian function does this for us.
        ste = self.standard_errors(x, y)

        # Compute t-values
        t_values = coefficients / ste

        # Compute p-values from t-values
        p_values = 2. * norm.sf(np.abs(t_values))

        # Compute normed coefficients and weight
        # normed_coefficients = np.array(self.coefficients * np.std(x, axis=0))
        # abs_normed_coefficients = np.abs(normed_coefficients)
        # weight = abs_normed_coefficients / np.sum(abs_normed_coefficients)
        weight = coefficients

        # Add stars for significance
        def add_stars(p_value):
            stars = ''
            if 0. <= p_value < 0.001:
                stars = '***'
            elif 0.001 <= p_value < 0.01:
                stars = '**'
            elif 0.01 <= p_value < 0.05:
                stars = '*'
            elif 0.05 <= p_value < 0.1:
                stars = '.'
            return stars

        significance = np.vectorize(add_stars)(p_values)

        # Construct report
        report = {
            'feature': features,
            'coefficient': coefficients,
            # 'normed_coefficient': normed_coefficients,
            # 'weight': weight,
            'standard_error': ste,
            'p_value': p_values,
            'significance': significance
        }

        # Return as pandas DataFrame
        return pd.DataFrame(report, columns=report.keys()).sort_values('weight', ascending=False)

    # Hessian
    def hessian(self, x, y):
        r"""
        Computes the Hessian matrix.

        The Hessian is the second-order derivative of the loss function evaluated at the maximum likelihood estimate.

        Let's take this generally from the position of a loss function :math:`L`, which is the negative log likelihood
        (i.e., joint probability distribution of classes predicted by the model.

        .. math:: L = p^y(1-p)^{1-y}

        Here, :math:`p` is the outcome from solving the logistic function, and :math:`y` is the true outcome. We can
        also compute the log loss,

        .. math:: log(L) = ylog(p) + (1-y)log(1-p)

        Computing the derivative of :math:`log(L)`,

        .. math:: \frac{\delta log(L)}{\delta p} = \frac{y}{p}\delta p - \frac{1-y}{1-p}\delta p

        Remember that :math:`p(\beta |x) = \frac{1}{1+e^{-\beta^Tx}`. The derivative of :math:`p(\beta |x)` is,

        .. math:: \frac{\delta p}{\delta \beta} = \frac{\delta}{\delta w} (\frac{1}{1+e^{-\beta x}})

        .. math:: \frac{\delta p}{\delta \beta} = -(1+e^{-\beta x})^{-2}  (-xe^{-\beta x})

        .. math:: \frac{\delta p}{\delta \beta} = xp(1-p)

        Going back to the derivative of :math:`log(L)`, we can now fill in :math:`delta p`,

        .. math:: \frac{\delta log(L)}{\delta \beta^T} = \frac{y}{p}xp(1-p) - \frac{1-y}{1-p}xp(1-p)

        .. math:: \frac{\delta log(L)}{\delta \beta^T} = xy(1-p) - x(1-y)p  = xy - xyp - x + xyp = x(y-1)

        .. math:: \frac{\delta log(L)}{\delta \beta^T} = x(p-y)


        In this equation, :math:`\hat{y}` is the true outcome, where :math:`y(w|x) = \frac{1}{1+e^{-w^Tx}}` is the
        logistic function. Then, we can compute the first derivative of :math:`J`. We take the derivative with respect
        to parameters :math:`w^T`, leaving the observations :math:`x` as constants.

        .. math:: \frac{\delta J(w)}{\delta w^T} = xy(w|x)(\hat{y} - y(w|x))(1-y(w|x))

        dy = (1+e^{-wx})^-1 = -1(1+e^{-wx})^{-1}*(1+e^{-wx})^{-1}*-xe^{wx}
                            = x*y*(1-y)

        dp = p(1-p)




        dJ = (y-p) * dy = (y-p) * (p) * (1-p) = (yp - p^2) * (1-p) = (yp - p^2 - yp^2 + p^3)
        ddJ = p - 2p - 2yp + 2p^2


        https://stats.stackexchange.com/questions/68391/hessian-of-logistic-function

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Hessian matrix
        """

        # Format x
        x = format_x(x)

        # We only know how to compute this in 2D, right?

        # Make sure model is fitted (only valid at maximum likelihood estimate)
        if not self.is_fitted:
            raise AttributeError('model must be fit first')

        # Compute the logistic derivative y' = p * (1-p)
        # TODO eliminate observations with 0 weight
        d = logistic_derivative(x, self.coefficients)  # np.prod(self.predict_proba(x), axis=1)

        # If there is an intercept, add to x
        x = self._add_intercept_to_x(x)

        # Return the Hessian
        return -np.dot(x.T * d, x)


# Solve the logistic function
# TODO evaluate if logistic function should be placed into sigmoid with mode = 'logistic'?
def logistic(x, beta=1.):
    r"""
    Solves the logistic function.

    This function has the form :math:`y(x) = \frac{1}{1+e^{-\beta x}}`

    Parameters
    ----------
    x : ArrayLike
        Independent variable(s)
    beta : ArrayLike, int, or float
        If ArrayLike, the coefficients for the logistic function. If singular, all coefficients set to that value.
        (Default: 1.)

    Returns
    -------
    numpy.ndarray
        `y`
    """

    # Convert x to numpy array, reshaping if necessary
    x = format_x(x)

    # Number of columns in x
    n_columns = x.shape[1]

    # Fix beta
    if isinstance(beta, (int, float)):
        beta = np.repeat(beta, n_columns)
    else:
        beta = np.array(beta)

    # Return evaluation of logistic function
    return 1. / (1. + np.exp(-beta * x))


# The derivative of the logistic function
def logistic_derivative(x, beta=1.):
    r"""
    Solves the first derivative of the logistic function

    We can simplify the logistic function :math:`y(x) = \frac{1}{1+e^{-\beta x}}` by setting :math:`z = -\beta x`.

    Formal definition of the derivative:

    .. math:: \frac{\delta y}{\delta z} = \frac{\delta}{\delta z} \frac{1}{1+e^{-z}}

    Using the chain rule,

    .. math:: \frac{\delta y}{\delta z} = \frac{1}{1+e^{-z}}\frac{e^{-z}}{1+e^{-z}}

    This simplifies to,

    .. math:: \frac{\delta y}{\delta z} = y(1-y)

    Parameters
    ----------
    x : ArrayLike
        Independent variable(s)
    beta : ArrayLike, int, or float
        If ArrayLike, the coefficients for the logistic function. If singular, all coefficients are set to that value.
        (Default: 1.)

    Returns
    -------
    numpy.ndarray
        first derivative of `y`
    """

    # Solve the logistic function
    y = logistic(x, beta)

    # Return the derivative
    return y * (1. - y)


# Cost function
def _cost(self, coefficients, x, y):
    return -np.mean(0.5 * np.square(y - _function(x, coefficients)))


# Solve the logistic function
def _function(self, x, coefficients):
    return 1. / (1. + np.exp(-np.dot(coefficients * x)))

