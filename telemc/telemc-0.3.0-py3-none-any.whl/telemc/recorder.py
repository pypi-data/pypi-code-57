import os
import threading
from abc import ABC

from telemc.telemc import TelemetrySubscriber, Telemetry


class TelemetryRecorder(threading.Thread, ABC):

    def __init__(self, rds, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rds = rds
        self._sub = None

    def stop(self, timeout=None):
        """
        Equivalent to recorder.close() and recorder.join(timeout).

        :param timeout: the join timeout
        """
        self.close()
        self.join(timeout=timeout)

    def close(self):
        if self._sub:
            self._sub.close()

    def run(self):
        self._sub = TelemetrySubscriber(self.rds)
        sub = self._sub.run()

        try:
            for telemetry in sub:
                self._record(telemetry)
        finally:
            self._sub.close()

    def _record(self, telemetry: Telemetry):
        raise NotImplementedError


class TelemetryPrinter(TelemetryRecorder):

    def _record(self, telemetry):
        print(telemetry)


class TelemetryFileRecorder(TelemetryRecorder):
    """
       Records the output of a telemetry subscriber.

       :param rds: redis client
       :param fpath: the file to write to
       :param flush_every: the number of records to buffer before flushing
       """

    def __init__(self, rds, fpath, flush_every=1) -> None:
        super().__init__(rds)
        self.fpath = fpath
        self.flush_every = flush_every
        self.fd = None
        self.i = 0

    def run(self):
        with open(self.fpath, 'w') as fd:
            try:
                self.fd = fd
                super().run()
            finally:
                self.fd.flush()

    def _record(self, telemetry):
        self.i = (self.i + 1) % self.flush_every
        telemetry = [t or '' for t in telemetry]
        self.fd.write(','.join(telemetry) + os.linesep)
        if self.i == 0:
            self.fd.flush()
