import pytest
from model_bakery import baker

pytestmark = pytest.mark.django_db


def test_is_active_with_inactivity_reference(subject, inactivity):
    assert subject.is_active is False


def test_is_active_without_inactivity_reference(subject):
    assert subject.is_active is True


def test_is_child_with_child_reference(subject):
    baker.make('subjects.Child', subject=subject)

    assert subject.is_child is True


def test_is_child_without_child_reference(subject):
    assert subject.is_child is False


def test_is_patient_with_patient_reference(subject):
    baker.make('subjects.Patient', subject=subject)

    assert subject.is_patient is True


def test_is_patient_without_patient_reference(subject):
    assert subject.is_patient is False
