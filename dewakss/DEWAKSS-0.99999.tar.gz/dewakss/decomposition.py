import scanpy as _sc
import scipy as _sp
import numpy as _np
from sklearn.utils import check_X_y as _check_X_y, check_array as _check_array
from scipy.sparse import issparse as _issparse, csr as _csr
# from sklearn.utils.validation import _is_arraylike, check_is_fitted
from sklearn.model_selection import ShuffleSplit as _ShuffleSplit
# from sklearn.utils.extmath import safe_sparse_dot as _safe_sparse_dot
from sklearn.metrics import mean_squared_error as _mse, r2_score as _r2
from copy import deepcopy
from .utils import ftt
# , calc_metrics
import warnings as _warnings
import matplotlib.pyplot as _plt
import time as _time

# _MKL_EXIST = True
# try:
#     from sparse_dot_mkl.sparse_dot import dot_product_mkl as _dot_product
# except ImportError:
#     # _warnings.simplefilter('error', UserWarning)

#     _warnings.warn("Couldn't find the intel math kernel library (MKL).\nThis might slow down this computation\nMake sure to add the mkl libraries to the LD_LIBRARY_PATH.")
#     _MKL_EXIST = False


def _rescale(X, rescaler={_sc.pp.scale: {"zero_center": False}}):

    for scalefun, params in rescaler.items():
        if "sparse" in params and params['sparse']:
            P = params.copy()
            __ = P.pop('sparse', None)
            X.data = scalefun(X.data, **P).copy()
        else:
            X = scalefun(X, **params)

    return X


def _Xsplit(X, strategy):

    if strategy == 'uniform':
        X_masked, X_target = _uniform(X.copy())
    elif strategy == 'binomial':
        X_masked, X_target = _binomial(X.copy())

    return X_masked, X_target


def _binomial(X, p=0.5):
    """Split the data as in noise2self into one masked and one target data matrix using binomial probability splitting strategy.

    :param X: ndarray, csr_matrix
    :returns: X_masked, X_target
    :rtype: ndarray, csr_matrix

    """

    binom = _sp.random.binomial
    if _issparse(X):
        X_target = binom(X.data.astype(int), p)

        X_masked = X.data - X_target

        X_target = _csr.csr_matrix((X_target, X.nonzero()))
        X_masked = _csr.csr_matrix((X_masked, X.nonzero()))

        X_target.eliminate_zeros()
        X_masked.eliminate_zeros()
        X_masked.data = X_masked.data.astype(float)
        X_target.data = X_target.data.astype(float)

    else:
        X_target = _sp.array([])
        for x in X:
            y = (binom(x, p)).reshape((1, -1))
            if X_target.size == 0:
                X_target = y
            else:
                X_target = _sp.append(X_target, y, 0)

        X_masked = X - X_target

        X_masked = X_masked.astype(float)
        X_target = X_target.astype(float)

    return X_masked, X_target


def _uniform(X, **kwargs):
    """Split the data as in noise2self into one masked and one target data matrix using uniform probability splitting strategy.

    :param X: ndarray, csr_matrix
    :returns: X_masked, X_target
    :rtype: ndarray, csr_matrix

    """

    from scipy.stats import uniform

    gtn = uniform()

    if _issparse(X):
        rn = gtn.rvs(X.data.shape)
        X_target = X.data * rn
        X_masked = X.data - X_target

        X_target = _csr.csr_matrix((X_target, X.nonzero()))
        X_masked = _csr.csr_matrix((X_masked, X.nonzero()))

    else:
        X_target = _sp.array([])
        for x in X:
            rn = gtn.rvs(x.shape)
            y = (x * rn).reshape((1, -1))
            if X_target.size == 0:
                X_target = y
            else:
                X_target = _sp.append(X_target, y, 0)

        X_masked = X - X_target

    return X_masked, X_target


