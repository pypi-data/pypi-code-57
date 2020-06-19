from datetime import timedelta

import pytest

from django.contrib.auth.models import Permission
from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


DAY_AFTER_TOMORROW = timezone.now().date() + timedelta(days=2)


def test_admin_user_can_set_inactivity(admin_client, subject):
    response = set_inactivity(admin_client, subject)

    assert response.status_code == HTTP_200_OK


def test_user_with_permissions_can_set_inactivity(client, user, subject):
    update_permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(update_permission)

    response = set_inactivity(client, subject)

    assert response.status_code == HTTP_200_OK


def test_user_without_permissions_cannot_set_inactivity(client, subject):
    response = set_inactivity(client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_set_inactivity(anonymous_client, subject):
    response = set_inactivity(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_inactivity_created(admin_client, subject):
    assert not subject.inactivity_set.exists()

    set_inactivity(admin_client, subject)

    inactivity = subject.inactivity_set.get()

    assert inactivity.subject == subject
    assert inactivity.until == DAY_AFTER_TOMORROW


def test_inactivity_updated(admin_client, inactivity):
    assert inactivity.until is None

    set_inactivity(admin_client, inactivity.subject)

    inactivity.refresh_from_db()

    assert inactivity.until == DAY_AFTER_TOMORROW


def test_set_inactivity_with_invalid_date(admin_client, subject):
    yesterday = timezone.now().date() - timedelta(days=1)

    response = set_inactivity(admin_client, subject, until=yesterday)

    assert response.status_code == HTTP_400_BAD_REQUEST


def set_inactivity(client, subject, until=DAY_AFTER_TOMORROW):
    return client.post(
        reverse('subject-inactivity', kwargs=dict(pk=subject.pk)),
        data=dict(subject=subject.pk, until=until)
    )
