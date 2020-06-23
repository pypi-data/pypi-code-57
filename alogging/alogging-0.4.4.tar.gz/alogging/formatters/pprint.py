import logging
import pprint


class PPrintRecordFormatter(logging.Formatter):
    '''Pretty print the __dict__ of the log record.'''
    def __init__(self, fmt=None, datefmt=None, options=None, indent=1, style='%'):
        super(PPrintRecordFormatter, self).__init__(fmt=fmt,
                                                    datefmt=datefmt,
                                                    style=style)

        self.indent = indent or options.get('indent') or 1

    def format(self, record):
        res_dict = record.__dict__.copy()
        message = record.getMessage()
        res_dict['message'] = message
        res = pprint.pformat(res_dict, indent=self.indent)
        return res

    def __repr__(self):
        buf = '%s(fmt="%s", options=%s, indent=%s)' % (self.__class__.__name__,
                                                       self._fmt, self.options,
                                                       self.indent)
        return buf
