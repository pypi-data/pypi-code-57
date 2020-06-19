import pytest
from model_bakery import baker

from huscy.subjects.serializers import ContactSerializer, SubjectSerializer

pytestmark = pytest.mark.django_db


def test_expose_contact_data(subject):
    data = SubjectSerializer(subject).data

    assert 'contact' in data
    assert data['contact'] == ContactSerializer(subject.contact).data


def test_expose_guardians(subject):
    guardians = baker.make('subjects.Contact', _quantity=2)
    subject.guardians.add(*guardians)
    subject.save()

    data = SubjectSerializer(subject).data

    assert 'guardians' in data
    assert data['guardians'] == ContactSerializer(guardians, many=True).data


def test_expose_empty_list_for_guardians_if_no_guardians_assigned(subject):
    data = SubjectSerializer(subject).data

    assert 'guardians' in data
    assert data['guardians'] == []


def test_is_child_is_exposed_as_false(subject):
    data = SubjectSerializer(subject).data

    assert 'is_child' in data
    assert data['is_child'] is False


def test_is_child_is_exposed_as_true(subject):
    baker.make('subjects.Child', subject=subject)

    data = SubjectSerializer(subject).data

    assert 'is_child' in data
    assert data['is_child'] is True


def test_is_patient_is_exposed_as_false(subject):
    data = SubjectSerializer(subject).data

    assert 'is_patient' in data
    assert data['is_patient'] is False


def test_is_patient_is_exposed_as_true(subject):
    baker.make('subjects.Patient', subject=subject)

    data = SubjectSerializer(subject).data

    assert 'is_patient' in data
    assert data['is_patient'] is True
