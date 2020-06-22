"""
tlnetcard_python.monitor.about.information.information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides an ``Information`` object to provide the functionality of TLNET Supervisor
-> Monitor -> About -> Information.
"""

# Required internal classes/functions.
from tlnetcard_python.login import Login

# pylint: disable=too-few-public-methods
class Information:
    """
    A TLNET Supervisor ``Information`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> Monitor -> About -> Information.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.monitor.about import Information
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.monitor.about.Information object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_info = Information(card)
    >>> # Now that the Information object has been created, functions belonging to the Information
    >>> # class can be used. For example GETing the current firmware version (the only function in
    >>> # this class):
    >>> card_info.get_firmware_version()
    '01.12.05c'
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Information`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/ups/about_info.asp"
    def get_firmware_version(self) -> str:
        """
        Returns the current TLNET Supervisor firmware version as a string.

        :rtype: ``str``
        """
        # GETing Information page.
        verify = self._login_object.get_reject_invalid_certs()
        resp = self._login_object.get_session().get(self._get_url,
                                                    timeout=self._login_object.get_timeout(),
                                                    verify=verify)
        resp.raise_for_status()

        # Parsing response for firmware version.
        start_index = str(resp.text).find("Version : ") + 10
        end_index = str(resp.text).find("\n", start_index)
        return resp.text[start_index:end_index]
