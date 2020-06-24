import slack
from airflow.hooks.base_hook import BaseHook

from awehflow.alerts.base import Alerter


class SlackAlerter(Alerter):
    def __init__(self, channel, slack_conn_id='slack_default',):
        self.channel = channel
        self.slack_conn_id = slack_conn_id

    def alert(self, context):
        client = slack.WebClient(token=BaseHook.get_connection(self.slack_conn_id).password)

        client.chat_postMessage(
            channel=self.channel,
            text=self.__message_title(context),
            blocks=self.__generate_blocks(context)
        )

    def __message_title(self, context):
        return context.get('name', 'alert').upper()

    def __message_header(self, context):
        if context.get('name', '') == 'failure':
            emoji = ':rotating_light:'
            title = '<{}|{}>'.format(context['body']['error']['log_url'], self.__message_title(context))
        else:
            emoji = ':warning:'
            title = self.__message_title(context)

        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "{} *{}*".format(emoji, title)
            }
        }

    def __generate_message_body(self, items_dict):
        return {
            "type": "section",
            "fields": [{
                "type": "mrkdwn",
                "text": "*{}*\n{}".format(key, value)
            } for key, value in items_dict.items()]
        }

    def __message_body(self, context):
        if context['name'] == 'failure':
            items = {
                'DAG': context['body']['name'],
                'Task': context['body']['error']['task_id'],
                'Exception': context['body']['error']['message']
            }
            if 'engineers' in context['body']:
                engineer_handles = []
                for engineer in context['body']['engineers']:
                    if 'slack' in engineer:
                        engineer_handles.append(engineer['slack'])
                if engineer_handles:
                    items['Engineers'] = ', '.join(['<@{}>'.format(handle) for handle in engineer_handles])

        else:
            items = {key: context['body'][key] for key in context['body'].keys() if
                     key not in ['project', 'engineers', 'status']}

        return self.__generate_message_body(items)

    def __message_footer(self, context):
        return {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":pushpin: *{}*".format(context['body']['project'])
                }
            ]
        }

    def __generate_blocks(self, context):
        blocks = [
            self.__message_header(context),
            {
                "type": "divider"
            },
            self.__message_body(context)
        ]

        if 'project' in context['body']:
            blocks.append(self.__message_footer(context))

        return blocks;