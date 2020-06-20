import copy
from scratch import NMF_HALS
from factors import NMF, VanillaALS

import numpy as np


def test_ALS():
    np.random.seed(1234)

    while True:
        N, M, K = 5, 4, 3
        X = np.random.rand(N, M)

        mine = VanillaALS(K, alpha=0, max_iter=200)

        # init W and H
        #  W = np.abs(np.random.rand(N, K))
        #  W /= np.linalg.norm(W, axis=0)
        #  H = np.abs(np.random.rand(K, M))

        mine.fit(X, verbose=True)
        import ipdb

        ipdb.set_trace()

        #  for k in mine.debug.keys():
        #      print("Testing {}:".format(k))
        #      np.testing.assert_allclose(mine.debug[k], theirs.debug[k], atol=1e-15)
        #      print("PASSED")


def test_NMF():
    np.random.seed(1234)

    while True:
        N, M, K = 5, 4, 3
        X = np.random.rand(N, M)

        mine = NMF(K, max_iter=1)
        theirs = NMF_HALS(default_max_iter=1)

        # init W and H
        W = np.abs(np.random.rand(N, K))
        W /= np.linalg.norm(W, axis=0)
        H = np.abs(np.random.rand(K, M))

        Wt, Ht, _ = theirs.run(
            X, K, init=[copy.deepcopy(W), copy.deepcopy(H.T)], verbose=-1
        )
        mine.fit(X, W=W, H=H, verbose=False)

        #  for k in mine.debug.keys():
        #      print("Testing {}:".format(k))
        #      np.testing.assert_allclose(mine.debug[k], theirs.debug[k], atol=1e-15)
        #      print("PASSED")

        np.testing.assert_allclose(mine.W, Wt)
        np.testing.assert_allclose(mine.H, Ht.T)
        print("PASSED")
