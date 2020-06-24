import time,math
from . import geometry
from . import control

class VerticalTarget :

    def __init__(self,
                 left,
                 active,
                 size,
                 color_active,
                 color_inactive,
                 position=(0,0)):

        self._left = left
        self._active = active
        self._position = position
        self._size = size
        if active:
            self._color = color_active
        else :
            self._color = color_inactive
        self._color_active = color_active
        self._color_inactive = color_inactive
        self._previous_time = None

    def get_position(self):
        return self._position
        
    def is_active(self):
        return self._active

    def is_inactive(self):
        return not self._active

    def set_active(self):
        self._color = self._color_active
        self._active = True

    def set_inactive(self):
        self._color = self._color_inactive
        self._active = False

    def should_deactivate(self,cursor):
        if self._left and cursor[0]<self._position[0]:
            return True
        if (not self._left) and cursor[0]>self._position[0]:
            return True
        return False
    
    # assumes world as a soft target attribute
    def __call__(self,world):

        cursor = world.cursor
        other_vertical_targets = [ovt
                                  for ovt in world.vertical_targets
                                  if id(ovt)!=id(self)]

        if not cursor :
            
            return self._position,self._size,self._color

        if self._active and self.should_deactivate(cursor):

            self.set_inactive()
            for ovt in other_vertical_targets:
                ovt.set_active()

        return self._position,self._size,self._color


def get_vertical_targets(x1,x2,
                         size,
                         color_active,
                         color_inactive,
                         width,height):

    vt_left= VerticalTarget(True,
                            True,
                            size,
                            color_active,
                            color_inactive,
                            (x1,0))

    vt_right = VerticalTarget(False,
                              False,
                              size,
                              color_active,
                              color_inactive,
                              (x2,0))
    
    return [vt_left,vt_right]
