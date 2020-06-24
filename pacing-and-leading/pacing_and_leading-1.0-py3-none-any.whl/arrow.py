import time,math
from . import geometry

class Arrow:

    def __init__(self,
                 position,
                 length,
                 width,
                 tip_size,
                 color):

        self.length = length
        self.width = width
        self.tip_size = tip_size
        self._position = position
        self._color = color
        
    def get(self):

        return (self._position,
                self.length,
                self.width,
                self.tip_size,
                self._color)
        
    def __call__(self,world):

        soft_target = world.soft_target

        if not soft_target:
            return self._position,[0,0],self._color

        delta = [st-p
                 for st,p in zip(soft_target,
                                 self._position)]

        delta = geometry.normalize(delta,target_norm=self.length)

        return self._position,delta,self._color
        
