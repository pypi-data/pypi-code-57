import json
from copy import deepcopy
from datetime import datetime
from unittest.mock import call, patch

from pytest import fixture

from testframework.checkers.checker_message import CheckerMessage


@fixture(scope="function", name="checker_message")
def checker_message():
    return CheckerMessage(
        {
            "customer_id": 0,
            "campaign_id": 0,
            "message_id": 0,
            "event_time": ""
        }
    )


def test_create_checker_message(checker_message):
    utcnow = datetime.utcnow().replace(microsecond=0)
    message = checker_message.get_message()
    assert message["customer_id"] == 123
    assert 10e5 <= message["campaign_id"] <= 10e7
    assert 10e5 <= message["message_id"] <= 10e7
    assert utcnow <= datetime.strptime(message["event_time"], '%Y-%m-%dT%H:%M:%SZ')


def test_not_randomizing_message_twice(checker_message):
    message1 = deepcopy(checker_message.get_message())
    message2 = deepcopy(checker_message.get_message())

    assert message1["campaign_id"] == message2["campaign_id"]
    assert message1["message_id"] == message2["message_id"]


def test_get_message_as_json(checker_message):
    message = checker_message.get_message()
    message_json = checker_message.get_message_as_json()

    assert message == json.loads(message_json)


def test_message_matches_checker_message_with_not_relevant_field_modification(checker_message):
    message = deepcopy(checker_message.get_message())
    message["baz"] = 1

    assert checker_message.matches_message_dict(message)


def test_message_does_not_match_checker_message_with_relevant_field_modification(checker_message):
    message = deepcopy(checker_message.get_message())
    message["customer_id"] = 1

    assert not checker_message.matches_message_dict(message)


def test_get_unique_fields_returns_unique_keys_with_values():
    with patch("random.randint", side_effect=[8, 9]):
        message = CheckerMessage({
            "customer_id": 0,
            "campaign_id": 0,
            "message_id": 0,
            "event_time": ""
        }, randomized_fields=("campaign_id", "message_id"))
        expected_output = {"customer_id": 123, "campaign_id": 8, "message_id": 9}

        assert expected_output == message.get_unique_fields()


def test_get_unique_fields_returns_unique_keys_with_values_if_randomized_fields_are_different():
    with patch("random.randint", side_effect=[8, 9]) as randint_mock:
        message = CheckerMessage(
            message_template='{"customer_id":0,"unique_id_1":0,"unique_id_2":0,"event_time":""}',
            randomized_fields=("unique_id_1", "unique_id_2"))
        message.get_message()
        expected_output = {"customer_id": 123, "unique_id_1": 8, "unique_id_2": 9}
        mock_call = call(10e5, 10e7)
        randint_mock.assert_has_calls([mock_call, mock_call])
        assert expected_output == message.get_unique_fields()


def test_get_unique_fields_returns_id_field_dynamically():
    with patch('random.randint', side_effect=[8, 9]) as randint_mock:
        message = CheckerMessage(
            message_template='{"this_is_a_very_unique_field":0,"unique_id_1":0,"unique_id_2":0,"event_time":""}',
            randomized_fields=("unique_id_1", "unique_id_2"),
            id_field="this_is_a_very_unique_field")
        message.get_message()
        expected_output = {"this_is_a_very_unique_field": 123, "unique_id_1": 8, "unique_id_2": 9}
        mock_call = call(10e5, 10e7)
        randint_mock.assert_has_calls([mock_call, mock_call])
        assert expected_output == message.get_unique_fields()


def test_clone_returns_new_message():
    original_message = CheckerMessage(
        message_template=
        """{
            "customer_id": 0,
            "event_time": "0",
            "message_id": 0,
            "campaign_id": 0,
            "link_id": 0
    }""",
        randomized_fields=("campaign_id", "message_id", "link_id")
    )
    cloned_message = original_message.clone()

    assert original_message is not cloned_message


