from rest_framework.reverse import reverse

from utils.asserts import assert_status_created, assert_status_forbidden
from utils.helper import add_permission


def test_admin_can_create_subject(admin_client, contact):
    assert_status_created(create_subject(admin_client, contact))


def test_anonymous_cannot_create_subject(client, contact):
    client.logout()
    assert_status_forbidden(create_subject(client, contact))


def test_user_with_permissions_can_create_subject(client, user, contact):
    add_permission(user, 'add_subject')
    assert_status_created(create_subject(client, contact))


def test_user_without_permissions_cannot_create_subject(client, contact):
    assert_status_forbidden(create_subject(client, contact))


def create_subject(client, contact):
    data = dict(
        pseudonym='foo',
        contact=contact.pk,
    )
    return client.post(reverse('subject-list'), data=data)
