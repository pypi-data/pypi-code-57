from unittest import TestCase
from unittest.mock import MagicMock

from awehflow.events.alerts import AlertsEventHandler


class TestAlertsEventHandler(TestCase):
    def test_handle_not_alerting(self):
        alerter1 = MagicMock()
        alerter2 = MagicMock()
        handler = AlertsEventHandler(alerters=[alerter1, alerter2], alert_on=['success'])

        event = {'name': 'woot'}
        handler.handle(event)

        alerter1.alert.assert_not_called()
        alerter2.alert.assert_not_called()

    def test_handle_alerting(self):
        alerter1 = MagicMock()
        alerter2 = MagicMock()
        handler = AlertsEventHandler(alerters=[alerter1, alerter2], alert_on=['success'])

        event = {'name': 'success'}
        handler.handle(event)

        alerter1.alert.assert_called_once_with(event)
        alerter2.alert.assert_called_once_with(event)
