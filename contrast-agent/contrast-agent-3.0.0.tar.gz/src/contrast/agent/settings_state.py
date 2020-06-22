# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import platform
import socket
import sys

import contrast
from contrast.agent.framework import Framework
from contrast.agent.heartbeat import Heartbeat
from contrast.agent.protect.mixins.REP_settings import SettingsREPMixin
from contrast.agent.protect.rule.rules_builder import RulesBuilder
from contrast.agent.reaction_processor import ReactionProcessor
from contrast.agent.service_client import ServiceClient
from contrast.api.dtm_pb2 import (
    AgentStartup,
    ApplicationCreate,
    ApplicationUpdate,
    Poll,
)
from contrast.api.settings_pb2 import (
    AccumulatorSettings,
    AgentSettings,
    ApplicationSettings,
    ServerFeatures,
)
from contrast.configuration import AgentConfig
from contrast.utils.exceptions.contrast_service_exception import (
    ContrastServiceException,
)
from contrast.utils.library_reader import LibraryReader
from contrast.utils.loggers.logger import setup_agent_logger, reset_agent_logger
from contrast.utils.singleton import Singleton
from contrast.utils.string_utils import truncate

import logging

logger = logging.getLogger("contrast")


class SettingsState(Singleton, SettingsREPMixin):
    DEFAULT_HOST = "localhost"
    DEFAULT_PATH = "/"

    def init(self, init_libs=True, app_name=None, config=None):
        """
        Singletons should override init, not __init__.
        """
        self.config = None
        self.client = None
        self.config_features = {}
        self.last_update = None
        self.heartbeat = None
        self.framework = Framework()
        self.sys_module_count = 0

        # Features and Settings from Service
        self.server_features = ServerFeatures()
        self.application_settings = ApplicationSettings()
        self.accumulator_settings = AccumulatorSettings()

        # Server
        self.server_name = None
        self.server_path = None
        self.server_type = None

        self.exclusion_matchers = []

        # Rules
        self.assess_rules = dict()
        self.defend_rules = dict()

        # Initialize values from config file
        self.library_tags = ""
        self.application_tags = ""

        # Initialize config and loggers
        if config:
            self.config = config
            self._initialized = True
        else:
            self._initialized = self.initialize_config()

        if self._initialized:
            self._initialized = self.initialize_loggers()

        if self._initialized:
            # Initialize application metadata
            self.app_name = self.get_app_name(app_name)

            # Build based views
            self.session_id = self.config.get_session_id()
            self.session_metadata = self.config.get_session_metadata()

            self._initialized = self.initialize_service_client()

        self.log_environment()

        # Initialize libraries
        self.library_reader = None
        self.libraries = []
        self.unused_libraries = []
        self.top_level_modules = {}
        self.installed_distribution_keys = []

        if self._initialized:
            self._initialized = self.initialize_libraries(init_libs)

        # Used for heartbeat messages
        self.poll = Poll()

        logger.info("Contrast Agent finished loading settings.")

    def initialize_libraries(self, init_libs=False):
        """
        If enabled, read libraries from the application
        :param init_libs: boolean
        :return: True
        """

        if not self.is_analyze_libs_enabled():
            return True

        self.library_reader = LibraryReader(self.library_tags)

        if init_libs:
            self.library_reader.read_libraries()

        self.libraries = self.library_reader.libraries
        self.unused_libraries = self.library_reader.unused_libraries
        self.top_level_modules = self.library_reader.top_level_modules
        self.installed_distribution_keys = (
            self.library_reader.installed_distribution_keys
        )

        return True

    def initialize_config(self):
        self.config = AgentConfig()

        if self.config.get("application.tags"):
            self.application_tags = self.config.get("application.tags")

        if self.config.get("inventory.tags"):
            self.library_tags = self.config.get("inventory.tags")

        return True

    def initialize_loggers(self):
        setup_agent_logger(self.config)
        return True

    def send_heartbeat_message(self):
        """
        Agent sends a Poll message to Speedracer as a way to maintain a heartbeat.
        Note that a Poll message should never be the first message sent to Speedracer,
        a Poll message should only be sent AFTER an AgentStartup.
        """
        return self.send_messages([self.poll])

    def _is_defend_enabled_in_server_features(self):
        return (
            self.server_features
            and self.server_features.defend
            and self.server_features.defend.enabled
        )

    def is_agent_config_enabled(self):
        return self.config.get("enable", True)

    def is_agent_enabled(self):
        """
        Agent is considered enabled if all of the following are true:
        1. config value for 'enable' is True (or empty, defaults to True)
        2. SettingsState._initialized is True
            (meaning no errors during initialization process including initial connection to Speedracer)
        3. ServiceClient connection to Speedracer is True

        NOTE: If #3 is false (the connection to Speedracer is down at any time during the request cycle) then
        the agent is automatically disabled.
        """
        if not self.is_agent_config_enabled():
            return False

        if not self._initialized:
            return False

        if not self.client.is_connected():
            try:
                self.initialize_service_client()
            except ContrastServiceException:
                return False

        # initialize_service_client should have set the connection to connected
        return self.client.is_connected()

    def get_app_name(self, app_name):
        # Used in DARPA-Screener to set the app's name (so TS can tell the difference between 5 instances of the app)
        if os.environ.get("CONTRASTSECURITY_APP_NAME"):
            return os.environ.get("CONTRASTSECURITY_APP_NAME")

        if self.config.get("application.name"):
            return self.config.get("application.name")

        return app_name if app_name else "root"

    def log_environment(self):
        """
        Log current working directory, python version and pip version
        """
        banner = "{0}ENVIRONMENT{0}".format("-" * 50)
        logger.debug(banner)
        logger.debug("Current Working Dir: %s", os.getcwd())
        logger.debug("Python Version: %s", sys.version)
        logger.debug("Framework Version: %s", self.framework)
        logger.debug("Contrast Python Agent Version: %s", contrast.__version__)
        logger.debug(
            "Contrast Service Version %s", self.server_features.contrast_service
        )
        logger.debug("Platform %s", platform.platform())

        try:
            import pip

            logger.debug("Pip Version: %s", pip.__version__)
        except:
            pass

        logger.debug(banner)

    def initialize_service_client(self):
        """
        Initialize ServiceClient and its connection to Speedracer by asking it to send the agent and app
        initialization messages. This is successful if responses are received to process for new settings.

        If self.client is already a defined attribute, do not redefine it. Only initialize the connection
        to Speedracer.

        :return: bool if successfuly able to send initial messages and receive and process responses.
        """
        initial_messages = [
            self.build_server_start_message(),
            self.build_startup_message(),
        ]

        if self.client is None:
            self.client = ServiceClient(self.config, self.app_name)

        responses = self.client.initialize_and_send_messages(initial_messages)
        if responses:
            self.process_responses(responses)
            return True

        # if we did not receive any responses from Speedracer, then we don't have any server or startup
        # messages to process, so we should not continue on with Agent setup.
        raise ContrastServiceException

    def send_messages(self, messages):
        """
        Rely on ServiceClient having already initialized its connection to Speedracer
        and ask it to send a list of messages.
        Process the responses from sending the messages.
        :param messages: a list of protobuf messages to send
        :side effect: ContrastServiceException could be raised but should be catch by the middleware
        """
        responses = self.client.send_messages_retry(messages, raise_exception=False)
        self.process_responses(responses)

    def establish_heartbeat(self):
        """
        Initialize Heartbeat between Agent and SR if it has not been already initialized.
        """
        if self.heartbeat is None:
            self.heartbeat = Heartbeat(self)
            self.heartbeat.daemon = True
            self.heartbeat.start()

    def process_responses(self, responses):
        """
        :param responses: list of Message responses from SR
        """
        self.establish_heartbeat()

        logger.debug("Processing %s responses", len(responses))

        for response in responses:
            if self.process_service_response(response):
                self.set_assess_rules()
                self.set_protect_rules()

    def process_service_response(self, data):
        reload_rules = False

        if data and isinstance(data, AgentSettings):
            self.last_update = data.sent_ms

            reload_rules = self.process_server_features(data) or reload_rules
            reload_rules = self.process_application_settings(data) or reload_rules
            reload_rules = self.process_accumulator_settings(data) or reload_rules

        if reload_rules:
            logger.debug(
                "Finished processing Contrast Service message and reloading rules."
            )

        return reload_rules

    def generate_server_matchers(self):
        if self.server_features is None or not self.server_features.HasField("defend"):
            return False

    def process_server_features(self, data):
        if not data.HasField("server_features"):
            return False

        self.server_features = data.server_features
        self.generate_server_matchers()
        self.update_logger_from_features()

        self.log_server_features(data.server_features)

        return True

    def log_server_features(self, server_features):
        """
        Record server features received from teamserver (via the contrast service)
        Remove the rule_definitions field before logging because it's long and ugly
        """
        server_features_copy = ServerFeatures()
        server_features_copy.CopyFrom(server_features)
        del server_features_copy.defend.rule_definitions[:]
        logger.debug(
            "Received updated server features (excluding rule_definitions from log):\n%s",
            server_features_copy,
        )

    @property
    def code_exclusion_matchers(self):
        return [x for x in self.exclusion_matchers if x.is_code]

    def process_application_settings(self, data):
        if not data.HasField("application_settings"):
            return False

        self.application_settings = data.application_settings

        ReactionProcessor.process(data.application_settings, self)

        self.reset_transformed_settings()
        self.reset_session_id()

        logger.debug(
            "Received updated application settings:\n%s", data.application_settings
        )

        return True

    def reset_session_id(self):
        """
        While session_id may initially be set in __init__ by grabbing the common config value via
        self.config.get_session_id(), agent should always use the session_id returned from Speedracer.

        In the case common config set session_id (and not session_metadata), the returned session_id
        from Speedracer should be equal to the common config one.
        """
        self.session_id = self.application_settings.session_id

    def reset_transformed_settings(self):
        self.exclusion_matchers = []

    def process_accumulator_settings(self, data):
        if data.HasField("accumulator_settings"):
            self.accumulator_settings = data.accumulator_settings

    def build_server_start_message(self):
        agent_startup = AgentStartup()

        agent_startup.server_name = self.get_server_name()
        agent_startup.server_path = self.get_server_path()
        agent_startup.server_type = self.get_server_type()
        agent_startup.server_version = contrast.__version__

        if self.config.get("server.environment"):
            agent_startup.environment = self.config.get("server.environment")

        if self.config.get("server.tags"):
            agent_startup.tags = self.config.get("server.tags")

        agent_startup.version = contrast.__version__

        return agent_startup

    def build_startup_message(self):
        create = ApplicationCreate()
        create.group = self.config.get("application.group", "")
        create.app_version = self.config.get("application.version", "")
        create.code = self.config.get("application.code", "")
        create.tags = self.application_tags

        create.metadata = self.config.get("application.metadata", "")

        # build based views
        create.session_id = self.session_id
        create.session_metadata = self.session_metadata

        return create

    def build_update_message(self, routes):
        """
        Create an ApplicationUpdate message with framework information, libraries, and routes.

        :param routes: Dict of RouteCoverage, will be empty if in Protect mode
        :return: ApplicationUpdate instance
        """
        if not self.is_inventory_enabled():
            return

        update_message = ApplicationUpdate()

        update_message.platform.major = self.framework.version.major
        update_message.platform.minor = self.framework.version.minor
        update_message.platform.build = self.framework.version.patch

        for library in self.libraries:
            if library.used_class_count > library.class_count:
                logger.debug(
                    "WARNING! Used count  > total count for library %s",
                    library.file_path,
                )

            if library.hash_code is not None:
                update_message.libraries[library.hash_code].CopyFrom(library)

        # Route coverage is an assess feature. Routes will be empty
        # so the update_message will have no routes.
        for route in routes.values():
            update_message.routes.extend([route])

        return update_message

    def update_logger_from_features(self):
        # Python does not support TRACE level so we use DEBUG for now
        log_level = (
            "DEBUG"
            if self.server_features.log_level == "TRACE"
            else self.server_features.log_level
        )
        reset_agent_logger(self.server_features.log_file, log_level)

    def is_inventory_enabled(self):
        """
        inventory.enable = false: Disables both route coverage and library analysis and reporting
        """
        return self.config.get("inventory.enable", True)

    def is_analyze_libs_enabled(self):
        """
        inventory.analyze_libraries = false: Disables only library analysis/reporting
        """
        return (
            self.config.get("inventory.analyze_libraries", True)
            and self.is_inventory_enabled()
        )

    def is_assess_enabled(self):
        """
        We do not allow assess and defend to be on at the same time. As defend
        is arguably the more important of the two, it will take precedence

        The agent config may enable assess even if it is turned off in TS. This
        allows unlicensed apps to send findings to TS, where they will appear
        as obfuscated results.
        """
        if self.config is None or self.is_protect_enabled():
            return False

        assess_enabled = self.config.get("assess.enable", None)
        if assess_enabled is not None:
            return assess_enabled

        return (
            self.server_features
            and self.server_features.assess
            and self.server_features.assess.enabled
        )

    def is_protect_enabled(self):
        """
         Protect is enabled only if both configuration and server features enable it.
        """
        if self.config is None:
            return False
        config_protect_enabled = self.config.get("protect.enable", True)
        return config_protect_enabled and self._is_defend_enabled_in_server_features()

    def set_assess_rules(self):
        self.assess_rules = RulesBuilder.build_assess_rules(self)

    def set_protect_rules(self):
        """
        Stores all of our defend rules

        """
        if not self._is_defend_enabled_in_server_features():
            self.defend_rules = dict()
            return
        self.defend_rules = RulesBuilder.build_protect_rules(self)
        logger.debug("Built %s protect rules from settings", len(self.defend_rules))

    def get_server_name(self):
        """
        Hostname of the server

        Default is localhost
        """
        if self.server_name is None:
            detected_server = truncate(socket.gethostname(), self.DEFAULT_HOST)
            self.server_name = self.config.get("server.name", detected_server)

        return self.server_name

    def get_server_path(self):
        """
        Working Directory of the server

        Default is root
        """
        if self.server_path is None:
            detected_path = truncate(os.getcwd(), self.DEFAULT_PATH)
            self.server_path = self.config.get("server.path", detected_path)

        return self.server_path

    def get_server_type(self):
        """
        Web Framework of the Application either defined in common config or via discovery.
        """
        if self.server_type is None:
            self.server_type = (
                self.config.get("server.type") or self.framework.name_lower
            )

        return self.server_type
