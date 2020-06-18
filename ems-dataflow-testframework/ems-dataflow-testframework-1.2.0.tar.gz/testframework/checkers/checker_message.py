import json
import logging
import random
from copy import deepcopy
from datetime import datetime
from typing import Union, Callable


class CheckerMessage:
    EVENT_TIME_FIELD_PATTERN = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self,
                 message_template: Union[str, dict],
                 id_field: str = "customer_id",
                 id_value: Union[int, str] = 123,
                 randomized_fields: tuple = ("campaign_id", "message_id"),
                 event_time_field: str = "event_time",
                 update_event_time_to: Union[datetime, str] = None,
                 bigtable_key_fields: tuple = ("customer_id", "campaign_id", "message_id"),
                 bigtable_key_factory: Callable[[dict], str] = None) -> None:
        self.__set_message_template(message_template)
        assert id_field in self.__message_template, "id_field not in message_template: {}".format(id_field)
        self._id_field = id_field
        self.__id_value = id_value
        for field in randomized_fields:
            assert field in self.__message_template, "randomized_fields not in message_template: {}".format(field)
        self._randomized_fields = randomized_fields
        self._event_time_field = event_time_field
        assert event_time_field in self.__message_template, "event_time_field not in message_template: {}".format(
            event_time_field)
        self.__update_event_time_to = update_event_time_to
        self.__message = None
        self._bigtable_key_fields = bigtable_key_fields
        self.__bigtable_key_factory = bigtable_key_factory
        self.__randomize_message()

    def get_message(self):
        return self.__message

    def get_message_as_json(self):
        return json.dumps(self.get_message(), separators=(",", ":"))

    def get_unique_fields(self):
        dict_of_unique_identifier = {self._id_field: self.__id_value}
        dict_of_randomized_identifiers = {}
        for field in self._randomized_fields:
            dict_of_randomized_identifiers[field] = self.__message[field]

        return {**dict_of_unique_identifier, **dict_of_randomized_identifiers}

    def get_bigtable_key(self) -> str:
        if self.__message is None:
            get_values_from = self.__message_template
        else:
            get_values_from = self.__message
        if self.__bigtable_key_factory:
            bt_key = self.__bigtable_key_factory(get_values_from)
        else:
            bt_key = self.create_default_bt_key(get_values_from)
        return bt_key

    def create_default_bt_key(self, values):
        key = []
        for key_element in self._bigtable_key_fields:
            key.append(str(values[key_element]))
        bt_key = "_".join(key)
        return bt_key

    def matches_message_dict(self, msg) -> bool:
        assert self._id_field in msg, "id_field not in message: {}".format(self._id_field)
        for field in self._randomized_fields:
            if field not in msg:
                logging.info("randomized_fields not in message: {}, {}".format(field, msg))
                return False

        assert self._event_time_field in msg, "event_time_field not in message: {}".format(
            self._event_time_field)

        is_match = all([msg[field] == self.__message[field] for field in self.get_unique_fields()])

        return is_match

    def clone(self):
        new_message = deepcopy(self)
        return new_message

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __getitem__(self, key):
        return self.__message[key]

    def __setitem__(self, key, value):
        self.__message[key] = value
        if key == self._id_field:
            self.__id_value = value

    def __set_message_template(self, message_template):
        if isinstance(message_template, str):
            self.__message_template = json.loads(message_template)
        else:
            self.__message_template = deepcopy(message_template)

    def __randomize_message(self):
        self.__init_message()
        for field in self._randomized_fields:
            is_string = isinstance(self.__message[field], str)
            new_value = random.randint(10e5, 10e7)
            if is_string:
                new_value = str(new_value)
            self.__message[field] = new_value

        return self

    def __init_message(self):
        self.__message = deepcopy(self.__message_template)
        self.__message[self._id_field] = self.__id_value
        if not self.__update_event_time_to:
            self.__message[self._event_time_field] = datetime.utcnow().strftime(self.EVENT_TIME_FIELD_PATTERN)
        elif isinstance(self.__update_event_time_to, datetime):
            self.__message[self._event_time_field] = self.__update_event_time_to.strftime(self.EVENT_TIME_FIELD_PATTERN)
        else:
            self.__message[self._event_time_field] = self.__update_event_time_to

        self.__update_event_time_to = None
