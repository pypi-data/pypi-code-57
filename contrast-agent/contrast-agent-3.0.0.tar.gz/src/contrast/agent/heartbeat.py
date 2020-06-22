# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
import time

from contrast.utils.decorators import fail_safely
from contrast.utils.timer import Timer

import logging

logger = logging.getLogger("contrast")


class Heartbeat(threading.Thread):
    def __init__(self, settings):
        super(Heartbeat, self).__init__()
        self.settings = settings
        self.stopped = False

        logger.debug("Establishing heartbeat")

        self.heartbeat_interval_ms = self.settings.config.get(
            "agent.polling.app_activity_ms", 30000
        )
        self.heartbeat_interval_sec = self.heartbeat_interval_ms / 1000

        # Agent should not ping too frequently
        if self.heartbeat_interval_ms < 10000:
            self.heartbeat_interval_ms = 10000
            self.heartbeat_interval_sec = 10

    def run(self):
        while not self.stopped:
            self.send_heartbeat()
            time.sleep(self.heartbeat_interval_sec)

    @fail_safely("Error sending a heartbeat message")
    def send_heartbeat(self):
        heartbeat_interval_ms = self.heartbeat_interval_ms

        # only send after we have not updated after the last interval time set in the config
        if (
            self.settings.last_update is not None
            and (Timer.now_ms() - self.settings.last_update) > heartbeat_interval_ms
        ):
            self.settings.send_heartbeat_message()
