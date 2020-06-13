import yaml

class ConfigFromYAML:

    def __init__(self, FILE_LOC):
        self.FILE = FILE_LOC
        self._loaddata()

    def _loaddata(self):
        with open(self.FILE, 'r') as infile:
            try:
                self.__dict__.update(yaml.safe_load(infile))
            except yaml.YAMLError as errors:
                raise errors.InvalidPackageListFormat("Invalid YAML in package list: %s" % str(ex))
    
    def dumpconfig(self, diff=True):
        if diff:
            suffix = "_mod." + self.FILE.split('.')[-1]
            file_loc = self.FILE[:-4] + suffix
        else:
            file_loc = self.FILE
                
        with open(file_loc, 'w') as dumpfile:
            yaml.dump(self.__dict__, dumpfile)

        return "you file has successfully saved"
    
    def make_global(self):
        yapl.config = self
