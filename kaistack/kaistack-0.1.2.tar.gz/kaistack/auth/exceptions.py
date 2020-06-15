class NoAuthContextException(Exception):
    def __init__(self):
        super(NoAuthContextException, self).__init__("Cannot load context and no environment variable set too")
