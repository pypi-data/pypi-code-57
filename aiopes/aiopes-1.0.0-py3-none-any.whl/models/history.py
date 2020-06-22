from datetime import datetime


class HistoryModel:
    def __init__(self, data):
        self.metadata = data["metadata"]
        self.time = datetime.utcfromtimestamp(
            data["time"]
        )
        self.type = data["type"]
        self.user = data["user"]
