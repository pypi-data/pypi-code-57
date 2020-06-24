from swap.messaging.registries import DefaultRegistry


class MessageHandler:
    def __init__(self, config, registry=DefaultRegistry):
        self.config = config
        self.registry = registry(config=config)

    def register_callback(self, message_type, callback):
        self.registry.register_callback(message_type=message_type, callback=callback)

    def action(self, message_type):
        return self.registry.action(message_type)

    def callback(self, message_type):
        return self.registry.callback(message_type)

    def handle(self, message):
        message_type = message.attributes.get('message_type')
        action = self.action(message_type=message_type)
        callback = self.callback(message_type=message_type)

        action.call(message_type=message_type, message=message, callback=callback)
