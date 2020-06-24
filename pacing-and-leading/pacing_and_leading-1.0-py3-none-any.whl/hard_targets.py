import time,math
from . import geometry
from . import control

class WaypointsHardTarget :

    def __init__(self,
                 waypoints,
                 velocity,
                 size=None,
                 color=None):

        self._velocity = velocity
        self._waypoints = waypoints
        self._position = self._waypoints[0]
        self._previous_waypoint = self._waypoints[0]
        self._start_time = None
        self._index = 1
        self._size = size
        self._color = color

    def __call__(self,world):

        t = time.time()
        if self._start_time is None:
            self._start_time = t
        delta_t = t - self._start_time

        waypoint = self._waypoints[self._index]
        total_d = geometry.distance(waypoint,self._previous_waypoint)
        performed_d = self._velocity * delta_t
        
        if performed_d > total_d:
            self._previous_waypoint = self._waypoints[self._index]
            self._index += 1
            if self._index >= len(self._waypoints):
                self._index = 0
            self._start_time = None
            return self(world)

        total_v = [w-pw
                   for w,pw in zip(waypoint,self._previous_waypoint)]
        norm_v = math.sqrt(sum([v**2 for v in total_v]))

        self._position = [pw+performed_d*v/norm_v
                          for pw,v in zip(self._previous_waypoint,total_v)]

        return self._position,self._size,self._color


class LineHardTarget:

    def __init__(self,
                 point1,
                 point2,
                 velocity,
                 size=None,
                 color=None):

        self._point1 = point1
        self._point2 = point2
        self._waypoints = WaypointsHardTarget([point1,point2],
                                              velocity,size=size,color=color)

    def __call__(self,world):

        return self._waypoints(world)
