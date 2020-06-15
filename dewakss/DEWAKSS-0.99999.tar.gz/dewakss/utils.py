from anndata import AnnData as _AnnData
import scipy as _sp
import numpy as _np
from scipy.sparse import issparse as _issparse, csr as _csr


def ftt(data, reversed=False, copy=False, correction=-1):
    """
    Freeman-Tukey transform (FTT), y = √(x) + √(x + 1) + correction

    reversed this is x = (y - correction)^2 - 1

    correction is default -1 to preserve sparse data.
    """

    if isinstance(data, _AnnData):
        copy = True if data.isview else copy
        if data.isview:
            print('Data is view. Making a copy.')
        adata = data.copy() if copy else data

        ftt(adata.X, reversed=reversed, copy=False)
        return adata if copy else None

    X = data.copy() if copy else data

    if _issparse(X):
        X.data = _sp.sqrt(X.data) + _sp.sqrt(X.data + 1) + correction

    else:
        X = _sp.sqrt(X) + _sp.sqrt(X + 1) + correction

    if reversed:
        raise NotImplementedError
        # X[nnz] = _sp.square(X[nnz] - correction) - 1

    return X if copy else None


def denoise_values(data, col_name, modest=None, copy=False):

    def _row_stochastic(C):
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

    if isinstance(data, _AnnData):
        adata = data.copy() if copy else data

    col = adata.obs[col_name].astype(float)

    C = adata.uns['dewakss']['Ms']['dewakss_connectivities'].copy()

    if modest is not None:
        modest_adjust(C, modest)

    isna = ~col.isna().values
    C = C[:, isna]
    if modest is not None:
        C = _row_stochastic(C)

    new_col = C @ col[isna].values

    adata.obs['dwks_' + col_name] = new_col

    return adata if copy else None


def modest_adjust(C, modest):

    if isinstance(modest, (int, float)):
        if _issparse(C):
            C.setdiag(modest)
        else:
            _np.fill_diagonal(C, modest)
    elif isinstance(modest, str):
        vecvals = []
        for row in C:
            method = getattr(_np, modest)
            vals = method(row.data)
            vecvals.append(vals)
        vecvals = _sp.sparse.spdiags(vecvals, 0, len(vecvals), len(vecvals))
        C = C + vecvals
    else:
        if modest:
            vecvals = C.astype(bool).sum(1).A1
            vecvals = _sp.sparse.spdiags(1 / vecvals, 0, len(vecvals), len(vecvals))
            C = C + vecvals


def calc_metrics(T, P=None):
    """Calculate MSE and R2,

    Only seem to be faster than the sklearn if both matrices are sparse.
    Of course sklearn computes the wrong MSE if that is the case."""

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
