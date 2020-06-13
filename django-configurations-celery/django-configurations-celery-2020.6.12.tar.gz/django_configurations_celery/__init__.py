from configurations import Configuration, values

class CeleryConfiguration(Configuration):
    BROKER_URL = values.Value(environ_required=True)
    BROKER_CONNECTION_TIMEOUT = values.FloatValue(4.0)
    BROKER_CONNECTION_RETRY = values.BooleanValue(True)
    BROKER_CONNECTION_MAX_RETRIES = values.PositiveIntegerValue(100)
    CELERY_ACCEPT_CONTENT = values.ListValue(['application/json'])
    CELERY_ACKS_LATE = values.BooleanValue(False)
    CELERY_CREATE_MISSING_QUEUES = values.BooleanValue(True)
    CELERY_ENABLE_UTC = values.BooleanValue(True)
    CELERY_RESULT_SERIALIZER = values.Value('json')
    CELERY_TASK_SERIALIZER = values.Value('json')
    CELERY_TIMEZONE = values.Value('UTC')
    CELERY_IMPORTS = values.ListValue([])
    CELERY_INCLUDE = values.ListValue([])
    CELERYBEAT_SCHEDULER = values.Value('celery.beat:PersistentScheduler')
    CELERYBEAT_SCHEDULE_FILENAME = values.Value('celerybeat-schedule')
    CELERYBEAT_SYNC_EVERY = values.Value(0)
