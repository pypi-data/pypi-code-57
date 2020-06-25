"""
Connection
==========
"""

from .accounts.connection import AccountConnection
from .crawls.connection import CrawlConnection
from .downloads.connection import DownloadConnection
from .projects.connection import ProjectConnection
from .reports.connection import ReportConnection


class DeepCrawlConnection(AccountConnection, ProjectConnection, CrawlConnection, ReportConnection, DownloadConnection):
    """Class which contains all connection types

    >>> connection = DeepCrawlConnection("API_ID", "API_KEY", sleep=0.5)
    >>> connection.token
    <token>

    The sleep arguments represents the time between requests for paginated responses. Default value is 0.5
    """

    __instance = None

    def __init__(self, id_user, key_pass, sleep=0.5, auth_type_user=False):
        super(DeepCrawlConnection, self).__init__(id_user, key_pass, sleep=sleep, auth_type_user=auth_type_user)

        DeepCrawlConnection.__instance = self

    @staticmethod
    def get_instance():
        """
        Return the last created connection

        >>> DeepCrawlConnection.get_instance()
        <deepcrawl.DeepCrawlConnection at 0x10583a898>

        :return: The latest created connection
        :rtype: DeepCrawlConnection
        """
        return DeepCrawlConnection.__instance
