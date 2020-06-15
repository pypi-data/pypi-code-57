""" function gate module.

"""

from mindstone.control.gates.gate import GateABC


class FunctionGate(GateABC):
    """ function gate class.

    A function gate, when activated, takes in input give from the previous
    gate and uses a given external function to process that data. The output
    of that function is the passed onto th next gate.

    Example of a defined function:

        def my_function(**previous_parcel) -> dict:
            return {"hello": "world"}

    The function can then be passed into the function gate when it is
    initialized:

        gates = [
            ...,
            FunctionGate(my_function)
            ...
        ]

    """

    def __init__(self, function):
        """ initialize the function gate.

        :param function (callable): function to be executed when the gate is activated.
        """
        super().__init__()
        self._function = function

    def next(self):
        return self.children[0] if len(self.children) > 0 else None

    def trigger(self, parcel: dict) -> tuple:
        function_return = self._function(**parcel)
        parcel = function_return if isinstance(function_return, dict) else dict()
        return parcel, self.next()
