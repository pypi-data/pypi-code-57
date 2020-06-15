from typing import Dict


class Config():
    config: Dict = {}

    def get(self, dotkey=None, config=None):
        # Recursive for dot notation
        if not dotkey:
            return self.config
        if config is None: config = self.config
        if "." in dotkey:
            key, rest = dotkey.split(".", 1)
            return self.get(rest, config[key])
        else:
            return config[dotkey]

    def set(self, dotkey, value, config=None):
        # Recursive for dot notation
        # Remember objects are byRef, so changing config also changes self.config
        if config is None: config = self.config
        if "." in dotkey:
            key, rest = dotkey.split(".", 1)
            if key not in config:
                config[key] = {}
            return self.set(rest, value, config[key])
        else:
            config[dotkey] = value
            return value

        #self.config[dotkey] = value
        #return value

    def __call__(self, dotkey=None):
        return self.get(dotkey)
