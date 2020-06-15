from buz.event import Subscriber


class SubscriberNotRegisteredException(Exception):
    def __init__(self, subscriber: Subscriber):
        self.subscriber = subscriber
        super().__init__("Subscriber has not been registered and cannot be unregistered")
