import logging


class BuildLogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        self.logs.append(self.format(record))

    def clear(self):
        self.logs = []
