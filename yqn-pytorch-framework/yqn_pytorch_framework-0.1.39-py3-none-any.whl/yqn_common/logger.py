from datetime import datetime


class NTLogger:
    def __init__(self, context, verbose):
        self.context = context
        self.verbose = verbose

    def info(self, msg, **kwargs):
        if self.verbose:
            print('I:%s:%s:%s' % (str(datetime.now()), self.context, msg), flush=True)

    def debug(self, msg, **kwargs):
        if self.verbose:
            print('D:%s:%s:%s' % (str(datetime.now()), self.context, msg), flush=True)

    def error(self, msg, **kwargs):
        print('E:%s:%s:%s' % (str(datetime.now()), self.context, msg), flush=True)

    def warning(self, msg, **kwargs):
        print('W:%s:%s:%s' % (str(datetime.now()), self.context, msg), flush=True)
