import numpy as np
import math
from . import control
from . import geometry

class ConstantSimilarity:

    def __init__(self,
                 value):
        self._value = value

    def __call__(self,_,__):

        return self._value

class LineDistanceSimilarity:

    def __init__(self,
                 point1,
                 point2,
                 max_distance):
    
        self._max_distance = max_distance
        self._p1 = np.array(point1)
        self._p2 = np.array(point2)

    def _line_distance(self,cursor):
        p = np.array(cursor)
        n1 = np.linalg.norm(self._p2-self._p1)
        n2 = np.linalg.norm(np.cross(self._p2-self._p1, self._p1-p))
        return n2/n1

    def __call__(self,cursor,_):

        if cursor is None:
            return None

        distance = self._line_distance(cursor)
        if distance > self._max_distance:
            return 0.
        distance_score =  1.0 - distance / self._max_distance

        return distance_score

    
class VelocityNormSimilarity:

    def __init__(self,
                 velocity):
        self._velocity = velocity
        self._velocity_cursor = control.Velocity()

    def __call__(self,cursor,_):

        if cursor is None:
            return None

        velocity_cursor = self._velocity_cursor.get(cursor)
        
        if velocity_cursor is None:
            return None
            
        speed = geometry.norm(velocity_cursor)
        if speed > self._velocity:
            speed_score = self._velocity / speed
        else:
            speed_score = speed / self._velocity 

        return speed_score

class VelocityLineSimilarity:

    def __init__(self,
                 point1,
                 point2,
                 min_velocity):
        self._vector = [p2-p1
                        for p2,p1 in zip(point1,point2)]
        self._min_velocity = min_velocity
        self._velocity_cursor = control.Velocity()

    def __call__(self,cursor,_):

        if cursor is None:
            return None

        velocity_cursor = self._velocity_cursor.get(cursor)
        
        if velocity_cursor is None:
            return None

        speed = geometry.norm(velocity_cursor)
        if(speed<self._min_velocity):
            return 0
        
        angle = abs(math.acos(geometry.dot(velocity_cursor,
                                           self._vector)))
        if angle > math.pi/2 :
            angle_score = 1.0 - (math.pi-angle) / (math.pi/2.0)
        else:
            angle_score = 1.0 - angle / (math.pi/2.0)

        return angle_score
    
    
        

class LineSimilarity:

    def __init__(self,
                 point1,
                 point2,
                 max_distance,
                 velocity):
        self._max_distance = max_distance
        self._p1 = np.array(point1)
        self._p2 = np.array(point2)
        self._velocity = velocity
        self._vector = [p2-p1
                        for p2,p1 in zip(point1,point2)]
        self._velocity_cursor = control.Velocity()

    def _line_distance(self,cursor):
        p = np.array(cursor)
        n1 = np.linalg.norm(self._p2-self._p1)
        n2 = np.linalg.norm(np.cross(self._p2-self._p1, self._p1-p))
        return n2/n1

    def __call__(self,cursor,_):

        if cursor is None:
            return None

        distance = self._line_distance(cursor)
        distance = min(distance,self._max_distance)
        distance_score =  1.0 - distance / self._max_distance

        velocity_cursor = self._velocity_cursor.get(cursor)
        
        if velocity_cursor is None:
            return None
            
        angle = abs(math.acos(geometry.dot(velocity_cursor,
                                           self._vector)))
        if angle > math.pi/2 :
            angle_score = 1.0 - (math.pi-angle) / (math.pi/2.0)
        else:
            angle_score = 1.0 - angle / (math.pi/2.0)

        speed = geometry.norm(velocity_cursor)
        if speed > self._velocity:
            speed_score = self._velocity / speed
        else:
            speed_score = speed / self._velocity 

        return (distance_score+angle_score+speed_score)/3.0

    
class DistanceSimilarity:

    def __init__(self,max_distance):

        self._max = max_distance

    def __call__(self,cursor,hard_target):

        if cursor is None:
            return None

        if hard_target is None:
            return None

        d = geometry.distance(cursor,hard_target)

        d = min(d,self._max)

        return 1.0 - d / self._max

class WeightedVelocitySimilarity:

    def __init__(self,weight_angle=0.5,
                 weight_norm=0.5,max_velocity=200):

        self._velocity_cursor = control.Velocity()
        self._velocity_hard_target = control.Velocity()
        self._weight_direction = weight_angle
        self._weight_norm = weight_norm
        self._weights  = weight_norm + weight_angle
        self._max_velocity = max_velocity

    def __call__(self,cursor,hard_target):

        velocity_cursor = self._velocity_cursor.get(cursor)
        velocity_hard_target = self._velocity_hard_target.get(hard_target)

        if velocity_cursor is None or velocity_hard_target is None:
            return None

        norm_cursor = geometry.norm(velocity_cursor)
        norm_hard_target = geometry.norm(velocity_hard_target)

        if norm_cursor > norm_hard_target:
            norm_similarity = norm_hard_target / norm_cursor
        else :
            norm_similarity = norm_cursor / norm_hard_target

        dot = geometry.dot(velocity_cursor,
                           velocity_hard_target)

        angle_similarity = 0.5+dot/2.0

        n = self._weight_norm*norm_similarity
        a = self._weight_direction*angle_similarity
        sim = (a+n)/self._weights
        return sim

class ProductVelocitySimilarity:

    def __init__(self,
                 max_velocity=200):

        self._velocity_cursor = control.Velocity()
        self._velocity_hard_target = control.Velocity()
        self._max_velocity = max_velocity

    def __call__(self,cursor,hard_target):

        velocity_cursor = self._velocity_cursor.get(cursor)
        velocity_hard_target = self._velocity_hard_target.get(hard_target)

        if velocity_cursor is None or velocity_hard_target is None:
            return None

        norm_cursor = geometry.norm(velocity_cursor)
        norm_hard_target = geometry.norm(velocity_hard_target)

        if norm_cursor > norm_hard_target:
            norm_similarity = norm_hard_target / norm_cursor
        else :
            norm_similarity = norm_cursor / norm_hard_target

        dot = geometry.dot(velocity_cursor,
                           velocity_hard_target)

        angle_similarity = 0.5+dot/2.0

        return angle_similarity*norm_similarity

