""" controller module.

"""

from mindstone.control.gates.network import GateNetwork


class Controller(GateNetwork):
    """ controller class.

    The controller class defines the control model for an agent,
    that is, the agent's behaviour. It does this by connecting
    what's known as gates which can perform operations, process
    data or control the flow of injected data. These gates ae
    also the interface between the local agent driver and the
    remote agent model.
    """

    def run(self) -> dict:
        network_resolved_data = self.resolve()
        self.close_connections()
        return network_resolved_data
