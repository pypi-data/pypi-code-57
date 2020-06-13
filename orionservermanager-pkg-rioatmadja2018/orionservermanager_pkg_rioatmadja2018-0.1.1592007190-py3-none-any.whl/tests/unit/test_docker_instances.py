#!/usr/bin/env python
from server_managers.docker_managers import DockerManagers
from unittest import TestCase
import pytest
import os
import logging
from utils.constants import REMOTE_IP

LOG = logging.getLogger(__name__)

class TestDocker(TestCase):

    @pytest.mark.skipif(os.getenv("BITBUCKET_BRANCH", "") == 'master' or os.getenv("BITBUCKET_BRANCH", "") == 'develop',reason="Local unit test")
    def test_check_docker_installation(self):
        self.username: str = "cloud_user"
        self.host: str = REMOTE_IP

        self.conn = DockerManagers(user=self.username, host=self.host, connect_kwargs={"key_filename": "/Users/rioatmadja/.ssh/cloud_user"})
        self.conn.login()
        self.assertEqual(self.conn.check_docker_installation(), True)
        self.conn.close()
