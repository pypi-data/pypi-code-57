import numpy as np


def ndcg(y, yhat, k=10):
    pass


def dcg(y, yhat, k=None, average_ties=True):
    r"""
    Compute the discounted cumulative gain.

    Notes
    -----
    DCG@k corresponds to a logarithmically discounted sum of the first `k`
    target values in `y`, ordered according to the scores in `yhat`.

    Parameters
    ----------
    y : numpy array of shape `(N,)`
    yhat : numpy array of shape `(N,)`
    k : int
        Report the cumulative gain over the first `k` items, ranked according
        to the scores in `yhat`. If None, return the gain summed over all `N`
        items. Default is None.
    average_ties : bool
        What to do if there are repeated values in `yhat`. If True, the gain at
        the repeated index in `yhat` is replaced by the average gain across the
        repeated group.

        The gain (`y`)
        of an index falling inside a tied group (in the order induced by
        `y_score`) is replaced by the average gain within this group.  The
        discounted gain for a tied group is then the average `y_true` within
        this group times the sum of discounts of the corresponding ranks
    """
    if isinstance(y, list) or isinstance(yhat, list):
        y, yhat = np.array(y), np.array(yhat)

    assert y.shape == yhat.shape

    N = y.shape[0]
    k = N if k is None else k

    log_discount = 1 / np.log2(np.arange(N) + 2)
    if average_ties:
        #  _, u_idxs, u_inv, u_counts = np.unique(
        #      -1 * yhat, return_index=True, return_inverse=True, return_counts=True
        #  )

        ranking_idxs = np.argsort(-1 * yhat)

        yr = y[ranking_idxs]
        yhatr = yhat[ranking_idxs]
        _, u_idxs, u_counts = np.unique(yhatr, return_index=True, return_counts=True)

        cg = 0
        ix = 0
        for i, c in zip(u_idxs, u_counts):
            if ix >= k:
                break
            dc = sum(log_discount[i : i + c])
            cg += np.mean(yr[i : i + c]) * dc
            ix += 1
    else:
        ranking_idxs = np.argsort(-1 * yhat)
        cg = y[ranking_idxs][:k] @ log_discount[:k]
    return cg


def test_dcg():
    y = np.array([3, 1, 8, 2, 5, 6]).astype(float)
    yhat = np.array([3, 2, 1, 3, 3, 2]).astype(float)

    mine = dcg(y, yhat, 1, average_ties=False)
    theirs = dcg_score(y[None, :], yhat[None, :], 1, ignore_ties=True)
    np.testing.assert_allclose(mine, theirs)
    print("Passed for average ties = False")

    mine = dcg(y, yhat, 1, average_ties=True)
    theirs = dcg_score(y[None, :], yhat[None, :], 1, ignore_ties=False)
    np.testing.assert_allclose(mine, theirs)
    print("Passed for average ties = True")
