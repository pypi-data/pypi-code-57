import logging

from google.cloud.pubsub import SubscriberClient
from tenacity import wait_fixed, stop_after_attempt, retry


class PubsubMessageReceiver:

    def __init__(self, time_module, subscriber_client: SubscriberClient, batch_size: int = 1000) -> None:
        self.__subscriber_client = subscriber_client
        self.__batch_size = batch_size
        self._time_module = time_module

    def receive(self, subscription_path: str, timeout_seconds: int = 30, sleep_seconds: int = 0.5):
        time_limit = self._time_module.time() + timeout_seconds
        while self._time_module.time() < time_limit:
            pulled = self.__pull(subscription_path).received_messages

            ack_ids = []
            messages_received = []
            for message in pulled:
                ack_id = message.ack_id
                data_received = message.message
                ack_ids.append(ack_id)
                msg_in_bytes = data_received.data
                msg_received = msg_in_bytes.decode("utf-8")
                messages_received.append(msg_received)

            if len(ack_ids) != 0:
                self.__subscriber_client.acknowledge(subscription_path, ack_ids)

            for message in messages_received:
                yield message

            self._time_module.sleep(sleep_seconds)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def __pull(self, subscription_path: str):
        logging.debug("Pulling from subscription: {}".format(subscription_path))
        return self.__subscriber_client.pull(subscription_path, max_messages=self.__batch_size, return_immediately=True)
