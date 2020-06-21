from .base import FileReader, DataDumper


class CSV(FileReader, DataDumper):
    ext = 'csv',

    def load_file(self, path):
        from csv import DictReader
        with open(path) as inp:
            data = list(DictReader(inp))
        return data
