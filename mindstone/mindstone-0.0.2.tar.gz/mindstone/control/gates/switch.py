""" switch gate class module.

"""

from mindstone.control.gates.gate import GateABC


class SwitchGate(GateABC):
    """ Switch gate class.

    Routes data to a child gate with respect to the content of
    that data.
    """

    def __init__(self, data_key: str, cases: list, comparison_method: str = "__eq__",
                 default_next=None):
        super().__init__()
        self.cases = cases
        self.comparison_method = comparison_method
        self.default_next = default_next
        self.data_key = data_key

    def next(self, parcel):
        for value, key in self.cases:
            if getattr(parcel[self.data_key], self.comparison_method)(value):
                return key
        return self.default_next

    def trigger(self, parcel: dict) -> tuple:
        return parcel, self.next(parcel)
