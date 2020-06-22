"""
tlnetcard_python.monitor.history.data_log.data_log
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``DataLog`` object to provide the functionality of TLNET Supervisor ->
Monitor -> History -> Data Log.
"""
# Standard library.
from pathlib import Path
from platform import system
# Required internal classes/functions.
from tlnetcard_python.login import Login

class DataLog:
    """
    A TLNET Supervisor ``DataLog`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> Monitor -> History -> Data Log.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.monitor.history import DataLog
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.monitor.history.DataLog object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_data_log = DataLog(card)
    >>> # Now that the DataLog object has been created, functions belonging to the DataLog class
    >>> # can be used. For example, downloading the data log:
    >>> card_data_log.download_data_log()
    "/home/sample_user/data_log.csv"
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``DataLog`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._post_url = self._login_object.get_base_url + "/delta/hist_data"
    def download_data_log(self, path: str = "") -> str:
        """
        Downloads the system data log and saves it as a CSV file. Returns a ``str`` which contains
        the path to the downloaded file.

        :param path: (optional) The qualified path to which the data log will be written. If no
        value is specified, then the configuration will be written to a file named ``data_log.csv``
        in the current user's ``Downloads`` directory.
        :rtype: ``str``
        """
        # Setting path to downloads directory for operating system if no path was specified.
        if path == "":
            path = str(Path.home())
            if system() == "Windows":
                path += "\\Downloads\\data_log.csv"
            else:
                path += "/Downloads/data_log.csv"

        # Creating download payload.
        download_data = {
            'DATA_BUT': 'Download'
        }

        # Submitting download request.
        verify = self._login_object.get_reject_invalid_certs()
        data = self._login_object.get_session().post(self._post_url, data=download_data,
                                                     timeout=self._login_object.get_timeout(),
                                                     verify=verify)
        data.raise_for_status()

        # Writing data log to file and returning the file path.
        with open(path, "w") as out_file:
            out_file.write(data.text)
        return path
