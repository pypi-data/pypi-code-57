"""
tlnetcard_python.monitor.history.configure.configure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``Configure`` object to provide the functionality of TLNET Supervisor ->
Monitor -> History -> Configure.
"""

# Required internal classes/functions.
from tlnetcard_python.login import Login

class Configure:
    """
    A TLNET Supervisor ``Configure`` object. Provides the functionality of the equivalent webpage
    TLNET Supervisor -> Monitor -> History -> Configure.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.monitor.history import Configure
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.monitor.history.Configure object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_configure = Configure(card)
    >>> # Now that the Configure object has been created, functions belonging to the Configure class
    >>> # can be used. For example, clearing the event log:
    >>> card_configure.clear_event_log()
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``Configure`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
