"""
tlnetcard_python.system.administration.time_server.time_server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``TimeServer`` object to provide the functionality of TLNET Supervisor ->
System -> Administration -> Time Server.
"""

# Standard library.
from warnings import warn
# Required internal classes/functions.
from tlnetcard_python.login import Login

class TimeServer:
    """
    A TLNET Supervisor ``TimeServer`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> System -> Administration -> Time Server.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import TimeServer
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.TimeServer object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_time_server = TimeServer(card)
    >>> # Now that the TimeServer object has been created, functions belonging to the TimeServer
    >>> # class can be used. For example, setting the primary SNTP time server:
    >>> card_time_server.set_primary_server('129.6.15.28')
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``TimeServer`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_time.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_time"
    def disable_daylight_savings(self) -> None:
        """
        Disables daylight savings for SNTP. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_DLS_EN": "0"
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def disable_sntp(self) -> None:
        """
        Disables SNTP. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "1"
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_daylight_savings(self, start_date: str = "04/01", end_date: str = "11/01") -> None:
        """
        Enables daylight savings from the start date to the end date for SNTP. Returns ``None``.

        :param start_date: (optional) The date to begin daylight savings.
        :param end_date: (optional) The date to end daylight savings.
        :rtype: ``None``
        """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_DLS_EN": "1",
            "NTP_DLS_SDATE": start_date,
            "NTP_DLS_EDATE": end_date
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_sntp(self) -> None:
        """
        Enables SNTP. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0"
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def get_primary_server(self) -> str:
        """
        Returns the primary time server for SNTP as a string.

        :rtype: ``str``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing config for primary SNTP server.
        if "Server1" in system_config:
            return system_config["Server1"]
        return ""
    def get_secondary_server(self) -> str:
        """
        Returns the secondary time server for SNTP as a string.

        :rtype: ``str``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing config for secondary SNTP server.
        if "Server2" in system_config:
            return system_config["Server2"]
        return ""
    def set_manual_time(self, date: str = "01/01/2000", time: str = "00:00:00") -> None:
        """
        Sets the time manually. Returns ``None``.

        :param date: (optional) The current date in ``MM/DD/YYYY`` format.
        :param time: (optional) The current time in ``hh:mm:ss`` format.
        :rtype: ``None``
        """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "1",
            "NTP_USE_PCTIME": "0",
            "NTP_SYSDATE": date,
            "NTP_SYSTIME": time
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_primary_server(self, server: str) -> None:
        """
        Sets the primary time server for SNTP. Returns ``None``.

        :param server: The primary SNTP server to be used.
        :rtype: ``None``
        """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_IP1": server
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_secondary_server(self, server: str) -> None:
        """
        Sets the secondary time server for SNTP. Returns ``None``

        :param server: The secondary SNTP server to be used.
        :rtype: ``None``
        """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_IP2": server
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_time_zone(self, offset: str = "GMT") -> bool:
        """
        Sets the time zone for SNTP. Returns ``False`` if an invalid offset values is provided.
        Otherwise, ``True`` is returned upon successful completion.

        :param offset: The timezone value to be used.
        :rtype: ``bool``
        """
        # Converting string to list value.
        offsets = ["GMT-12", "GMT-11", "GMT-10", "GMT-09", "GMT-08", "GMT-07",
                   "GMT-06", "GMT-05", "GMT-04", "GMT-03:30", "GMT-03", "GMT-02",
                   "GMT-01", "GMT", "GMT+01", "GMT+02", "GMT+03", "GMT+03:30",
                   "GMT+04", "GMT+05", "GMT+05:30", "GMT+06", "GMT+07", "GMT+08",
                   "GMT+09", "GMT+10", "GMT+11", "GMT+12"]

        # Checking if zone value is valid (otherwise an improper offset value was provided).
        if offset not in offsets:
            warn("Invalid time zone specified!", ValueError)
            return False

        # Generating payload.
        time_server_data = {
            "NTP_MANU": "0",
            "NTP_ZONE": str(offset)
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
        return True
    def use_local_time(self) -> None:
        """
        Sets the manual time to the time of the computer sending this command. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        time_server_data = {
            "NTP_MANU": "1",
            "NTP_USE_PCTIME": "1"
        }

        # Uploading time server configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=time_server_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