def test_get_bt_key_generatesBigtableKeyAsExpected():
    message = CheckerMessage(
        message_template='{"customer_id": 0, "campaign_id": 0, "message_id": 0, "event_time": ""}',
        randomized_fields=("campaign_id", "message_id"))

    assert "{}_{}_{}".format(message.get_message()["customer_id"], message.get_message()["campaign_id"],
                             message.get_message()["message_id"]) == message.get_bigtable_key()


def test_get_bt_key_generatesCorrectBigtableKeyWithoutMessageRandomization():
    message = CheckerMessage(
        message_template='{"customer_id": 0, "campaign_id": 0, "message_id": 0, "event_time": ""}',
        randomized_fields=("campaign_id", "message_id"))

    assert "{}_{}_{}".format(message.get_message()["customer_id"], message.get_message()["campaign_id"],
                             message.get_message()["message_id"]) == message.get_bigtable_key()


def test_get_bt_key_bigTableKeyFactoryIsGiven_generatesKeyBasedOnTheFactory():
    message = CheckerMessage(
        message_template='{"customer_id": 0, "campaign_id": 0, "message_id": 0, "event_time": ""}',
        randomized_fields=("campaign_id", "message_id"),
        bigtable_key_factory=lambda v: "{}_event".format(v["customer_id"]))

    expected = "{}_event".format(message.get_message()["customer_id"])
    assert expected == message.get_bigtable_key()


def test_init_useDictAsTemplateInsteadOfJsonString():
    utcnow = datetime.utcnow().replace(microsecond=0)
    checker_message = CheckerMessage({"customer_id": 0, "campaign_id": 0, "message_id": 0, "event_time": "0"})
    message = checker_message.get_message()

    assert message["customer_id"] == 123
    assert 10e5 <= message["campaign_id"] <= 10e7
    assert 10e5 <= message["message_id"] <= 10e7
    assert utcnow <= datetime.strptime(message["event_time"], '%Y-%m-%dT%H:%M:%SZ')


def test_init_modifyingMessageTemplateAfterCreation_doesNotAffectCheckerMessage():
    template = {"customer_id": 0, "campaign_id": 0, "message_id": 0, "event_time": "0", "extra": 1}
    checker_message = CheckerMessage(template)
    template["extra"] = 2
    assert checker_message["extra"] == 1


def test_create_eventTimeFieldIsSetToGivenValue():
    expected_event_time = datetime(2017, 12, 12, 10, 0, 0)
    msg = CheckerMessage(message_template='{"customer_id":0,"campaign_id":0,"message_id":0,"event_time":""}',
                         update_event_time_to=expected_event_time
                         )
    assert datetime.strftime(expected_event_time, "%Y-%m-%dT%H:%M:%SZ") == msg["event_time"]


def test_eq_allPropertiesMatch_returnsTrue():
    event1 = CheckerMessage(
        {
            "field1": 1,
            "field2": 2,
            "event_time_field1": 3
        },
        id_field="field2",
        randomized_fields=(),
        event_time_field="event_time_field1"
    )

    event2 = CheckerMessage(
        {
            "field1": 1,
            "field2": 2,
            "event_time_field1": 3
        },
        id_field="field2",
        randomized_fields=(),
        event_time_field="event_time_field1"
    )

    assert event1 == event2


def test_eq_notAllPropertiesMatch_returnsFalse():
    event1 = CheckerMessage(
        {
            "field1": 1,
            "field2": 2,
            "event_time_field1": 3
        },
        id_field="field2",
        randomized_fields=(),
        event_time_field="event_time_field1"
    )

    event2 = CheckerMessage(
        {
            "field1": 1,
            "field2": 2,
            "event_time_field1": 3
        },
        id_field="field1",
        randomized_fields=("event_time_field1",),
        event_time_field="event_time_field1"
    )

    assert event1 != event2
