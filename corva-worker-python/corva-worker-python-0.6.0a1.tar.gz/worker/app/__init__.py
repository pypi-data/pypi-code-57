import json
import time

from worker.app.modules.time_activity_module import TimeActivityModule
from worker.framework import constants
from worker.data.operations import gather_wits_for_period
from worker.framework.mixins import RedisMixin, LoggingMixin, RollbarMixin
from worker.framework.state import State
from worker import exceptions


class App(RedisMixin, LoggingMixin, RollbarMixin):
    app_state_fields = {
        'asset_id': int,
        'last_processed_timestamp': int
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.asset_id = None
        self.event = None
        self.state = None

        self.app_name = constants.get('global.app-name')
        self.app_key = constants.get('global.app-key')

    def load(self, event: str):
        """
        :param event: a scheduler event or wits stream
        :return:
        """
        event_type = self.get_event_type()
        event = self.clean_event(event)

        max_lookback_seconds = self.get_max_lookback_seconds()
        event = self.format_event(event_type, event)
        self.asset_id = self.determine_asset_id(event)

        self.state = self.load_state()

        self.event = self.load_event(event_type, event, max_lookback_seconds)
        self.log_event(self.event, max_lookback_seconds)

    def log_event(self, event, max_lookback_seconds):
        self.debug(self.asset_id, "WITS input to {0} -> {1}".format(self.app_name, event))

        if not event:
            return

        batch_size = len(event)
        start_time = event[0].get("timestamp")
        end_time = event[-1].get("timestamp")
        system_time = time.time()

        self.debug(
            self.asset_id,
            "Received {} elements from {} to {} at {}. {} seconds of initial data are lookback.".format(
                batch_size, start_time, end_time, system_time, max_lookback_seconds
            )
        )

    @staticmethod
    def get_event_type():
        event_type = constants.get('global.event-type', "")

        if event_type not in ("scheduler", "wits_stream"):
            raise Exception('event_type specified incorrectly: {}'.format(event_type))

        return event_type

    @staticmethod
    def clean_event(event):
        if not event:
            raise Exception("Empty event")

        try:
            if isinstance(event, (str, bytes, bytearray)):
                event = json.loads(event)
        except ValueError:
            raise Exception("Invalid event JSON")

        return event

    def get_max_lookback_seconds(self):
        """
        For each module (mostly in time-base modules), the time of processing does not
        match the last time of the event so extra data is required to look back and get
        the data so the processing can start from where it left off.
        :return:
        """

        time_modules = [module for module in self.get_modules() if issubclass(module, TimeActivityModule)]
        maximum_lookback = 0
        for module in time_modules:
            module_lookback = constants.get('{}.{}.export-duration'.format(self.app_key, module.module_key), default=0)
            maximum_lookback = max(module_lookback, maximum_lookback)

        return maximum_lookback

    def load_event(self, event_type, event, max_lookback_seconds):
        if event_type == 'scheduler':
            return self.load_scheduler_event(self.asset_id, event, max_lookback_seconds)

        if event_type == 'wits_stream':
            return self.load_wits_stream_event(self.asset_id, event, max_lookback_seconds)

        return None

    def load_scheduler_event(self, asset_id, event, max_lookback_seconds):
        """
        To load a scheduler event and get the wits stream data
        :param asset_id: The asset to load
        :param event: The cleaned event from Kafka scheduler stream
        :param max_lookback_seconds: Maximum amount of time to look back prior to the scheduler event to cover gaps
        :return: list of WITS data between the last processed timestamp and the final event item timestamp
        """

        start_timestamp = self.state.get('last_processed_timestamp', event[0].get('timestamp') - 1)
        end_timestamp = event[-1].get('timestamp')

        # the event is converted from scheduler to wits stream
        scheduler_event = gather_wits_for_period(
            asset_id=asset_id,
            start=start_timestamp - max_lookback_seconds,
            end=end_timestamp,
            limit=constants.get('global.query-limit'))

        return scheduler_event

    @staticmethod
    def load_wits_stream_event(asset_id, event, max_lookback_seconds):
        """
        To load a wits stream event and get more data if necessary
        :param asset_id: The asset to load
        :param event: The cleaned event from Kafka WITS stream
        :param max_lookback_seconds: Maximum amount of time to look back prior to WITS data to cover gaps
        :return: list of WITS data between the first event timestamp and the first timestamp
        """

        if event and max_lookback_seconds:
            first_timestamp = event[0].get('timestamp')

            if not first_timestamp:
                return event

            # Subtract one from the timestamp so that we don't reselect the final data item that was sent in the event
            end_timestamp = first_timestamp - 1

            previous_events = gather_wits_for_period(
                asset_id=asset_id,
                start=first_timestamp - max_lookback_seconds,
                end=end_timestamp,
                limit=constants.get('global.query-limit'))

            event = previous_events + event

        return event

    @staticmethod
    def format_event(event_type: str, event: list) -> list:
        """
        validate the wits_stream event, flatten and organize the data into a desired format
        :param event_type: type of event
        :param event: a wits_stream event
        :return: a list of wits records
        """

        first_event = event[0]
        if isinstance(first_event, list):
            # This is possible for both scheduler and old wits stream event types
            try:
                # Because the events are structured into 'list of lists', using the following code
                # converts them into a flat single list. This is done for better data processing in
                # the proceeding steps.
                event = [item for sublist in event for item in sublist]
            except ValueError:
                raise Exception("Records are not valid JSON")

            if not isinstance(event, list):
                raise Exception("Records is not an array")

            if not event:
                raise Exception("Records is empty.")

            if event_type == 'scheduler':
                event = [
                    {
                        "asset_id": item["asset_id"],
                        "timestamp": int(item['schedule_start'] / 1000)
                    }
                    for item in event
                ]
            return event

        elif isinstance(first_event, dict):
            # This is possible for the new wits stream event type
            records = []
            for each in event:
                records = records + each.get("records", [])
            return records

        else:
            raise TypeError("Event is neither a scheduler, old nor new kafka consumer")

    @staticmethod
    def determine_asset_id(event: list) -> int:
        try:
            return int(event[0]["asset_id"])
        except Exception:
            raise Exception('Event does not contain asset_id: {}'.format(event))

    def load_state(self):
        try:
            r = self.get_redis()
            previous_state = r.get(self.get_redis_key(self.asset_id, self.app_key))
            previous_state = json.loads(previous_state)
        except Exception as ex:
            self.error(self.asset_id, "REDIS connection error: {0}".format(ex))
            previous_state = {
                "asset_id": self.asset_id,
            }

        state = State(self.app_state_fields, previous_state)

        if not state.get('asset_id', None):
            state['asset_id'] = self.asset_id

        return state

    def save_state(self):
        r = self.get_redis()
        r.set(self.get_redis_key(self.asset_id, self.app_key), value=self.state.to_json())

    def get_modules(self):
        raise exceptions.Misconfigured("No modules found")

    def run_modules(self):
        if not self.event:
            return

        for module_type in self.get_modules():
            try:
                module = module_type(self.state, rollbar=self.rollbar)
            except Exception:
                raise exceptions.Misconfigured("Module {0} not able to initialize for asset_id {1}".format(module_type, self.asset_id))

            try:
                module.run(self.event)
            except Exception:
                self.track_error(message=f"Error in module {module_type.module_key}")

        last_processed_timestamp = self.event[-1].get('timestamp')
        self.state['last_processed_timestamp'] = last_processed_timestamp
