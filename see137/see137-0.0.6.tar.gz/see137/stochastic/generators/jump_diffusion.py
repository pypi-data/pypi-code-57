import time as _time
import math
import numpy
import random
from see137.stochastic.generators.geometric_brownian import geometric_brownian_motion_log_returns
from see137.stochastic import ModelParameters, convert_to_prices



def jump_diffusion_process(param):
    """
    This method produces a sequence of Jump Sizes which represent a jump diffusion process. These jumps are combined
    with a geometric brownian motion (log returns) to produce the Merton model.
    :param param: the model parameters object
    :return: jump sizes for each point in time (mostly zeroes if jumps are infrequent)
    """
    assert isinstance(param, ModelParameters)
    s_n = time = 0
    small_lamda = -(1.0 / param.lamda)
    jump_sizes = []
    for k in range(0, param.all_time):
        jump_sizes.append(0.0)
    
    last_step = 0.0
    while s_n < param.all_time:
        s_n += small_lamda * math.log(random.uniform(0, 1))
        last_step = _time.time()
        for j in range(0, param.all_time):
            delta = _time.time()-last_step
            if delta > 1:
                print("lingering gere")
            if time * param.all_delta <= s_n * param.all_delta <= (j + 1) * param.all_delta:
                jump_sizes[j] += random.normalvariate(param.jumps_mu, param.jumps_sigma)
                break
            # print()
        time += 1
    return jump_sizes


def geometric_brownian_motion_jump_diffusion_log_returns(param):
    """
    This method constructs combines a geometric brownian motion process (log returns) with a jump diffusion process
    (log returns) to produce a sequence of gbm jump returns.
    :param param: model parameters object
    :return: returns a GBM process with jumps in it
    """
    assert isinstance(param, ModelParameters)
    jump_diffusion = jump_diffusion_process(param)
    geometric_brownian_motion = geometric_brownian_motion_log_returns(param)
    return numpy.add(jump_diffusion, geometric_brownian_motion)


def geometric_brownian_motion_jump_diffusion_levels(param):
    """
    This method converts a sequence of gbm jmp returns into a price sequence which evolves according to a geometric
    brownian motion but can contain jumps at any point in time.
    :param param: model parameters object
    :return: the price levels
    """
    return convert_to_prices(param, geometric_brownian_motion_jump_diffusion_log_returns(param))