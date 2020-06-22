
import os
import random
import string
import celery


# broker stuff
broker_connection_parameter = {
    'hostname': os.environ.get('RABBITMQ_HOST', '127.0.0.1'),
    'port': os.environ.get('RABBITMQ_PORT', 5672),
    'userid': os.environ.get('RABBITMQ_DEFAULT_USER', 'guest'),
    'password': os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest')
}
cp = broker_connection_parameter
broker_url = f"amqp://{cp['userid']}:{cp['password']}@{cp['hostname']}:{cp['port']}"


# backend stuff
backend_connection_parameter = {
    'hostname': os.environ.get('REDIS_HOST', '127.0.0.1'),
    'port': os.environ.get('REDIS_PORT', 6379),
    'password': os.environ.get('REDIS_PASSWORD', '')
}
bp = backend_connection_parameter
backend_url = f"redis://:{bp['password']}@{bp['hostname']}:{bp['port']}/0"


celery_app = celery.Celery('tasks', broker=broker_url, backend=backend_url)

celery_app.conf.update(
    CELERY_BROKER=broker_url,
    CELERY_RESULT_BACKEND=backend_url,
    CELERY_IMPORTS=('test.rpc_server', 'kombunicator.tasks')
)


def get_random_string():
    return ''.join(random.choice(string.ascii_letters) for i in range(10))
