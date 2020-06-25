# -*- coding: utf-8 -*-
import numpy as np
import math

__all__ = ["haversine",
           "manhattan",
           "euclidean",
           "minkowski",
           "cosine_similarity",
           "hamming"]


def _validate_vector(vector, dtype=None):
    vector = np.asarray(vector, dtype=dtype).squeeze()
    vector = np.atleast_1d(vector)
    if vector.ndim > 1:
        raise ValueError("Input vector should be 1-D.")
    return vector

def _validate_var_type(value, dtype=None):
    if isinstance(value, dtype):
        return value
    else:
        raise ValueError("Input value not of type: " + str(dtype))

def _validate_weights(w, dtype=np.double):
    w = _validate_vector(w, dtype=dtype)
    if np.any(w < 0):
        raise ValueError("Input weights should be all non-negative")
    return w

def hamming(vector1, vector2) :
    if type(vector1) == type(vector2) == int:
        return bin(vector1 ^ vector2).count('1')
    elif type(vector1) == type(vector2) == str:
        if len(vector1) != len(vector2):
            raise ValueError("Undefined for sequences of unequal length.")
        return sum(el1 != el2 for el1, el2 in zip(vector1, vector2))
    else:
        return "Hi"

def haversine(coord1, coord2, R = 6372800):
    '''
    Important to note is that we have to take the radians of the longitude and latitude values.
    R  corresponds to Earths mean radius in meters (6372800)
    '''
    lat1, lon1 = _validate_vector(coord1, dtype=np.double)
    lat2, lon2 = _validate_vector(coord2, dtype=np.double)
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

def manhattan(vector_1, vector_2):
    '''
    ## Input
    manhattan([1,2.3213213,3],[4,5.321,6.123])
    ## Output
    -9.1226787
    '''
    vector_1 = _validate_vector(vector_1, dtype=np.double)
    vector_2 = _validate_vector(vector_2, dtype=np.double)
    return minkowski(vector_1, vector_2, p=1)

def euclidean(vector_1, vector_2):
    '''
    ## Input
    euclidean([1,2.3213213,3],[4,5.321,6.123])
    ## Output
    5.267940897849338
    '''
    vector_1 = _validate_vector(vector_1, dtype=np.double)
    vector_2 = _validate_vector(vector_2, dtype=np.double)
    return minkowski(vector_1, vector_2, p=2)


def minkowski(vector_1, vector_2, p=1):
    vector_1 = _validate_vector(vector_1, dtype=np.double)
    vector_2 = _validate_vector(vector_2, dtype=np.double)
    distance = 0.0
    for i in range(len(vector_1)):
            distance += (vector_1[i] - vector_2[i])**p
    return (distance)**(1.0/p)

def cosine_similarity(vector_1, vector_2):
    vector_1 = _validate_vector(vector_1, dtype=np.double)
    vector_2 = _validate_vector(vector_2, dtype=np.double)
    num = np.dot(vector_1, vector_2)
    den = (np.sqrt(np.dot(vector_1, vector_1)) * np.sqrt(np.dot(vector_2, vector_2)))
    return num / den




