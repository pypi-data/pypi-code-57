import math,time
from collections import deque


def linear_controller( previous_time,
                       current_position,
                       target_position,
                       kp ):

    t = time.time()
    if previous_time is None:
        return t,current_position
    delta_t = t - previous_time
    previous_time = t
    return previous_time, [ cp+kp*(tp-cp)*delta_t for cp,tp
                            in zip(current_position,target_position) ]


class Velocity:

    def __init__(self,estimation_period=0.5,memory=1000):
        self._period = estimation_period
        self._stamped_positions = deque([None
                                         for _ in range(memory)],memory)
        self._memory = 100

    def _get_previous(self,t):
        target_time = t-self._period
        for i in range(self._memory-1):
            candidate = self._stamped_positions[-i-1]
            if candidate is not None and candidate[1]<target_time:
                return candidate
        return None
            
    def get(self,position):

        t = time.time()
        self._stamped_positions.append((position,t))

        previous = self._get_previous(t)
        if previous is None:
            return None

        previous_position,previous_time = previous
        delta_t = t-previous_time
        delta_p = [p-pp for p,pp in zip(position,previous_position)]
        velocity = [dp-delta_t for dp in delta_p]
        return velocity



class Averager:

    def __init__(self,
                 average_period,
                 memory=50000):
        
        self._values = deque([None for _ in range(memory)],memory)
        self._average_period = average_period
        self._memory = memory
        
    def get(self,value):

        t = time.time()
        self._values.append((value,t))
        target_time = t - self._average_period
        target_index = 0
        for index in range(self._memory):
            candidate = self._values[-index-1]
            if candidate is None:
                break
            if candidate[1]<target_time:
                target_index = self._memory-index-1
                break
        values = list(self._values)[target_index:]
        values = [v[0] for v in values
                  if v is not None]
        if not values :
            return None
        return sum(values) / float(len(values))

