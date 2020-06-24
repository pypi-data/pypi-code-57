from unittest import TestCase
from unittest.mock import MagicMock

from awehflow.events.base import EventHandler


class TestEventHandler(TestCase):
    def test_handle(self):
        handler = EventHandler()
        handler.catch_all = MagicMock()

        event = {'name': 'start'}
        handler.handle(event)
        handler.catch_all.assert_called_once_with(event)

    def test_handle_with_custom_event_method(self):
        class DummyEventHandler(EventHandler):
            def boogie(self, event):
                pass

        handler = DummyEventHandler()
        handler.boogie = MagicMock()
        handler.catch_all = MagicMock()

        event = {'name': 'boogie'}
        handler.handle(event)
        handler.boogie.assert_called_once_with(event)
        handler.catch_all.assert_not_called()