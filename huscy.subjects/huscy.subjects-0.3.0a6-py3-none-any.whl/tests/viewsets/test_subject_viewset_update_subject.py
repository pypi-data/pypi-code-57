from rest_framework.reverse import reverse

from utils.asserts import assert_status_ok, assert_status_forbidden
from utils.helper import add_permission


def test_admin_can_update_subject(admin_client, contact, subject):
    assert_status_ok(update_subject(admin_client, contact, subject))


def test_anonymous_cannot_update_subject(client, contact, subject):
    client.logout()
    assert_status_forbidden(update_subject(client, contact, subject))


def test_user_with_permissions_can_update_subject(client, user, contact, subject):
    add_permission(user, 'change_subject')
    assert_status_ok(update_subject(client, contact, subject))


def test_user_without_permissions_cannot_update_subject(client, contact, subject):
    assert_status_forbidden(update_subject(client, contact, subject))


def update_subject(client, contact, subject):
    data = dict(
        pseudonym='bar',
        contact=contact.pk,
    )
    return client.put(reverse('subject-detail', kwargs=dict(pk=subject.pk)),
                      data=data, format='json')
