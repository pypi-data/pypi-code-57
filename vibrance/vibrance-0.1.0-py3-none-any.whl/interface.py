import logging


class Interface:
    """Provides a user-friendly API for creating color messages and launching
    user functions based on input."""

    def __init__(self, name=""):
        self.name = name

        self.clear()
        self.callbacks = {}
        self.loopCallback = None
        self.onTelemetryCallback = None

        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting interface")

    def clear(self):
        """Clears the messages buffer and resets the delay offset."""
        self.messages = {}
        self.delay = 0

    def add(self, zone, color=None, **kwargs):
        """Adds a new message to the messages buffer."""

        if zone not in self.messages:
            self.messages[zone] = []

        message = {}
        if color is not None:
            message["color"] = color

        for key, val in kwargs.items():
            message[key] = val

        self.messages[zone].append(message)

    def color(self, zones, color):
        """Creates a message to show the given color on the given ports after
        the delay offset."""

        if hasattr(zones, "__iter__"):
            for zone in zones:
                self.add(zone, color, delay=self.delay)
        else:
            self.add(zones, color, delay=self.delay)

    def wait(self, sec):
        """Adds to the current delay offset."""
        self.delay += sec * 1000

    def onTelemetry(self, func):
        """Launches the function when new telemetry data is received."""
        self.onTelemetryCallback = func
        return func

    def update(self, ctrl):
        """Sends the current messages to a relay through the provided
        controller, then clears the internal message buffer and delay
        offset."""
        telemetry = ctrl.write(self.messages)
        if self.onTelemetryCallback:
            self.onTelemetryCallback(telemetry)
        self.clear()

    def on(self, driver, event):
        if driver not in self.callbacks:
            self.callbacks[driver] = {}

        def decorator(func):
            self.logger.info("Registering %s for callback %s, %s",
                             func, driver, event)
            self.callbacks[driver][event] = func
            return func
        return decorator

    def loop(self, func):
        self.logger.info("Registering %s as a loop function", func)
        self.loopCallback = func
        return func

    def handle(self, driver, ctrl):
        if self.loopCallback:
            self.loopCallback()
            self.update(ctrl)
        for event in driver.read():
            if event["driver"] in self.callbacks:
                if event["type"] in self.callbacks[event["driver"]]:
                    self.callbacks[event["driver"]][event["type"]](event)
                    self.update(ctrl)

    def run(self, driver, ctrl):
        while True:
            self.handle(driver, ctrl)

    def getStatus(self):
        status = {}
        if self.name == "None":
            status["health"] = "inactive"
            status["message"] = "No Script"
        else:
            status["health"] = "success"
            status["message"] = f"{self.name} loaded"
        return status
