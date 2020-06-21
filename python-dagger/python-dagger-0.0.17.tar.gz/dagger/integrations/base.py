import abc

class Integration(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    def isInIntegration(self):
        return False

    def autoloadIntegration(self, function_wrapper):
        """
        Not abstract because not every integration will have this feature

        Args:
            function_wrapper ([type]): [description]

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def getStaticTask(self, **kwargs):
        raise NotImplementedError()
