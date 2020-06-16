import numpy as np


def first_fn(x, y):
    if x + y < 10:
        z = np.nan
    else:
        z = x + y

    return z


# print(first_fn(1, 2))
# print(first_fn(3, 10))
