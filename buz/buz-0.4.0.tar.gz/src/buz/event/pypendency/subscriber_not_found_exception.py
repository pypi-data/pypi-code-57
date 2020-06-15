class SubscriberNotFoundException(Exception):
    def __init__(self, subscriber_id: str):
        self.subscriber_id = subscriber_id
        super().__init__(
            f"Subscriber with id {subscriber_id} has not been found in the container and cannot be registered"
        )
