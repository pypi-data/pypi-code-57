from ruamel_yaml import YAML


class Hyamler(YAML):

    def __init__(self, config_file, run_file):
        self.metadata = dict()
        self.conf_file = config_file
        self.run_file = run_file

    def load_config(self):
        with open(self.conf_file, 'r') as c:
            conf = self.load(c)
        self.metadata = conf

    def add_metadata(self, key1, key2, value, *args, **kwargs):
        key3 = kwargs.get('key3', None)

        if key3 is not None:
            self.metadata[key1][key2][key3] = value
        else:
            self.metadata[key1][key2] = value

    def write_metadata(self):
        with open(self.run_file, "w") as mdf:
            self.dump(self.metadata, mdf)
