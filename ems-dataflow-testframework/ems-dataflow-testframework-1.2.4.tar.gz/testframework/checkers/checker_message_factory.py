from datetime import datetime, timedelta

from testframework.checkers.checker_message import CheckerMessage


class CheckerMessageFactory:

    def get_old_event_from(self, event):
        event_time = datetime.strptime(event["event_time"], CheckerMessage.EVENT_TIME_FIELD_PATTERN)
        old_event_time = event_time - timedelta(days=7)
        old_event = event.clone()
        old_event["event_time"] = old_event_time.strftime(CheckerMessage.EVENT_TIME_FIELD_PATTERN)

        return old_event

    def get_event_as_waiting(self, original_event: CheckerMessage, event_type: str) -> CheckerMessage:
        waiting_event = CheckerMessage(
            {
                "event_type": event_type,
                "event_json": original_event.get_message_as_json(),
                "loaded_at": 0
            },
            id_field="event_type",
            id_value=event_type,
            randomized_fields=(),
            event_time_field="loaded_at",
        )

        return waiting_event

    def get_event_as_backup(self, original_event: CheckerMessage) -> CheckerMessage:
        backup_event = CheckerMessage(
            {
                "json_data": original_event.get_message_as_json(),
                "loaded_at": 0
            },
            id_field="json_data",
            id_value=original_event.get_message_as_json(),
            randomized_fields=(),
            event_time_field="loaded_at",
        )
        return backup_event

    def get_event_as_error(self, original_event: CheckerMessage, id_field: str, id_value: str) -> CheckerMessage:
        error_event = CheckerMessage(
            {
                "data": original_event.get_message_as_json(),
                "timestamp": 0,
                "event_type": "",
                "stacktrace": "",
                "message": ""
            },
            id_field=id_field,
            id_value=id_value,
            randomized_fields=(),
            event_time_field="timestamp"
        )
        return error_event

    def get_event_as_send(self, original_event: CheckerMessage) -> CheckerMessage:
        send_event = CheckerMessage(
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
            id_value=original_event["customer_id"],
            update_event_time_to=datetime.strptime(original_event["event_time"], CheckerMessage.EVENT_TIME_FIELD_PATTERN)
        )
        send_event["campaign_id"] = original_event["campaign_id"]
        send_event["message_id"] = original_event["message_id"]

        return send_event
