

class DjangoDbSqlCeleryFilter(object):
    '''Filter to prevent logging celery periodtasks'''

    def filter(self, record):
        sql = getattr(record, 'sql', None)
        if not sql:
            return 1
        if 'djcelery_periodictask' in sql:
            return 0

        return 1
