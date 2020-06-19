import numpy as np


def generate_degrees(maxdegs, max_deg_total=None):
    """
    generates an array of monomial exponents (or degrees)
    that can be used to generate a design matrix to perform
    linear basis polynomial regression

    intput:
        maxdegs: list of len number of dimensions
            list of max deg in each dimension
        max_deg_total: int (default: None)
            max degree of a term.
            If None then will use the maximum of `maxdegs`.

    returns:
        numpy.ndarray of shape (M, dim)
        M = total number of terms
        dim = dimension
    """
    if max_deg_total == None:
        max_deg_total = np.max(maxdegs)

    # create lists of degrees for each dimension
    xsdims = [range(deg+1) for deg in maxdegs]
    # tensor product them
    xs = np.meshgrid(*xsdims)
    # ravel them into a list into a 1D array
    xs = list(map(np.ravel, xs))
    # degrees is an np.ndarray of shape (M, dim)
    degrees = np.array(list(zip(*xs)))
    # restrict the max degree of each term to be less than max_deg_total+1
    mask_total_deg = np.sum(degrees, axis=-1) < max_deg_total + 1
    # restrict the max degree of each dimension
    mask_degs = [degrees[:, i] < maxdegs[i] + 1 for i in range(len(maxdegs))]
    # make a mega mask of all masks
    mask = np.prod(np.row_stack((mask_total_deg, *mask_degs)),
                   axis=0, dtype=bool)
    return np.array(degrees[mask])


class LinearPolynomialBasisRegression(object):
    """
    Linear Basis Function Regression with polynomials
    """

    def __init__(self):
        pass

    def make_degrees(self, maxdegs, max_deg_total):
        return generate_degrees(maxdegs, max_deg_total)

    def fit(self, X, y, maxdegs, method='direct', max_deg_total=None):
        """
        input:
            X: np.ndarray. shape (N, ndim)
            y: np.ndarray. shape (N, 1)
            method: str (default: 'direct')
                'direct': np.linalg.pinv. moore-penrose pseudo inverse
                'least-squres': np.linalg.lstsq. lapack least squares algorithm

            max_deg_total: int (default: None)
                max degree of a term.
                If None then will use the maximum of `maxdegs`.

        assigns the self.w_ml attribute.
        These are the maximum likelihood coefficients or weights.

        """

        self.degrees = generate_degrees(maxdegs, max_deg_total).tolist()

        Phi = self.make_design_matrix(X, self.degrees)

        if method == 'direct':
            self.w_ml = np.dot(np.linalg.pinv(Phi), y)
        elif method == 'least-squres':
            self.w_ml = np.linalg.lstsq(Phi, y, rcond=-1)[0]

    def make_design_matrix(self, X, degrees):
        Phi = np.stack([np.prod(X**d, axis=1) for d in degrees], axis=-1)
        return Phi

    def predict(self, X):

        Phi = self.make_design_matrix(X, self.degrees)
        return np.dot(Phi, self.w_ml)

    def loss(self, X, y, method='sum-of-squares', return_information_criteria=False):
        """
        input:
            X: np.ndarray.shape (N, ndim)
            y: np.ndarray.shape (N, 1)
            method:
                'sum-of-squres':
                'RMSE':
                'MSE':
            return_information_criteria: bool Default: False
                if True then returns AIC, AICc, BIC
        """

        yhat = self.predict(X)

        def mse(y, yhat):
            """
            mean-squared-error function
            """
            errors = (y - yhat)
            loss = np.sum(errors**2, axis=0) / len(y)
            return loss

        if method == 'sum-of-squares':
            errors = (y - yhat)
            loss = np.sum(errors**2, axis=0) / 2.0
        elif method == 'MSE':
            loss = mse(y, yhat)
        elif method == 'RMSE':
            loss = np.sqrt(mse(y, yhat))
        else:
            raise ValueError(f"method = {method} not valid.")

        if return_information_criteria:

            N = len(y)
            k = len(self.degrees) + 1
            likelihood = loss
            aic = self.AIC(N, likelihood, k)
            try:
                aicc = self.AICc(N, likelihood, k)
            except ZeroDivisionError:
                aicc = np.inf
            bic = self.BIC(N, likelihood, k)

            return loss, [aic, aicc, bic]
        else:
            return loss

    def AIC(self, N, likelihood, k):
        """
        N: number of samples
        likelihood: likelihood e.g. sum-of-squares
        k: degrees of freedom
        """
        aic = N * np.log(likelihood) + 2 * k
        return aic

    def AICc(self, N, likelihood, k):
        """
        N: number of samples
        likelihood: likelihood e.g. sum-of-squares
        k: degrees of freedom
        """
        aic = self.AIC(N, likelihood, k)
        aicc = aic + (2 * k * (k+1))/(N - k - 1)
        return aicc

    def BIC(self, N, likelihood, k):
        """
        N: number of samples
        likelihood: likelihood e.g. sum-of-squares
        k: degrees of freedom
        """
        bic = N*np.log(likelihood) + k*np.log(N)
        return bic


