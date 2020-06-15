""" gate network module.

"""

from mindstone.connection import tcp_connect_to
from mindstone.control.gates.communication import CommunicationGate
from mindstone.control.gates.gate import GateABC
from mindstone.control.gates.root import RootGate
from mindstone.control.memory import Memory
from mindstone.control.network import Network


def get_root_key(gates: dict) -> int:
    """ gets the key of a root gate contained in a collection of gates.

    :param gates: dictionary of gate objects.
    :return: index of root gate.
    """
    for key, gate in gates.items():
        if isinstance(gate, RootGate):
            return key
    raise NotImplementedError("{} does not exist in gates list.".format(RootGate.__class__.__name__))


class GateNetwork(Network):
    """ gate network class.

    """

    def __init__(self, gates, edges, hosts: dict = None):
        if isinstance(gates, list) or isinstance(gates, tuple):
            _gates = {}
            for i, gate in enumerate(gates):
                _gates[i] = gates
            gates = _gates
        self.memory = Memory()
        self.hosts = {} if hosts is None else hosts
        self.path = []

        super().__init__(gates, edges, start=get_root_key(gates))

    def setup(self):
        # create host sockets
        host_sockets = {}
        for key, value in self.hosts.items():
            host_sockets[key] = tcp_connect_to(*value)

        for key in self.nodes.keys():
            # 1. check if node value is a gate
            if not isinstance(self.nodes[key], GateABC):
                TypeError("Node value is not a gate.")

            # 2. add the networks memory to each gate
            self.nodes[key].memory = self.memory

            # 3. setup connection gates
            if isinstance(self.nodes[key], CommunicationGate):
                self.nodes[key].socket = host_sockets[self.nodes[key].host]

    def close_connections(self):
        for key in self.nodes.keys():
            # 1. close the socket attached to each communication gate
            if isinstance(self.nodes[key], CommunicationGate):
                self.nodes[key].socket.close()

    def resolve(self) -> dict:
        return self._resolve_util(self.nodes[self.start])

    def _resolve_util(self, gate: GateABC, parcel: dict = None) -> dict:
        parcel = {} if parcel is None else parcel
        returned_parcel, next_gate = gate.trigger(parcel)
        if next_gate is None:
            return returned_parcel
        self.path.append(next_gate)
        return self._resolve_util(self.nodes[next_gate], returned_parcel)
