import math
import numpy
from see137.stochastic import brownian_motion_log_returns


def cox_ingersoll_ross_levels(param):
    """
        This method returns the rate levels of a mean-reverting cox ingersoll ross process. It is used to model interest
        rates as well as stochastic volatility in the Heston model. Because the returns between the underlying and the
        stochastic volatility should be correlated we pass a correlated Brownian motion process into the method from which
        the interest rate levels are constructed. The other correlated process is used in the Heston model
        :param param: the model parameters object
        :return: the interest rate levels for the CIR process
    """
    brownian_motion = brownian_motion_log_returns(param)
    # Setup the parameters for interest rates
    a, mu, zero = param.cir_a, param.cir_mu, param.all_r0
    # Assumes output is in levels
    levels = [zero]
    for i in range(1, param.all_time):
        drift = a * (mu - levels[i-1]) * param.all_delta
        # The main difference between this and the Ornstein Uhlenbeck model is that we multiply the 'random'
        # component by the square-root of the previous level i.e. the process has level dependent interest rates.
        randomness = math.sqrt(levels[i - 1]) * brownian_motion[i - 1]
        levels.append(levels[i - 1] + drift + randomness)
    return numpy.array(levels)