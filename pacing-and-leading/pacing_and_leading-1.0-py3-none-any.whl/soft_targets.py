import time,math
from collections import deque
from . import geometry
from . import control
    

class TimeDriftingSoftTarget:

    """ Moves from the user cursor to the 
        hard target over a fixed duration
    """
    
    def __init__(self,duration,
                 size=None,color=None):

        self._duration = duration
        self._time_start = None
        self._color = color
        self._size = size

    def __call__(self,world):

        t = time.time()
        if self._time_start is None:
            self._time_start = t

        delta_t = t-self._time_start

        cursor = world.cursor
        hard_target = world.hard_target

        if delta_t > self._duration :
            return hard_target,self._size,self._color

        v = [ht-c for ht,c in
             zip(hard_target,cursor)]
        norm_v = geometry.norm(v)
        
        ratio = delta_t / self._duration
        total_d = geometry.distance(cursor,hard_target)
        d = ratio * total_d
        
        self._position = [c+d*v_/norm_v
                          for c,v_ in zip(cursor,v)] 

        return self._position,self._size,self._color


# if similar : toward hard target,
# else, toward cursor
    
class SimilaritySoftTarget:

    def __init__(self,
                 similarity_average_period,
                 invert,
                 size=None,
                 color=None):

        if similarity_average_period is not None:
            self._similarities = control.Averager(similarity_average_period)
        else :
            self._similarities = None
        self._color = color
        self._size = size
        self._invert = invert
        
    def __call__(self,world):

        cursor = world.cursor
        hard_target = world.hard_target
        similarity = world.similarity

        if similarity is None:
            return cursor,self._size,self._color

        if self._similarities is not None:
            similarity = self._similarities.get(similarity)

        if self._invert:
            similarity = 1.0-similarity
            
        v = [ht-c for ht,c in
             zip(hard_target,cursor)]
        norm_v = geometry.norm(v)
        total_d = geometry.distance(cursor,hard_target)
        d = similarity * total_d
        
        position = [c+d*v_/norm_v
                    for c,v_ in zip(cursor,v)] 
        
        return position,self._size,self._color
    
