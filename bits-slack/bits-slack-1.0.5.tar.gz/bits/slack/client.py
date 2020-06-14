"""Slack command line client class."""


class Client:
    """Slack client class."""

    def __init__(self, slack):
        """Initialize a class instance."""
        self.slack = slack

    def channels_list(self):
        """Display a list of channels (public conversations)."""
        slack_channels = self.slack.get_conversations_dict()
        print('Found %s channels in Slack.' % (len(slack_channels)))
        for cid in sorted(slack_channels, key=lambda x: slack_channels[x]['name']):
            channel = slack_channels[cid]
            print('%s %s' % (
                cid,
                channel['name'],
            ))
