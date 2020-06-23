import logging


class DjangoDbSqlExcludeFilter(logging.Filter):
    '''Filter to prevent logging misc queries'''

    def __init__(self, name="", excludes=None):
        super(DjangoDbSqlExcludeFilter, self).__init__(name=name)
        self.excludes = excludes or []

    def filter(self, record):
        sql = getattr(record, 'sql', None)
        if not sql:
            return 1

        # TODO: use any(), set ops, etc
        for exclude in self.excludes:
            if exclude in sql:
                return 0

        return 1
