import inspect

from argument.custom_action import CustomAction


class Argument(object):
    """
    Decorator to create a command line argument
    """
    arguments = []

    def __init__(self, method=None, **kwargs):
        self.method = method
        # if method is None the decorator has parameters
        if method is not None:
            self.args = tuple(['--' + method.__name__])

            self.kwargs.update({
                'action': CustomAction,
                'method': method,
            })
            parameters = [p for p in inspect.signature(method).parameters if not p.startswith('_')]
            # nargs = number of arguments in method
            self.kwargs['nargs'] = len(parameters)
            if parameters:
                self.kwargs['metavar'] = ' '.join(parameters)

            self.arguments.append(self)
        else:
            self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        # if method is None the decorator has parameters and the first argument is the method
        if self.method is None:
            self.method = list(args)[0]
            self.__init__(**vars(self))
            return self
        return self.method(*args, **kwargs)
