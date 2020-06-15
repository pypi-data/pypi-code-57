from buz.event import Subscriber


class SubscriberAlreadyRegisteredException(Exception):
    def __init__(self, subscriber: Subscriber):
        self.subscriber = subscriber
        super().__init__("Subscriber has been registered and cannot be registered another time")
