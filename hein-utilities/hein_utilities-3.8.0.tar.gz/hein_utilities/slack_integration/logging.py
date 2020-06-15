"""
Legacy support for logging to Slack. Use the Slack bots directly.
"""
import warnings
from .bots import SlackBot, RTMSlackBot


warnings.warn(  # v3.1
    'the slack_integration.logging module has been consolidated into their parent bots. '
    'Please update your code to instantiate a bot and add the bot instance as a handler directly',
    DeprecationWarning,
    stacklevel=2,
)


class SlackLoggingHandler(SlackBot):
    def __init__(self, **kwargs):
        """
        DEPRECATED
        A logging stream handler which logs to a slack channel. This class encompasses the RTMSlackBot class to enable
        real-time-messaging handling using the connected slack bot.
        """
        warnings.warn(  # v3.1
            f'{self.__class__.__name__} has been deprecated, use slack_integration.bots.SlackBot instead',
            DeprecationWarning,
            stacklevel=2,
        )
        SlackBot.__init__(self, **kwargs)

    @property
    def bot(self):
        """legacy pass through"""
        return self


class RTMSlackLoggingHandler(RTMSlackBot):
    def __init__(self, **kwargs):
        """
        DEPRECATED
        A logging stream handler which logs to a slack channel. This class encompasses the RTMSlackBot class to enable
        real-time-messaging handling using the connected slack bot.
        """
        warnings.warn(  # v3.1
            f'{self.__class__.__name__} has been deprecated, use slack_integration.bots.RTMSlackBot instead',
            DeprecationWarning,
            stacklevel=2,
        )
        RTMSlackBot.__init__(self, **kwargs)

    @property
    def bot(self):
        """legacy pass through"""
        return self
