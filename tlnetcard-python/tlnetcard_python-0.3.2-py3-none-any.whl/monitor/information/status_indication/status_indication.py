""" Allows UPS status to be viewed. """

# Required internal classes/functions.
from tlnetcard_python.login import Login

class StatusIndication:
    """ Class for the StatusIndication object. """
    def __init__(self, login_object: Login) -> None:
        """ Initializes the StatusIndication object. """
