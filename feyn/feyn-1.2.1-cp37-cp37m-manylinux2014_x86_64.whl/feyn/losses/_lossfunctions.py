import numpy as np

def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute the mean absolute error loss.

    Arguments:
        y_true -- Ground truth (correct) target values.
        y_pred -- Predicted values.

    Returns:
        nd.array -- The losses as an array of floats.
    """
    return np.mean(np.abs(y_true - y_pred))

mean_absolute_error.c_derivative = "mean_absolute_error"

def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute the mean squared error loss. 
    
    This is the default loss function used in fitting and selecting graphs from QGraphs.

    Arguments:
        y_true -- Ground truth (correct) target values.
        y_pred -- Predicted values.

    Returns:
        nd.array -- The losses as an array of floats.
    """
    return np.mean(np.power((y_pred - y_true), 2))

mean_squared_error.c_derivative = "mean_squared_error"

def categorical_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute the crossentropy loss between the labels and predictions.

    This is a good alternative choice for binary classification problems. If cannot be used for fitting QGraphs with output data that is not binary. Doing so will result in a RuntimeError.

    Arguments:
        y_true -- Ground truth (correct) target values.
        y_pred -- Predicted values.

    Returns:
        nd.array -- The losses as an array of floats.
    """
    epsilon = 1e-7
    y_pred = np.clip(y_pred, epsilon, 1. - epsilon)
    N = y_pred.shape[0]
    y_true = y_true.astype(int)
    if (y_true>1).any() or (y_true<0).any():
        raise RuntimeError("Categorical loss function requires boolean truth values")

    return (1/N) * np.sum(-y_true*np.log(y_pred) - (1-y_true)*np.log(1-y_pred))


categorical_cross_entropy.c_derivative = "categorical_cross_entropy"


def _get_loss_function(name_or_func):
    # The loss function was provided instead of the name.
    # Return the function itself, if it is among the
    # known loss functions.
    if type(name_or_func).__name__ == "function":
        name_or_func = name_or_func.__name__

    if (name_or_func == "mean_absolute_error"):
        return mean_absolute_error
    if (name_or_func == "mean_squared_error"):
        return mean_squared_error
    if (name_or_func == "categorical_cross_entropy"):
        return categorical_cross_entropy

    raise ValueError("Unknown loss provided")
