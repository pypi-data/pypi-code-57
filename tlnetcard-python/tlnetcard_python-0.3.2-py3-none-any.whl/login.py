"""
tlnetcard_python.login
~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Login`` object to manage and persist settings across multiple interactions
with the TLNET Supervisor (requests' Session, hostname, port, SNMP and system configurations, etc.).
"""

# Standard library.
from getpass import getpass
from hashlib import md5
from typing import Dict
from warnings import filterwarnings, warn
# Related third-party library.
from requests import Session
from urllib3.exceptions import InsecureRequestWarning

class Login:
    """
    A TLNET Supervisor ``Login`` object.

    A ``Login`` object is required by all classes in this repository. Provides login persistence and
    saves pertinent session information.

    Basic Usage:

    >>> import tlnetcard_python
    >>> card = tlnetcard_python.Login(user="admin", passwd="password", host="10.0.0.100")
    >>> # Now this Login object "card" can be provided as the sole argument to any other class
    >>> # initializer in this API. For example, the BatchConfiguration class:
    >>> batch_config = tlnetcard_python.system.administration.BatchConfiguration(card)
    >>> # Now any method from the initialized class can be used. For example, saving the system
    >>> # configuration to a file in the current directory:
    >>> batch_config.download_system_configuration(path="system_config.ini")
    'system-config.ini'
    """
    # pylint: disable=too-many-arguments,too-many-instance-attributes
    def __init__(self, user: str = "admin", passwd: str = "password", host: str = "",
                 save_passwd: bool = False, ssl: bool = True,
                 reject_invalid_certs: bool = True, timeout: float = 10.0, port: int = None
                 ) -> None:
        """
        Initializes the ``Login`` object. If the ``passwd`` argument is not ``None``, then this
        function will call ``self._perform_login()`` to execute the login. Returns ``None``.

        :param user: (optional) The TLNET Supervisor username.
        :param passwd: (optional) The TLNET Supervisor password.
        :param host: (optional) The address of the TLNETCARD.
        :param save_passwd: (optional) Determines whether or not the ``passwd`` value will be saved
        in the object. When set to ``False``, the ``passwd`` value will not be saved.
        :param ssl: (optional) Determines whether or not the TLNET Supervisor at the host address
        has an SSL certificate i.e. does it use HTTPS. When set to ``True``, HTTPS will be used.
        :param reject_invalid_certs: (optional) Determines whether or not an invalid (i.e. a
        self-signed) SSL certificate will be rejected. When set to ``True``, invalid certificates
        will be rejected.
        :param timeout: (optional) The timeout value which will be used for all web and SNMP
        requests.
        :param port: (optional) The port which the TLNET Supervisor is using.
        :rtype: ``None``
        """
        # Saving values which will be used independently.
        self._host = host
        self._user = user
        self._reject_invalid_certs = reject_invalid_certs
        self._save_passwd = save_passwd
        self._ssl = ssl
        self._timeout = timeout
        # Setting port.
        if self._ssl and port is None:
            self._port = 443
        elif not self._ssl and port is None:
            self._port = 80
        else:
            self._port = port
        # Checking to see if password should be saved.
        if self._save_passwd:
            self._passwd = passwd
        else:
            self._passwd = ""
        # Executing login if a host was specified.
        if self._host != "":
            self._perform_login(passwd)
        # Initializing system/snmp config list variables.
        self._snmp_config = {}
        self._system_config = {}
        self._renew_snmp = True
        self._renew_system = True
    def get_base_url(self) -> str:
        """
        Returns the base URL for TLNET Supervisor as a string.

        :rtype: ``str``
        """
        # Generating base URL.
        if self._ssl:
            base_url = 'https://' + self._host + ":" + str(self._port)
        else:
            base_url = 'http://' + self._host + ":" + str(self._port)
        return base_url
    def get_host(self) -> str:
        """
        Returns the host as a string.

        :rtype: ``str``
        """
        return self._host
    def get_port(self) -> int:
        """
        Returns the port number as an integer.

        :rtype: ``int``
        """
        return self._port
    def get_reject_invalid_certs(self) -> bool:
        """
        Returns whether to reject invalid SSL certificates (i.e. self-signed SSL certificates) as a
        boolean.

        :rtype: ``bool``
        """
        return self._reject_invalid_certs
    def get_session(self) -> Session:
        """
        Returns the requests ``Session`` object that was created by the ``self._perform_login()``
        function. If the ``self._perform_login()`` function has not run yet (i.e. no host was
        specified), this function will return ``None``.

        :rtype: ``requests.Session``
        """
        return self._session
    def get_snmp_config(self, force: bool = False) -> Dict[str, str]:
        """
        Checks if a refresh of the SNMP configuration has been requested (or forced). If so,
        initializes a ``tlnetcard_python.system.administration.BatchConfiguration`` object to pull
        the current SNMP configuration and stores it locally as a dictionary. This information is
        then returned. If a refresh was neither forced nor requested, it will return the
        saved dictionary without pulling a new one.

        :param force: Whether a new config file should be pulled from the TLNET Supervisor,
        regardless as to whether one has been requested by another function in this API. Setting
        this parameter to ``True`` guarantees the returned dictionary was just pulled, but
        frequent use will increase program runtimes while providing little or no benefit.
        :rtype: ``Dict[str, str]``
        """
        # Checking if a snmp config is required or forced and returning if neither.
        if not self._renew_snmp and not force:
            return self._snmp_config
        # Otherwise initializing BatchConfiguration object pulling new SNMP config.
        batch_object = BatchConfiguration(self)
        snmp_config = batch_object.download_snmp_configuration(no_write=True).split('\n')
        # Clearing existing SNMP config and writing new config.
        self._snmp_config.clear()
        for i in snmp_config:
            if "=" in i:
                info = i.split("+")
                self._snmp_config[info[0]] = info[1]
        # Resetting _renew_snmp variable to False.
        self._renew_snmp = False
        return self._snmp_config
    def get_system_config(self, force: bool = False) -> Dict[str, str]:
        """
        Checks if a refresh of the system configuration has been requested (or forced). If so,
        initializes a ``tlnetcard_python.system.administration.BatchConfiguration`` object to pull
        the current system configuration and stores it locally as a dictionary. This information is
        then returned. If a refresh was neither forced nor requested, it will return the
        saved dictionary without pulling a new one.

        :param force: Whether a new config file should be pulled from the TLNET Supervisor,
        regardless as to whether one has been requested by another function in this API. Setting
        this parameter to ``True`` guarantees the returned dictionary was just pulled, but
        frequent use will increase program runtimes while providing little or no benefit.
        :rtype: ``Dict[str, str]``
        """
        # Checking if a system config is required or forced and returning if neither.
        if not self._renew_system and not force:
            return self._system_config
        # Otherwise initializing BatchConfiguration object pulling new system config.
        batch_object = BatchConfiguration(self)
        system_config = batch_object.download_system_configuration(no_write=True).split('\n')
        # Clearing existing system config and writing new config.
        self._system_config.clear()
        for i in system_config:
            if "=" in i:
                info = i.split("+")
                self._system_config[info[0]] = info[1]
        # Resetting _renew_system variable to False.
        self._renew_system = False
        return self._system_config
    def get_timeout(self) -> float:
        """
        Returns the timeout value.

        :rtype: ``float``
        """
        return self._timeout
    def logout(self) -> None:
        """ Closes the session. """
        # Restoring warnings in case reject_invalid_certs flag is used.
        filterwarnings("default", category=InsecureRequestWarning)
        self._session.close()
    def _perform_login(self, passwd: str) -> bool:
        """
        Logs in to the TLNET Supervisor using the provided password, ``passwd``. Generates a POST
        request to the TLNET Supervisor login page at ``self._host`` and executes this request
        within a new requests ``Session``. If the login fails, the ``Session`` object is closed, a
        ``RuntimeWarning`` is thrown, and ``False`` is returned. If the login succeeds, the
        ``Session`` object is saved into ``self._session`` and ``True`` is returned.

        This function was not meant to be called directly by the user of this API, but is instead
        intended to be called indirectly via either the function initializer or by the
        ``self.set_host()`` function.

        :param passwd: The password to be used with the TLNET Supervisor.
        :rtype: ``bool``
        """
        # Ignoring self-signed SSL certificate warning when reject_invalid_certs is False.
        if not self._reject_invalid_certs:
            filterwarnings("ignore", category=InsecureRequestWarning)

        # Setting login URLs for future use.
        login_get_url = self.get_base_url() + '/home.asp'
        login_post_url = self.get_base_url() + '/delta/login'

        # Initializing session (to provide login persistence).
        session = Session()

        # Getting login screen HTML (so that Challenge can be retrieved).
        login_screen = session.get(login_get_url, timeout=self._timeout,
                                   verify=self._reject_invalid_certs)
        login_screen.raise_for_status()

        # Retrieving challenge from HTML.
        challenge_loc = login_screen.text.find('name="Challenge"')
        challenge = str(login_screen.text[challenge_loc + 24:challenge_loc + 32])

        # Generating 'Response' value (see login screen HTML for more details).
        response_str = self._user + passwd + challenge
        response = md5(response_str.encode('utf-8')).hexdigest()

        # Creating login payload.
        login_data = {
            'Username': self._user,
            'password': passwd,
            'Submitbtn': '      OK      ',
            'Challenge': challenge,
            'Response': response
        }

        # Logging in.
        session.post(login_post_url, data=login_data, timeout=self._timeout,
                     verify=self._reject_invalid_certs).raise_for_status()

        # Checking if login was successful.
        login_response = session.get(login_get_url, timeout=self._timeout,
                                     verify=self._reject_invalid_certs)
        login_response.raise_for_status()
        if login_response.text.find("login_title") != -1:
            warn("login failed for host at URL " + self._host, RuntimeWarning)
            session.close()
            return False

        # Saving session.
        self._session = session
        return True
    def request_snmp_config_renewal(self) -> None:
        """
        Sets the ``self._renew_snmp`` attribute to ``True`` so that the next call to
        ``get_snmp_config()`` will trigger a re-pull of the SNMP config file.

        This method was not intended to be called directly by the user of this API, but is instead
        intended to be called by functions in this API which make POST requests which may alter
        values in the SNMP configuration file. If the user wishes to pull a fresh dictionary of SNMP
        values this should be accomplished using the ``self.get_snmp_config()`` function (see the
        ``force`` parameter in particular).

        :rtype: ``None``
        """
        self._renew_snmp = True
    def request_system_config_renewal(self) -> None:
        """
        Sets the ``self._renew_system`` attribute to ``True`` so that the next call to
        ``get_system_config()`` will trigger a re-pull of the SNMP config file.

        This method was not intended to be called directly by the user of this API, but is instead
        intended to be called by functions in this API which make POST requests which may alter
        values in the SNMP configuration file. If the user wishes to pull a fresh dictionary of SNMP
        values this should be accomplished using the ``self.get_system_config()`` function (see the
        ``force`` parameter in particular).

        :rtype: ``None``
        """
        self._renew_system = True
    def set_host(self, host: str, passwd: str = "") -> None:
        """
        Sets host and then calls ``self._perform_login()``. Returns ``None``.

        :param host: The host of the TLNET Supervisor.
        :param passwd: (optional) The password to use to log in to the TLNET Supervisor. If the
        ``self._save_passwd`` value (set in the function initializer from the ``save_passwd``
        parameter) is ``True`` and a password was provided in the function initializer (see the
        ``passwd`` parameter), this password will be used if nothing is provided. If there is no
        value saved in ``self.passwd`` and none was provided in this parameter, one will be promted.
        If ``self._save_passwd`` is ``True``, then the provided password will be saved for
        subsequent calls to this function.
        :rtype: ``None``
        """
        # Closing previous session (if there was one).
        if self._host != "":
            self.logout()
        # Saving host value.
        self._host = host

        # Checking if password was provided or if password was saved, and then logging in.
        if passwd != "":
            self._perform_login(passwd)
        elif self._save_passwd:
            self._perform_login(self._passwd)
        else:
            passwd = getpass()
            if self._save_passwd:
                self._passwd = passwd
            self._perform_login(passwd)

# Importing BatchConfiguration module to access configuration files.
# pylint: disable=line-too-long,wrong-import-position
from tlnetcard_python.system.administration.batch_configuration.batch_configuration import BatchConfiguration
