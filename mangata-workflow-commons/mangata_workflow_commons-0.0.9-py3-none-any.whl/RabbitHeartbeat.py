
import logging
import time
from threading import Thread, Event
import threading
import json
import pika
from typing import Any


class RabbitHeartbeat(Thread):
    """
    RabbitHeartbeat constructor for rabbitmq

    :param: logger object
    :param: connection object
    :param: int heartbeat
    :param: heartbeat_lock object
    :return: None
    """
    def __init__(self, logger: Any, connection: Any, heartbeat: int, heartbeat_lock: Any, group=None, target=None,
                 name=None, args=(), kwargs=None, verbose=None):
        # noinspection PyArgumentList
        super().__init__()
        self.logger = logger
        self.connection = connection
        self.heartbeat = heartbeat
        self.daemon = True
        self.signal = False
        self.heartbeat_lock = heartbeat_lock
        self._kill_the_wabbit = Event()

    def run(self) -> None:
        """
        run method to make rabbitmq connection
        :param: None
        :return: None
        """
        try:
            while not self._kill_the_wabbit.is_set():
                if self.signal:
                    self.logit("Processing RabbitMQ Heartbeat")

                    with self.heartbeat_lock:
                        self.connection.process_data_events()

                time.sleep(self.heartbeat)

        except Exception as ex:
            with self.heartbeat_lock:
                if self.logger:
                    self.logger.error(ex)

    def start_heartbeat(self):
        self.logit("Starting RabbitMQ Heartbeat Loop")
        self.signal = True

    def stop_heartbeat(self):
        self.logit("Stopping RabbitMQ Heartbeat Loop")
        self.signal = False

    def kill_the_wabbit(self):
        self._kill_the_wabbit.set()

    def logit(self, message):
        if self.logger:
            with self.heartbeat_lock:
                self.logger.debug(message)

