# vim: fdm=indent
# author:     Fabio Zanini
# date:       17/06/20
# content:    Test the algorithm on same artificial data
import numpy as np
import pandas as pd
import anndata
import anndataks


def test_version():
    print(anndataks.version)


def test_ks2samp():
    data1 = np.array([0, 1, 2, 3, 3, 4], np.float32)
    data2 = np.array([0, 3, 3, 4, 6, 6], np.float32)
    res = anndataks.ks_2samp(data1, data2)
    assert(res[0] == 0.3333333333333333)
    assert(res[1] == 1.0)
    assert(res[2] == 0.9307359307359307)


def test_compare():
    X1 = np.array([
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 4],
        [3, 5],
        ])
    X2 = np.array([
        [0, 1],
        [6, 2],
        [6, 3],
        [6, 5],
        ])

    adata1 = anndata.AnnData(X=X1)
    adata2 = anndata.AnnData(X=X2)
    adata1.var_names = ['Gene1', 'Gene2']
    adata2.var_names = ['Gene1', 'Gene2']

    ress = anndataks.compare(adata1, adata2, log1p=False)

    ress_exp = pd.DataFrame(
        [[0.75, 1.5, 0.142857, 1.485427, 2.459432, 0.974005],
         [0.05, 3.5, 1.000000, 2.000000, 1.906891, -0.093109]],
        columns=['statistic', 'value', 'pvalue', 'avg1', 'avg2', 'log2_fold_change'],
        index=adata1.var_names,
        )
    assert((ress.shape == ress_exp.shape))
    assert((np.abs(ress.values - ress_exp.values) < 1e-5).all())


if __name__ == '__main__':

    test_version()
    test_ks2samp()
    test_compare()
