import numpy as np
import scipy.sparse as sps
import scipy.optimize as opt
import numpy.linalg as nla
import time
import json
import math
from numpy import random


def norm_fro_err(X, W, H, norm_X):
    """ Compute the approximation error in Frobeinus norm
    norm(X - W.dot(H.T)) is efficiently computed based on trace() expansion
    when W and H are thin.
    Parameters
    ----------
    X : numpy.array or scipy.sparse matrix, shape (m,n)
    W : numpy.array, shape (m,k)
    H : numpy.array, shape (n,k)
    norm_X : precomputed norm of X
    Returns
    -------
    float
    """
    sum_squared = (
        norm_X * norm_X
        - 2 * np.trace(H.T.dot(X.T.dot(W)))
        + np.trace((W.T.dot(W)).dot(H.T.dot(H)))
    )
    return math.sqrt(np.maximum(sum_squared, 0))


def column_norm(X, by_norm="2"):
    """ Compute the norms of each column of a given matrix
    Parameters
    ----------
    X : numpy.array or scipy.sparse matrix
    Optional Parameters
    -------------------
    by_norm : '2' for l2-norm, '1' for l1-norm.
              Default is '2'.
    Returns
    -------
    numpy.array
    """
    if sps.issparse(X):
        if by_norm == "2":
            norm_vec = np.sqrt(X.multiply(X).sum(axis=0))
        elif by_norm == "1":
            norm_vec = X.sum(axis=0)
        return np.asarray(norm_vec)[0]
    else:
        if by_norm == "2":
            norm_vec = np.sqrt(np.sum(X * X, axis=0))
        elif by_norm == "1":
            norm_vec = np.sum(X, axis=0)
        return norm_vec


def normalize_column_pair(W, H, by_norm="2"):
    """ Column normalization for a matrix pair
    Scale the columns of W and H so that the columns of W have unit norms and
    the product W.dot(H.T) remains the same.  The normalizing coefficients are
    also returned.
    Side Effect
    -----------
    W and H given as input are changed and returned.
    Parameters
    ----------
    W : numpy.array, shape (m,k)
    H : numpy.array, shape (n,k)
    Optional Parameters
    -------------------
    by_norm : '1' for normalizing by l1-norm, '2' for normalizing by l2-norm.
              Default is '2'.
    Returns
    -------
    ( W, H, weights )
    W, H : normalized matrix pair
    weights : numpy.array, shape k
    """
    norms = column_norm(W, by_norm=by_norm)

    toNormalize = norms > 0
    W[:, toNormalize] = W[:, toNormalize] / norms[toNormalize]
    H[:, toNormalize] = H[:, toNormalize] * norms[toNormalize]

    weights = np.ones(norms.shape)
    weights[toNormalize] = norms[toNormalize]
    return (W, H, weights)


def norm_fro(X):
    """ Compute the Frobenius norm of a matrix
    Parameters
    ----------
    X : numpy.array or scipy.sparse matrix
    Returns
    -------
    float
    """
    if sps.issparse(X):  # scipy.sparse array
        return math.sqrt(X.multiply(X).sum())
    else:  # numpy array
        return np.linalg.norm(X)


