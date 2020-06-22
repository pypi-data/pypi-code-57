"""
tlnetcard_python.system.administration.user_manager.user_manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``UserManager`` object to provide the functionality of TLNET Supervisor ->
System -> Administration -> User Manager.
"""

# Standard library.
from os import remove
from time import sleep
from typing import Any, Dict
# Related third-party library.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Required internal classes/functions.
from tlnetcard_python.login import Login
from tlnetcard_python.system.administration.batch_configuration import BatchConfiguration

class UserManager:
    """
    A TLNET Supervisor ``UserManager`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> System -> Administration -> User Manager.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import UserManager
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.UserManager object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_user_man = UserManager(card)
    >>> # Now that the UserManager object has been created, functions belonging to the UserManager
    >>> # class can be used. For example, getting the permissions of a particular user.
    >>> card_user_man.get_permissions("Administrator")
    {'Login User': False, 'Framed User': False, 'Callback Login': False, 'Callback Framed': False,
    'Outbound': False, 'Administrative': True, 'NAS Prompt': False, 'Authenticate Only': False,
    'Callback NAS Prompt': False, 'Call Check': False, 'Callback Administrative': False}
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``UserManager`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/adm_user.asp"
        self._post_url = login_object.get_base_url() + "/delta/adm_user"
        self._batch_object = BatchConfiguration(self._login_object)
    def disable_radius(self) -> None:
        """
        Disables RADIUS authentication. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        user_data = {
            "radius": "0"
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def enable_radius(self) -> None:
        """
        Enables RADIUS authentication. Returns ``None``.

        :rtype: ``None``
        """
        # Generating payload.
        user_data = {
            "radius": "1"
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def get_permissions(self, user: str = "Administrator") -> Dict[str, bool]:
        """
        Returns the permissions for the provided user as a dictionary.

        :param user: (optional) The user type to get permissions for.
        :rtype: ``Dict[str, bool]``
        """
        # Creating permission type list.
        permission_types = ["Login User", "Framed User", "Callback Login", "Callback Framed",
                            "Outbound", "Administrative", "NAS Prompt", "Authenticate Only",
                            "Callback NAS Prompt", "Call Check", "Callback Administrative"]

        # Generating dictionary of user translations.
        pretty = {
            "Administrator": "RADIUS Admin User",
            "Device Manager": "RADIUS Device User",
            "Read Only User": "RADIUS User User"
        }

        # Exiting if user is not a valid value.
        if user not in pretty:
            return {}

        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing list for permissions code.
        if user in system_config:
            permission_code = system_config[user]
        else:
            return {}

        # Converting permissions code to binary string.
        permission_code_bin = format(permission_code, '011b')
        # Reversing binary.
        permission_code_bin = permission_code_bin[::-1]

        # Parsing binary to create dictionary.
        out = {}
        # pylint: disable=consider-using-enumerate
        for i in range(0, len(permission_types)):
            out[permission_types[i]] = bool(int(permission_code_bin[i]))
        return out
    def get_server_info(self) -> Dict[str, Any]:
        """
        Returns information about the RADIUS server as a dictionary.

        :rtype: ``Dict[str, Any]``
        """
        # Generating dictionary of items to search for and initializing out dictionary.
        pretty = {
            "RADIUS Server": "IP",
            "RADIUS Secret": "Secret",
            "RADIUS Port": "Port"
        }
        out = {}

        # GETing system config.
        system_config = self._login_object.get_system_config()

        for i in pretty:
            if i in system_config:
                out[pretty[i]] = system_config[i]
        out['Port'] = int(out['Port'])
        return out
    def get_user(self, user: str = "Administrator") -> Dict[str, Any]:
        """
        Returns information about the provided user as a dictionary.

        :param user: (optional) The user type to get information about.
        :rtype: ``Dict[str, Any]``
        """
        # Generating dictionary of search translations.
        pretty = {
            user + ' Account': 'Name',
            user + ' Password': 'Password',
            user + ' Limit': 'WAN Access'
        }

        # Exiting if user is not a valid value.
        if user not in ["Administrator", "Device Manager", "Read Only"]:
            return {}
        out = {
            'Type': user
        }

        # GETing system config.
        system_config = self._login_object.get_system_config()

        # Parsing list for required values.
        for i in pretty:
            if i in system_config:
                out[pretty[i]] = system_config[i]
        out[user + ' Limit'] = bool(out[user + ' Limit'])
        return out
    # pylint: disable=too-many-arguments,too-many-locals
    def set_permissions(self, user: str = "Administrator", login_user: bool = False,
                        framed_user: bool = False, callback_login: bool = False,
                        callback_framed: bool = False, outbound: bool = False,
                        administrative: bool = False, nas_prompt: bool = False,
                        authenticate_only: bool = False, callback_nas_prompt: bool = False,
                        call_check: bool = False, callback_administrative: bool = False,
                        selenium: bool = False) -> bool:
        """
        Sets permissions for the provided user. Returns ``False`` if an invalid user type is
        specified. Otherwise, ``True`` is returned upon successful completion.

        :param user: (optional) The user type to set permissions for.
        :param login_user: (optional) Whether the user type is to be a login user.
        :param framed_user: (optional) Whether the user type is to be framed.
        :param callback_login: (optional) Whether the user type is to be a callback login user.
        :param callback_framed: (optional) Whether the user type is to be callback framed.
        :param outbound: (optional) Whether the user is to be outbound.
        :param administrative: (optional) Whether the user is to be administrative.
        :param nas_prompt: (optional) Whether the user is to have a NAS prompt.
        :param authenticate_only: (optional) Whether the user is to be authenticate only.
        :param callback_nas_prompt: (optional) Whether the user is to have a callback NAS prompt.
        :param call_check: (optional) Whether the user is to have a call check.
        :param callback_administrative: (optional) Whether the user is to be callback
        administrative.
        :param selenium: (optional) Whether Selenium is to be used to retreive permissions.
        :rtype: ``bool``
        """
        # Generating required dictionaries.
        pretty = {
            "Administrator": ['RADIUS Admin User', 0],
            "Device Manager": ['RADIUS Device User', 20],
            "Read Only User": ['RADIUS User User', 40]
        }
        permissions = {
            0: login_user,
            1: framed_user,
            2: callback_login,
            3: callback_framed,
            4: outbound,
            5: administrative,
            6: nas_prompt,
            7: authenticate_only,
            8: callback_nas_prompt,
            9: call_check,
            10: callback_administrative
        }

        # Exiting if invalid user type was specified.
        if user not in pretty:
            return False

        if not selenium:
            # Generating binary permissions string.
            permission_code_bin = ""
            for i in permissions:
                permission_code_bin += str(int(permissions[i]))

            # Reversing string.
            permission_code_bin = permission_code_bin[::-1]
            # Converting binary string to integer.
            permission_code = int(permission_code_bin, 2)

            # GETing system configuration and writing lines to list.
            self._batch_object.download_system_configuration("system_config_temp.ini")
            with open("system_config_temp.ini", "r") as sys_config_file:
                sys_config = sys_config_file.readlines()

            # Parsing list and adding permissions code.
            updated_sys_config = []
            for line in sys_config:
                if line.find(pretty[user][0]) != -1:
                    updated_sys_config.append(pretty[user][0] + " Type="
                                              + str(permission_code) + "\n")
                else:
                    updated_sys_config.append(line)

            # Writing updated config to file.
            with open("system_config_temp.ini", "w") as sys_config_file:
                sys_config_file.writelines(updated_sys_config)

            # Uploading updated batch configuration file.
            self._batch_object.upload_system_configuration("system_config_temp.ini")

            # Cleaning up.
            remove("system_config_temp.ini")
        else:
            # Configuring Selenium to run headless (i.e. without a GUI).
            browser_options = Options()
            browser_options.add_argument("--headless")
            browser = webdriver.Chrome(options=browser_options)
            # Getting webpage.
            browser.get(self._get_url)
            # Adding cookies from requests session.
            requests_cookies = self._login_object.get_session().cookies.get_dict()
            for cookie in requests_cookies:
                browser.add_cookie({'name': cookie,
                                    'domain': self._login_object.get_host(),
                                    'value': requests_cookies[cookie]})
            # Getting webpage now that cookies are installed.
            browser.get(self._get_url)
            # A very brief sleeping period to let elements load.
            sleep(0.5)

            # Clicking boxes.
            for i in permissions:
                if (permissions[i] and
                        not browser.find_element_by_id(str(i + pretty[user][1])).is_selected()):
                    browser.find_element_by_id(str(i + pretty[user][1])).click()
                elif (not permissions[i] and
                      browser.find_element_by_id(str(i + pretty[user][1])).is_selected()):
                    browser.find_element_by_id(str(i + pretty[user][1])).click()

            # Clicking submit and closing browser.
            browser.find_element_by_id("@adm_console#11").click()
            browser.close()

        # Requesting system config renewal.
        self._login_object.request_system_config_renewal()
        return True
    def set_server_info(self, server: str, secret: str, port: int = 1812) -> None:
        """
        Sets information for the RADIUS server. Returns ``None``.

        :param server: The RADIUS server to use.
        :param secret: The RADIUS server secret to use.
        :param port: (optional) port to use for RADIUS.
        :rtype: ``None``
        """
        # Generating payload.
        user_data = {
            "radius": "1",
            "USR_RADSRV": server,
            "USR_RADSEC": secret,
            "USR_RADPRT": str(port)
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
    def set_user(self, username: str, passwd: str, wan_access: bool = False,
                 user: str = "Administrator") -> bool:
        """
        Sets information for the provided user. Returns ``False`` if an invalid user type is
        specified. Otherwise, ``True`` is returned upon successful completion.

        :param username: The username to use for the specified user type.
        :param passwd: The password to use for the specified user type.
        :param wan_access: Whether the user should be accessible from outside of the LAN.
        :param user: The user type the user belongs to.
        :rtype: ``bool``
        """
        # Setting user num string.
        if user == "Administrator":
            num = "1"
        elif user == "Device Manager":
            num = "2"
        elif user == "Read Only User":
            num = "3"
        else:
            return False

        # Generating payload.
        user_data = {
            "account" + num: username,
            "passwd" + num: passwd,
            "limit" + num: str(int(wan_access))
        }

        # Uploading console configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=user_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        self._login_object.request_system_config_renewal()
        return True
