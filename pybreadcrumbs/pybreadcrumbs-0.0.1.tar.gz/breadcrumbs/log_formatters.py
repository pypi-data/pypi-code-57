"""log_formatter.py."""
import logging

import ujson


class JSONLogFormatter(logging.Formatter):
    """JSONLogFormatter.

    A log formatter class which formats the log dict to a JSON string.
    with additional support for:
        remove unneeded keys
        add constant key value pair for each log.
    """
    def __init__(self, *args, **kwargs):
        """Init."""
        self.constant_keys = kwargs.pop("constant_keys", {})
        self.redundant_keys = kwargs.pop("redundant_keys", ())
        logging.Formatter.__init__(self)

    def format(self, record):
        """format."""
        data = record.__dict__.copy()

        for i in self.redundant_keys:
            data.pop(i, None)

        if len(self.constant_keys) > 0:
            data.update(self.constant_keys)
        if data.get("msg").__class__.__name__ == "dict":
            data.update(data.pop("msg"))
        return ujson.dumps(data)
