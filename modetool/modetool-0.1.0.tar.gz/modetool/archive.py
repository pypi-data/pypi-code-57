import os
import pathlib
import re
import zipfile

from py7zr import Bad7zFile, SevenZipFile


class InvalidArchive(Exception):
    pass


class Archive:
    def __init__(self, file):
        try:
            self.archive = (
                zipfile.ZipFile(file, mode="r")
                if zipfile.is_zipfile(file)
                else SevenZipFile(file, mode="r")
            )
        except Bad7zFile:
            raise InvalidArchive

    @property
    def name(self):
        return pathlib.Path(self.archive.filename).stem

    @property
    def region(self):
        results = re.findall(r"\((.*?)\)", self.name)
        return results[0] if results else None

    def extract(self, dest):
        self.archive.extractall(path=os.path.join(dest, self.name))
