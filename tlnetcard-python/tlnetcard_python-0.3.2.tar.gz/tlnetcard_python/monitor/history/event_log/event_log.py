"""
tlnetcard_python.monitor.history.event_log.event_log
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``EventLog`` object to provide the functionality of TLNET Supervisor ->
Monitor -> History -> Event Log.
"""
# Standard library.
from pathlib import Path
from platform import system
# Required internal classes/functions.
from tlnetcard_python.login import Login

class EventLog:
    """
    A TLNET Supervisor ``EventLog`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> Monitor -> History -> Event Log.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.monitor.history import EventLog
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.monitor.history.EventLog object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_event_log = EventLog(card)
    >>> # Now that the EventLog object has been created, functions belonging to the EventLog class
    >>> # can be used. For example, downloading the event log:
    >>> card_event_log.download_event_log()
    "/home/sample_user/event_log.csv"
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``EventLog`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._post_url = self._login_object.get_base_url + "/delta/hist_log"
    def download_event_log(self, path: str = "") -> str:
        """
        Downloads the system event log and saves it as a CSV file. Returns a ``str`` which contains
        the path to the downloaded file.

        :param path: (optional) The qualified path to which the event log will be written. If no
        value is specified, then the configuration will be written to a file named ``event_log.csv``
        in the current user's ``Downloads`` directory.
        :rtype: ``str``
        """
        # Setting path to downloads directory for operating system if no path was specified.
        if path == "":
            path = str(Path.home())
            if system() == "Windows":
                path += "\\Downloads\\event_log.csv"
            else:
                path += "/Downloads/event_log.csv"

        # Creating download payload.
        download_data = {
            'DLLOG_BUT': 'Download All'
        }

        # Submitting download request.
        verify = self._login_object.get_reject_invalid_certs()
        data = self._login_object.get_session().post(self._post_url, data=download_data,
                                                     timeout=self._login_object.get_timeout(),
                                                     verify=verify)
        data.raise_for_status()

        # Writing event log to file and returning the file path.
        with open(path, "w") as out_file:
            out_file.write(data.text)
        return path
