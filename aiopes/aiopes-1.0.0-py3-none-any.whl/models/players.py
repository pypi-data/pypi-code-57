from datetime import datetime


class PlayersHistoryModel:
    def __init__(self, data):
        self.players = data["players"]
        self.time = datetime.utcfromtimestamp(
            data["time"]
        )
