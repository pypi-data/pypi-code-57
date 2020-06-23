import logging

import sqlparse

HAS_PYGMENTS = True
try:
    from .django_sql_color import DjangoDbSqlColorFormatter
except ImportError:
    HAS_PYGMENTS = False

# TODO: Could add a filter that uses sqlparse to extract record attributes
#       for table, statement type, etc.


class DjangoDbSqlPlainFormatter(logging.Formatter):
    '''pretty print django.db sql'''

    def __init__(self, fmt=None, datefmt=None, options=None, style='%'):
        super(DjangoDbSqlPlainFormatter, self).__init__(fmt=fmt,
                                                        datefmt=datefmt,
                                                        style=style)

        self.options = options or {'reindent': True,
                                   'keyword_case': 'upper'}

    def format(self, record):
        pretty_sql = sqlparse.format(record.sql,
                                     **self.options)

        record.sql = pretty_sql
        # import pprint
        # return '\n__dict__=%s\n' % pprint.pformat(record.__dict__)
        return super(DjangoDbSqlPlainFormatter, self).format(record)

    def __repr__(self):
        buf = 'DjangoDbSqlFormatter(fmt="%s", options=%s)' % (self._fmt, self.options)
        return buf


DjangoDbSqlFormatter = DjangoDbSqlPlainFormatter
if HAS_PYGMENTS:
    DjangoDbSqlFormatter = DjangoDbSqlColorFormatter
