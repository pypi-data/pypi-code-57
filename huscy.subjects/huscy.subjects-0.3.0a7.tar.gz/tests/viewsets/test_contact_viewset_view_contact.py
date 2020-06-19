import pytest

from rest_framework.reverse import reverse

from huscy.subjects.serializers import ContactSerializer

from utils.asserts import assert_status_forbidden, assert_status_ok
from utils.helper import add_permission


# all tests in this suite will require db access
pytestmark = pytest.mark.django_db


def test_admin_user_can_list_contacts(admin_client):
    response = list_contacts(admin_client)
    assert_status_ok(response)


def test_user_can_list_contacts(client, user):
    add_permission(user, 'view_contact')
    assert_status_ok(list_contacts(client))


def test_user_without_permission_cannot_list_contacts(client, user):
    assert_status_forbidden(list_contacts(client))


def test_anonymous_cannot_list_contacts(client):
    client.logout()
    assert_status_forbidden(list_contacts(client))


def test_admin_user_can_retrieve_contact(contact, admin_client):
    response = retrieve_contact(admin_client, contact)
    assert response.json() == ContactSerializer(contact).data
    assert_status_ok(response)


def test_user_can_retrieve_contact(contact, client, user):
    add_permission(user, 'view_contact')
    response = retrieve_contact(client, contact)
    assert response.json() == ContactSerializer(contact).data
    assert_status_ok(response)


def test_user_without_permission_cannot_retrieve_contacts(contact, client, user):
    assert_status_forbidden(retrieve_contact(client, contact))


def test_anonymous_cannot_retrieve_contact(client, contact):
    client.logout()
    assert_status_forbidden(retrieve_contact(client, contact))


def list_contacts(client):
    return client.get(reverse('contact-list'))


def retrieve_contact(client, contact):
    return client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk)))
