import multiprocessing

from . import driver


class PipeDriver(driver.Driver):
    """Driver that reads input from a separate thread.

    Useful for reading input from event-based systems (e.g. GUI apps).
    """
    def __init__(self, name="", driver_type="pipe"):
        super().__init__(name)
        self.driver_type = driver_type

        self.in_pipe, self.out_pipe = multiprocessing.Pipe()

    def launch(self, event_type, obj={}):
        self.in_pipe.send((event_type, obj))

    def _read(self):
        events = []
        while self.out_pipe.poll():
            event_type, event_attrs = self.out_pipe.recv()

            events.append({"driver": self.driver_type,
                           "type": event_type, **event_attrs})

        return tuple(events)

    def getStatus(self):
        status = {}

        if self.enabled:
            status["health"] = "success"
            status["message"] = "Pipe Enabled"
        else:
            status["health"] = "inactive"
            status["message"] = "Pipe Disabled"

        return status
