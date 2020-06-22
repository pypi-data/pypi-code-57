"""
tlnetcard_python.system.administration.web.web
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Web`` object to provide the functionality of TLNET Supervisor -> System
-> Administration -> Web.
"""

# Standard library.
from os.path import isfile
from warnings import warn
# Required internal classes/functions.
from tlnetcard_python.login import Login

class Web:
    """
    A TLNET Supervisor ``Web`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> System -> Administration -> Web.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import Web
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.Web object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_web = Web(card)
    >>> # Now that the Web object has been created, functions belonging to the Web class can
    >>> # be used. For example, disabling HTTP access to the card:
    >>> card_web.disable_http()
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Web`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_web.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_web"
    def disable_http(self) -> None:
        """
        Disables HTTP access. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        web_data = {
            "WEB_HTTP": "0"
        }

        # Uploading web configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def disable_https(self) -> None:
        """
        Disables HTTPS access. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        web_data = {
            "WEB_HTTPS": "0"
        }

        # Uploading web configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_http(self) -> None:
        """
        Enables HTTP access. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        web_data = {
            "WEB_HTTP": "1"
        }

        # Uploading web configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_https(self) -> None:
        """
        Enables HTTPS access. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        web_data = {
            "WEB_HTTPS": "1"
        }

        # Uploading web configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def get_http_port(self) -> int:
        """
        Returns the port in use for HTTP as an integer.

        :rtype: ``int``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing config for HTTP port.
        if "HTTP Port" in system_config:
            return int(system_config["HTTP Port"])
        return -1
    def get_https_port(self) -> int:
        """
        Returns the port in use for HTTPS as an integer.

        :rtype: ``int``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing config for HTTPS port.
        if "HTTPS Port" in system_config:
            return int(system_config["HTTPS Port"])
        return -1
    def get_web_refresh(self) -> int:
        """
        Returns the web refresh time in seconds as an integer.

        :rtype: ``int``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing config for web refresh time.
        if "Web Refresh" in system_config:
            return int(system_config["Web Refresh"])
        return -1
    def set_http_port(self, port: int = 80) -> None:
        """
        Sets the port for use by HTTP. Returns ``None``.

        :param port: (optional) The port to be used.
        :rtype: ``None``
        """
        # Generating payload.
        web_data = {
            "WEB_HTTP": "1",
            "WEB_PORT_HTTP": str(port)
        }

        # Uploading web configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_https_port(self, port: int = 443) -> None:
        """
        Sets the port for use by HTTPS. Returns ``None``.

        :param port: (optional) The port to be used.
        :rtype: ``None``
        """
        # Generating payload.
        web_data = {
            "WEB_HTTPS": "1",
            "WEB_PORT_HTTPS": str(port)
        }

        # Uploading web configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_web_refresh(self, seconds: int = 10) -> None:
        """
        Sets the web refresh time to the provided number of seconds. Returns ``None``.

        :param seconds: The number of seconds the web refresh is to be.
        :rtype: ``None``
        """
        # Generating payload.
        web_data = {
            "WEB_REFRESH": str(seconds)
        }

        # Uploading web configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=web_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def upload_ssl_cert(self, path: str) -> bool:
        """
        Uploads the provided SSL certificate. Returns ``False`` if the provided key does not exist.
        Otherwise, ``True`` is returned upon successful completion.

        :param path: The path of the SSL certificate to upload.
        :rtype: ``bool``
        """
        # Testing if the file specified in path exists.
        if not isfile(path):
            warn("Specified PEM file does not exist!", FileNotFoundError)
            return False

        # Creating upload payload.
        upload_data = {
            'OK': 'Submit'
        }
        upload_file = {
            'WEB_SSLCERT': (path.split("/")[-1], open(path, 'rb'), 'multipart/form-data'),
        }

        # Uploading SSL certificate.
        self._login_object.get_session().post(self._post_url, data=upload_data, files=upload_file,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        return True
