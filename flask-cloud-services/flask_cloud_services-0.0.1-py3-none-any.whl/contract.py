import abc


class DataListener:
    """Object used for BusNotifications.listener()

    Attributes:
        message: type unknown
        response: type unknown
    """

    def __init__(
        self,
        message_type: str = None,
        topic_arn: str = None,
        message=None,
        response=None
    ):
        self.message_type = message_type
        self.topic_arn = topic_arn
        self.message = message
        self.response = response


class BusNotificationsContract(metaclass=abc.ABCMeta):
    """Contract for notifications buses"""

    @abc.abstractmethod
    def listener(self) -> DataListener:
        """It must Suscribe or Receive Notifications from Notifications Bus
        Implementation of `listener` of Notifications Bus

        Returns:
            DataListener:
        """
        pass

    @abc.abstractmethod
    def publisher(
        self,
        topic_arn: str,
        message,
        *args,
        **kwargs
    ):
        """It must Publish to Notifications Bus

        Args:
            topic_arn (str): topic arn of channel
            message (str): message to publish

        Note: Any parameter the adapter needs,
            wich does not deliver in request
        """
        pass
