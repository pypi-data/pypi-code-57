""" gate module.

"""

from abc import ABC, abstractmethod

from mindstone.control.memory import Memory
from mindstone.control.network import Node


class GateABC(ABC, Node):
    """ gate abstract base class.

    A gate is a single operation unit that represents a node in a
    graph data structure. when activated, a gate will take in
    key-value (dict) information, called a parcel, and operate on
    that information.

    The way in which gates are connected dictates the flow of
    information through the network.

    """

    def __init__(self):
        super().__init__()
        self._memory = None

    @property
    def memory(self) -> Memory:
        if self._memory is None:
            raise NotImplementedError("Connection object for this gate has not been set.")
        return self._memory

    @memory.setter
    def memory(self, m: Memory):
        if not isinstance(m, Memory):
            raise TypeError("Object is not valid.")
        self._memory = m

    @abstractmethod
    def trigger(self, *args, **kwargs) -> tuple:
        """ the trigger method is called by the controllers the graph is being resolved.
        :return: A tuple containing the next parcel followed by the next gate.
        """
        pass

    @abstractmethod
    def next(self, *args, **kwargs):
        """ returns the key of the next gate. if no gate precedes then it should return a None value. """
        pass
