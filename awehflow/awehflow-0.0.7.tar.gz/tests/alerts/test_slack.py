from unittest import TestCase
from unittest.mock import patch

from awehflow.alerts.slack import SlackAlerter


class TestSlackAlerter(TestCase):
    def setUp(self):
        self.alerter = SlackAlerter(channel='#channel_name')

    @patch('awehflow.alerts.slack.slack')
    @patch('awehflow.alerts.slack.BaseHook')
    def test_success_alert(self, MockBaseHook, mock_slack):
        MockBaseHook.get_connection.return_value.password = 'token'

        client = mock_slack.WebClient.return_value

        self.alerter.alert({
            'name': 'success',
            'body': {
                'key': 'value',
                'key2': 'value2',
                'project': 'some_project'
            }
        })

        client.chat_postMessage.assert_called_once_with(
            channel='#channel_name',
            text='SUCCESS',
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":warning: *SUCCESS*"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*key*\nvalue"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*key2*\nvalue2"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": ":pushpin: *some_project*"
                        }
                    ]
                }
            ]
        )

    @patch('awehflow.alerts.slack.slack')
    @patch('awehflow.alerts.slack.BaseHook')
    def test_failure_alert(self, MockBaseHook, mock_slack):
        MockBaseHook.get_connection.return_value.password = 'token'

        client = mock_slack.WebClient.return_value

        self.alerter.alert({
            'name': 'failure',
            'body': {
                'name': 'dag_name',
                'key': 'value',
                'key2': 'value2',
                'project': 'some_project',
                'error': {
                    'task_id': 'some_task_id',
                    'message': 'error message',
                    'log_url': 'example.com'
                },
                'engineers': [
                    {
                        'slack': 'piet'
                    },
                    {
                        'slack': 'pompies'
                    },
                    {
                        'email': 'piet@pompies.com'
                    }
                ]
            }
        })

        client.chat_postMessage.assert_called_once_with(
            channel='#channel_name',
            text='FAILURE',
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":rotating_light: *<example.com|FAILURE>*"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*DAG*\ndag_name"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Task*\nsome_task_id"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Exception*\nerror message"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Engineers*\n<@piet>, <@pompies>"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": ":pushpin: *some_project*"
                        }
                    ]
                }
            ]
        )