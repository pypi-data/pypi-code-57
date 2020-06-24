import time,math
from . import geometry
from . import control
    

class LinearMediator :

    def __init__(self,kp,size,color,position=(0,0),x_shift=0):
        
        self._kp = kp
        self._position = position
        self._size = size
        self._color = color
        self._previous_time = None
        self._x_shift = x_shift

    # assumes world as a soft target attribute
    def __call__(self,world):

        soft_target = world.soft_target
        v = control.linear_controller( self._previous_time,
                                       self._position,
                                       soft_target,
                                       self._kp)
        self._previous_time,self._position = v
        return self._position,self._size,self._color,self._x_shift



# higher similarity -> higher kp
class SimilarityMediator:

    def __init__(self,similarity_average_period,
                 kp_min,kp_max,size,color,position=(0,0),
                 x_shift=0):

        if similarity_average_period is not None:
            self._similarities = control.Averager(similarity_average_period)
        else:
            self._similarities = None
        self._size = size
        self._color = color
        self._kp = [kp_min,kp_max]
        self._kp_range = kp_max-kp_min
        self._position = position
        self._previous_time=None
        self._x_shift = x_shift
        
    def __call__(self,world):

        similarity = world.similarity

        if similarity is None:
            return self._position,self._size,self._color

        if self._similarities is not None:
            similarity = self._similarities.get(similarity)
        
        kp = self._kp[0]+similarity*self._kp_range

        soft_target = world.soft_target
        v = control.linear_controller( self._previous_time,
                                       self._position,
                                       soft_target,
                                       kp)
        self._previous_time,self._position = v
        
        return self._position,self._size,self._color,self._x_shift
        
        
                
