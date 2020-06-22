""" Allows shutdown agent information to be read. """

# Required internal classes/functions.
from tlnetcard_python.login import Login

class ShutdownAgent:
    """ Class for the ShutdownAgent object. """
    def __init__(self, login_object: Login) -> None:
        """ Initializes the ShutdownAgent object. """
