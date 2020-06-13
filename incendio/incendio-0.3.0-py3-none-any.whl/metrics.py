# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/03_metrics.ipynb (unless otherwise specified).

__all__ = ['percent_positive', 'mean_soft_prediction', 'std_soft_prediction', 'batch_size']


# Cell
def percent_positive(y_true, y_pred):
    """Compute the percent of predictions that are positive. This
    can help us identify when a model is predicting all ones or zeros.
    """
    return (y_pred == 1).float().mean()


# Cell
def mean_soft_prediction(y_true, y_score):
    """Compute the mean predicted probability."""
    return y_score.mean()


# Cell
def std_soft_prediction(y_true, y_score):
    """Compute the standard deviation of the predicted
    probabilities. This helps us identify if the model is
    always predicting roughly the same probability.
    """
    return y_score.std()


# Cell
def batch_size(y_true, y_pred):
    """Count the number of items in the current batch."""
    return y_true.shape[0]