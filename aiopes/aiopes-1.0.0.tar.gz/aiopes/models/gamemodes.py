class GameModesModel:
    def __init__(self, data):
        self.name = data["name"]
        self.key = data["key"]
        self.game_type = data["game_type"]
        self.game_mode = data["game_mode"]
