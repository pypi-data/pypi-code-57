import scanpy as _sc
import scipy as _sp
import numpy as _np
import pandas as _pd
from anndata import AnnData as _AnnData
from scipy.sparse import issparse as _issparse, csr as _csr
import scipy.sparse as _scs
# from sklearn.utils import check_X_y as _check_X_y, check_array as _check_array
# from sklearn.utils.validation import _is_arraylike
from scipy.stats import chi2 as _chi2
from sklearn.utils.validation import check_is_fitted as _check_is_fitted
import warnings as _warnings
from sklearn.base import BaseEstimator as _BaseEstimator, TransformerMixin as _TransformerMixin
from scvelo.preprocessing.neighbors import select_connectivities as _select_connectivities, select_distances as _select_distances
import time as _time
import matplotlib.pyplot as _plt
import seaborn as _sns
from sklearn.model_selection import ShuffleSplit as _ShuffleSplit
from scanpy.neighbors import _compute_connectivities_umap

_MKL_EXIST = True
try:
    from sparse_dot_mkl.sparse_dot import dot_product_mkl as _dot_product
except ImportError:
    # _warnings.simplefilter('error', UserWarning)

    _warnings.warn("Couldn't find the intel math kernel library (MKL).\nThis may slow down DEWAKSS significantly\nMake sure to add the mkl libraries to the LD_LIBRARY_PATH to avoid slowing down computations.")
    _MKL_EXIST = False


def _get_indices_distances_from_sparse_matrix(D, con):
    n_neighbors = max([i.data.shape[0] for i in con]) + 1
    indices = _np.zeros((con.shape[0], n_neighbors), dtype=int) - 1
    distances = _np.zeros((D.shape[0], n_neighbors), dtype=D.dtype) - 1
    n_neighbors_m1 = n_neighbors - 1
    for i in range(indices.shape[0]):
        neighbors = con[i].nonzero()  # 'true' and 'spurious' zeros
        indices[i, 0] = i
        distances[i, 0] = 0
        # account for the fact that there might be more than n_neighbors
        # due to an approximate search
        # [the point itself was not detected as its own neighbor during the search]
        if len(neighbors[1]) > n_neighbors_m1:
            sorted_indices = _np.argsort(D[i][neighbors].A1)[:n_neighbors_m1]
            indices[i, 1:] = neighbors[1][sorted_indices]
            distances[i, 1:] = D[i][
                neighbors[0][sorted_indices], neighbors[1][sorted_indices]]
        else:
            indices[i, 1:(len(neighbors[1]) + 1)] = neighbors[1]
            distances[i, 1:(len(neighbors[1]) + 1)] = D[i][neighbors]

    return indices, distances, n_neighbors


def _matmul(A, B):
    """A wrapper for matrix mutiplication. Should handle most types of 2d arrays.

    :param A: A matrix
    :param B: A matrix
    :returns: A matrix
    :rtype: matrix, ndarray

    """

    if (not _issparse(A)) and _issparse(B):
        C = A @ B
    else:
        if _MKL_EXIST:
            C = _dot_product(A, B)
        else:
            C = A @ B

    return C


