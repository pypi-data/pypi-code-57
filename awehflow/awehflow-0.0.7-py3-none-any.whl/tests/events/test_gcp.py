from unittest import TestCase
from unittest.mock import patch, MagicMock

from awehflow.events.gcp import PublishToGooglePubSubEventHandler


class TestPublishToGooglePubSubEventHandler(TestCase):
    @patch('awehflow.events.gcp.PubSubHook')
    def setUp(self, _):
        self.handler = PublishToGooglePubSubEventHandler(
            project_id='some_project_id',
            topic='some_topic'
        )

    def test_handle(self):
        """All events should literally just pass the event the event along to pubsub"""
        self.handler._PublishToGooglePubSubEventHandler__emit_message = MagicMock()
        event = {'name': 'woot'}
        self.handler.handle(event)
        self.handler._PublishToGooglePubSubEventHandler__emit_message.assert_called_once_with(event)

        self.handler._PublishToGooglePubSubEventHandler__emit_message = MagicMock()
        event = {'name': 'start'}
        self.handler.handle(event)
        self.handler._PublishToGooglePubSubEventHandler__emit_message.assert_called_once_with(event)

        self.handler._PublishToGooglePubSubEventHandler__emit_message = MagicMock()
        event = {'name': 'failure'}
        self.handler.handle(event)
        self.handler._PublishToGooglePubSubEventHandler__emit_message.assert_called_once_with(event)

    def test_emit_message(self):
        self.handler._PublishToGooglePubSubEventHandler__emit_batch = MagicMock()
        self.handler._PublishToGooglePubSubEventHandler__emit_message({})
        self.handler._PublishToGooglePubSubEventHandler__emit_batch.assert_called_once()

    def test_emit_batch(self):
        self.handler._PublishToGooglePubSubEventHandler__emit_batch([{'msg': 'hello world'}])
        self.handler.pubsub_hook.publish.assert_called_once_with('some_project_id', 'some_topic', [{'msg': 'hello world'}])

    def test_encode_message(self):
        encoded_message = PublishToGooglePubSubEventHandler._PublishToGooglePubSubEventHandler__encode_message('Hello World!')
        self.assertEqual(encoded_message, 'IkhlbGxvIFdvcmxkISI=')