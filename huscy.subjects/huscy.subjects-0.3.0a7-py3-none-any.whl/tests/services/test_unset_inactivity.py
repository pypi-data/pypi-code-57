import pytest

from huscy.subjects.services import unset_inactivity

pytestmark = pytest.mark.django_db


def test_unset_inactivity(inactivity, subject):
    assert subject.is_active is False

    unset_inactivity(subject)

    assert subject.is_active is True


def test_unset_inactivity_without_inactivity_reference(subject):
    assert subject.is_active is True

    unset_inactivity(subject)

    assert subject.is_active is True
