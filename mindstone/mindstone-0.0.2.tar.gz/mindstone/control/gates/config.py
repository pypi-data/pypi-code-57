""" config gate class module.

"""

from mindstone.control.gates.communication import CommunicationGate


class ConfigGate(CommunicationGate):
    """ Config gate class.

    the configuration gate is used to communicate new configurations for
    in use components to the driver. This will send the data from the previous gate ad a
    new configuration to the connected driver.
    """

    def trigger(self, configs_to_send: dict) -> tuple:
        return super(ConfigGate, self).trigger({
            "type": "config",
            "data": configs_to_send
        })
