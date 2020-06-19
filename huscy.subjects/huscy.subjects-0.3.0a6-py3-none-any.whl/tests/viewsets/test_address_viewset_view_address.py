from operator import itemgetter

from rest_framework.reverse import reverse

from huscy.subjects.serializers import AddressSerializer

from utils.asserts import assert_status_forbidden, assert_status_not_allowed, \
                          assert_status_ok, debug_response
from utils.helper import add_permission


def test_admin_cannot_list_addresses(admin_client, address):
    assert_status_not_allowed(list_addresses(admin_client))


def test_user_cannot_list_addresses(client, user, address):
    add_permission(user, 'view_address')
    assert_status_not_allowed(list_addresses(client))


def test_user_without_permission_cannot_list_addresses(client):
    assert_status_not_allowed(list_addresses(client))


def test_admin_cannot_retrieve_address(admin_client, address):
    assert_status_not_allowed(retrieve_address(admin_client, address))


def test_user_cannot_retrieve_address(client, user, address):
    add_permission(user, 'view_address')
    assert_status_not_allowed(retrieve_address(client, address))


def test_user_without_permission_cannot_retrieve_address(client, address):
    assert_status_not_allowed(retrieve_address(client, address))


def test_admin_can_get_address_from_contact(admin_client, contact, address):
    response = admin_client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk)))
    assert_status_ok(response)
    assert_address_inside_contact_response(address, response)


def test_user_without_permissions_cannot_get_addresses_from_contact(client, contact):
    response = client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk)))
    assert_status_forbidden(response)


def test_user_can_get_address_from_contact(client, user, contact, address):
    add_permission(user, 'view_contact')
    response = client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk)))
    assert_status_ok(response)
    assert_address_inside_contact_response(address, response)


def test_anonymous_cannot_get_phonenumbers(client, contact, address):
    client.logout()
    assert_status_forbidden(client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk))))


def assert_address_inside_contact_response(address, response):
    dbg_msg = debug_response(response)
    assert 'addresses' in response.json(), dbg_msg

    expected = sorted(AddressSerializer([address], many=True).data, key=itemgetter('id'))

    assert sorted(response.json()['addresses'], key=itemgetter('id')) == expected, dbg_msg


def list_addresses(client):
    return client.get(reverse('address-list'))


def retrieve_address(client, address):
    return client.get(reverse('address-detail', kwargs=dict(pk=address.pk)))
