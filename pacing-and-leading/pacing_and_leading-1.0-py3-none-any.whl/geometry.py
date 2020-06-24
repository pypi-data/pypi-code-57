import time,math
import numpy as np

def distance(p1,p2):
    
    return math.sqrt(sum([(a-b)**2
                          for a,b in zip(p1,p2)]))

def norm(v):

    return math.sqrt(sum([a**2 for a in v]))


def normalize(v,target_norm=1):

    n = norm(v)
    return [v_*target_norm/n for
            v_ in v]


def dot(v1,v2):

    v1_ = normalize(v1)
    v2_ = normalize(v2)

    return sum([a*b
                for a,b in zip(v1_,v2_)])

def linear_combination(weight_vectors):

    wvs = [ (weight,np.array(vector))
            for weight,vector in weight_vectors ]
    return sum([w*v for w,v in wvs])

