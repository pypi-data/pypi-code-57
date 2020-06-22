""" Allows general UPS properties to be read. """

# Required internal classes/functions.
from tlnetcard_python.login import Login

class UpsProperties:
    """ Class for the UpsProperties object. """
    def __init__(self, login_object: Login) -> None:
        """ Initializes the UpsProperties object. """
