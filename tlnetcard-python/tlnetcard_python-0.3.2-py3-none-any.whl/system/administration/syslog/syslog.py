"""
tlnetcard_python.system.administration.syslog.syslog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Syslog`` object to provide the functionality of TLNET Supervisor -> System
-> Administration -> Syslog.
"""

# Standard library.
from typing import List
# Required internal classes/functions.
from tlnetcard_python.login import Login

class Syslog:
    """
    A TLNET Supervisor ``Syslog`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> System -> Administration -> Syslog.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import Syslog
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.Syslog object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_syslog = Syslog(card)
    >>> # Now that the Syslog object has been created, functions belonging to the Syslog class can
    >>> # be used. For example, adding a new syslog server:
    >>> card_syslog.add_server("10.0.0.200")
    True
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Syslog`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_syslog.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_syslog"
    def add_server(self, server: str) -> bool:
        """
        Adds a syslog server. If there are already more than 4 syslog servers in use, the provided
        server will not be added and ``False`` will be returned. Otherwise, ``True`` will be
        returned upon success.

        :param server: The address of the server to add.
        :rtype: ``bool``
        """
        # Quitting if four servers are already listed.
        curr_servers = self.get_servers()
        if len(curr_servers) >= 4:
            return False

        # Returning success if server is already in use.
        if server in curr_servers:
            return True

        # Adding current servers to payload.
        syslog_data = {}
        i = 0   # Setting i to 0 here prevents error if curr_servers is empty.
        # pylint: disable=consider-using-enumerate
        for i in range(0, len(curr_servers)):
            syslog_data["SLG_SERVER" + str(i + 1)] = curr_servers[i]

        # Adding new server to payload.
        syslog_data["SLG_SERVER" + str(i + 2)] = server

        # Adding empty server lines to payload.
        for j in range(i + 2, 4):
            syslog_data["SLG_SERVER" + str(j + 1)] = ""

        # Uploading syslog configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
        return True
    def clear_servers(self) -> None:
        """
        Clears all syslog servers. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        syslog_data = {}
        for i in range(0, 4):
            syslog_data["SLG_SERVER" + str(i + 1)] = ""

        # Uploading syslog configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def disable_syslog(self) -> None:
        """
        Disables syslog. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        syslog_data = {
            'SLG_SLG': 0
        }

        # Uploading syslog configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_syslog(self) -> None:
        """
        Enables syslog. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        syslog_data = {
            'SLG_SLG': 1
        }

        # Uploading syslog configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def get_servers(self) -> List[str]:
        """
        Returns syslog servers in a list.

        :rtype: ``List[str]``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()
        items = ["SysLog Server", "SysLog Server2", "SysLog Server3", "SysLog Server4"]

        servers = []
        for i in items:
            if i in system_config:
                servers.append(system_config[i])
        return servers
    def remove_server(self, server: str) -> bool:
        """
        Removes a syslog server. If the provided server is not listed, ``False`` is returned.
        Otherwise, ``True`` will be returned upon success.

        :param server: The server to be removed.
        :rtype: ``bool``
        """
        # Quitting if server isn't listed.
        curr_servers = self.get_servers()
        if server not in curr_servers:
            return False

        # Removing server from list.
        curr_servers.remove(server)

        # Adding remaining servers to payload.
        syslog_data = {}
        # pylint: disable=consider-using-enumerate
        for i in range(0, len(curr_servers)):
            syslog_data["SLG_SERVER" + str(i + 1)] = curr_servers[i]

        # Adding empty server lines to payload.
        for j in range(i + 1, 4):
            syslog_data["SLG_SERVER" + str(j + 1)] = ""

        # Uploading syslog configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=syslog_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
        return True
