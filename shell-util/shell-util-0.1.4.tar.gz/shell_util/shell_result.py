

class ShellResult:

    STATUS_OK = 'OK'
    STATUS_ERROR = 'ERROR'

    def __init__(self, status, output, command):
        super().__init__()

        self._status = status
        self._output = output
        self._command = command

    def __repr__(self):
        output = f"<ShellResult status:{self.status_word}({self.status_int})>"
        return output

    @property
    def status_int(self):
        return self._status

    @property
    def status_word(self):
        if self.status_int == 0:
            return self.STATUS_OK
        else:
            return self.STATUS_ERROR

    @property
    def output(self):
        return self._output

    @property
    def command(self):
        return self._command