def decomposition_wrapper(cls):
    """A wrapper for decomposition methods following the format in scikit-learn. However due to different complexities of the inverse_transform and transform. It's unlikely that this is currently a general solution

    :param cls: The scikit-learn decomposition class to use as a base. Recommendend TruncatedSVD
    :returns: DEWAKSSDecomposition class.
    :rtype: class

    Example:
    ========
    from sklearn.decomposition import TruncatedSVD

    TruncatedSVD = decomposition_wrapper(TruncatedSVD)
    pca = TruncatedSVD()
    pca.fit(X)

    """

    class MCVDecomposition(cls):

        def __init__(self, strategy='binomial', rescaler={_sc.pp.normalize_per_cell: {"copy": True}, ftt: {'copy': True}}, subsample=None, random_state=42, n_components=50, layer='X', test_size=None, run2best=False, verbose=False, safe_trans=True, **super_params):
            """DEWAKSSDecomposition class. Self supervised optimal PCA selection.

            :param strategy: Only 'binomial' is supported.
            :param rescaler: A nested dictionary with functions as keys and arguments as sub dictionaries.
                             Will be applied to the data before decomposition is applied.
                             If set to None will select from the strategy (not implemented).
                             Default: {_sc.pp.normalize_per_cell: {}, ftt: {}}
            :param subsample: Use a subsample of data for optimal component selection. Default None.
            :param random_state: use this random state, Default 42.
            :param n_components: Number of components that should be tested (or computed).
            :param layer: Use this layer if input data is AnnData object.
            :param test_size: Should be 1-subsample. Default None.
            :returns: self.
            :rtype: DEWAKSSDecomposition class.

            Adds the
            :self.optimal_: property with the number of components that minimizes the MSE.
            :self.mse_: the MSE for all tests.
            :self.r2: the R2 of all tests.
            :self.rank_range: the PC order tested.

            Alternatives for the rescale could be e.g.
            with:
            import scanpy as sc
            rescaler={sc.pp.normalize_per_cell: {}, sc.pp.log1p: {}}
            rescaler={sc.pp.normalize_per_cell: {}, sc.pp.sqrt: {}}
            rescaler={sc.pp.normalize_per_cell: {}, sc.pp.log1p: {}, sc.pp.scale: {'copy': True, 'zero_center': False}}

            """

            super().__init__(n_components=n_components, random_state=random_state, **super_params)
            self.strategy = strategy
            self.verbose = verbose
            self.safe_trans = safe_trans

            if rescaler is None:
                if strategy == 'uniform':
                    rescaler = {_sc.pp.scale: {"zero_center": False}}
                elif strategy == 'binary':
                    rescaler = {_sc.pp.scale: {"zero_center": True}}
                elif strategy == 'binomial':
                    rescaler = {_sc.pp.normalize_per_cell: {"counts_per_cell_after": None, "copy": True}, ftt: {'copy': True}}
                else:
                    rescaler = {_sc.pp.scale: {"zero_center": False}}

            if run2best:
                _warnings.warn(f'Using run2best = {run2best} is not stable, and not recommended\nproceed with caution.')
            self.run2best = run2best
            self.rescaler = rescaler

            self.layer_ = layer

            self.subsample = subsample
            if test_size is None and (subsample is not None):
                self.test_size = 1 - subsample
            else:
                self.test_size = test_size

        def _trans_inv_trans(self, X, decomper):

            # if self.safe_trans and _MKL_EXIST:
            #     prediction = _np.dot(_dot_product(X.astype(float), decomper.components_.T.astype(float)), decomper.components_)
            # else:

            prediction = decomper.inverse_transform(decomper.transform(X))

            return prediction

        def extractX(self, data):

            if self.layer_ not in [None, 'X', 'raw']:
                if self.layer_ not in data.layers.keys():
                    raise KeyError('Selected layer: {} is not in the layers list. The list of '
                                   'valid layers is: {}'.format(self.layer_, data.layers.keys()))
                matrix = data.layers[self.layer_]
            elif self.layer_ == 'raw':
                matrix = data.raw.X
            else:
                matrix = data.X

            return matrix

        def fit(self, X_m, X_t=None, use_genes=None):
            """Fit function

            :param X_m: Should be a count matrix
            :param X_t: if supplied will skip the split of X_m and assume these matrices are correctly split. Default None.
            :param use_genes: boolean or indice vector to determine what variables to use for the analysis. E.g. Highly variable genes.
            :returns: self
            :rtype: DEWAKSSDecomposition

            """

            ncomp = self.n_components
            if X_t is not None:
                X_m, X_t = _check_X_y(X_m, X_t, accept_sparse=['csr', 'csc', 'coo'], force_all_finite=True, multi_output=True)
                if use_genes is not None:
                    X_m, X_t = X_m[:, use_genes], X_t[:, use_genes]
            else:
                X_m = _check_array(X_m, accept_sparse=['csr', 'csc', 'coo'], force_all_finite=True)
                if use_genes is not None:
                    X_m = X_m[:, use_genes]

            if X_t is None:
                X_m, X_t = _Xsplit(X_m, self.strategy)
                X_m = _rescale(X_m, rescaler=self.rescaler)
                X_t = _rescale(X_t, rescaler=self.rescaler)

            if self.subsample is not None:
                rs = _ShuffleSplit(1, test_size=self.test_size, train_size=self.subsample, random_state=self.random_state)
                train_index, test_index = next(rs.split(X_m))
                super().fit(X_m[train_index, :])
            else:
                super().fit(X_m)

            decomper = deepcopy(self)

            mses = []
            r2s = []
            rank_range = _sp.arange(1, self.n_components)
            past_mse = _sp.inf
            rr = []
            start_time = _time.time()
            # loopt = _time.time()
            loopt = 0
            for k in rank_range:

                decomper.n_components = k
                decomper.components_ = self.components_[:k, :]

                currt = _time.time()
                if self.verbose:
                    print(f'Working on component: {k} of {ncomp}, ET too completion: {(1-k/ncomp)*ncomp*loopt:3.2f}s', end='\r')

                if self.subsample is not None:
                    # prediction = decomper.inverse_transform(decomper.transform(X_m[test_index, :]))
                    prediction = self._trans_inv_trans(X_m[test_index, :], decomper)
                    # current_mse, current_r2, __, __ = calc_metrics(X_t, prediction)
                    current_mse = _mse(X_t[test_index, :].toarray() if _issparse(X_t) else X_t[test_index, :], prediction)
                    current_r2 = _r2(X_t[test_index, :].toarray() if _issparse(X_t) else X_t[test_index, :], prediction)
                else:
                    # prediction = decomper.inverse_transform(decomper.transform(X_m))
                    prediction = self._trans_inv_trans(X_m, decomper)
                    # current_mse, current_r2, __, __ = calc_metrics(X_t, prediction)
                    current_mse = _mse(X_t.toarray() if _issparse(X_t) else X_t, prediction)
                    current_r2 = _r2(X_t.toarray() if _issparse(X_t) else X_t, prediction)

                loopt = _time.time() - currt

                if past_mse < current_mse:
                    if self.run2best:
                        self._extime = _time.time() - start_time
                        break

                past_mse = current_mse
                mses.append(current_mse)
                r2s.append(current_r2)
                rr.append(k)

            self.mse_ = mses
            self.r2_ = r2s
            self.optimal_ = rank_range[_sp.argmin(mses)]
            self.rank_range = rr

            if self.run2best:
                self.components_ = decomper.components_.copy()
                self.n_components = decomper.n_components.copy()

            self._extime = _time.time() - start_time
            return self

        def plot(self, ax=None, metric='mse', verbose=None, skipfirst=False):
            """Simple overview plot of fit performance

            :param ax: a figure axis, Default None
            :param metric: one of 'mse' or 'r2'
            :param verbose: Should we use annotation on plot. If None will use the DEWAKSS default. Default None
            :returns: (figure, ax) if ax is not None else (None, ax)
            :rtype: matplotlib axis

            """

            if ax is None:
                fig = _plt.figure(figsize=(5, 3), constrained_layout=True)
                axs = fig.subplots(1, 1)
            else:
                axs = ax

            steps = self.rank_range
            mse = self.mse_
            r2 = self.r2_
            evr = self.explained_variance_ratio_[steps]
            evcs = _sp.cumsum(self.explained_variance_ratio_)[steps]

            besti = self.optimal_

            steps, mse, r2 = (steps[1:], mse[1:], r2[1:]) if skipfirst else (steps, mse, r2)

            if metric == 'mse':
                axs.plot(steps, mse)
                axs.set_ylabel('MSE')
            elif metric == 'r2':
                axs.plot(steps, r2)
                axs.set_ylabel(r'$R^2$')
            elif metric == 'evr':
                axs.plot(steps, evr)
                axs.set_ylabel(r'EV ratio')
            elif metric == 'evcs':
                axs.plot(steps, evcs)
                axs.set_ylabel(r'EV cumsum')

            axs.set_xlabel('components')
            axs.grid()

            if not self.run2best:
                ylims = _sp.array(axs.get_ylim())
                axs.vlines(besti, *(ylims), zorder=500, linestyle=':')

            if verbose is None:
                verbose = self.verbose

            if verbose:
                texttoshow = f"optimal i: {besti:d},\nt: {self._extime:10.3g}"
                _plt.text(0.9, 0.9, texttoshow, fontsize=12, horizontalalignment='right', transform=axs.transAxes)

            return (fig, axs) if (ax is None) else (None, axs)

    return MCVDecomposition
