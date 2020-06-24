from macrobase_driver.config import BaseConfig, DriverConfig, fields


class RabbitmqPropertyConfig(BaseConfig):
    host = fields.Str('localhost')
    port = fields.Int(5672)

    user        = fields.Str('rabbitmq')
    password    = fields.Str('test')

    vhost = fields.Str('/')


class QueuePropertyConfig(BaseConfig):
    name        = fields.Str('queue')
    auto_delete = fields.Bool(False)
    durable     = fields.Bool(True)


class AiopikaDriverConfig(DriverConfig):

    logo = fields.Str("""
 _____       _
|  __ \     (_)               
| |  | |_ __ ___   _____ _ __ 
| |  | | '__| \ \ / / _ \ '__|
| |__| | |  | |\ V /  __/ |   
|_____/|_|  |_| \_/ \___|_|aiopika""")

    workers = fields.Int(1)

    health_endpoint = fields.Bool(False)

    rabbitmq: RabbitmqPropertyConfig    = fields.Nested(RabbitmqPropertyConfig)
    queue: QueuePropertyConfig          = fields.Nested(QueuePropertyConfig)

    # Processing
    prefetch_count      = fields.Int(10)
    ignore_processed    = fields.Bool(True)
    requeue_delay       = fields.Int(10)
    default_retry_delay = fields.Int(60)
    requeue_unknown     = fields.Bool(False)
    requeue_if_failed   = fields.Bool(True)  # TODO: Set `requeue` for all AiopikaException subclasses

    sentry_dsn = fields.Str('', env_key='SENTRY_DSN')
    sentry_env = fields.Str('', env_key='SENTRY_ENV')
