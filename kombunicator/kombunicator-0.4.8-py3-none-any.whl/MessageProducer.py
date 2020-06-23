
from kombu import Connection, Producer

from kombunicator.Exceptions import AMQPConnectionError


class MessageProducer():
    def __init__(self, connection_parameter: dict):
        """Create a message producer to publish messages
        to a RabbitMQ instance.

        Parameters
        ----------
        connection_parameter : `dict`
            Holds the connection parameters to a RabbitMQ instance.
            - 'hostname': `str` Host where RabbitMQ is accessible
            - 'virtual_host': `str` virtual host of RabbitMQ instance
            - 'port': `int` port to RabbitMQ instance
            - 'userid': `str` username
            - 'password': `str` password

        Raises
        ------
        `kombunicator.AMQPConnectionError`
        """
        self.connection_parameter = connection_parameter

        try:
            conn = Connection(**self.connection_parameter)
            conn.connect()
        except (ConnectionRefusedError, AttributeError, TypeError):
            raise AMQPConnectionError('AMQP connection cannot be established.')
        else:
            # when try was successful
            conn.release()

    def publish(self, message, headers: dict = {}, exchange: str = '',
                routing_key: str = 'default', correlation_id: str = ''):
        """Publish a message to the RabbitMQ instance.

        Parameters
        ----------
        message : `dict` or `str`
            Message to be published
        headers : `dict`
            Mapping of arbitrary headers to pass along
            with the message
        exchange : `str`
            Name of the exchange to publish a message to
        routing_key : `str`
            Queue routing key
        correlation_id : `str`
            correlation ID to match a specific message
        """
        with Connection(**self.connection_parameter) as connection:
            with Producer(connection) as producer:
                producer.publish(
                    body=message,
                    headers=headers,
                    exchange=exchange,
                    routing_key=routing_key,
                    correlation_id=correlation_id,
                    retry_policy={
                        'interval_start': 0,
                        'interval_step': 2,
                        'interval_max': 30,
                        'max_retries': 30
                    }
                )
