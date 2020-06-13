
import numpy as np


class Refunction:
    """
    Refunction creates a new function from an existing function with specific arguments now set as parameters.

    Examples
    --------
    1. When we're expecting a result

    from izzy.features import granulate
    from izzy.misc import Refunction
    import numpy as np

    f = Refunction(granulate, bins=10, mode='equal')
    x = np.random.rand(100)
    x_binned = f(x)

    2. When we just want to execute the function (no result)

    from izzy.misc import Refunction
    import matplotlib.pyplot as plt
    import numpy as np

    def plot(x, y):
        plt.figure()
        plt.plot(x, y)
        plt.show()

    x = np.random.rand(100)
    y = np.random.rand(100)
    f = Refunction(plot, x, y)
    f.execute()
    """

    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    # Allows us to use Refunction instance as a function
    def __call__(self, *args, **kwargs):
        # Process args
        args = self._process_args(args)

        # Run the function
        return self.function(*args, **kwargs, **self.kwargs)

    # Process positional arguments
    def _process_args(self, args):
        # Send warning if we've specified positional arguments at class declaration and call
        if self.args is not None and args is not None:
            Warning('appending new args to first position')
            args += self.args

        # If we've only specified positional arguments at class declaration, use those
        elif self.args is not None:
            args = self.args

        # Return
        return args

    # Execute the function without returning anything
    def execute(self, *args, **kwargs):
        # Process args
        args = self._process_args(args)

        # Run the function
        self.function(*args, **kwargs, **self.kwargs)
