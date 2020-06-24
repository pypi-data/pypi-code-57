
from celery import Celery
from celery import Signature
from strongtyping.strong_typing import match_typing

from kombunicator.MessageConsumer import MessageConsumer

# How it works:
# RPCServer is a MessageConsumer, i.e. a direct consumer, which is a thread itself.
# RPCServer provides a producer function, which must be registered as a celery task.
# The callback method passed into the RPC server must be a celery task, too.
# result_publisher is then chain attached (celery.chain) to the callback method.


class RPCServer(MessageConsumer):

    @match_typing
    def __init__(self, connection_parameter: dict, listening_key: str, celery_app: Celery,
                 processing_task_name: str, ready):
        super().__init__(
            connection_parameter=connection_parameter,
            consumer_type='direct',
            binding_keys=[listening_key]
        )

        self.celery_app = celery_app
        self._thread_ready = ready

        # the name of the registered celery task is the
        # main application to process the data.
        self.processing_task_name = processing_task_name
        self.register_message_handler(self._on_message)

    def _on_message(self, payload, headers, properties):

        # if the incoming request has headers the processing task of the server has to accept these as an argument.
        task_args = (payload, headers) if headers else (payload, )

        # see: https://stackoverflow.com/questions/31239241/chain-two-remote-tasks-in-celery-by-send-task
        self.celery_app.send_task(
            name=self.processing_task_name,
            args=task_args,
            chain=[
                Signature(
                    'kombunicator.tasks._rpc_server_publisher',
                    kwargs={
                        'connection_parameter': self.connection_parameter,
                        'routing_key': properties.get('reply_to', ''),
                        'correlation_id': properties.get('correlation_id', '')
                    }
                )
            ]
        )
