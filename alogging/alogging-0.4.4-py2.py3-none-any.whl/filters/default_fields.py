import logging


class DefaultFieldsFilter(logging.Filter):
    '''Make sure log records have a default value for the provided field/attribute

    ie, if you want to use a default format string with a 'request_id' or 'sql'
    attribute, but not all records get those attributes added, then you could
    add this filter to add them'''

    def __init__(self, name="", defaults=None):
        super(DefaultFieldsFilter, self).__init__(name=name)
        self.defaults = defaults or {}

    def filter(self, record):
        for attr_name, default_value in self.defaults.items():
            if not hasattr(record, attr_name):
                setattr(record, attr_name, default_value)

        return True
