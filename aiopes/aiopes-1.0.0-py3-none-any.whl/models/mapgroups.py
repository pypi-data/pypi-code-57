class MapGroupsMapModel:
    def __init__(self, data):
        self.name = data["name"]
        self.key = data["key"]


class MapsModel:
    def __init__(self, data):
        self.data = data

    def maps(self):
        for map_name in self.data.values():
            yield MapGroupsMapModel(map_name)


class MapGroupsModel:
    def __init__(self, data):
        self.name = data["name"]
        self.key = data["key"]
        self.maps = MapsModel(data["maps"]).maps
