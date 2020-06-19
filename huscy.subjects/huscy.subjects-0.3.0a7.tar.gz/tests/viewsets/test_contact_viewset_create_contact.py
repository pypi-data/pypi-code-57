from model_bakery import baker
from rest_framework.reverse import reverse

from utils.asserts import assert_status_created, assert_status_forbidden
from utils.helper import add_permission


def test_admin_can_create_contact(admin_client):
    assert_status_created(create_contact(admin_client))


def test_user_without_permissions_cannot_create_contact(client):
    assert_status_forbidden(create_contact(client))


def test_user_with_permissions_can_create_contact(client, user):
    add_permission(user, 'add_contact')
    assert_status_created(create_contact(client))


def test_anonymous_cannot_create_contact(client):
    client.logout()
    assert_status_forbidden(create_contact(client))


def create_contact(client):
    contact = baker.prepare('subjects.Contact', display_name='Bar')
    data = dict(
        first_name=contact.first_name,
        last_name=contact.last_name,
        display_name=contact.display_name,
        gender=contact.gender,
        date_of_birth=contact.date_of_birth,
        email=contact.email,
    )
    return client.post(reverse('contact-list'), data=data, format='json')
