"""
tlnetcard_python.system.administration.upgrade.upgrade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Upgrade`` object to provide the functionality of TLNET Supervisor -> System
-> Administration -> Upgrade.
"""

# Standard library.
from os.path import isfile
from warnings import warn
# Required internal classes/functions.
from tlnetcard_python.login import Login
from tlnetcard_python.monitor.about.information import Information

class Upgrade:
    """
    A TLNET Supervisor ``Upgrade`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> System -> Administration -> Upgrade.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import Upgrade
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.Upgrade object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_upgrade = Upgrade(card)
    >>> # Now that the Upgrade object has been created, functions belonging to the Upgrade class can
    >>> # be used. For example, upgrading the SNMP firmware:
    >>> card_upgrade.upgrade_snmp_firmware("/path/to/firmware/file.bin")
    True
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Upgrade`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._post_url = login_object.get_base_url() + "/delta/adm_upgrade"
        self._information_object = Information(self._login_object)
    def get_firmware_version(self) -> str:
        """
        Returns the current firmware version as a string.

        :rtype: ``str``
        """
        return self._information_object.get_firmware_version()
    def upgrade_snmp_firmware(self, path: str = "ups-tl-01_12_05c.bin") -> bool:
        """
        Upgrades SNMP Device Firmware. Returns ``False`` if the provided upgrade file doesn't exist.
        Otherwise, ``True`` is returned upon successful completion.

        :param path: (optional) The SNMP firmware file to upgrade with.
        :rtype: ``bool``
        """
        # Testing if the file specified in path exists.
        if not isfile(path):
            warn("Specified upgrade file does not exist!", FileNotFoundError)
            return False

        # Creating upload payload.
        upgrade_data = {
            'UL_F_NETWORK': path
        }

        # Uploading SNMP configuration.
        self._login_object.get_session().post(self._post_url, data=upgrade_data,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        warn("NOTE: The card at " + self._login_object.get_base_url()
             + " will be offline for approximately 1 minute.", RuntimeWarning)

        return True
