# import pstats
# import cProfile
import sys
import numpy as np
from deepdiff import DeepDiff
# from deepdiff.distance import _get_numpy_array_distance
# from deepdiff.helper import cartesian_product_numpy, subtract_numpy_arrays
# from deepdiff.diff import IndexedHash


if False:
    a1 = np.array([[1, 2, 3], [2, 5, 3]], dtype=np.int64)
    a2 = np.array([[3, 2, 2], [3, 6, 3]], dtype=np.int64)
    DeepDiff(a1, a2, ignore_order=True, log_frequency_in_sec=0, cache_size=5000)

    sys.exit()


elif False:
    a1 = np.array([1, 2, 3], dtype=np.int64)
    a2 = np.array([4, 5, 6], dtype=np.int64)
    print(cartesian_product_numpy(a1, a2))
    sys.exit()


elif False:
    # sorted unique items
    a1 = np.unique(np.loadtxt('mat1_short.txt'))
    a2 = np.unique(np.loadtxt('mat2_short.txt'))
    added = subtract_numpy_arrays(a2, a1)
    removed = subtract_numpy_arrays(a1, a2)

    pairs = cartesian_product_numpy(added, removed)

    pairs_transposed = pairs.T

    distances = _get_numpy_array_distance(pairs_transposed[0], pairs_transposed[1])

    print(distances)

elif False:
    a1 = [[1.0, 2.0, 3.0, 4.0], [2.0, 3.0, 4.0, 4.0]]
    a2 = [[2.0, 2.0, 3.1, 4.0], [1.02, 2.0, 3.0, 4.0]]

    # a1 = np.array([[1.0, 2.0, 3.0, 4.0], [2.0, 3.0, 4.0, 4.0]])
    # a2 = np.array([[2.0, 2.0, 3.1, 4.0], [1.02, 2.0, 3.0, 4.0]])
    print(DeepDiff(a1, a2, ignore_order=True, log_frequency_in_sec=0, cache_size=5000))

elif True:

    a1 = np.loadtxt('mat1_short.txt')
    a2 = np.loadtxt('mat2_short.txt')


    # a1 = np.array([np.loadtxt('mat1_short.txt')])
    # a2 = np.array([np.loadtxt('mat2_short.txt')])

    print(DeepDiff(a1, a2, ignore_order=True, log_frequency_in_sec=0, cache_size=5000))

elif False:
    # a1 = [[1, 2, 3], [4, 2, 2]]
    # a2 = [[1, 2, 5], [4, 1, 2]]
    a1 = np.array([[1, 2, 3], [4, 2, 2]], np.int8)
    a2 = np.array([[1, 2, 5], [4, 1, 2]], np.int8)
    print(DeepDiff(a1, a2, ignore_order=False, log_frequency_in_sec=0, cache_size=5000, view='_delta'))

    # cProfile.run('DeepDiff(a1, a2, ignore_order=True, log_frequency_in_sec=0, cache_size=5000)', 'temp2_optimized.profile')
    # p = pstats.Stats('temp.profile')
    # p.sort_stats('calls', 'cumulative')
    # p.print_stats()

# print(cartesian_product_transpose_pp([a1, a2]))
# print(cartesian_product_numpy([a1, a2]))



