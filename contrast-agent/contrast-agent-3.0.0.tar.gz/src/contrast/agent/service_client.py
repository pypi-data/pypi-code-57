# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import socket
import struct
import time

from contrast.agent.connection_status import ConnectionStatus
from contrast.agent.service_config import ServiceConfig
from contrast.api.dtm_pb2 import (
    Activity,
    AgentStartup,
    ApplicationCreate,
    ApplicationUpdate,
    HttpRequest,
    Message,
    ObservedRoute,
    Poll,
    ServerActivity,
)
from contrast.api.settings_pb2 import AgentSettings
from contrast.utils.exceptions.contrast_service_exception import (
    ContrastServiceException,
)
from contrast.utils.service_util import ServiceUtil
from contrast.utils.timer import Timer

import logging

logger = logging.getLogger("contrast")


class ServiceClient(object):
    client_count = 0
    RECV_FMT = ">I"

    APPLICATION_LANGUAGE = "Python"

    def __init__(self, config, app_name):
        self.service_config = ServiceConfig(config)
        self.app_name = app_name

        self.number = ServiceClient.client_count = ServiceClient.client_count + 1

        self.count = 0
        self.success = 0
        self.failure = 0

        self.config = config
        self.send_as_json = True  # always true for the python agent

        self.connection_status = ConnectionStatus()

        # this will hold the master pid if we get forked
        self.parent_pid = os.getpid()

        self.bundled_flag = "external"

    def initialize_and_send_messages(self, initial_messages):
        """
        Initializing the connection to Contrast Service requires checking if the app is configured
        to use the bundled service and turning it on if so.

        If the app isn't configured to use the bundled service or after turning the bundled service on,
        agent sends initial messages to Contrast Service (AgentStartup, ApplicationCreate, ApplicationUpdate)
        to determine that it is successfully able to communicate with it.

        If configuration specifies an external service, whatever manages the external service should handle cases
        of the service being down. The agent should not be responsible for managing service state in this case.

        :return: list of Message responses

        """
        responses = []

        if self.is_bundled_enabled and self.local_service_configured:
            self.bundled_flag = "bundled"

            if not self.start_service():
                # if bundled service is configured but it could not be started, return empty responses
                return responses

        logger.info("Will communicate with Contrast Service")

        # it's only necessasry to wait to send messages when using the bundled service because it takes a bit to start up
        wait = 1 if self.bundled_flag == "bundled" else 0
        return self.send_messages_retry(initial_messages, wait=wait)

    @property
    def is_bundled_enabled(self):
        """The default across agents is to use the bundled service by default"""
        return self.config.get("agent.service.enable", True)

    @property
    def local_service_configured(self):
        return self.service_config.local_service_configured

    def is_connected(self):
        """
        Are we currently connected?
        """
        return self.connection_status.connected

    def was_connected(self):
        """
        Were we connected?
        """
        return self.connection_status.was_connected

    def send_dtm(self, message):
        """
        This takes in a json string so that we can encode and decode in separate tasks

        :param message: json string representation of the dtm object
        :return: json string of the response
        :side effect: ContrastServiceException if any problems connecting / sending messages occur
        """
        packed = message.SerializeToString()
        sock = None
        try:
            sock = socket.socket(self.service_config.socket_type, socket.SOCK_STREAM)
            sock.connect(self.service_config.address)
            self.send_message(sock, packed)
            response = self.receive_message(sock)

            if response is not None:
                settings = AgentSettings()
                settings.ParseFromString(response)
                return settings

            logger.warning("Received an empty response from Contrast Service")
        except Exception:
            # If there are any issues connecting or sending messages to Contrast Service,
            # we raise a special exception for middleware handle_exception to catch but not raise
            # so the request can be processed without the agent.
            raise ContrastServiceException
        finally:
            if sock is not None:
                sock.close()

    def start_service(self):
        """
        Start the bundled service.

        Should not be run if the user would like to connect to an external service.

        :return: bool if bundled Contrast Service was started.
        """
        logger.info(
            "Attempted to start bundled Contrast Service for application %s.",
            self.app_name,
        )
        logger.info(
            "If socket already exists at %s, will attempt to connect to that instead",
            self.service_config.address,
        )

        path = self.config.get("agent.service.logger.path")

        if ServiceUtil(path).start_bundled_service():
            return True

        logger.error("Contrast Service did not start")
        return False

    def send_messages_retry(self, messages, attempts=0, wait=0, raise_exception=True):
        """
        Attempt to send a list of messages to Speedracer. If sending messages fails, this method
        recursively calls itself to attempt to resend 3 times.

        If after 3 times sending messages still failed, the connection status is set to faise
        and the exception may or may not be raised.

        :param messages: message(s) to to send to Speedracer
        :param attempts: a count of number of attempts to send to messages.
        :param wait: seconds to wait before sending the messages.
            This is used when the bundled service is getting started (start_service has been called)
            because sometimes it takes a second for it to get setup.
        :param raise_exception: bool to determine if to raise an exception or not
            The caller of this method will determine if to ask this method to raise the exception or not.
            Currently the logic is that the caller will ask to raise the exception if the caller itself is catching for it.

            Current callers that will ask for this exception to be raised are:
            1. when initializing communication to Speedracer, because the middleware needs to know if this initialization
                has failed to set settings initialization to false.
            2. when input analysis messages are send to Speedracer, because the middleware needs to know if
                this analysis has failed to re-route the request to call_without_agent.

            Current callers that will not want the exception to be raised:
            1. when final messages are sent to Speedracer for reporting. The middleware is not equipped
                to handle an exception at that time, so if sending these messages fails, the reporting will fail
                but the application should not.

        :return: list of responses from Speedracer
        :side effect: ContrastServiceException if raise_exception is True
        """
        time.sleep(wait)

        try:
            return self._send_messages(messages)
        except ContrastServiceException:
            logger.debug(
                "Trying to send messages, but received ContrastServiceException"
            )

            if attempts < 3:
                if self.bundled_flag == "bundled":
                    # this may lead to multiple contrast-service processes existing on the same host if
                    # the first initialized process is not up before other app workers / threads attempt
                    # to start the service.
                    self.start_service()
                logger.debug("Retrying to send messages...")
                return self.send_messages_retry(
                    messages, attempts + 1, wait, raise_exception
                )

            logger.warning(
                "Unable to send messages to Contrast Service after 3 attemps."
            )
            self.connection_status.failure()
            if raise_exception:
                raise

        return []

    def _send_messages(self, messages):
        responses = []
        to_send = [messages] if not isinstance(messages, list) else messages
        to_send = self.update_messages(to_send)

        logger.debug("Sending %s messages to Contrast Service", len(to_send))
        for agent_message, msg in zip(messages, to_send):
            logger.debug(
                "Sending %s message with msg_count=%s, pid=%s",
                agent_message.__class__.__name__,
                msg.message_count,
                msg.pid,
            )

            response = self.send_dtm(msg)
            if response is not None:
                logger.debug(
                    "Received response for message with msg_count=%s, pid=%s",
                    msg.message_count,
                    msg.pid,
                )
                responses.append(response)
            else:
                logger.debug(
                    "No response for message with msg_count=%s, pid=%s",
                    msg.message_count,
                    msg.pid,
                )

        self.connection_status.success()
        return responses

    def update_message(self, agent_message):
        message = self.build_empty_message()

        if isinstance(agent_message, Activity):
            agent_message.duration_ms = Timer.now_ms()
            message.activity.CopyFrom(agent_message)

        if isinstance(agent_message, AgentStartup):
            message.agent_startup.CopyFrom(agent_message)

        if isinstance(agent_message, ServerActivity):
            message.server_activity.CopyFrom(agent_message)

        if isinstance(agent_message, ApplicationCreate):
            message.application_create.CopyFrom(agent_message)

        if isinstance(agent_message, ApplicationUpdate):
            message.application_update.CopyFrom(agent_message)

        if isinstance(agent_message, HttpRequest):
            message.prefilter.CopyFrom(agent_message)

        if isinstance(agent_message, ObservedRoute):
            message.observed_route.CopyFrom(agent_message)

        if isinstance(agent_message, Poll):
            message.poll.CopyFrom(agent_message)

        return message

    def update_messages(self, messages):
        """
        Possible messages supported currently

        contrast.api.dtm.ServerActivity server_activity = 10;
        contrast.api.dtm.AgentStartup agent_startup = 11;
        contrast.api.dtm.ApplicationCreate application_create = 12;
        contrast.api.dtm.ApplicationUpdate application_update = 13;
        contrast.api.dtm.Activity activity = 14;
        contrast.api.dtm.Poll
        """
        updated = []
        for item in messages:
            prepared_msg = self.update_message(item)
            updated.append(prepared_msg)

        return updated

    @property
    def client_id(self):
        """
        Client id is used by Speedracer to recognize when messages are sent by different
        worker processes of the same application.
        client_id must be the parent process id as it is the same for all workers serving an app.
        :return: str app name and parent process id
        """
        return str(self.app_name) + "-" + str(os.getppid())

    @property
    def pid(self):
        """
        pid is used by Speedracer to recognize a unique worker process for an application.

        pid must be unique for each worker process of an app.
        :return: int current process id
        """
        return os.getpid()

    @property
    def app_path(self):
        """
        Return the path for where the application is running, either configured
        in common config or by looking at the current working dir.
        """
        return self.config.get("application.path") or os.getcwd()

    def build_empty_message(self):
        message = Message()
        message.app_name = self.app_name
        message.app_path = self.app_path
        message.app_language = self.APPLICATION_LANGUAGE
        message.client_id = self.client_id
        message.client_number = self.number
        message.client_total = ServiceClient.client_count
        message.timestamp_ms = Timer.now_ms()
        message.pid = self.pid

        self.count += 1
        message.message_count = self.count

        return message

    def send_message(self, sock, msg):
        """
        Prefix each message with a 4-byte length (network byte order)
        """
        msg = struct.pack(self.RECV_FMT, len(msg)) + msg
        sock.sendall(msg)

    def receive_message(self, sock):
        """
        Read message length and unpack it into an integer

        :param sock - socket to receive information from
        :return bytes if successful else None
        """
        raw_message_length = self.receive_all(sock, 4)

        if not raw_message_length:
            logger.debug("Falsy raw message length of %s", raw_message_length)
            return

        message_length = struct.unpack(self.RECV_FMT, raw_message_length)[0]
        return self.receive_all(sock, message_length)

    def receive_all(self, sock, n):
        """
        Helper function to recv n bytes or return None if EOF is hit
        """
        buffer_array = bytearray()
        while len(buffer_array) < n:
            packet = sock.recv(n - len(buffer_array))
            if not packet:
                return None
            buffer_array.extend(packet)
        return bytes(buffer_array)
