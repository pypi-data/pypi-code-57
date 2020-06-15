"""Slack control manager"""
import logging
import slack
import re
from typing import Union, List, Callable, Pattern
from .bots import RTMSlackBot, WebClientOverride
from .parsing import is_event, is_bot_message
from ..control_manager import ControlManager, do_nothing, return_empty


# todo consider using children
logger = logging.getLogger(__name__)

# pattern for help retrieval
help_pattern = re.compile('help', re.IGNORECASE)


class RTMControlManager(RTMSlackBot, ControlManager):
    # default message parsing methods
    DEFAULT_PARSING_METHODS = [
        is_event,
        is_bot_message,
    ]

    help_pattern = help_pattern

    def __init__(self,
                 user_member_ids: Union[str, List[str]] = None,
                 token: str = None,
                 channel_name: str = None,
                 auto_reconnect: bool = True,
                 ping_interval: int = 10,
                 start_action: Callable = do_nothing,
                 stop_action: Callable = do_nothing,
                 resume_action: Callable = do_nothing,
                 pause_action: Callable = do_nothing,
                 status_query: Callable = return_empty,
                 help_query: Callable = return_empty,
                 pre_parsing_methods: List[Callable] = None,
                 ):
        """
        A control manager for executing steps contextually based on slack trigger messages.

        :param str, user_member_ids: Slack user ID(s) for the slack bot to be able to message user. find this by going to
            a user's profile, click the three dots (...) and there is the member ID. Example of a slack member ID: ABCDEF.
        :param str token: token to connect to slack client
        :param str channel_name: channel to message on. for example, #channelname
        :param auto_reconnect: enable/disable RTM auto-reconnect
        :param ping_interval: ping interval for RTM client
        :param start_action: callable action to execute on a start trigger
        :param stop_action: callable action to execute on a stop trigger
        :param resume_action: callable action to execute on a resume trigger
        :param pause_action: callable action to execute on a pause trigger
        :param status_query: callable which returns a string representing the status of the thing being controlled
        :param help_query: callable which returns a help string for the Slack interface
        :param pre_parsing_methods: methods to execute on an RTM payload prior to executing targetted methods.
            These methods must accept an RTM payload and return a bool (False will proceed with action execution,
            True on any parsing method will fail to trigger the action methods). See slack_integration.parsing for
            examples.
        """
        # initialize bot and manager
        RTMSlackBot.__init__(
            self,
            user_member_ids=user_member_ids,
            token=token,
            channel_name=channel_name,
            auto_reconnect=auto_reconnect,
            ping_interval=ping_interval,
        )
        ControlManager.__init__(
            self,
            start_action=start_action,
            stop_action=stop_action,
            resume_action=resume_action,
            pause_action=pause_action,
            status_query=status_query,
        )

        # register catch methods
        slack.RTMClient.on(
            event='message',
            callback=self.start_catch,
        )
        slack.RTMClient.on(
            event='message',
            callback=self.pause_catch,
        )
        slack.RTMClient.on(
            event='message',
            callback=self.stop_catch,
        )
        slack.RTMClient.on(
            event='message',
            callback=self.resume_catch,
        )
        slack.RTMClient.on(
            event='message',
            callback=self.status_catch,
        )
        # store pre-parsing methods
        if pre_parsing_methods is None:
            pre_parsing_methods = self.DEFAULT_PARSING_METHODS
        self.parsing_methods: List[Callable] = pre_parsing_methods

        self._help_query = return_empty
        self.help_query = help_query

    @property
    def help_query(self) -> Callable:
        """the callable which is used to retrieve a help string"""
        return self._help_query

    @help_query.setter
    def help_query(self, value):
        if callable(value) is False:
            raise TypeError(f'{value} is not callable')
        self._help_query = value

    @help_query.deleter
    def help_query(self):
        self._help_query = return_empty

    def catch_and_match(self, pattern: Pattern, **payload) -> bool:
        """
        Attempts to match a regex pattern to the message provided

        :param pattern: regex pattern to compare against the text
        :param payload: RTM payload
        :return: match truth
        """
        # apply pre-parsing methods
        if any([pre_parse(**payload) is True for pre_parse in self.parsing_methods]):
            return False
        message = payload['data']
        text = message.get('text')
        if pattern.search(text) is not None:
            logger.debug(f'{pattern} catch triggered by "{text}"')
            return True
        return False

    def start_catch(self, **payload):
        """Catches start calls and executes the start action"""
        if self.catch_and_match(self.start_pattern, **payload) is True:
            with WebClientOverride(self, payload['web_client']):
                if self.start_action is not do_nothing:
                    self.post_slack_message(
                        'Sure thing! Starting things up! :science_parrot:'
                    )
                    # assumes non-blocking
                    self.start_action()
                else:
                    self.post_slack_message(
                        'Sorry, there is no start action defined :disappointed:'
                    )

    def pause_catch(self, **payload):
        """catches pause calls and executes the pause action"""
        if self.catch_and_match(self.pause_pattern, **payload) is True:
            with WebClientOverride(self, payload['web_client']):
                if self.pause_action is not do_nothing:
                    self.post_slack_message(
                        'Pausing the thing!'
                    )
                    # assumes non-blocking
                    self.pause_action()
                else:
                    self.post_slack_message(
                        'Sorry, there is no pause action defined :disappointed:'
                    )

    def resume_catch(self, **payload):
        """catches resume calls and execute the resume action"""
        if self.catch_and_match(self.resume_pattern, **payload) is True:
            with WebClientOverride(self, payload['web_client']):
                if self.resume_action is not do_nothing:
                    self.post_slack_message(
                        'Resuming the thing!'
                    )
                    # assumes non-blocking
                    self.resume_action()
                else:
                    self.post_slack_message(
                        'Sorry, there is no resume action defined :disappointed:'
                    )

    def stop_catch(self, **payload):
        """catches stop calls and executes the stop action"""
        if self.catch_and_match(self.stop_pattern, **payload) is True:
            with WebClientOverride(self, payload['web_client']):
                if self.stop_action is not do_nothing:
                    self.post_slack_message(
                        'Stopping the thing!'
                    )
                    # assumes non-blocking
                    self.stop_action()
                else:
                    self.post_slack_message(
                        'Sorry, there is no stop action defined :disappointed:'
                    )

    def status_catch(self, **payload):
        """catches and posts the status query string"""
        if self.catch_and_match(self.status_pattern, **payload) is True:
            with WebClientOverride(self, payload['web_client']):
                if self.status_query is not return_empty:
                    self.post_slack_message(
                        f"Here's the current status: `{self.status_query()}`"
                    )
                else:
                    self.post_slack_message(
                        'Sorry, there is no status query defined :disappointed:'
                    )

    def help_catch(self, **payload):
        """catches and posts the help string"""
        if self.catch_and_match(self.help_pattern, **payload) is True:
            with WebClientOverride(self, payload['web_client']):
                # todo
                #   - iterate through defined
                #   - check if defined
                #   - add to help string
                if self.help_query is not return_empty:
                    self.post_slack_message(
                        f"Here's how to use the Slack interface: `{self.help_query()}`"
                    )
                else:
                    self.post_slack_message(
                        'Sorry, there is no help query defined :disappointed:'
                    )
