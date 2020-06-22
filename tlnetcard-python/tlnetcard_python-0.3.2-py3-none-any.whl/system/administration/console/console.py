"""
tlnetcard_python.system.administration.console.console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Console`` object to provide the functionality of TLNET Supervisor -> System
-> Administration -> Console.
"""

# Standard library.
from os.path import isfile
from warnings import warn
# Required internal classes/functions.
from tlnetcard_python.login import Login

class Console:
    """
    A TLNET Supervisor ``Console`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> System -> Administration -> Console.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import Console
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.Console object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_console = Console(card)
    >>> # Now that the Console object has been created, functions belonging to the Console class can
    >>> # be used. For example, enabling SSH access to the card:
    >>> card_console.enable_ssh()
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Console`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_console.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_console"
    def disable_ssh(self) -> None:
        """
        Disables SSH. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        console_data = {
            "CON_SSH": "0"
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def disable_telnet(self) -> None:
        """
        Disables Telnet. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        console_data = {
            "CON_TELNET": "0"
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_ssh(self) -> None:
        """
        Enables SSH. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        console_data = {
            "CON_SSH": "1"
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_telnet(self) -> None:
        """
        Enables Telnet. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        console_data = {
            "CON_TELNET": "1"
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def get_ssh_port(self) -> int:
        """
        Returns the port in use for SSH as an integer.

        :rtype: ``int``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing config for SSH port.
        if "SSH Port" in system_config:
            return int(system_config["SSH Port"])
        return -1
    def get_telnet_port(self) -> int:
        """
        Returns the port in use for Telnet as an integer.

        :rtype: ``int``
        """
        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing config for telnet port.
        if "Telnet Port" in system_config:
            return int(system_config["Telnet Port"])
        return -1
    def set_ssh_port(self, port=22) -> None:
        """
        Sets the port for use by SSH. Returns ``None``.

        :param port: (optional) The port to use for SSH.
        :rtype: ``None``
        """
        # Generating payload.
        console_data = {
            "CON_SSH": "1",
            "CON_PORT_SSH": str(port)
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_telnet_port(self, port=23) -> None:
        """
        Sets the port for use by Telnet. Returns ``None``.

        :param port: (optional) The port to use for Telnet.
        :rtype: ``None``
        """
        # Generating payload.
        console_data = {
            "CON_TELNET": "1",
            "CON_PORT_TELNET": str(port)
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=console_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def upload_auth_public_key(self, key: str) -> bool:
        """
        Uploads the provided authentication public key. Returns ``True`` upon successful completion,
        and ``False`` if the file does not exist.

        :param key: The keyfile to be uploaded.
        :rtype: ``bool``
        """
        # Testing if the file specified in path exists.
        if not isfile(key):
            warn("Specified key file does not exist!", FileNotFoundError)
            return False

        # Creating upload payload.
        upload_data = {
            'OK': 'Submit'
        }
        upload_file = {
            'CON_PUB': (key.split("/")[-1], open(key, 'rb'), 'multipart/form-data'),
        }

        # Uploading public authentication key.
        self._login_object.get_session().post(self._post_url, data=upload_data, files=upload_file,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        return True
    def upload_dsa_host_key(self, key: str) -> bool:
        """
        Uploads the provided DSA key. Returns ``True`` upon successful completion, and ``False`` if
        the file does not exist.

        :param key: The keyfile to be uploaded.
        :rtype: ``bool``
        """
        # Testing if the file specified in path exists.
        if not isfile(key):
            warn("Specified key file does not exist!", FileNotFoundError)
            return False

        # Creating upload payload.
        upload_data = {
            'OK': 'Submit'
        }
        upload_file = {
            'CON_DSA': (key.split("/")[-1], open(key, 'rb'), 'multipart/form-data'),
        }

        # Uploading DSA key.
        self._login_object.get_session().post(self._post_url, data=upload_data, files=upload_file,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        return True
    def upload_rsa_host_key(self, key: str) -> bool:
        """
        Uploads the provided RSA key. Returns ``True`` upon successful completion, and ``False`` if
        the file does not exist.

        :param key: The keyfile to be uploaded.
        :rtype: ``bool``
        """
        # Testing if the file specified in path exists.
        if not isfile(key):
            warn("Specified key file does not exist!", FileNotFoundError)
            return False

        # Creating upload payload.
        upload_data = {
            'OK': 'Submit'
        }
        upload_file = {
            'CON_RSA': (key.split("/")[-1], open(key, 'rb'), 'multipart/form-data'),
        }

        # Uploading DSA key.
        self._login_object.get_session().post(self._post_url, data=upload_data, files=upload_file,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        return True
