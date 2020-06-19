from time import time

from .interactive import pr


class IterationTimer:
    def __init__(self, total: int, init_interval: int = 1, max_interval: int = 15, interval_amp_mod: float = 2):
        if total < 1:
            raise ValueError('"total" cannot be lower than 1')
        if init_interval < 1:
            raise ValueError('"init_interval" cannot be lower than 1')
        if max_interval < init_interval:
            raise ValueError(
                '"max_interval" cannot be lower than "init_interval"')
        if interval_amp_mod < 1.0:
            raise ValueError('"interval_amp_mod" cannot be lower than 1')

        self.total = total
        self.interval = init_interval
        self.max_interval = max_interval
        self.current = self.last = 0
        self.lt = time()

    def tick(self) -> None:
        # Progress
        c = self.current = self.current + 1
        ts = time()

        if ts - self.lt > self.interval:
            # Show status
            delta = c - self.last
            if not delta:
                return pr('No progression!', '!')
            spd = int(delta / self.interval)
            prcnt = c / (self.total / 100)
            eta = int((self.total - c) / spd)
            pr('%.2f%% ' % prcnt +
               f'[{c}/{self.total}]\t@ {spd} ps\tETA: {eta} secs')

            # Checkpoint
            self.lt = ts
            self.last = c
            if self.interval <= self.max_interval:
                self.interval *= 2
