from model_bakery import baker
from rest_framework.reverse import reverse

from utils.asserts import assert_status_created, assert_status_forbidden
from utils.helper import add_permission


def test_admin_can_create_address(admin_client):
    assert_status_created(create_address(admin_client))


def test_anonymous_cannot_create_address(client):
    client.logout()
    assert_status_forbidden(create_address(client))


def test_user_with_permissions_can_create_address(client, user):
    add_permission(user, 'add_address')
    assert_status_created(create_address(client))


def test_user_without_permissions_cannot_create_address(client):
    assert_status_forbidden(create_address(client))


def create_address(client):
    contact = baker.make('subjects.Contact')
    address = baker.prepare('subjects.Address', contact=contact)
    data = dict(
        city=address.city,
        country=str(address.country),
        zip_code=address.zip_code,
        street=address.street,
        contact=address.contact.pk,
    )
    return client.post(reverse('address-list'), data=data)
