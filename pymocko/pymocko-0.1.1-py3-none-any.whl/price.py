import random as r

def mock(f=0, t=10000, decimal=2, neg=False):
    if f is None:
        f = 0
    if t is None:
        t = f+10000
    if neg == True:
        return round(r.uniform(f,t), decimal) * -1

    return round(r.uniform(f,t), decimal)