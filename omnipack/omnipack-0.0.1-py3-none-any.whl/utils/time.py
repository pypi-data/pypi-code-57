import time


class Timer():
    def __init__(self):
        self._running = False
        self._interval_list = []
        self._interval_count = 0

    @property
    def is_running(self):
        return self._running

    @property
    def interval_count(self):
        return self._interval_count

    def clear(self):
        self._running = False
        self._interval_list = []
        self._interval_count = 0

    def start(self):
        self._running = True
        self._interval_list.append(time.time())

    def clock(self):
        if not self._running:
            raise Exception("Timer is not started")
        else:
            self._interval_list.append(time.time())
            self._interval_count += 1

    def stop(self):
        self._running = False

    def avg_interval(self):
        return self.total_time()/self._interval_count

    def total_time(self):
        return sum(self._interval_list)

    def since_last_clock(self):
        return time.time()-self._interval_list[-1]

    def since_start(self):
        return time.time()-self._interval_list[0]


def get_timestamp():
    return time.strftime('%Y%m%d_%H%M%S', time.localtime())
