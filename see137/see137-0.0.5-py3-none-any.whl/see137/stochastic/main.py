import numpy
from see137.stochastic import is_acceptable_type
from see137.stochastic.utils.parameters import get_super_parameters
from see137.stochastic.generators import (
    geometric_brownian_motion_levels,
    heston_model_levels,
    geometric_brownian_motion_jump_diffusion_levels,
    cox_ingersoll_ross_levels,
    ornstein_uhlenbeck_levels
)

def generate_super_price(base_price:float=1000.0, base_type:str="MERTON", base_time:int=2000) -> numpy.array:


    if is_acceptable_type(base_type) == False:
        raise ValueError("Stochastic type is not appropiately specified")

    super_params = get_super_parameters(base_price, base_time)
    
    if base_type.upper() == "GBM":
        m = geometric_brownian_motion_levels(super_params)
        return m
    elif base_type.upper() == "HESTON":
        m = heston_model_levels(super_params)[0]
        return m
    elif base_type.upper() == "MERTON":
        m = geometric_brownian_motion_jump_diffusion_levels(super_params)
        return m
    elif base_type.upper() == "COX":
        m = cox_ingersoll_ross_levels(super_params)
        return m
    elif base_type.upper() == "ORNSTEIN":
        m = ornstein_uhlenbeck_levels(super_params)
        return m