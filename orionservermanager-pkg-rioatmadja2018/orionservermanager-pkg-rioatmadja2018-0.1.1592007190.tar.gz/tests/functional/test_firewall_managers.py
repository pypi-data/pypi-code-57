#!/usr/bin/env python
from utils.firewall_managers import FirewallManagers
from unittest import TestCase
import pytest
import os
import logging
from utils.constants import REMOTE_IP

LOG = logging.getLogger(__name__)

class TestFirewallManager(TestCase):

    @pytest.mark.skipif(os.getenv("BITBUCKET_BRANCH", "") == 'master' or os.getenv("BITBUCKET_BRANCH", "") == 'develop',reason="Test functionality locally.")
    def test_create_ipset(self):
        self.username: str = "root"
        self.host: str = REMOTE_IP

        firewall_manager = FirewallManagers(ip="172.123.22.28", ipset='amazon_gov', zone="internal", user=self.username, host=self.host, connect_kwargs={"key_filename": "/Users/rioatmadja/.ssh/cloud_user"})
        firewall_manager.login()
        self.assertListEqual(firewall_manager.create_ipset(), ['success'] * 4)
        firewall_manager.close()

    @pytest.mark.skipif(os.getenv("BITBUCKET_BRANCH", "") == 'master' or os.getenv("BITBUCKET_BRANCH", "") == 'develop',reason="Test functionality locally.")
    def test_get_ipset(self):
        self.username: str = "root"
        self.host: str = REMOTE_IP

        firewall_manager = FirewallManagers(ip="172.123.22.28", ipset='internal', zone="internal", user=self.username, host=self.host, connect_kwargs={"key_filename": "/Users/rioatmadja/.ssh/cloud_user"})
        firewall_manager.login()
        self.assertListEqual(firewall_manager.get_ipset(), ['172.31.112.0/32'])
        firewall_manager.close()

    @pytest.mark.skipif(os.getenv("BITBUCKET_BRANCH", "") == 'master' or os.getenv("BITBUCKET_BRANCH", "") == 'develop', reason="Test functionality locally.")
    def test_delete_ipset(self):

        self.username: str = "root"
        self.host: str = REMOTE_IP

        firewall_manager = FirewallManagers(ip="172.123.22.22", ipset='amazon_gov', zone="internal", user=self.username,
                                            host=self.host,
                                            connect_kwargs={"key_filename": "/Users/rioatmadja/.ssh/cloud_user"})
        firewall_manager.login()

        self.assertListEqual(firewall_manager.delete_ipset(), ['success'] * 2)
        firewall_manager.close()


