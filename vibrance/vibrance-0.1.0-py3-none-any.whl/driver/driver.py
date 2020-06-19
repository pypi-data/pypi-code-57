class Driver:
    """An object that reads from some input source and generates events.

    To do anything useful, this class should be subclassed, and the
    _open(), _close(), _read(), and getStatus() methods should be overridden.
    """
    def __init__(self, name=""):
        self.name = name
        self.enabled = False

    def _open(self):
        """Open any objects (e.g. ports) necessary for this Driver.

        This should be overridden. Subclasses can assume this will not be
        called if this Driver is already enabled.
        """
        pass

    def _close(self):
        """Close any objects (e.g. ports) necessary for this Driver.

        This should be overridden. Subclasses can assume this will not be
        called if this Driver is not enabled.
        """
        pass

    def _read(self):
        """Read any pending input and return a series of corresponding events.

        This should be overridden. Subclasses can assume this will not be
        called if this Driver is not enabled.
        """
        return tuple()

    def open(self):
        """Open this Driver so that it can be read from."""
        if not self.enabled:
            self._open()
        self.enabled = True

    def close(self):
        """Close this Driver."""
        if self.enabled:
            self._close()
        self.enabled = False

    def read(self):
        """Return a series of events from this Driver's input."""
        if self.enabled:
            return self._read()
        else:
            return tuple()

    def getStatus(self):
        """Get the current health and status message of this Driver."""
        status = {}
        status["health"] = "inactive"
        status["message"] = "No Driver"

        return status
