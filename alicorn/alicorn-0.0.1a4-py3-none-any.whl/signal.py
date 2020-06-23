#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#


class Signal(list):
    """A signal handler that manages callbacks registered against it. This works like a list but when called all
    items in the list are called with the given arguments. If a handler returns true then don't call subsequent handlers

    Example:
        >>> def handler(n):
        ...     print(n * 2)
        >>> signal = Signal('test')
        >>> signal.append(handler)
        >>> signal(2)
        4

    """

    def __init__(self, name='Undefined'):
        super(Signal, self).__init__()
        self._name = name

    def __call__(self, *args, **kwargs):
        """Call any handlers for this signal"""
        for handler in self:
            if handler(*args, **kwargs):
                return

    def __repr__(self):
        return f'<Signal: {self._name}>'
