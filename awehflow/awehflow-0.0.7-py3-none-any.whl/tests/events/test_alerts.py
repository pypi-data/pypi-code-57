from unittest import TestCase

from awehflow.events.alerts import AlertsEventHandler


class TestAlertsEventHandler(TestCase):
    def test_handle(self):
        handler = AlertsEventHandler()

        event = {'name': 'woot'}
        handler.handle(event)
