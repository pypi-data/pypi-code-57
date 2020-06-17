# vim: fdm=indent
# author:     Fabio Zanini
# date:       17/06/20
# content:    Kolmogorov Smirnov test on gene expression for AnnData objects
import numpy as np
import pandas as pd
import scipy.sparse
from .stats import ks_2samp


def compare(adata1, adata2, log1p=False):
    '''Compare two AnnData gene expression by KS test

    Args:
        adata1 (AnnData): The first dataset
        adata2 (AnnData): The second dataset
        log1p (False or float): Whether the datasets are already pseudocounted
           and logged. If a float, it should specify the base of the log
    
    Returns:
        pd.DataFrame: Rows are var_names, columns are the KS statistic (with
        sign > 0 if adata2 had a higher expression at the key spot), the
        expression level of the maximal KS statistic, the P value, the average
        of the expression in the first dataset, the average in the second
        dataset (both logged 2 with pseudocount of 1), and the log2 fold change
        of 2 over 1.

    '''
    X1 = adata1.X
    X2 = adata2.X

    m1, m2 = X1.shape[1], X2.shape[1]
    if m1 != m2:
        raise ValueError('The AnnData matrices must have the same width')

    if scipy.sparse.issparse(X1) and (not scipy.sparse.isspmatrix_csc(X1)):
        X1 = X1.tocsc()

    if scipy.sparse.issparse(X2) and (not scipy.sparse.isspmatrix_csc(X2)):
        X2 = X2.tocsc()

    # Get the numbers out of the aux function
    ress = pd.DataFrame(
            np.zeros((m1, 3), np.float64),
            index=adata1.var_names,
            columns=['statistic', 'value', 'pvalue'],
            )
    for i in range(m1):
        data1 = X1[:, i]
        data2 = X2[:, i]
        res = ks_2samp(data1, data2)
        ress.iloc[i] = res

    # Compute averages and log2 fold changes
    avg1 = X1.mean(axis=0)
    avg2 = X2.mean(axis=0)
    if log1p is False:
        avg1 = np.log2(avg1 + 1)
        avg2 = np.log2(avg2 + 1)
    elif log1p != 2:
        avg1 /= np.log2(log1p)
        avg2 /= np.log2(log1p)

    log2_fc = avg2 - avg1
    ress['avg1'] = avg1
    ress['avg2'] = avg2
    ress['log2_fold_change'] = log2_fc

    return ress
