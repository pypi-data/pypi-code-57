from functools import wraps
import yaml
from .boa_obj import boa


def boa_wraps_yaml(fun, Loader):
    @wraps(fun)
    def dec(*args, **kwargs):
        return boa(fun(*args, Loader=Loader, **kwargs))
    return dec


load = boa_wraps_yaml(yaml.load, Loader=yaml.SafeLoader)  # make safe_load the default
load_all = boa_wraps_yaml(yaml.load_all, Loader=yaml.SafeLoader)  # make safe_load the default

safe_load = boa(yaml.safe_load)
unsafe_load = boa(yaml.unsafe_load)
full_load = boa(yaml.full_load)
