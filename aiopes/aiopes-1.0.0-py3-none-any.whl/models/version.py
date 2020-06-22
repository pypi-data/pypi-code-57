class VersionModel:
    def __init__(self, data):
        self.server = data["server_version"]
        self.node = data["node_version"]
        self.out_of_date = data["server_out_of_date"]
