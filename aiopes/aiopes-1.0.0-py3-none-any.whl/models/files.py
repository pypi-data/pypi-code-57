from datetime import datetime


class FilesModel:
    def __init__(self, data):
        self.name = data["name"]
        self.md5 = data["md5"]
        self.size = data["size"]
        self.last_modified = datetime.utcfromtimestamp(
            data["last_modified"]
        )
        self.link = data["link"]
