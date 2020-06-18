class CommandNotFoundError(RuntimeError):
    def __init__(self, message):
        super(CommandNotFoundError, self).__init__(message)
