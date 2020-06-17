import random as r

def mock(f=0, t=1000, neg=False):
    if f is None:
        f = 0
    if t is None:
        t = f+1000
    if neg == True:
        return int(r.uniform(f,t)) * -1
        
    return int(r.uniform(f,t))