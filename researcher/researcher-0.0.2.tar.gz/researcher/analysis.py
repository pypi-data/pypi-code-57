import math
import json

def analyse(res, metric):
    def get_mean(res):
        mean = 0
        count = 0
        for fold in res:
            for attempt in fold:
                mean += attempt[metric]
                count += 1
        return mean/count
    
    def get_sd(res, mean):
        sd = 0
        count = 0
        for fold in res:
            for attempt in fold:
                sd += (attempt[metric] -mean)**2
                count+=1
        return math.sqrt(sd/count)
    
    mean = get_mean(res)
    sd = get_sd(res, mean)
    
    return mean, sd


def load_params(name, keep_results=False):
    with open(name) as f:
        params = json.load(f)

    if not keep_results:
        del params["results"]
    return params