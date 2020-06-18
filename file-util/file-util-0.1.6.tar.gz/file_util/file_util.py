from pathlib import Path
import yaml


class File:
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def pathlib(self):
        return Path(self.path)

    @property
    def exists(self):
        return self.pathlib.exists()

    @property
    def does_not_exists(self):
        return not self.exists

    @property
    def is_yaml(self):
        return ".yaml" in self.path

    @property
    def text(self):
        return self.pathlib.read_text()

    def create(self):
        self.pathlib.touch()

    def write(self, text):
        self.pathlib.write_text(text)

    def read(self):
        return self.text

    def to_dict(self):
        if self.is_yaml:
            return yaml.safe_load(self.text)
        else:
            raise NotImplementedError