class NMF_Base(object):

    """ Base class for NMF algorithms

    Specific algorithms need to be implemented by deriving from this class.
    """

    default_max_iter = 100
    default_max_time = np.inf

    def __init__(self):
        raise NotImplementedError(
            "NMF_Base is a base class that cannot be instantiated"
        )

    def set_default(self, default_max_iter, default_max_time):
        self.default_max_iter = default_max_iter
        self.default_max_time = default_max_time

    def run(self, A, k, init=None, max_iter=None, max_time=None, verbose=0):
        """ Run a NMF algorithm

        Parameters
        ----------
        A : numpy.array or scipy.sparse matrix, shape (m,n)
        k : int - target lower rank

        Optional Parameters
        -------------------
        init : (W_init, H_init) where
                    W_init is numpy.array of shape (m,k) and
                    H_init is numpy.array of shape (n,k).
                    If provided, these values are used as initial values for NMF iterations.
        max_iter : int - maximum number of iterations.
                    If not provided, default maximum for each algorithm is used.
        max_time : int - maximum amount of time in seconds.
                    If not provided, default maximum for each algorithm is used.
        verbose : int - 0 (default) - No debugging information is collected, but
                                    input and output information is printed on screen.
                        -1 - No debugging information is collected, and
                                    nothing is printed on screen.
                        1 (debugging/experimental purpose) - History of computation is
                                        returned. See 'rec' variable.
                        2 (debugging/experimental purpose) - History of computation is
                                        additionally printed on screen.
        Returns
        -------
        (W, H, rec)
        W : Obtained factor matrix, shape (m,k)
        H : Obtained coefficient matrix, shape (n,k)
        rec : dict - (debugging/experimental purpose) Auxiliary information about the execution
        """
        info = {
            "k": k,
            "alg": str(self.__class__),
            "A_dim_1": A.shape[0],
            "A_dim_2": A.shape[1],
            "A_type": str(A.__class__),
            "max_iter": max_iter if max_iter is not None else self.default_max_iter,
            "verbose": verbose,
            "max_time": max_time if max_time is not None else self.default_max_time,
        }
        if init != None:
            W = init[0].copy()
            H = init[1].copy()
            info["init"] = "user_provided"
        else:
            W = random.rand(A.shape[0], k)
            H = random.rand(A.shape[1], k)
            info["init"] = "uniform_random"

        if verbose >= 0:
            print("[NMF] Running: ")
            print(json.dumps(info, indent=4, sort_keys=True))

        norm_A = norm_fro(A)
        total_time = 0

        if verbose >= 1:
            his = {"iter": [], "elapsed": [], "rel_error": []}

        start = time.time()
        # algorithm-specific initilization
        (W, H) = self.initializer(W, H)

        for i in range(1, info["max_iter"] + 1):
            start_iter = time.time()
            # algorithm-specific iteration solver
            (W, H) = self.iter_solver(A, W, H, k, i)
            elapsed = time.time() - start_iter

            if verbose >= 1:
                rel_error = norm_fro_err(A, W, H, norm_A) / norm_A
                his["iter"].append(i)
                his["elapsed"].append(elapsed)
                his["rel_error"].append(rel_error)
                if verbose >= 2:
                    print(
                        "iter:"
                        + str(i)
                        + ", elapsed:"
                        + str(elapsed)
                        + ", rel_error:"
                        + str(rel_error)
                    )

            total_time += elapsed
            if total_time > info["max_time"]:
                break

        W, H, weights = normalize_column_pair(W, H)

        final = {}
        final["norm_A"] = norm_A
        final["rel_error"] = norm_fro_err(A, W, H, norm_A) / norm_A
        final["iterations"] = i
        final["elapsed"] = time.time() - start

        rec = {"info": info, "final": final}
        if verbose >= 1:
            rec["his"] = his

        if verbose >= 0:
            print("[NMF] Completed: ")
            print(json.dumps(final, indent=4, sort_keys=True))
        return (W, H, rec)

    def run_repeat(self, A, k, num_trial, max_iter=None, max_time=None, verbose=0):
        """ Run an NMF algorithm several times with random initial values
            and return the best result in terms of the Frobenius norm of
            the approximation error matrix

        Parameters
        ----------
        A : numpy.array or scipy.sparse matrix, shape (m,n)
        k : int - target lower rank
        num_trial : int number of trials

        Optional Parameters
        -------------------
        max_iter : int - maximum number of iterations for each trial.
                    If not provided, default maximum for each algorithm is used.
        max_time : int - maximum amount of time in seconds for each trial.
                    If not provided, default maximum for each algorithm is used.
        verbose : int - 0 (default) - No debugging information is collected, but
                                    input and output information is printed on screen.
                        -1 - No debugging information is collected, and
                                    nothing is printed on screen.
                        1 (debugging/experimental purpose) - History of computation is
                                        returned. See 'rec' variable.
                        2 (debugging/experimental purpose) - History of computation is
                                        additionally printed on screen.
        Returns
        -------
        (W, H, rec)
        W : Obtained factor matrix, shape (m,k)
        H : Obtained coefficient matrix, shape (n,k)
        rec : dict - (debugging/experimental purpose) Auxiliary information about the execution
        """
        for t in iter(range(num_trial)):
            if verbose >= 0:
                print("[NMF] Running the {0}/{1}-th trial ...".format(t + 1, num_trial))
            this = self.run(A, k, verbose=(-1 if verbose is 0 else verbose))
            if t == 0:
                best = this
            else:
                if this[2]["final"]["rel_error"] < best[2]["final"]["rel_error"]:
                    best = this
        if verbose >= 0:
            print("[NMF] Best result is as follows.")
            print(json.dumps(best[2]["final"], indent=4, sort_keys=True))
        return best

    def iter_solver(self, A, W, H, k, it):
        raise NotImplementedError

    def initializer(self, W, H):
        return (W, H)


