import logging
from slacker import Slacker


class Reporter:
    def __init__(self, logger=None, slack_config=None):
        """
        Helps LabManager and Experimenters classes to report progress to user
        :param logger: (Logger) a Logger instance
        :param slack_config: (dict) slack configuration to report a slack recipient.
        Structure: {"slack_token": token, "recipient": #channel/@user}
        """
        self._logger = self.init_logger() if logger is None else logger

        self._slack_bot = self.init_slack_bot(slack_config) if slack_config is not None else None

    @staticmethod
    def init_logger():
        """
        Create Logger Labs if not exists.
        If exists return the existed instance (use case - when user has defined custom logger).
        Else create and add a console handler
        :return: Logger instance
        """
        # logger
        logger = logging.getLogger('Labs')

        # if handler already exists in logger name "Labs", get the logger instance
        if len(logger.handlers) > 0:
            return logger

        logger.setLevel(logging.INFO)

        # create console handler and set level to info
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("'%(asctime)s %(levelname)s %(message)s'")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    @staticmethod
    def init_slack_bot(slack_config):
        """
        Init SlackBot instance.
        :param slack_config: (dict) Structure: {"slack_token": token, "recipient": #channel/@user}
        :return: SlackBot instance
        """
        return SlackBot(**slack_config)

    def report_status(self, text):
        """
        report message by logging and slack message(if exists)
        :param text:
        """
        if self._slack_bot:
            self._slack_bot.report_msg(text)
        if self._logger:
            self._logger.info(text)


class SlackBot:
    def __init__(self, slack_token, recipient):
        """
        SlackBot is used to report progress of the tasks to a slack recipient.
        :param slack_token: (str) a slack-app/bot valid token.
        :param recipient: (str) a @user/#channel to send messages.
        """
        # Slacker instance
        self._slack_bot = Slacker(slack_token)

        self.slack_recipient = recipient

        # slack bot name
        self.slack_bot_name = 'Labs'

    def report_msg(self, text):
        """
        Report msg using Slack API through Slacker package.
        :param text: test to send.
        """
        self._slack_bot.chat.post_message(channel=self.slack_recipient, text=text, as_user=False)
