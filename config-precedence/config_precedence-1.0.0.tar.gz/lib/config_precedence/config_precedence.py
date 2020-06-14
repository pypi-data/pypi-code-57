class ConfigPrecedence:

    def __init__(self, config_options):
        self.config_options = config_options

    def sorted_config_options(self, reverse):
        return sorted(
            self.config_options,
            key=lambda cg: cg.precedence_value,
            reverse=reverse
        )

    def get_config_by_key(self, key, reverse=False):
        for config_option in self.sorted_config_options(reverse):
            if config_option.has_config_key(key):
                return config_option.get_config_by_key(key)
