from configurations import Configuration, values

class CeleryConfiguration(Configuration):
    CELERY_ACCEPT_CONTENT = values.ListValue(['application/json'])
    CELERY_ENABLE_UTC = values.BooleanValue(True)
    CELERY_IMPORTS = values.ListValue([])
    CELERY_INCLUDE = values.ListValue([])
    CELERY_TIMEZONE = values.Value('UTC')

    CELERYBEAT_MAX_LOOP_INTERVAL = values.Value(0)
    CELERYBEAT_SCHEDULE = {}
    CELERYBEAT_SCHEDULER = values.Value('celery.beat:PersistentScheduler')
    CELERYBEAT_SCHEDULE_FILENAME = values.Value('celerybeat-schedule')
    CELERYBEAT_SYNC_EVERY = values.PositiveIntegerValue(0)

    BROKER_URL = values.Value(None)
    # BROKER_TRANSPORT
    BROKER_TRANSPORT_OPTIONS = {}
    BROKER_CONNECTION_TIMEOUT = values.FloatValue(4.0)
    BROKER_CONNECTION_RETRY = values.BooleanValue(True)
    BROKER_CONNECTION_MAX_RETRIES = values.PositiveIntegerValue(100)
    BROKER_FAILOVER_STRATEGY = values.Value('round-robin')
    BROKER_HEARTBEAT = values.FloatValue(120.0)
    BROKER_LOGIN_METHOD = values.Value('AMQPLAIN')
    BROKER_POOL_LIMIT = values.PositiveIntegerValue(10)
    BROKER_USE_SSL = values.BooleanValue(False)

    # CELERY_CACHE_BACKEND no longer used
    CELERY_CACHE_BACKEND_OPTIONS = {}

    CASSANDRA_COLUMN_FAMILY = values.Value(None)
    CASSANDRA_ENTRY_TTL = values.PositiveIntegerValue(None)
    CASSANDRA_KEYSPACE = values.Value(None)
    CASSANDRA_PORT = values.PositiveIntegerValue(9042)
    CASSANDRA_READ_CONSISTENCY = values.Value(None)
    CASSANDRA_OPTIONS = {}

    S3_ACCESS_KEY_ID = values.Value(None)
    S3_SECRET_ACCESS_KEY = values.Value(None)
    S3_BUCKET = values.Value(None)
    S3_BASE_PATH = values.Value(None)
    S3_ENDPOINT_URL = values.Value(None)
    S3_REGION = values.Value(None)

    CELERY_COUCHBASE_BACKEND_SETTINGS = {}
    CELERY_ARANGODB_BACKEND_SETTINGS = {}
    CELERY_MONGODB_BACKEND_SETTINGS = {}

    CELERY_EVENT_QUEUE_EXPIRES = values.FloatValue(60.0)
    CELERY_EVENT_QUEUE_TTL = values.FloatValue(5.0)
    CELERY_EVENT_QUEUE_PREFIX = values.Value('celeryev')
    CELERY_EVENT_SERIALIZER = values.Value('json')

    CELERY_REDIS_DB = values.Value(None)
    CELERY_REDIS_HOST = values.Value(None)
    CELERY_REDIS_MAX_CONNECTIONS = values.PositiveIntegerValue(None)
    CELERY_REDIS_PASSWORD = values.Value(None)
    CELERY_REDIS_PORT = values.PositiveIntegerValue(None)
    CELERY_REDIS_BACKEND_USE_SSL = values.BooleanValue(False)

    CELERY_RESULT_BACKEND = values.Value(None)
    CELERY_MAX_CACHED_RESULTS = values.BooleanValue(False)
    CELERY_MESSAGE_COMPRESSION = values.Value(None)

    CELERY_RESULT_EXCHANGE = values.Value(None)
    CELERY_RESULT_EXCHANGE_TYPE = values.Value(None)
    # CELERY_RESULT_EXPIRES timedelta 1 day.
    CELERY_RESULT_PERSISTENT = values.BooleanValue(False)
    CELERY_RESULT_SERIALIZER = values.Value('json')
    CELERY_RESULT_DBURI = values.Value(None)
    CELERY_RESULT_ENGINE_OPTIONS = {}
    # _DB_SHORT_LIVED_SESSIONS
    CELERY_RESULT_DB_TABLE_NAMES = values.ListValue([])
    CELERY_SECURITY_CERTIFICATE = values.Value(None)
    CELERY_SECURITY_CERT_STORE = values.Value(None)
    CELERY_SECURITY_KEY = values.Value(None)

    CELERY_ACKS_LATE = values.BooleanValue(False)
    CELERY_ACKS_ON_FAILURE_OR_TIMEOUT = values.BooleanValue(True)
    CELERY_ALWAYS_EAGER = values.BooleanValue(False)
    CELERY_ANNOTATIONS = None # dict/list
    CELERY_COMPRESSION = values.Value(None)
    CELERY_CREATE_MISSING_QUEUES = values.BooleanValue(True)
    CELERY_DEFAULT_DELIVERY_MODE = values.Value('persistent')
    # CELERY_DEFAULT_EXCHANGE
    CELERY_DEFAULT_EXCHANGE_TYPE = values.Value('direct')
    CELERY_DEFAULT_QUEUE = values.Value('celery')
    CELERY_DEFAULT_RATE_LIMIT = values.Value(None)
    # CELERY_DEFAULT_ROUTING_KEY str
    CELERY_EAGER_PROPAGATES = values.BooleanValue(False)
    CELERY_IGNORE_RESULT = values.BooleanValue(False)
    CELERY_PUBLISH_RETRY = values.BooleanValue(True)
    # CELERY_PUBLISH_RETRY_POLICY
    CELERY_QUEUES = None
    CELERY_ROUTES = None
    CELERY_SEND_SENT_EVENT = values.BooleanValue(False)
    CELERY_SERIALIZER = values.Value('json')
    CELERYD_SOFT_TIME_LIMIT = values.PositiveIntegerValue(None)
    CELERYD_TIME_LIMIT = values.PositiveIntegerValue(None)
    CELERY_TRACK_STARTED = values.BooleanValue(False)

    CELERYD_AGENT = values.Value(None)
    CELERYD_AUTOSCALER = values.Value('celery.worker.autoscale:Autoscaler')
    CELERYD_CONCURRENCY = values.PositiveIntegerValue(None)
    CELERYD_CONSUMER = values.Value('celery.worker.consumer:Consumer')

    CELERY_WORKER_DIRECT = values.BooleanValue(False)
    CELERY_DISABLE_RATE_LIMITS = values.BooleanValue(False)
    CELERY_ENABLE_REMOTE_CONTROL = values.BooleanValue(True)
    CELERYD_HIJACK_ROOT_LOGGER = values.BooleanValue(True)
    # CELERYD_LOG_COLOR
    CELERYD_LOG_FORMAT = values.Value('[%(asctime)s: %(levelname)s/%(processName)s] %(message)s')
    CELERYD_WORKER_LOST_WAIT = values.FloatValue(10.0)
    CELERYD_MAX_TASKS_PER_CHILD = values.PositiveIntegerValue(None)
    CELERYD_POOL = values.Value('prefork')
    # CELERYD_POOL_PUTLOCKS ?
    CELERYD_POOL_RESTARTS = values.BooleanValue(False)
    CELERYD_PREFETCH_MULTIPLIER = values.PositiveIntegerValue(4)
    CELERYD_REDIRECT_STDOUTS = values.BooleanValue(True)
    CELERYD_REDIRECT_STDOUTS_LEVEL = values.Value('WARNING')
    CELERY_SEND_EVENTS = values.BooleanValue(False)
    CELERYD_STATE_DB = values.Value(None)
    CELERYD_TASK_LOG_FORMAT = values.Value("""[%(asctime)s: %(levelname)s/%(processName)s]
[%(task_name)s(%(task_id)s)] %(message)s""")
    CELERYD_TIMER = values.Value(None)
    CELERYD_TIMER_PRECISION = values.FloatValue(1.0)
