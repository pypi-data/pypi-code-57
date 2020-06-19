from sklearn.preprocessing import StandardScaler
import numpy as np
import warnings


def make_scalers(X):
    """
    returns a list of sklearn.preprocessing.StandardScaler
    of input matrix.

    N, M = X.shape
    N = number of entries
    M = dimensionality
    """
    N, M = X.shape

    scalers = []

    # make a scaler for each dimension
    for i in range(M):
        scalers.append(StandardScaler())
        scalers[i].fit(X[:, i].reshape(-1, 1))

    return scalers


def apply_scaler(X, scalers):
    """
    applies the scalers to X
    N, M = X.shape
    N = number of entries
    M = dimensionality
    """
    N, M = X.shape

    X_scaled = np.zeros(shape=(N, M))

    for i in range(M):
        X_scaled[:, i] = scalers[i].transform(
            X[:, i].reshape(-1, 1)).reshape(1, -1)

    return X_scaled


def apply_inverse_scaler(X_scaled, scalers):
    """
    applies the inverse scalers to X_scaled
    N, M = X.shape
    N = number of entries
    M = dimensionality
    """
    N, M = X_scaled.shape

    X = np.zeros(shape=(N, M))

    for i in range(M):
        X[:, i] = scalers[i].inverse_transform(
            X_scaled[:, i].reshape(-1, 1)).reshape(1, -1)

    return X


def scale_data(X, y, validation_data=None):
    warnings.warn("function 'scale_data' is deprecated", DeprecationWarning)

    # domain
    N, M = X.shape
    # N = number of data points
    # M = dimension

    X_scalers = []
    X_scaled = np.zeros(shape=(N, M))

    for i in range(M):
        X_scalers.append(StandardScaler())
        X_scaled[:, i] = X_scalers[i].fit_transform(
            X[:, i].reshape(-1, 1)).reshape(-1,)

    # range
    # currently only have 1 y output
    y_scaler = StandardScaler()
    y_scaled = y_scaler.fit_transform(y.reshape(-1, 1)).reshape(-1,)

    if validation_data:
        Xval, yval = validation_data

        Nval, Mval = Xval.shape
        assert M == Mval, "train and validation M not the same"
        Xval_scaled = np.zeros(shape=(Nval, Mval))
        for i in range(Mval):
            Xval_scaled[:, i] = X_scalers[i].transform(
                Xval[:, i].reshape(-1, 1)).reshape(-1,)

        yval_scaled = y_scaler.transform(yval.reshape(-1, 1)).reshape(-1,)

        return X_scaled, y_scaled, Xval_scaled, yval_scaled
    else:
        return X_scaled, y_scaled
