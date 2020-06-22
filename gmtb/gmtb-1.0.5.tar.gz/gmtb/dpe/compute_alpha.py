import numpy as np


# projects x onto the line between a and b, returns the alpha between them
def compute_alpha(a, b, x):
    v = x-a
    u = b-a

    alpha = 0.5

    # check for division by 0
    div = np.dot(u, u)
    if div != 0:
        alpha = np.dot(u, v) / np.dot(u, u)
        alpha = max(alpha, 0)
        alpha = min(alpha, 1)

    return alpha
