"""
Module containing the reader for chimera.
"""

import os
import io
import avro.io
import avro.schema
from typing import List
from confluent_kafka import Message, Consumer
from chimera_client.environ import Environment
from chimera_client.schema import Schema
from typing import Any, Dict


class ChimeraConsumer:

    def __init__(self, channels):
        environ = Environment()
        self._consumer = Consumer({
            'bootstrap.servers': environ.bootstrapServers,
            'group.id': environ.chimeraNodeID,
            'auto.offset.reset': "earliest",
            'enable.auto.commit': False,
        })

        self._consumer.subscribe(channels)
        self._lastMessage: Message = None


class Consumers(dict):
    def __getitem__(self, key):

        # Get the specific channel consumer of Pipeline
        if key:
            return super().__getitem__(key)
        return super().__getitem__('all')
    def set_last_message(self, channel: str, message: Message):
        super().__getitem__(channel)._lastMessage = message


class Reader:
    """
    Reader is a class that reads messages from `Chimera`'s channels, and decodes them.
    """

    def __init__(self, readAll: bool = True):
        """
        Initializes the reader with all information needed.

        Parameter
            readAll: bool 

            True: Read messages comming from all channels.
            Call readMessage() with no parameters.

            False: Read messages from a scpecific channel.
            Call readMessage(channel) where channel is the desired channel.

        """
        environ = Environment()
        channels: List[str] = list(map(
            lambda x: environ.chimeraNamespace + "_" + x, environ.inputChannels.split(';')[:-1]))

        self.__consumers = Consumers()
        if readAll:
            self.__consumers['all'] = ChimeraConsumer(channels)
        else:
            # Create a consumer for each channel
            for channel in channels:
                self.__consumers[channel] = ChimeraConsumer(channel)

    def readMessage(self, channel: str = None) -> Any:
        """
        Reads a message from chimera.

        Returns the message read from channel.
        """

        

        while True:
            messageEncoded: Message = self.__consumers[channel]._consumer.poll(100)
            if messageEncoded is None:
                continue

            if messageEncoded.error():
                raise Exception('[READ MESSAGE]: ', messageEncoded.error())

            self.__consumers[channel]._lastMessage = messageEncoded
            try:
                chan = "_".join(messageEncoded.topic().split('_')[1:])
                # Decoding  message
                bytes_reader = io.BytesIO(messageEncoded.value())
                decoder = avro.io.BinaryDecoder(bytes_reader)
                schema = avro.schema.Parse(
                    Schema().getSchema(chan))
                reader = avro.io.DatumReader(schema)
                message = reader.read(decoder)

            except Exception as e:
                print("Couldn't desserialize message: ", message.value())
                print(e)
                continue

            return message

    def commit(self, channel: str = None):
        """
        Commits the last message received.
        """

        self.__consumers[channel]._consumer.commit(self.__consumers[channel]._lastMessage)

    def close(self, channel: str = None):
        """
        Closes connection with the chimera cluster.
        """

        self.__consumers[channel]._consumer.close()
