"""
generic.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from .metrics import confusion_matrix, log_likelihood, performance_report
from ._utilities import _coerce_y_prob, classify

from izzy.misc import ArrayLike

from abc import ABC
import numpy as np
import pandas as pd
from scipy.linalg import lapack


# TODO model preparation workflow? For instance, if regularized, check that variables are standardized (https://www.quora.com/Why-do-we-normalize-the-data?share=1)


# GenericModel class
class GenericModel(ABC):
    """
    GenericModel class. Note that this is an abstract class.
    """

    # Initialize instance of class
    def __init__(self):
        """
        Initialize instance of the GenericModel class
        """

        # Identifier that tells us this in an izzy package
        self._package = 'izzy'

        # Number of observations and predictors
        self.n_observations = None
        self.n_predictors = None

        # Class information
        self.classes = None
        self.n_classes = None

    # Compute the log-likelihood from y_true and y_pred
    # TODO is log-likelihood model specific? Why isn't this in metrics?
    def _log_likelihood(self, y_true, y_pred, normalize=True):
        """
        Compute the log likelihood from true and predicted outcomes

        Parameters
        ----------
        y_true : ArrayLike
            True outcomes
        y_pred : ArrayLike
            Probabilistic outcomes
        normalize : bool
            Should we compute the average log likelihood per sample? (Default: True)

        Returns
        -------
        float
            log-likelihood
        """

        # Sanity checking
        if not (len(np.unique(y_true)) == self.n_classes == y_pred.shape[1]):
            raise AttributeError('n_classes must match # unique values in y_true')

        # Transform y_true into an expanded form
        y_true = np.eye(self.n_classes)[np.array([y_true], dtype='int').reshape(-1)]

        # Return log likelihood
        f = np.mean if normalize else np.sum
        return f(np.log(np.sum(y_true * y_pred, axis=1)))

    # Compute the log-loss from y_true and y_pred
    def _log_loss(self, y_true, y_pred, normalize=True):
        """
        Computes the log loss from true and predicted outcomes.

        Parameters
        ----------
        y_true : ArrayLike
            True outcomes
        y_pred : ArrayLike
            Predicted outcomes
        normalize : bool
            Should we normalize by the number of samples? (Default: True)

        Returns
        -------
        float
            log loss
        """

        return -self._log_likelihood(y_true, y_pred, normalize=normalize)

    # Classify
    def classify(self, x, classes=None, threshold=None):
        """
        Evaluate at ``x`` and then classify

        If the problem is binomial, ``threshold`` is used to perform classification. Otherwise, the class with greatest
        probability is chosen.

        See :func:`classify`

        Parameters
        ----------
        x : ArrayLike
            Independent variables
        classes : ArrayLike
            Class labels (Default: numbers from `0` to `number classes - 1`)
        threshold : float
            Decision boundary cutoff (Default: 0.5)

        Returns
        -------
        numpy.ndarray
            Predicted classes of each observation
        """

        # Evaluate model at x
        y_prob = self.evaluate(x)

        # Return classifications
        return classify(y_prob, classes, threshold)

    # Confusion matrix
    def confusion_matrix(self, x, y):
        """
        Compute the confusion matrix for the model instance

        See :func:`izzy.classification.confusion_matrix`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        pandas.DataFrame
            confusion matrix
        """

        # Format x
        x = format_x(x)

        # Return
        return confusion_matrix(y, self.predict_proba(x))

    # Evaluate the model
    def evaluate(self, x):
        return self.predict_proba(x)

    # Fit the model (NotImplemented)
    def fit(self, *args, **kwargs):
        """
        Implemented in children classes.
        """

        raise NotImplementedError

    # DOF (alias to degrees_of_freedom)
    def dof(self, x):
        """
        Alias to :func:`~degrees_of_freedom`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)

        Returns
        -------
        int
            degrees of freedom
        """

        return self.degrees_of_freedom(x)

    # Degrees of freedom (NotImplemented)
    def degrees_of_freedom(self, x):
        """
        Implemented in children classes
        """

        raise NotImplementedError

    # FIM
    def fim(self, x, y):
        """
        Alias of :func:`~fisher_information_matrix`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Fisher information matrix
        """

        return self.fisher_information_matrix(x, y)

    # Fisher
    def fisher(self, x, y):
        """
        Alias of :func:`~fisher_information_matrix`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Fisher information matrix
        """

        return self.fisher_information_matrix(x, y)

    # Fisher information matrix
    def fisher_information_matrix(self, x, y):
        """
        Computes the Fisher information matrix (FIM)

        FIM is the negative Hessian

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Fisher information matrix
        """

        return -self.hessian(x, y)

    # Compute the Hessian (NotImplemented)
    def hessian(self, x, y):
        """
        Implemented in children classes
        """

        raise NotImplementedError

    # Information (alias of fisher_information_matrix)
    def information(self, x, y):
        """
        Alias of :func:`~fisher_information_matrix`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        numpy.ndarray
            Fisher information matrix
        """

        return self.fisher_information_matrix(x, y)

    # Log likelihood
    def log_likelihood(self, x, y, normalize=True):
        """
        Compute the log-likelihood

        Mathematically, for a sample :math:`i`, we compute the likelihood :math:`L_i = p_i^{y_i} (1-p_i)^{1-y_i}.` Here,
        we compute :math:`p` as the predicted probability and :math:`y` as the true outcome.

        We can choose to `normalize` by the number of samples to get the average log likelihood per sample.

        The procedure is to use `x` to get the predicted probabilities, and then compute :math:`L_i` above.

        Note that the log likelihood depends on the specific variables in the model, i.e., cross-comparison of models is
        with different features is technically incorrect.

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)
        normalize : bool
            Should we normalize by the number of samples? (Default: True)

        Returns
        -------
        float
            log likelihood
        """

        return log_likelihood(y, self.predict_proba(x), normalize=normalize)

    # Log loss
    def log_loss(self, x, y):
        """
        Compute the log loss. This is the negative log likelihood. See :func:`~log_likelihood`

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)

        Returns
        -------
        float
            log loss
        """

        return self._log_loss(y, self.predict_proba(x))

    # Generate performance report
    def performance_report(self, x, y, threshold=0.5):
        """
        Generate a performance report for the model

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)
        threshold : float
            Decision threshold (Default: 0.5)

        Returns
        -------
        pandas.DataFrame
            performance report
        """

        # Get predicted y values from model
        y_prob = self.predict_proba(x)

        # Get the log-likelihood and degrees of freedom
        # log_likelihood = self._log_likelihood(y, y_pred)
        degrees_of_freedom = self.degrees_of_freedom(x)

        # Return performance report
        return performance_report(y, y_prob, degrees_of_freedom, threshold=threshold)

    # Predict outcome probability (NotImplemented)
    def predict_proba(self, x):
        """
        Implemented in children classes.
        """

        raise NotImplementedError

    # Standard errors of parameters
    # TODO validate standard errors for multiclass?
    def standard_errors(self, x, y, mode='R'):
        """
        Computes the standard errors of parameters

        .. math:: standard errors = \sqrt{diag(covariance matrix)}

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)
        mode : str
            See `mode` in :func:`~variance_covariance_matrix`

        Returns
        -------
        numpy.ndarray
            standard errors
        """

        return np.sqrt(np.diag(self.variance_covariance_matrix(x, y, mode=mode)))

    # Compute the variance-covariance matrix
    # TODO exclude variables with coefficient = 0
    def variance_covariance_matrix(self, x, y, mode='R'):
        r"""
        Computes the variance-covariance matrix

        The covariance matrix can be calculated in two ways.
            1. `statsmodels` method, which calculates the inverse of the Fisher information matrix (FIM). Note that FIM
               is the negative Hessian, which is equal to the second derivative of the loss function evaluated at the
               maximum likelihood estimate.
            2. `R` method, which calculates the QR decomposition of :math:`x\sqrt{d}`. Here, :math:`d` indicates
               :math:`y_{pred} (1 - y_{pred})`. If there are :math:`n` features, then the Householder reflector
               :math:`h` from QR provides the Cholesky matrix :math:`h[:n, :n]`. The inverse of this matrix gives us the
               covariance. This method, which relies on LAPACK, is *significantly* more efficient than (1).

        https://stats.stackexchange.com/questions/68080/basic-question-about-fisher-information-matrix-and-relationship-to-hessian-and-s
        https://stats.stackexchange.com/questions/224302/how-does-r-function-summary-glm-calculate-the-covariance-matrix-for-glm-model/407734#407734

        Parameters
        ----------
        x : ArrayLike
            Independent variable(s)
        y : ArrayLike
            Dependent variable(s)
        mode : str
            'statsmodels' for covariance computed from the Hessian or 'R' for the Cholesky method (Default: 'R')

        Returns
        -------
        numpy.ndarray
            variance-covariance matrix
        """

        # Right now, we only know how to solve this in the binomial case
        if self.n_classes > 2:
            raise AttributeError('can only solve if binomial')

        # If mode = 'statsmodels'
        if mode == 'statsmodels':
            # Compute Fisher information matrix (FIM)
            fim = self.fisher_information_matrix(x, y)

            # Compute covariance as the inverse of FIM
            cov = np.linalg.pinv(fim)

        # Elif mode = 'R'
        elif mode == 'R':
            # Compute y_prime = p * (1 - p)
            y_prime = np.prod(self.predict_proba(x), axis=1).reshape(-1, 1)

            # Compute QR decomposition ('raw' gets us Householder reflector)
            # TODO we need to add 1 to x here
            q, r = np.linalg.qr(x * np.sqrt(y_prime), mode='raw')

            # Compute covariance from inverse Cholesky (from LAPACK's dpotri function)
            # TODO "4" here is actually the number of columns in x
            cov = lapack.dpotri(q.T[:4, :4])[0]

        # If we get here, we have a problem
        else:
            raise AttributeError('unknown mode')

        # Return covariance
        return cov


# Format weight
def _format_weight(weight, n=None):
    # If weight and n are None, we have a problem
    if weight is None and n is None:
        raise AttributeError

    # If weight is None, fill with 1s
    if weight is None:
        weight = np.ones(n)

    # Make sure that weight is of length n
    assert len(weight) == n

    # Return
    return weight


# Format x
# TODO why is this a public function?
def format_x(x):
    # If list or tuple, convert to numpy array
    if isinstance(x, (list, tuple)):
        x = np.array(x)

    # If Series, convert to DataFrame
    if isinstance(x, pd.Series):
        x = pd.DataFrame(x)

    # If ndim = 1, convert to 2D array
    if x.ndim == 1:
        x = x.reshape(-1, 1)

    # We should now have either a pandas DataFrame or numpy array
    assert isinstance(x, (pd.DataFrame, np.ndarray))

    # ndim should also be 2
    assert x.ndim == 2

    # Return
    return x


# Determines if `engine` is an instance of an izzy model instance
def is_model_instance(engine):
    """
    Determines if `engine` is an instance of an izzy model instance.

    Parameters
    ----------
    engine : object
        An izzy model instance.

    Returns
    -------
    bool
        True or False if engine is an izzy instance.
    """

    # Result True if engine is an object that is linked to izzy package
    return isinstance(engine, object) & (getattr(engine, '_package', None) == 'izzy')


