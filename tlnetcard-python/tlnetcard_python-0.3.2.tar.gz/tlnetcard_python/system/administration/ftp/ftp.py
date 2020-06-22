"""
tlnetcard_python.system.adminsitration.ftp.ftp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Ftp`` object to provide the functionality of TLNET Supervisor -> System ->
Administration -> FTP.
"""

# Required internal classes/functions.
from tlnetcard_python.login import Login

class Ftp:
    """
    A TLNET Supervisor ``Ftp`` object. Provides the functionality of the equivalent webpage TLNET
    Supervisor -> System -> Administration -> Batch Configuration.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import Ftp
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.Ftp object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_ftp = Ftp(card)
    >>> # Now that the Ftp object has been created, functions belonging to the Ftp class can be
    >>> # used. For example, setting a new FTP port:
    >>> card_ftp.set_ftp_port(12345)
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Ftp`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_ftp.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_ftp"
    def disable_ftp(self) -> None:
        """
        Disables FTP. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ftp_data = {
            "FTP_FTP": "0",
        }

        # Uploading FTP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ftp_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_ftp(self) -> None:
        """
        Enables FTP. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        ftp_data = {
            "FTP_FTP": "1",
        }

        # Uploading FTP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ftp_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def get_ftp_port(self) -> int:
        """
        Returns the port in use for FTP as an integer.

        :rtype: ``int``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing config for FTP port.
        if "FTP Port" in system_config:
            return int(system_config["FTP Port"])
        return -1
    def set_ftp_port(self, port: int = 21) -> None:
        """
        Sets the port for use by FTP. Returns ``None``.

        :param port: (optional) The port to use for FTP.
        :rtype: ``None``
        """
        # Generating payload.
        ftp_data = {
            "FTP_FTP": "1",
            "FTP_PORT_FTP": str(port),
        }

        # Uploading FTP configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=ftp_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
