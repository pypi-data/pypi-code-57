from datetime import datetime

from testframework.checkers.checker_message import CheckerMessage
from testframework.checkers.checker_message_factory import CheckerMessageFactory


class TestCheckerMessageFactory:

    def setup_method(self):
        self.original_event = CheckerMessage(
            {
                "message_id": 0,
                "customer_id": 0,
                "campaign_id": 0,
                "bounce_type": "some_type",
                "event_time": ""
            }
        )
        self.factory = CheckerMessageFactory()

    def test_get_event_as_waiting_returnsMessageAsWaitingEvent(self):
        event_type = "some_event_type"

        expected_waiting_event = CheckerMessage(
            {
                "event_type": event_type,
                "event_json": self.original_event.get_message_as_json(),
                "loaded_at": 0
            },
            id_field="event_type",
            id_value=event_type,
            randomized_fields=(),
            event_time_field="loaded_at")

        generated_waiting_event = self.factory.get_event_as_waiting(self.original_event, event_type)

        expected_waiting_event["loaded_at"] = generated_waiting_event["loaded_at"]

        assert expected_waiting_event == generated_waiting_event

    def test_get_event_as_send_returnsMessageAsSendEvent(self):
        expected_send_event = CheckerMessage(
            {
                "customer_id": 0,
                "campaign_id": 0,
                "message_id": 0,
                "contact_id": 0,
                "launch_id": 0,
                "campaign_type": "batch",
                "domain": "emarsys.com",
                "event_time": ""
            },
            randomized_fields=("campaign_id", "contact_id", "message_id", "launch_id"),
            id_value=self.original_event["customer_id"],
            update_event_time_to=datetime.strptime(self.original_event["event_time"], "%Y-%m-%dT%H:%M:%SZ")
        )
        expected_send_event["campaign_id"] = self.original_event["campaign_id"]
        expected_send_event["message_id"] = self.original_event["message_id"]

        generated_send_message = self.factory.get_event_as_send(self.original_event)

        expected_send_event["contact_id"] = generated_send_message["contact_id"]
        expected_send_event["launch_id"] = generated_send_message["launch_id"]

        assert isinstance(generated_send_message, CheckerMessage)
        assert expected_send_event == generated_send_message

    def test_get_old_event_from_returnsNewCheckerMessageWithOneWeekOldEventTimeField(self):
        source_event = CheckerMessage(
            {
                "message_id": 0,
                "customer_id": 0,
                "campaign_id": 0,
                "bounce_type": "some_type",
                "event_time": ""
            },
            update_event_time_to=datetime(2018, 1, 8, 16, 0, 0)
        )
        expected_old_event = CheckerMessage(
            {
                "message_id": 0,
                "customer_id": 0,
                "campaign_id": 0,
                "bounce_type": "some_type",
                "event_time": ""
            },
            update_event_time_to=datetime(2018, 1, 1, 16, 0, 0)
        )
        source_event["campaign_id"] = expected_old_event["campaign_id"]
        source_event["message_id"] = expected_old_event["message_id"]
        generated_old_enough_message = self.factory.get_old_event_from(source_event)

        assert isinstance(generated_old_enough_message, CheckerMessage)
        assert expected_old_event == generated_old_enough_message
