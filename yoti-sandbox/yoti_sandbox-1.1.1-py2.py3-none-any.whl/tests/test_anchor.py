from datetime import datetime, timezone

from yoti_python_sandbox.anchor import SandboxAnchor

import pytest


def test_builder_should_set_sub_type():
    sub_type = "some_sub_type"
    anchor = SandboxAnchor.builder().with_sub_type(sub_type).build()

    assert sub_type == anchor.sub_type


def test_builder_should_set_value():
    some_value = "some_value"
    anchor = SandboxAnchor.builder().with_value(some_value).build()

    assert some_value == anchor.value


def test_builder_should_set_anchor_type():
    anchor_type = "some_type"
    anchor = SandboxAnchor.builder().with_type(anchor_type).build()

    assert anchor_type == anchor.anchor_type


@pytest.mark.parametrize(
    "timestamp, expected_unix_microsecond_equivalent",
    [
        (
            datetime(1960, 1, 4, 0, 0, 0, 000000, tzinfo=timezone.utc),
            int(-315360000000000),
        ),
        (
            datetime(2020, 3, 23, 12, 29, 49, 456789, tzinfo=timezone.utc),
            int(1584966589456789),
        ),
        (
            datetime(2050, 1, 1, 1, 1, 1, 456789, tzinfo=timezone.utc),
            int(2524611661456789),
        ),
    ],
)
def test_builder_should_set_timestamp(timestamp, expected_unix_microsecond_equivalent):
    anchor = SandboxAnchor.builder().with_timestamp(timestamp).build()

    assert anchor.timestamp == expected_unix_microsecond_equivalent


@pytest.mark.parametrize(
    "timestamp", ["2006-11-02T15:04:05.010Z", "2006-11-02T15:04:05.010", -1, 123456789]
)
def test_builder_should_throw_error_for_invalid_timestamp(timestamp):
    with pytest.raises(TypeError):
        SandboxAnchor.builder().with_timestamp(timestamp).build()
