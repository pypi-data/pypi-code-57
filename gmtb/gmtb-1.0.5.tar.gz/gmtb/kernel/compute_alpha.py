import numpy as np


# compute_alpha computes the alpha of the projection in kernel space
# weights = weights of the objects
# k_a_set = array of kernel values between object a and the set
# k_a_a = kernel between object a and itself
# k_b_set = array of kernel values between object b and the set
# k_b_b = kernel between object b and itself
# k_a_b = kernel between object a and b
def compute_alpha(weights, k_a_set, k_a_a, k_b_set, k_b_b, k_a_b):

    div = k_b_b - 2 * k_a_b + k_a_a

    # in case of negative values in sqrt, return 0.5 instead
    if div > 0:
        alpha = (np.sum(weights * (k_b_set - k_a_set)) / np.sum(weights) - k_a_b + k_a_a) \
                / np.power(np.sqrt(div), 2)
    else:
        alpha = 0.5

    alpha = max(alpha, 0)
    alpha = min(alpha, 1)
    return alpha
