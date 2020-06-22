from datetime import datetime


class LogsModel:
    def __init__(self, data):
        self.log = data["log"]
        self.stream = data["stream"]
        self.time = datetime.fromisoformat(
            data["time"]
        )
