class Command(object):
    """Next action to be taken in response to a dialogue state."""

    def name(self):
        """Unique identifier of this simple action."""

        raise NotImplementedError("An action must implement a name")

    def run(self, args, sio, project_configuration):
        raise NotImplementedError("An action must implement its run method")

    def __str__(self):
        return "Action('{}')".format(self.name())
