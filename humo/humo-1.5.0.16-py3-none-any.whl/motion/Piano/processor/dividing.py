import functools
import numpy as np

def dividingData(dimension):
    def _dividingData(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data, sp, ep = func(*args, **kwargs)
            if dimension == 3:
                inter_data = []
                for start,end in zip(sp, ep):
                    inter_data.append(data[start:end,:])
                return np.array(inter_data)
            elif dimension == 1:
                inter_data = []
                for start, end in zip(sp, ep):
                    inter_data.append(data[start:end])
                return np.array(inter_data)
        return wrapper
    return _dividingData
