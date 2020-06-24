from swap.messaging.clients import MessageSubscriberClient
from swap.messaging.handlers import MessageHandler


class MessageListener:
    def __init__(self, config):
        self.handler = MessageHandler(config=config)
        self.subscriber_client = MessageSubscriberClient(
            project=config.project,
            topic=config.topic,
            subscription=config.subscription
        )

    def callback(self, message):
        message.ack()
        self.handler.handle(message)

    def listen(self):
        future = self.subscriber_client.subscribe(callback=self.callback)

        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
