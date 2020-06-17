# -*- coding: utf-8 -*-
"""
kafka module
"""

import json

from kafka import KafkaProducer

from sail_utils import LOGGER


class Producer:
    """
    kafka message producer
    """

    def __init__(self, hosts, topic):
        self._topic = topic
        self._producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                       bootstrap_servers=hosts)

    def write(self, msg):
        """
        send message
        :param msg:
        :return:
        """
        LOGGER.info("sending: {0}".format(msg))
        self._producer.send(self._topic, value=msg)
        self._producer.flush()

    def __str__(self):
        return f"<{self._producer}> - <{self._topic}>"
