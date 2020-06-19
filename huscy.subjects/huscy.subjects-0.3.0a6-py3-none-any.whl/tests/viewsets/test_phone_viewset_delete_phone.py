from rest_framework.reverse import reverse

from utils.asserts import assert_status_forbidden, assert_status_no_content
from utils.helper import add_permission


def test_admin_can_delete_phone(admin_client, phone_home):
    assert_status_no_content(delete_phone(admin_client, phone_home))


def test_user_with_permission_can_delete_phone(client, user, phone_home):
    add_permission(user, 'delete_phone')
    assert_status_no_content(delete_phone(client, phone_home))


def test_user_without_permission_cannot_delete_phone(client, phone_home):
    assert_status_forbidden(delete_phone(client, phone_home))


def test_anonymous_cannot_delete_phone(client, phone_home):
    client.logout()
    assert_status_forbidden(delete_phone(client, phone_home))


def delete_phone(client, phone):
    return client.delete(reverse('phone-detail', kwargs=dict(pk=phone.pk)))