class NMF_HALS(NMF_Base):

    """ NMF algorithm: Hierarchical alternating least squares

    A. Cichocki and A.-H. Phan, Fast local algorithms for large scale
    nonnegative matrix and tensor factorizations, IEICE Transactions on
    Fundamentals of Electronics, Communications and Computer Sciences, vol.
    E92-A, no. 3, pp. 708-721, 2009.
    """

    def __init__(self, default_max_iter=100, default_max_time=np.inf):
        self.eps = 1e-16
        self.set_default(default_max_iter, default_max_time)
        self.debug = {}

    def initializer(self, W, H):
        #  W, H, weights = normalize_column_pair(W, H)
        return W, H

    def iter_solver(self, A, W, H, k, it):
        import copy

        D = self.debug
        D["X_orig"] = copy.deepcopy(A)
        D["W_orig"] = copy.deepcopy(W)
        D["H_orig"] = copy.deepcopy(H).T

        AtW = A.T.dot(W)
        WtW = W.T.dot(W)

        D["XtW"] = copy.deepcopy(AtW)
        D["WtW"] = copy.deepcopy(WtW)

        for kk in iter(range(0, k)):
            temp_vec = H[:, kk] + AtW[:, kk] - H.dot(WtW[:, kk])
            H[:, kk] = np.maximum(temp_vec, self.eps)

        D["H_update"] = copy.deepcopy(H).T

        AH = A.dot(H)
        HtH = H.T.dot(H)

        D["XHt"] = copy.deepcopy(AH)
        D["HHt"] = copy.deepcopy(HtH)

        for kk in iter(range(0, k)):
            temp_vec = W[:, kk] * HtH[kk, kk] + AH[:, kk] - W.dot(HtH[:, kk])
            W[:, kk] = np.maximum(temp_vec, self.eps)
            #  print("THEIRS W[:, {}]:\n{}\n".format(kk, W[:, kk]))
            ss = nla.norm(W[:, kk])
            if ss > 0:
                W[:, kk] = W[:, kk] / ss

        D["W_update"] = copy.deepcopy(W)

        return (W, H)


class NMF_MU(NMF_Base):

    """ NMF algorithm: Multiplicative updating

    Lee and Seung, Algorithms for non-negative matrix factorization,
    Advances in Neural Information Processing Systems, 2001, pp. 556-562.
    """

    def __init__(self, default_max_iter=500, default_max_time=np.inf):
        self.eps = 1e-16
        self.set_default(default_max_iter, default_max_time)

    def iter_solver(self, A, W, H, k, it):
        AtW = A.T.dot(W)
        HWtW = H.dot(W.T.dot(W)) + self.eps
        H = H * AtW
        H = H / HWtW

        AH = A.dot(H)
        WHtH = W.dot(H.T.dot(H)) + self.eps
        W = W * AH
        W = W / WHtH

        return (W, H)
