from rest_framework.reverse import reverse

from utils.asserts import assert_status_forbidden, assert_status_no_content
from utils.helper import add_permission


def test_admin_can_delete_subject(admin_client, subject):
    assert_status_no_content(delete_subject(admin_client, subject))


def test_user_with_permission_can_delete_subject(client, user, subject):
    add_permission(user, 'delete_subject')
    assert_status_no_content(delete_subject(client, subject))


def test_user_without_permission_cannot_delete_subject(client, subject):
    assert_status_forbidden(delete_subject(client, subject))


def test_anonymous_cannot_delete_subject(client, subject):
    client.logout()
    assert_status_forbidden(delete_subject(client, subject))


def delete_subject(client, subject):
    return client.delete(reverse('subject-detail', kwargs=dict(pk=subject.pk)))
