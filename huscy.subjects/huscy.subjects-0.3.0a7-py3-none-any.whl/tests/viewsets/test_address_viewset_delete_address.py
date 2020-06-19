from rest_framework.reverse import reverse

from utils.asserts import assert_status_forbidden, assert_status_no_content
from utils.helper import add_permission


def test_admin_can_delete_address(admin_client, address):
    assert_status_no_content(delete_address(admin_client, address))


def test_user_with_permission_can_delete_address(client, user, address):
    add_permission(user, 'delete_address')
    assert_status_no_content(delete_address(client, address))


def test_user_without_permission_cannot_delete_address(client, address):
    assert_status_forbidden(delete_address(client, address))


def test_anonymous_cannot_delete_address(client, address):
    client.logout()
    assert_status_forbidden(delete_address(client, address))


def delete_address(client, address):
    return client.delete(reverse('address-detail', kwargs=dict(pk=address.pk)))
