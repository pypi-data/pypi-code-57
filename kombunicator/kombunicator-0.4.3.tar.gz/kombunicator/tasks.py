
from celery import shared_task
from kombunicator.MessageProducer import MessageProducer

# see: https://stackoverflow.com/questions/48320227/import-shared-tasks-in-celery


@shared_task
def _rpc_server_publisher(message, connection_parameter: dict, routing_key: str, correlation_id: str):
    producer = MessageProducer(connection_parameter)
    producer.publish(
        message=message,
        routing_key=routing_key,
        correlation_id=correlation_id
    )