class DEWAKSS(_BaseEstimator, _TransformerMixin):

    def __init__(self,
                 data=None,
                 n_neighbors=None,
                 n_pcs=None,
                 mode='distances',
                 use_global_err=True,
                 iterations=1,
                 use_layer='X',
                 create_layer='Ms',
                 neighbor_alg=_sc.pp.neighbors,
                 weighted=True,
                 keep0=False,
                 init_diag=0,
                 set_diag=0,
                 symmetrize=True,
                 denoise_type='mean',
                 run2best=True,
                 verbose=True,
                 modest=None,
                 replace_graph=True,
                 detect_outlier=None,
                 memoryefficient=True,
                 subset=False,
                 random_state=42,
                 max_dense=0.4,
                 decay=1,
                 settype=_sp.float32,
                 pca_args={'use_highly_variable': False},
                 neighbor_args={},
                 alpha=0.05,
                 copy=True):
        """DEWAKSS does Denoising of Expression data with
        Weighted Affinity Kernel and Self Supervision.

        DEWAKSS accepts an Affinity Kernal matrix to determine what
        datapoints should be averaged over and uses noise2self to
        determine what level of denoising most informative.

        Parameters marked with [*] will only affect the input if
        data is an AnnData object [pip insall anndata]

        Params:
        -------
        data: an object containing the data to be denoised [AnnData object, numpy.ndarray, scipy.csr_matrix].
        use_layer: [*] determine what layer should be used as the data. Default 'X'
        create_layer: [*] name of layer in AnnData object to be create. Default 'Ms'
        n_neighbors: number of k nearest neighbors to use and iterate over.
        n_pcs: number of PCs to use and iterate through.
        mode: [*] 'distances' or 'connectivities'. If data is AnnData will select the appropriate measure for the Affinity graph. Default: 'distances'.
        use_global_err: Boolean. If global neighbors should be used or local cell vise error. Default True.
        iterations: Number of diffusion steps to perform if run2best is False. Parameter will be ignored if other value is supplied in the fit function. Default is None (1) step, i.e. the weighted kNN is used without diffusion.
        neighbor_alg: function call or string. if it's a string it has to be in SCANPY external module. Has to be able to take the argument n_neighbors and n_pcs.
        weighted: [*] If False will use the initial Affintiy matrix with equally weighted neighbor influences. This will change when diffusing.
        keep0: Preserve 0 entries in the data matrix during iteration and transformation, Default False.
        init_diag: Explicitly set the diagonal entries of the initial affinity matrix to this value
                          before transforming to right stochastic matrix. Default 0
        set_diag: Explicitly set the diagonal entries of the affinity matrix at each step to this value before transforming to right stochastic matrix. Default 0
        symmetrize: Transform the initial affinity matrix to a symmetric matrix by summing M + M.T. Default True
        denoise_type: what operation should be performed to denoise, ['mean', 'median']. Default 'mean'. (median is very slow!)
        run2best: Should we stop as soon as optimal is reached. Default True.
        verbose: Should we print progress at each iteration step. Should we annotate the plot. Default True.
        modest: how much should the original datapoint be wighted when transforming, default None, float, or numpy function string e.g. 'max', 'median', 'mean', 'min' relative to neighbors.
        memoryefficient: Should we try to be memory efficient by keeping data sparse. Default True
        subset: Should we select a subset of genes to fit on. Accepts float or int or bool or array. Default False.
        random_state: For random operations what random state should be used, Default 42
        max_dense: At what density should we transform our Affinity matrix to dense. Default 0.4
        decay: Parameter that tries to mimic MAGIC decay parameter. However it is not the same. Set at own risk. Default 1
        settype: type that the graph should be converted too. Default numpy.float32
        returns: self
        rtype: DEWAKSS

        """

        super(DEWAKSS, self).__init__()

        self.random_state = random_state
        self.memoryefficient = memoryefficient
        self.subset = subset
        self.max_dense = max_dense
        self.use_layer = use_layer
        self.create_layer = create_layer
        self.mode = mode
        self.set_diag = set_diag
        self.init_diag = init_diag
        self.decay = decay
        self.weighted = weighted
        self.use_global_err = use_global_err
        self._local_optima_fit = False
        self.modest = modest
        self.detect_outlier = detect_outlier

        self._alpha = alpha

        self.denoise_type = denoise_type
        self.run2best = run2best
        self.verbose = verbose

        self.iterations = 1 if (iterations is None) else iterations
        self.keep0 = keep0
        self.symmetrize = symmetrize
        self._settype = settype
        self.n_neighbors = n_neighbors
        self.n_pcs = n_pcs
        self.pca_args = pca_args
        self.neighbor_args = neighbor_args
        self._copy_input = copy
        self.replace_graph = replace_graph

        self._parse_input_alg(neighbor_alg)

        self._parse_input_data(data)

    def _parse_input_alg(self, neighbor_alg):

        if isinstance(neighbor_alg, str):
            name = neighbor_alg
        else:
            name = neighbor_alg.__name__

        if name == 'neighbors':
            self.neighbor_alg = _sc.pp.neighbors
        elif name == 'bbknn':
            self.neighbor_alg = self._bbknn_wrapper
        else:
            self.neighbor_alg = getattr(_sc.external.pp, name) if type(neighbor_alg, str) else neighbor_alg

    def _bbknn_wrapper(self, data, n_neighbors=3, **kwargs):
        '''bbknn wrapper function to handle number of neighbors use in bbknn.
        Number of neighbors will be divided by the number of batches with a min of 1 per batch, rounded up.
        https://doi.org/10.1093/bioinformatics/btz625
        '''

        if 'batch_key' in kwargs:
            nb = data.obs[kwargs['batch_key']].cat.categories.shape[0]
        else:
            nb = data.obs['batch'].cat.categories.shape[0]

        n_neighbors = _np.max([_np.ceil(n_neighbors / float(nb)), 1]).astype(int)

        _sc.external.pp.bbknn(data, neighbors_within_batch=n_neighbors, **kwargs)

    def _parse_input_data(self, data):

        if data is None:
            pass
        elif not isinstance(data, _AnnData):
            data = _sc.AnnData(data)
        else:
            data = data.copy() if self._copy_input else data

        # mode = self.mode
        if self.n_pcs is None:
            maxpcs = data.shape[0]
            self.n_pcs = _sp.floor(_sp.logspace(_sp.log10(10), _sp.log10(min(200, maxpcs)), 10)).astype(int)

        n_pcs = _np.max(self.n_pcs) if hasattr(self.n_pcs, "__iter__") else self.n_pcs

        if self.n_neighbors is None:
            maxN = data.shape[0]
            self.n_neighbors = _sp.floor(_sp.logspace(_sp.log10(5), _sp.log10(min(400, maxN)), 10)).astype(int)

        # n_neighbors = _sp.max(self.n_neighbors) if hasattr(self.n_neighbors, "__iter__") else self.n_neighbors

        N_computed = False
        if 'neighbors' in data.uns_keys():
            precomp_neighbors = data.uns['neighbors']['params']['n_neighbors']
            N_tmp = (_np.max(self.n_neighbors) if hasattr(self.n_neighbors, "__iter__") else self.n_neighbors)
            if precomp_neighbors >= N_tmp:
                N_computed = True

        pca_computed = False
        if 'X_pca' in data.obsm_keys():

            npcs = data.obsm['X_pca'].shape[1]
            if npcs >= n_pcs:
                pca_computed = True

        if not pca_computed:

            if self.verbose:
                print(f'Computing PCA with components = {n_pcs}')
            _sc.pp.pca(data, n_comps=n_pcs, **self.pca_args)
            if self.verbose:
                print(f'PCs computed')

        self._data = data
        # self._graph = data.uns['neighbors'][mode].copy().astype(self._settype)
        # self.n_neighbors = n_neighbors

    def _make_dense(self, X):

        if not self.memoryefficient and _issparse(X):
            X = X.A

        return X

    def _row_stochastic(self, C):

        cs = C.sum(1)
        cs[cs == 0] = 1
        if _issparse(C):
            C = C.multiply(1. / cs)
            C.eliminate_zeros()
            C = _csr.csr_matrix(C)
        else:
            # https://stackoverflow.com/questions/18522216/multiplying-across-in-a-numpy-array
            C = C * (1. / cs)[:, _sp.newaxis]

        return C

    def get_connectivities(self, data, n_neighbors=None):

        mode = self.mode
        decay = self.decay
        symmetrize = self.symmetrize
        set_diag = self.init_diag

        if isinstance(data, _AnnData):
            C = data.uns['neighbors'][mode].copy()
            if n_neighbors is None:
                n_neighbors = data.uns['neighbors']['params']['n_neighbors']
        else:
            C = data

        C = _select_connectivities(C, n_neighbors) if mode == 'connectivities' else _select_distances(C, n_neighbors)

        if self.weighted:
            if mode == 'distances':
                # C.data = C.data / C.data.mean()
                meand = _sp.array([d.data.mean() for d in C])
                C = C.multiply(1. / meand)
                C.data = _sp.power(C.data, decay)  # TODO: Should this be below C.multiply above instead?
                C.data = _sp.exp(-1 * C.data)
                if set_diag is not None:
                    C.setdiag(set_diag)

            else:
                if set_diag is not None:
                    C.setdiag(set_diag)

                C.data = _sp.power(C.data, decay)

            if symmetrize:
                C = (C + C.T) / 2  # Symmetrize.

            connectivities = C

        else:
            if symmetrize:
                C = (C + C.T) / 2  # Symmetrize.
            connectivities = (C > 0).astype(self._settype)

        connectivities = self._row_stochastic(connectivities).astype(self._settype)  # If this is failing, look at the solution I commented out above (cs = C.sum(1)....)
        connectivities.eliminate_zeros()

        if _issparse(connectivities):
            connectivities.tocsr().astype(self._settype)

        return connectivities

    def _apply_denoising(self, X, connectivities=None, transformtype=None):

        if transformtype is None:
            denoise_type = self.denoise_type
        else:
            denoise_type = transformtype

        if connectivities is None:
            connectivities = self.opt_connectivities.copy()

        if self.keep0:
            Xtmp = _sp.abs(X).astype(bool).astype(self._settype).copy()

        if denoise_type == 'mean':

            if self.modest is not None and hasattr(self, '_extime'):  # Meaning it has been fitted.
                if isinstance(self.modest, (int, float)):
                    connectivities = self._renormalize(connectivities, set_diag=self.modest)
                elif isinstance(self.modest, str):
                    vecvals = []
                    for row in connectivities:
                        method = getattr(_np, self.modest)
                        vals = method(row.data)
                        vecvals.append(vals)
                    vecvals = _sp.sparse.spdiags(vecvals, 0, len(vecvals), len(vecvals))
                    connectivities = self._renormalize(connectivities + vecvals)
                else:
                    if self.modest:
                        vecvals = connectivities.astype(bool).sum(1).A1
                        vecvals = _sp.sparse.spdiags(1 / vecvals, 0, len(vecvals), len(vecvals))
                        connectivities = self._renormalize(connectivities + vecvals)

            X_out = _matmul(connectivities, X)

        elif denoise_type == 'median':
            D = []
            for r in connectivities:

                if _issparse(X):
                    rind = r.nonzero()[1] if _issparse(r) else r.nonzero()[0]
                    D.append(_csr.csr_matrix(_sp.median(X[rind, :].A, 0)))

                else:
                    rind = r.nonzero()[1] if _issparse(r) else r.nonzero()[0]
                    D.append(_sp.median(X[rind, :], 0))

            if _issparse(X):
                X_out = _scs.vstack(D)
            else:
                X_out = _sp.vstack(D)

        if self.keep0:
            X_out = _sp.multiply(X_out, Xtmp)

        return X_out

    def _renormalize(self, connectivities, set_diag=None):

        if set_diag is None:
            set_diag = self.set_diag

        if set_diag is not None:
            if _issparse(connectivities):
                connectivities.setdiag(set_diag)
            else:
                _np.fill_diagonal(connectivities, set_diag)

        if not self.weighted:
            connectivities = connectivities.astype(bool).astype(self._settype)

        connectivities = self._row_stochastic(connectivities)

        return connectivities

    def _diffuse(self, connectivities):

        tmp = _matmul(connectivities, self.connectivities)
        return self._renormalize(tmp)

    def calc_metrics(self, T, P=None):
        """Calculate MSE and R2"""

        M, N = T.shape
        if P is None:
            P = _csr.csr_matrix((M, N))

        sstot_cells = _sp.array([((i.A - i.mean() if _issparse(i) else i - i.mean()).flatten()**2).sum() for i in T])
        sstot = _sp.sum(sstot_cells)

        if any([not _issparse(T), not _issparse(P)]):
            __ = _np.power(((T.A if _issparse(T) else T) - (P.A if _issparse(P) else P)), 2)
            ssres_cells = (__).sum(1)
            ssres = ssres_cells.sum()
        else:
            ssres_cells = _sp.sparse.csr_matrix.power((T - P), 2).sum(1).A1
            ssres = ssres_cells.sum()

        mse = ssres / _sp.prod([M, N])
        msec = ssres_cells / N

        r2 = 1 - ssres / sstot
        r2c = 1 - ssres_cells / sstot_cells

        return mse, r2, msec, r2c

    def _optimize(self, X, iterations=None):

        mse, r2, msec, r2c = self.calc_metrics(X)
        self.opt_iterations = 0
        self.opt_N = 0

        self.__global_err_ = {}
        self.__global_err_[(-1, 0, 0)] = [mse, r2]

        self.__cell_err_ = {}

        self.__cell_err_['R2'] = {}
        self.__cell_err_['R2'][(_sp.nan, 0, 0)] = r2c

        self.__cell_err_['MSE'] = {}
        self.__cell_err_['MSE'][(_sp.nan, 0, 0)] = msec

        self._mse = mse
        self._global_mse = mse

        self._iterate_pcs(X, iterations=iterations)

    def _iterate_pcs(self, X, iterations=None):

        mode = self.mode
        PCs = self.n_pcs if hasattr(self.n_pcs, '__iter__') else [self.n_pcs]
        N_tmp = _np.max(self.n_neighbors) if hasattr(self.n_neighbors, "__iter__") else self.n_neighbors

        for pc in PCs:

            if self.verbose:
                print(f'Computing {N_tmp} neighbors with nPCs = {pc}')
            self.neighbor_alg(self._data, n_neighbors=N_tmp, n_pcs=pc, **self.neighbor_args)
            graph = self._data.uns['neighbors'][mode].copy().astype(self._settype)
            self._iterate_neighbors(X, graph, pcs=pc, iterations=iterations)

    def _iterate_neighbors(self, X, graph, pcs=None, iterations=None):

        Ns = self.n_neighbors if hasattr(self.n_neighbors, '__iter__') else [self.n_neighbors]
        for N in Ns:
            if self.verbose:
                print(f'Compute objective for PCs={pcs} N={N}', end='\r')
            self.connectivities = self.get_connectivities(graph, N).copy()

            self.iterate_diffusion(X, pcs=pcs, N=N, iterations=iterations)

    def iterate_diffusion(self, X, pcs=None, N=None, iterations=None):

        connectivities = self.connectivities.copy()
        if (self._global_mse > self._mse) and not hasattr(self, 'opt_connectivities'):
            self.opt_connectivities = connectivities.copy()
        optimal_mse = current_mse = mse = self._mse
        fixed_iterations = True
        if iterations is None:
            fixed_iterations = False
            iterations = self.iterations

        for i in _sp.arange(iterations):
            if self.verbose and iterations > 1:
                print(f'Progress = {100*(i+1)/(iterations):.3f}%, i={i+1}, delta mse = {current_mse-mse:.2e}, optimal mse = {optimal_mse:.2e}', end='\r')

            X_out = self._apply_denoising(X, connectivities=connectivities)
            mse, r2, msec, r2c = self.calc_metrics(X, X_out)
            self.__global_err_[(pcs, N, i + 1)] = [mse, r2]
            self.__cell_err_['R2'][(pcs, N, i + 1)] = r2c
            self.__cell_err_['MSE'][(pcs, N, i + 1)] = msec
            self._mse = mse

            better = False
            if (mse < self._global_mse):
                self._global_mse = mse
                better = True

            if (mse < optimal_mse) and not fixed_iterations:
                optimal_mse = mse
                self.opt_iterations = i + 1

            if fixed_iterations and (i == iterations):
                if self.verbose and iterations > 1:
                    print(f"Run max iteration, i={i}, delta mse = {current_mse-mse:.2e}, optimal mse = {optimal_mse:.2e}. Exiting.", end='\r')
                # self.opt_iterations = i + 1
                return

            elif self.run2best and (mse > optimal_mse) and not fixed_iterations:
                if self.verbose and iterations > 1:
                    print(f"Found optimal, i={i-1}, delta mse = {optimal_mse-mse:.2e}, optimal mse = {optimal_mse:.2e}. Exiting.", end='\r')
                return

            if better or fixed_iterations:
                self.opt_connectivities = connectivities
            if iterations > 1:
                connectivities = self._diffuse(connectivities)

            current_mse = mse

    def _densify(self):
        if _issparse(self.connectivities):
            if self.connectivities.nnz > _sp.prod(self.connectivities.shape) * self.max_dense:
                self.connectivities = self.connectivities.toarray()

    def _get_layer_data(self, data, copy=True):

        if isinstance(data, _AnnData):
            adata = data.copy() if copy else data
            if self.use_layer == 'X':
                X = adata.X
            elif self.use_layer == 'raw':
                X = adata.raw.X
            else:
                X = adata.layers[self.use_layer]

        else:
            X = data.copy()

        X = self._make_dense(X)

        return X

    def plot_global_performance(self, ax=None, metric='mse', verbose=None, skipfirst=True, plot_style='seaborn-poster'):
        """Simple overview plot of fit performance

        ax: a figure axis, Default None
        metric: one of 'mse' or 'r2'
        verbose: Should we use annotation on plot. If None will use the DEWAKSS default. Default None
        skipfirst: Should the first unfit MSE be shown.
        :returns: (figure, ax) if ax is not None else (None, ax)
        :rtype: matplotlib axis

        """

        if skipfirst:
            pdata = self.global_performance.iloc[1:]
        else:
            pdata = self.global_performance

        pdata = pdata.reset_index(drop=True)

        pdata['PCs'] = pdata['PCs'].astype(int)
        pdata['neighbors'] = pdata['neighbors'].astype(int)
        optvals = pdata.loc[pdata['MSE'].idxmin()].copy()
        optvals['PCs'] = optvals['PCs'].astype(int)
        optvals['neighbors'] = optvals['neighbors'].astype(int)
        optvals['i'] = optvals['i'].astype(int)

        pdata = pdata.groupby(['PCs', 'neighbors'])[metric.upper()].min().reset_index()

        style_label = plot_style
        with _plt.style.context(style_label):
            if ax is None:
                fig = _plt.figure(figsize=(8, 6), constrained_layout=True)
                axs = fig.subplots(1, 1)
            else:
                axs = ax

            for l, df in pdata.groupby(['PCs']):

                axs.scatter(df['neighbors'], df[metric.upper()], label=str(l))

            ymin = pdata[metric.upper()].min()
            ymax = pdata[metric.upper()].max()
            xmin = pdata['neighbors'].min()
            xmax = pdata['neighbors'].max()
            axs.grid(linestyle='--', linewidth=1)
            axs.set_xscale('log')
            axs.set_xlim([xmin - 1, xmax + 10])
            axs.set_xlabel('neighbors')
            axs.set_ylabel(metric.upper())
            axs.set_ylim([ymin - (ymax - ymin) * 0.05, ymax + (ymax - ymin) * 0.05])
            axs.legend(title='PCs', bbox_to_anchor=(1, 1))
            _sns.despine(offset=5)
            axs.set_title('DEWAKSS global performance')

        if verbose is None:
            verbose = self.verbose

        if verbose:
            texttoshow = f"run t: {self._extime:10.3g}s\noptimal:\n"
            texttoshow = texttoshow + str(optvals)
            fig.text(0.01, 0.01, texttoshow, fontsize=12, horizontalalignment='left', transform=axs.transAxes)

        return (fig, axs) if (ax is None) else (None, axs)

    def plot_local_performance(self, metric='MSE', ax=None, plot_style='seaborn-poster', figsize=(6, 4)):

        MSE = self.local_performance[metric]
        grp = MSE.groupby(level=0, axis=1)

        data = {}
        for mse, df in grp:
            data[mse] = df.min(1).mean()

        data = _pd.DataFrame(data, index=[metric]).T
        data.index.name = 'PCs'
        # self._local_err_

        style_label = plot_style
        with _plt.style.context(style_label):
            if ax is None:
                fig = _plt.figure(figsize=figsize, constrained_layout=True)
                axs = fig.subplots(1, 1)
            else:
                axs = ax

            axs.plot(data, ls='', marker='o')
            axs.grid(linestyle='--')
            axs.set_xlabel(data.index.name)
            axs.set_ylabel(metric)
            _sns.despine(offset=5)
            axs.set_title('DEWAKSS Cell local performance')

        return (fig, axs) if (ax is None) else (None, axs)

    def plot_diffusion_performance(self, fig=None, metric='mse', verbose=None, skipfirst=True, plot_style='seaborn-poster', fold=1, figsize=(16, 4), order='F'):

        if skipfirst:
            pdata = self.global_performance.iloc[1:]
        else:
            pdata = self.global_performance

        metric = metric.upper()
        pdata = pdata.reset_index(drop=True)

        pdata['PCs'] = pdata['PCs'].astype(int)
        pdata['neighbors'] = pdata['neighbors'].astype(int)
        optvals = pdata.loc[pdata['MSE'].idxmin()]
        optvals['PCs'] = optvals['PCs'].astype(int)
        optvals['neighbors'] = optvals['neighbors'].astype(int)
        optvals['i'] = optvals['i'].astype(int)

        maxits = pdata['i'].max()

        style_label = plot_style

        combos = pdata[['neighbors']].drop_duplicates()

        with _plt.style.context(style_label):
            if fig is None:
                fig = _plt.figure(figsize=figsize, constrained_layout=True)

            fold = fold
            ncols = combos.shape[0] // fold
            if combos.shape[0] % fold > 0:
                fold = fold + 1
            ax = fig.subplots(fold, ncols, sharex=True, sharey=True).flatten(order=order)

            combos['axes'] = ax[0:combos.shape[0]]
            combos = combos.set_index('neighbors')

            for (neighbors, pcs), subdf in pdata.groupby(['neighbors', 'PCs']):
                axes = combos.loc[neighbors][0]
                subdf = subdf[~(subdf['i'] == 0)]
                axes.plot(subdf['i'].values, subdf[metric].values, label=pcs, zorder=-pcs + 1000, linewidth=2)
                axes.legend().set_visible(False)
                axes.set_xlabel('iteration')
                axes.set_ylabel(f"{metric}")

                axes.set_xticks(subdf['i'].values)
                axes.set_title(f"k={neighbors}")
                axes.grid(linewidth=0.5, linestyle='--')
                axes.label_outer()

            ax[-1].legend(title='PCs', bbox_to_anchor=(1, 1))

            if metric == 'MSE':
                optind = pdata.groupby(['neighbors'])[metric].min()
            elif metric == 'R2':
                optind = pdata.groupby(['neighbors'])[metric].max()

            optit = pdata.set_index(['neighbors'])
            for (neighbors), value in combos.iterrows():
                axes = value[0]
                minmse = optind.loc[neighbors]
                opts = (optit.loc[neighbors][metric] == minmse).values
                its = optit.loc[neighbors][opts]['i'].values[0]
                optpcs = optit.loc[neighbors][opts]['PCs'].values[0]
                _sns.despine()
                ylims = _np.array(axes.get_ylim())
                axes.vlines([its, its], *(ylims), zorder=500, linestyle=':')
                if maxits > 1:
                    hl = 'left' if its < maxits / 2 else 'right'
                    xl = its + 1 if its < maxits else its - 1
                else:
                    hl = 'center'
                    xl = 1

                axes.text(xl, ylims[1], f"MSE={minmse:.4f}\nPCs={optpcs}", ha=hl, va='top')
                axes.set_ylim(*ylims)

            if metric == 'MSE':
                opte = optit[optit[metric] == optind.min()]
            elif metric == 'R2':
                opte = optit[optit[metric] == optind.max()]

            fig.suptitle(f"Optimal: MSE={opte['MSE'].values[0]:.4f}, it={opte['i'].values[0]}, PCs={opte['PCs'].values[0]}, k={opte.reset_index()['neighbors'].values[0]}", fontsize=16)

        return fig, ax

    def _subset(self, X):

        if self.subset:
            if isinstance(self.subset, bool):
                subset = 0.1
            else:
                subset = self.subset

            if isinstance(subset, (list, _sp.ndarray)):
                train_index = subset
            else:
                rs = _ShuffleSplit(1, test_size=None, train_size=subset, random_state=self.random_state)

                train_index, test_index = next(rs.split(X.T))

            return X[:, train_index]

        return X

    def _get_optimal_connectivities(self):

        mode = self.mode
        PCs = self.local_err['MSE'].idxmin().astype(int)

        N_tmp = _np.max(self.n_neighbors) if hasattr(self.n_neighbors, "__iter__") else self.n_neighbors

        if self.verbose:
            print(f'Computing {N_tmp} neighbors with nPCs = {PCs}', end='\r')
        self.neighbor_alg(self._data, n_neighbors=N_tmp, n_pcs=PCs, **self.neighbor_args)
        if self.verbose:
            print('Done!\nProceeding to compute local neighbor optima.')

        graph = self._data.uns['neighbors'][mode].copy().astype(self._settype)
        M, J = graph.shape
        opt_connectivities = _csr.csr_matrix((M, J)).astype(self._settype)
        for pcs, N, It in self._run_configs_:

            if not ((pcs, N, It) in self._cell_optimal_config_.index):
                continue

            # Put first outlier detect code here.
            connectivities = self.get_connectivities(graph, N).copy()
            diff_steps = iter(range(It))
            __ = next(diff_steps)
            for i in diff_steps:
                connectivities = self._diffuse(connectivities)

            idx = self._cell_optimal_config_.loc[(pcs, N, It)].values.flatten().tolist()
            opt_connectivities[idx, :] = connectivities[idx, :]

        opt_connectivities.eliminate_zeros()
        opt_connectivities = self._renormalize(opt_connectivities)
        self.opt_connectivities = opt_connectivities
        if self.mode == 'distances':
            I, D, N = _get_indices_distances_from_sparse_matrix(graph, opt_connectivities)
            nobs = self._data.shape[0]
            DD, CC = _compute_connectivities_umap(I, D, nobs, N)
            self._connectivities = CC.astype(self._settype)
            self._distances = DD.astype(self._settype)

        self._local_optima_fit = True

    def _find_local_denoising(self):

        if (not self.use_global_err) and (not self._local_optima_fit):
            self._get_optimal_connectivities()

    def SNR(self, data, Xmean=None, copy=True):
        """Calculate feature vise signal to noise ratios - denoised expression.

        data: AnnData object or matrix
        Xmean: If precacluated the local mean expression matrix, else it will be calculated from the input data. Default None.
        :returns: SNR and variance of X - dewakss(X)
        :rtype: ndarray, sparse
        """

        _check_is_fitted(self, attributes='opt_iterations')

        if isinstance(data, _AnnData):
            adata = data.copy() if copy else data

            feature_SNR, data_SNR, feature_variance, data_variance = self.SNR(self._get_layer_data(adata, copy=True), Xmean=Xmean, copy=True)

            adata.var['SNR'] = feature_SNR
            adata.uns['SNR'] = data_SNR
            adata.var['variance'] = feature_variance
            adata.uns['variance'] = data_variance
            return adata if copy else None

        X = self._get_layer_data(data, copy=copy)

        feature_variance, data_variance, Xmean = self.var(X, Xmean=Xmean, copy=copy)

        df = data.shape[1] - 1
        chi2inv = _chi2.ppf(1 - self._alpha, df)
        feature_SNR = []
        minnorm = _np.inf
        for var, vec in zip(feature_variance, Xmean.T):
            norm = _np.linalg.norm(vec.A if _issparse(vec) else vec)
            feature_SNR.append(norm / _np.sqrt(chi2inv * var))
            if norm < minnorm:
                minnorm = norm

        feature_SNR = _np.array(feature_SNR)

        data_SNR = _np.linalg.norm(Xmean.A if _issparse(Xmean) else Xmean, 'fro') / _np.sqrt(_chi2.ppf(1 - self._alpha, _np.prod(Xmean.shape) - 1) * data_variance)

        return feature_SNR, data_SNR, feature_variance, data_variance

    def var(self, data, Xmean=None, copy=True):
        """Calculate the variance of the noise - denoised expression.

        data: AnnData object or matrix
        Xmean: If precacluated the local mean expression matrix, else it will be calculated from the input data. Default None.
        :returns: X - dewakss(X)
        :rtype: ndarray, sparse
        """

        _check_is_fitted(self, attributes='opt_iterations')

        if isinstance(data, _AnnData):
            adata = data.copy() if copy else data

            feature_variance, data_variance, __ = self.var(self._get_layer_data(adata, copy=True), Xmean=Xmean, copy=True)

            adata.var['variance'] = feature_variance
            adata.uns['variance'] = data_variance
            return adata if copy else None

        X = self._get_layer_data(data, copy=copy)

        if Xmean is None:
            Xmean = self._apply_denoising(X)
            deltaX = X - Xmean
        else:
            deltaX = X - Xmean

        feature_variance = _sp.var(deltaX.A if _issparse(deltaX) else deltaX, 0)
        data_variance = _sp.var(deltaX.A if _issparse(deltaX) else deltaX)

        feature_variance = feature_variance.A1 if isinstance(feature_variance, _sp.matrix) else feature_variance
        return feature_variance, data_variance, Xmean

    @property
    def global_performance(self):
        pf = _pd.DataFrame(self.__global_err_).T.reset_index()

        pf.columns = ['PCs', 'neighbors', 'i', 'MSE', 'R2']

        return pf

    @property
    def global_opt_configuration(self):

        return self.global_performance.iloc[self.global_performance['MSE'].idxmin()]

    @property
    def local_performance(self):

        msepf = _pd.DataFrame(self.__cell_err_['MSE'])
        r2pf = _pd.DataFrame(self.__cell_err_['R2'])

        return {'MSE': msepf, 'R2': r2pf}

    @property
    def run_configurations(self):

        rconf = _pd.DataFrame(self._run_configs_)

        rconf.columns = ['PCs', 'neighbors', 'i']

        return rconf

    @property
    def local_err(self):

        lerr = _pd.DataFrame(self._local_err_, index=['MSE']).T

        lerr.index.name = 'PCs'

        return lerr

    def _compute_cell_performance(self, optkey='MSE'):

        MSE = self.local_performance['MSE']
        grp = MSE.groupby(level=0, axis=1)

        data = {}
        local_err = _np.inf
        for mse, df in grp:
            data[mse] = df.min(1).mean()

            if data[mse] < local_err:
                local_err = data[mse]
            else:
                continue

            self.cell_optimal_err_ = df.min(1).values
            self._cell_optimal_config_ = df.idxmin(1).values
            self._cell_optimal_config_ = {i: j for i, j in enumerate(self._cell_optimal_config_)}
            self._run_configs_ = tuple(df.keys())

            self._cell_optimal_config_ = _pd.DataFrame(self._cell_optimal_config_).T.reset_index().set_index([0, 1, 2])
            self._cell_optimal_config_.columns = ['cell']
            self._cell_optimal_config_.index.names = ('PCs', 'neighbors', 'i')
            self._local_err_ = data

    def fit(self, data, iterations=None):
        """Fit function for training DEWAKSS

        data: AnnData object or matrix
        iterations: If this is set it hard sets the number of iterations ignoring DEWAKSS settings and stores the opt_connectivities as the final iteration instead of the best one. Default None.
        :returns: self
        :rtype: DEWAKSS object

        """

        X = self._get_layer_data(data, copy=True)
        X = self._subset(X)

        start_time = _time.time()

        self._optimize(X, iterations=iterations)
        self._extime = _time.time() - start_time
        self._compute_cell_performance()

        return self

    def transform(self, data, copy=True, transformtype=None, denoise=True):
        """Transform function for DEWAKSS

        Will transform an input matrix with the fitted affinity kernal. If AnnData object will add the transformed data to the create_layer to layer.

        data: AnnData or matrix like data.
        copy: if the AnnData object should be handled in place or returned.
        :returns: matrix data or None
        :rtype: nparray, sparse, AnnData, None

        """

        if isinstance(data, _AnnData):
            adata = data.copy() if copy else data

            X_out = self.transform(self._get_layer_data(data, copy=True), copy=True)

            if _scs.issparse(X_out):
                if X_out.data.shape[0] / _np.prod(X_out.shape) > self.max_dense:
                    X_out = X_out.toarray()

            if X_out is not None:
                adata.layers[self.create_layer] = X_out
                self.SNR(adata, Xmean=X_out, copy=False)

            adata.uns['dewakss'] = {self.create_layer: {'dewakss_graph': self.opt_connectivities, "opt_iterations": self.opt_iterations, "mode": self.mode, 'layer': self.use_layer, 'modest': self.modest}}
            # _sc.tl.leiden(adata, adjacency=self.opt_connectivities, key_added=f'dewakss_{self.create_layer}_leiden')
            _sc.tl.leiden(adata, adjacency=self._connectivities, key_added=f'dewakss_{self.create_layer}_leiden')
            adata.obs['dewakss_n'] = self.opt_connectivities.astype(bool).sum(1).A1
            if self.mode == 'distances' and self.replace_graph and (not self.use_global_err):
                if 'neighbors' not in adata.uns:
                    adata.uns['neighbors'] = {}
                adata.uns['neighbors']['distances'] = self._distances
                adata.uns['neighbors']['connectivities'] = self._connectivities
                adata.uns['dewakss'][self.create_layer]['distances'] = self._distances
                adata.uns['dewakss'][self.create_layer]['connectivities'] = self._connectivities

            return adata if copy else None

        X = self._get_layer_data(data, copy=copy)
        self._find_local_denoising()

        X_out = self._apply_denoising(X, transformtype=transformtype) if denoise else None

        return X_out
