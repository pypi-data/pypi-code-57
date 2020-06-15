""" root gate module.

"""

from mindstone.control.gates.communication import CommunicationGate


class RootGate(CommunicationGate):
    """ root gate class.

    """

    def __init__(self, host: str, components: dict = None):
        super(RootGate, self).__init__(host)
        self.components = components if components else dict()

    def trigger(self, *args, **kwargs) -> tuple:
        return super(RootGate, self).trigger({
            "type": "boot",
            "data": self.components
        })
