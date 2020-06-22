import time
import sys


class Timer:
    def __init__(self, minutes):
        self.seconds = minutes * 60

    def count_down(self):
        endtime = time.time() + self.seconds

        while time.time() < endtime:
            time.sleep(10)


class Segment:
    def __init__(self, minutes, type_):
        self.minutes = minutes
        self.type = type_
        self.timer = Timer(minutes)

    def start(self):
        self.timer.count_down()


class Session:
    def __init__(self, segments):
        self.segments = iter(segments)
        self.current_segment = next(self.segments)

    def segment_type(self):
        return self.current_segment.type

    def next_segment(self):
        try:
            self.current_segment = next(self.segments)
            self.current_segment.start()
            return True
        except StopIteration:
            return False

    def start(self):
        self.current_segment.start()
        return True

    def stop(self):
        sys.exit(0)
