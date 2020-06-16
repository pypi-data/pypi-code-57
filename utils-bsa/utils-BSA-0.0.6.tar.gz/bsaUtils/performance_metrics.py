import numpy as np


def mae_metric(actual, predicted):
    # Mean Absolute Error: Calculate mean absolute error
    return abs(predicted - actual).mean()


def rmse_metric(actual, predicted):
    # Root Mean Squared Error: Calculate root mean squared error
    return np.sqrt(((predicted - actual) ** 2).mean())


def r2_metric(x_values, y_values):
    # R2 Value Coefficient of Determination
    correlation_matrix = np.corrcoef(x_values, y_values)
    correlation_xy = correlation_matrix[0, 1]
    r_squared = correlation_xy**2
    return r_squared