def findpolyfit(X, y, max_degs, output_best=False, validation_data=None, method='sum-of-squares', verbose=True):
    """
    X, y data to fit
    max_degs: max deg to try in each dim. e.g., if 2D X data then max_degs could be
        array([[0, 0],
            [1, 0],
            [2, 0],
            [0, 1],
            [1, 1],
            [0, 2]])
        In practice use fits.poly.generate_degrees([2,2])

    returns a bunch of stuff included the prefereed degree
    according to min([AIC, AICc, BIC])

    if output_best=True
    then you will simply get the best fit

    """
    if validation_data:
        Xval, y_val = validation_data
        # validation losses and info crit
        v_losses = []
        v_AICs = []
        v_AICcs = []
        v_BICs = []

    lrs = []
    # training and info crit
    t_losses = []
    t_AICs = []
    t_AICcs = []
    t_BICs = []

    for deg in max_degs:
        lr = LinearPolynomialBasisRegression()
        lr.fit(X, y, maxdegs=deg)
        tloss, [taic, taicc, tbic] = lr.loss(
            X, y, method=method, return_information_criteria=True)
        t_losses.append(tloss)
        t_AICs.append(taic)
        t_AICcs.append(taicc)
        t_BICs.append(tbic)

        min_t_AICs = np.argmin(t_AICs)
        min_t_AICcs = np.argmin(t_AICcs)
        min_t_BICs = np.argmin(t_BICs)

        lrs.append(lr)

        if validation_data:
            vloss, [vaic, vaicc, vbic] = lr.loss(
                Xval, y_val, method=method, return_information_criteria=True)
            v_losses.append(vloss)
            v_AICs.append(vaic)
            v_AICcs.append(vaicc)
            v_BICs.append(vbic)
            min_v_AICs = np.argmin(v_AICs)
            min_v_AICcs = np.argmin(v_AICcs)
            min_v_BICs = np.argmin(v_BICs)

    lowest_deg_t = min([min_t_AICs, min_t_AICcs, min_t_BICs])
    lowest_loss_t = np.min(t_losses)

    if verbose:
        print(f"lowest_deg for training set = {lowest_deg_t}")
        print(f"lowest loss for training set = {lowest_loss_t}")

    if validation_data:
        lowest_deg_v = min([min_v_AICs, min_v_AICcs, min_v_BICs])
        lowest_loss_v = np.min(v_losses)

        if verbose:
            print(f"lowest_deg for validation set = {lowest_deg_v}")
            print(f"lowest loss for validation set = {lowest_loss_v}")

    if output_best:
        return lrs[lowest_deg_t], lowest_deg_t

    if validation_data:
        return lrs[lowest_deg_t], lowest_deg_t, lrs, (lowest_deg_t, t_losses, t_AICs, t_AICcs, t_BICs), (lowest_deg_v, v_losses, v_AICs, v_AICcs, v_BICs)
    else:
        return lrs[lowest_deg_t], lowest_deg_t, lrs, (lowest_deg_t, t_losses, t_AICs, t_AICcs, t_BICs)
