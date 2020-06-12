import numpy
from see137.stochastic import brownian_motion_log_returns

def ornstein_uhlenbeck_levels(param):
    """
    This method returns the rate levels of a mean-reverting ornstein uhlenbeck process.
    :param param: the model parameters object
    :return: the interest rate levels for the Ornstein Uhlenbeck process
    """
    ou_levels = [param.all_r0]
    brownian_motion_returns = brownian_motion_log_returns(param)
    for i in range(1, param.all_time):
        drift = param.ou_a * (param.ou_mu - ou_levels[i-1]) * param.all_delta
        randomness = brownian_motion_returns[i - 1]
        ou_levels.append(ou_levels[i - 1] + drift + randomness)
    return numpy.array(ou_levels)