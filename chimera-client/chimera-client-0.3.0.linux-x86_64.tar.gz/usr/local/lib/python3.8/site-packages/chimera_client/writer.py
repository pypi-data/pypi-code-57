"""
Module containing the `Chimera` writer class.
"""

import io
import os
import avro.io
import avro.schema
from typing import List
from confluent_kafka import Producer
from chimera_client.environ import Environment
from chimera_client.schema import Schema

class Writer:
    """
    Writer is a class that writes into chimera. 
    """

    def __init__(self):
        """
        Initializes the writer with the environment variables.
        """
        self.__environ = Environment()
        self._producer: Producer = Producer({'bootstrap.servers': self.__environ.bootstrapServers})


    def writeMessage(self, message: object, channel: str):
        """
        Writes a message in the given `Chimera` topic.

        The message should be in the format specified in the channel's avro schema, set previously.

        - message: the message that will be encoded.
        - channel: the channel on which the message will be sent

        """
        allowedTopics: List[str] = self.__environ.outputChannels.split(';')
        print(allowedTopics)
        if channel not in allowedTopics:
            raise Exception('Not allowed to write on channel ' + channel + '.')

        # Encoding message
        json = Schema().getSchema(channel)
        print(json)
        schema = avro.schema.Parse(json)
        avrowriter = avro.io.DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        avrowriter.write(message, encoder)

        value = bytes_writer.getvalue()

        self._producer.produce(
            topic=self.__environ.chimeraNamespace + "_" + channel, value=value)
        self._producer.flush()
