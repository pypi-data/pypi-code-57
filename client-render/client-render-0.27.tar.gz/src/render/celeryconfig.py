import os

broker_url = (
    'amqp://'
    f'{os.environ["RABBITMQ_DEFAULT_USER"]}'
    f':{os.environ["RABBITMQ_DEFAULT_PASS"]}'
    f'@{os.environ["RABBITMQ_HOST"]}'
    f':{os.environ.get("RABBITMQ_PORT", "5672")}'
    f'/{os.environ["RABBITMQ_DEFAULT_VHOST"]}'
)

task_routes = {
    'local': {'queue': 'local'},
    'rendering': {'queue': 'rendering'},
}

task_serializer = 'json'
accept_content = ['json']
enable_utc = True

task_acks_late = True
worker_prefetch_multiplier = 1
worker_concurrency = 1
worker_disable_rate_limits = True

worker_send_task_events = True
task_send_sent_event = True
