class IllegalArgumentError(RuntimeError):
    def __init__(self, message):
        super(IllegalArgumentError, self).__init__(message)
