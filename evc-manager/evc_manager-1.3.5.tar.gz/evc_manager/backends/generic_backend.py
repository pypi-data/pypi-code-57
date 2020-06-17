""" Generic backend for future upgrades. """


class Backend(object):
    """ Generic backend for future upgrades. """

    def __init__(self):
        self.user = None
        self.password = None
        self.url = None
        self.tenant = None
        self.session_request = None
        self.requester = None

    def authenticate(self):
        """ Authenticate using credentials provided via CLI """
        return True

    def get_evcs(self):
        """ Get all EVC """
        return dict()

    def add_evc(self, new_evc, change=False):
        """ Add/Change EVC based on the provided EVC name """
        return dict()

    def change_evc(self, change_evc):
        """ Change EVC based on the provided EVC name """
        return dict()

    def delete_evc(self, evc_to_delete):
        """ Delete EVC with the provided EVC name """
        return dict()

    def move_evc(self, evc_to_move, current_primary, current_backup, nni):
        """ Move EVC out of a provided NNI """
        return dict()
