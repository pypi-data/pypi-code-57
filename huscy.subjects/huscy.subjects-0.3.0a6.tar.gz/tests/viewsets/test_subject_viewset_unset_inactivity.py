import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_unset_inactivity(admin_client, subject, inactivity):
    response = unset_inactivity(admin_client, subject)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permissions_can_unset_inactivity(client, user, subject, inactivity):
    update_permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(update_permission)

    response = unset_inactivity(client, subject)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permissions_cannot_unset_inactivity(client, subject, inactivity):
    response = unset_inactivity(client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_unset_inactivity(anonymous_client, subject, inactivity):
    response = unset_inactivity(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_inactivity_deleted(admin_client, subject, inactivity):
    assert subject.inactivity_set.exists()

    unset_inactivity(admin_client, subject)

    assert not subject.inactivity_set.exists()


def unset_inactivity(client, subject):
    return client.delete(reverse('subject-inactivity', kwargs=dict(pk=subject.pk)))
