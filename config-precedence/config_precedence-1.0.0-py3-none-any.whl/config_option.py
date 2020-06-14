import abc


class ConfigOption(abc.ABC):

    def __init__(self, precedence_value):
        self.precedence_value = precedence_value

    def __repr__(self):
        return "<ConfigOption(precedence_value={})>".format(
            self.precedence_value)

    @abc.abstractmethod
    def get_config_by_key(self, key):
        pass

    @abc.abstractmethod
    def has_config_key(self, key):
        pass
