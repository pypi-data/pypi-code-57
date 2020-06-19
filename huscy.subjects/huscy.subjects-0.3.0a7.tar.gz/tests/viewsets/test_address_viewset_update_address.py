from model_bakery import baker
from rest_framework.reverse import reverse

from utils.asserts import assert_status_forbidden, assert_status_ok
from utils.helper import add_permission


def test_admin_can_update_address(admin_client, address):
    response = update_address(admin_client, address)

    assert_status_ok(response)
    assert response.json()['city'] != address.city


def test_user_without_permissions_cannot_update_address(client, address):
    assert_status_forbidden(update_address(client, address))


def test_user_with_permissions_can_update_address(client, address, user):
    add_permission(user, 'change_address')

    response = update_address(client, address)

    assert_status_ok(response)
    assert response.json()['city'] != address.city


def test_anonymous_cannot_update_address(client, address):
    client.logout()
    assert_status_forbidden(update_address(client, address))


def update_address(client, address):
    new_address = baker.prepare('subjects.Address', contact=address.contact)
    data = dict(
        city=new_address.city,
        country=str(new_address.country),
        zip_code=new_address.zip_code,
        street=new_address.street,
        contact=new_address.contact.pk,
    )
    return client.put(reverse('address-detail', kwargs=dict(pk=address.pk)), data=data)
