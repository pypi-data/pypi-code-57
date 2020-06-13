#!/usr/bin/env python
from server_managers.server_managers import ServerManager
from unittest import TestCase
import pytest
import os
import logging
from utils.constants import REMOTE_IP, KEY_PATH

LOG = logging.getLogger(__name__)

class TestConnection(TestCase):

    @pytest.mark.skipif(os.getenv("BITBUCKET_BRANCH", "") == 'master' or os.getenv("BITBUCKET_BRANCH", "") == 'develop',reason="Test functionality locally.")
    def test_connection(self):
        self.username: str = "root"
        self.host: str = REMOTE_IP

        print(KEY_PATH)
        connect = ServerManager(user=self.username, host=self.host, port=8000, connect_kwargs={"key_filename": KEY_PATH})
        connect.login()
        execute_cmd = connect.run_cmd("ls -l")
        connect.close()

        self.assertGreater(len(execute_cmd), 0)


