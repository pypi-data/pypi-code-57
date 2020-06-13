"""
_utilities.py
=============
written in Python3

author: C. Lockhart

This file exists because all models require some utilities. These utility functions need to be housed in a neutral
location to prevent circular imports.
"""

import numpy as np
from typelike import ArrayLike


# Coerce sample weights
def _coerce_sample_weights(sample_weights, n_samples):
    """
    Coerce sample weights into a suitable form

    Parameters
    ----------
    sample_weights : ArrayLike
        Weight of observations
    n_samples : int
        Number of samples expected

    Returns
    -------
    numpy.ndarray
        Coerced ``sample_weights``
    """

    # If sample weights is None, set to ones
    if sample_weights is None:
        sample_weights = np.ones(n_samples)

    # Return
    return sample_weights


# Coerce y_prob
def _coerce_y_prob(y_prob, assert_binomial=False):
    """
    Coerces ``y_prob`` into a suitable form

    Parameters
    ----------
    y_prob : ArrayLike
        Predicted outcomes expressed as probabilities

    Returns
    -------
    numpy.ndarray
        Coerced ``y_prob``
    """

    # Convert y_prob to numpy array for convenience
    y_prob = np.array(y_prob)

    # If y_prob only has 1 dimensions, assume that this is a binomial problem and coerce it into [1 - y_prob, y_prob]
    if y_prob.ndim == 1:
        Warning('coercing into binomial form [1 - y_prob, y_prob]')
        y_prob = np.vstack([1. - y_prob, y_prob]).T

    # Otherwise if ndim > 2, fail
    elif y_prob.ndim > 2 :
        raise AttributeError('y_prob can be at maximum 2 dimensions')

    # Finally, if assert_binomial is true, we are expecting y_prob to have 2 columns
    if assert_binomial and y_prob.shape[1] != 2:
        raise AttributeError('y_prob expected to be suitable for binomial classification')

    # Return y_prob
    return y_prob


# Classify
def classify(y_prob, classes=None, threshold=0.5):
    """
    Classify predicted probabilistic outcomes

    Parameters
    ----------
    y_prob : ArrayLike
        Predicted outcomes expressed as probabilities. We call this ``y_prob`` instead of ``y_pred`` here to
        emphasize this point.
    classes : ArrayLike
        Names of classes (Default: integers from 1 to `n` classes)
    threshold : float
        Decision cutoff, only applied if the number of classes = 2; otherwise, the most likely class is chosen
        (Default: 0.5)

    Returns
    -------
    numpy.ndarray
        classified outcomes
    """

    # Coerce y_prob into correct form
    y_prob = _coerce_y_prob(y_prob)

    # Now that's done, compute the number of classes
    n_classes = y_prob.shape[1]

    # If classes is not set, set to sequence
    if classes is None:
        classes = np.arange(n_classes, dtype='int')

    # Otherwise, run sanity check AND ensure classes is numpy array
    else:
        if len(classes) != n_classes:
            raise AttributeError('number of elements in classes ({0}) does not match y_pred shape ({1})'
                                 .format(len(classes), n_classes))
        classes = np.array(classes)

    # If binomial, use the threshold
    if n_classes == 2:
        # If threshold isn't supplied, set to 0.5
        if threshold is None:
            threshold = 0.5

        # Classify
        y_pred = np.array(y_prob[:, 1] > threshold, dtype='int')

    # Otherwise, the class is the one with the maximum probability
    else:
        # If threshold is not None, send a Warning to make sure user is making good choices
        if threshold is not None:
            Warning('threshold is only used with binomial classifiers')

        # Classify
        y_pred = np.argmax(y_prob, axis=1)

    # Return class labels
    return classes[y_pred]
