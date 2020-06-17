import numpy as np


def merge_intervals(intervals):
    """
    Given a set of intervals, merge any overlapping intervals in O(NlogN)
    Input:
        intervals -- 2D numpy array with format [[start_0, end_0], [start_1, end_1], ...]
    Return:
        merged intervals
    """
    # sort intervals according to start
    intervals = intervals[intervals[:, 0].argsort()]

    merged = [intervals[0]]  # LIFO stack
    for itvl in intervals[1:]:
        top = merged[-1]
        if top[1] < itvl[0]:
            merged.append(itvl)
        elif top[1] < itvl[1]:
            top[1] = itvl[1]
            merged.pop(-1)
            merged.append(top)

    return np.array(merged)
