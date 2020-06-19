import pytest

from rest_framework.reverse import reverse

from utils.asserts import assert_status_forbidden, assert_status_ok
from utils.helper import add_permission

pytestmark = pytest.mark.django_db


def test_admin_can_list_subjects(admin_client, subject):
    assert_status_ok(list_subjects(admin_client))


def test_user_can_list_subjects(client, user, subject):
    add_permission(user, 'view_subject')
    assert_status_ok(list_subjects(client))


def test_user_without_permission_cannot_list_subjects(client):
    assert_status_forbidden(list_subjects(client))


def test_anonymous_user_cannot_list_subjects(anonymous_client):
    assert_status_forbidden(list_subjects(anonymous_client))


def test_admin_can_retrieve_subject(admin_client, subject):
    assert_status_ok(retrieve_subject(admin_client, subject))


def test_user_can_retrieve_subject(client, user, subject):
    add_permission(user, 'view_subject')
    assert_status_ok(retrieve_subject(client, subject))


def test_user_without_permission_cannot_retrieve_subject(client, subject):
    assert_status_forbidden(retrieve_subject(client, subject))


def test_anonymous_cannot_retrive_subject(anonymous_client, subject):
    assert_status_forbidden(retrieve_subject(anonymous_client, subject))


def list_subjects(client):
    return client.get(reverse('subject-list'))


def retrieve_subject(client, subject):
    return client.get(reverse('subject-detail', kwargs=dict(pk=subject.pk)))
