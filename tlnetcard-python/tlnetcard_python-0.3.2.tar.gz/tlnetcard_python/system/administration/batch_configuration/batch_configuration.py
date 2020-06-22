"""
tlnetcard_python.system.administration.batch_configuration.batch_configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``BatchConfiguration`` object to provide the functionality of TLNET
Supervisor -> System -> Administration -> Batch Configuration.
"""

# Standard library.
from os.path import isfile
from pathlib import Path
from platform import system
from warnings import warn
# Required internal classes/functions.
from tlnetcard_python.login import Login

class BatchConfiguration:
    """
    A TLNET Supervisor ``BatchConfiguration`` object. Provides the functionality of the equivalent
    webpage TLNET Supervisor -> System -> Administration -> Batch Configuration.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.system.administration import BatchConfiguration
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.system.administration.BatchConfiguration object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_batch_config = BatchConfiguration(card)
    >>> # Now that the BatchConfiguration object has been created, functions belonging to the
    >>> # BatchConfiguration class can be used. For example, uploading a new system configuration
    >>> # file:
    >>> card_batch_config.upload_system_configuration("path/to/config/file.ini")
    RuntimeWarning: The card at https://10.0.0.100:443 will be offline for approximately 10 seconds.
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``BatchConfiguration`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._post_url = login_object.get_base_url() + "/delta/adm_batch"
    def download_snmp_configuration(self, path: str = "", no_write: bool = False) -> str:
        """
        Downloads the SNMP configuration. If ``no_write`` is ``False``, then the configuration will
        be written to a file, and the file path will be returned as a string. If ``no_write`` is
        ``True``, the configuration file will be returned as a string.

        :param path: (optional) The qualified path to which the configuration will be written. If no
        value is specified (and ``no_write`` is ``False``), then the configuration will be written
        to a file named ``snmp_config.ini`` in the current user's ``Downloads`` directory.
        :param no_write: (optional) Whether the configuration should be returned as a string rather
        than saved to a file.
        :rtype: ``str``
        """
        # Setting path to downloads directory for operating system if no path was specified.
        if path == "" and not no_write:
            path = str(Path.home())
            if system() == "Windows":
                path += "\\Downloads\\snmp_config.ini"
            else:
                path += "/Downloads/snmp_config.ini"

        # Creating download payload.
        download_data = {
            'DL_SNMP': 'Download'
        }

        # Submitting download request.
        verify = self._login_object.get_reject_invalid_certs()
        data = self._login_object.get_session().post(self._post_url, data=download_data,
                                                     timeout=self._login_object.get_timeout(),
                                                     verify=verify)
        data.raise_for_status()
        # Returning raw configuration data if no_write was set to True.
        if no_write:
            return data.text
        # Otherwise writing configuration data to file an returning the file path.
        with open(path, "w") as out_file:
            out_file.write(data.text)
        return path
    def download_system_configuration(self, path: str = "", no_write: bool = False) -> None:
        """
        Downloads the system configuration. If ``no_write`` is ``False``, then the configuration
        will be written to a file, and the file path will be returned as a string. If ``no_write``
        is ``True``, the configuration file will be returned as a string.

        :param path: (optional) The qualified path to which the configuration will be written. If no
        value is specified (and ``no_write`` is ``False``), then the configuration will be written
        to a file named ``system_config.ini`` in the current user's ``Downloads`` directory.
        :param no_write: (optional) Whether the configuration should be returned as a string rather
        than saved to a file.
        :rtype: ``str``
        """
        # Setting path to downloads directory for operating system if no path was specified.
        if path == "" and not no_write:
            path = str(Path.home())
            if system() == "Windows":
                path += "\\Downloads\\system_config.ini"
            else:
                path += "/Downloads/system_config.ini"

        # Creating download payload.
        download_data = {
            'DL_SYSTEM': 'Download'
        }

        # Submitting download request.
        verify = self._login_object.get_reject_invalid_certs()
        data = self._login_object.get_session().post(self._post_url, data=download_data,
                                                     timeout=self._login_object.get_timeout(),
                                                     verify=verify)
        data.raise_for_status()
        # Returning raw configuration data if no_write was set to True.
        if no_write:
            return data.text
        # Otherwise writing configuration data to file and returning the file path.
        with open(path, "w") as out_file:
            out_file.write(data.text)
        return path
    def upload_snmp_configuration(self, path: str = "snmp_config.ini") -> None:
        """
        Uploads the specified SNMP configuration file. Returns ``None``.

        :param path: (optional) The qualified path of the file to upload. If no path is specified,
        a file named ``snmp_config.ini`` will be uploaded from the current directory. If the file
        to be uploaded cannot be found, a ``FileNotFoundError`` will be thrown.
        :rtype: ``None``
        """
        # Testing if the file specified in path exists.
        if not isfile(path):
            warn("Specified configuration file does not exist!", FileNotFoundError)
            return

        # Creating upload payload.
        upload_data = {
            'UL_SNMP': 'Upload'
        }
        upload_file = {
            'UL_F_SNMP': (path.split("/")[-1], open(path, 'rb'), 'multipart/form-data'),
        }

        # Uploading SNMP configuration and requesting SNMP config renewal.
        self._login_object.get_session().post(self._post_url, data=upload_data, files=upload_file,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        warn("The card at " + self._login_object.get_base_url()
             + " will be offline for approximately 10 seconds.", RuntimeWarning)
        self._login_object.request_snmp_config_renewal()
    def upload_system_configuration(self, path: str = "system_config.ini") -> None:
        """
        Uploads the specified system configuration file. Returns ``None``.

        :param path: (optional) The qualified path of the file to upload. If no path is specified,
        a file named ``system_config.ini`` will be uploaded from the current directory. If the file
        to be uploaded cannot be found, a ``FileNotFoundError`` will be thrown.
        :rtype: ``None``
        """
        # Testing if the file specified in path exists.
        if not isfile(path):
            warn("Specified configuration file does not exist!", FileNotFoundError)
            return

        # Creating upload payload.
        upload_data = {
            'UL_SYSTEM': 'Upload'
        }
        upload_file = {
            'UL_F_SYSTEM': (path.split("/")[-1], open(path, 'rb'), 'multipart/form-data'),
        }

        # Uploading system configuration and requesting system config renewal.
        self._login_object.get_session().post(self._post_url, data=upload_data, files=upload_file,
                                              timeout=self._login_object.get_timeout(),
                                              verify=self._login_object.get_reject_invalid_certs()
                                              ).raise_for_status()
        warn("The card at " + self._login_object.get_base_url()
             + " will be offline for approximately 10 seconds.", RuntimeWarning)
        self._login_object.request_system_config_renewal()
