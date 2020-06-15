from configparser import ConfigParser


class CommonConf(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)
        self.add_sec = "Additional"

    def optionxform(self, option_str):
        return option_str
