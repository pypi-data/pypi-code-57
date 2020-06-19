from rest_framework.reverse import reverse

from huscy.subjects.models import Phone

from utils.asserts import assert_status_forbidden, assert_status_ok
from utils.helper import add_permission


def test_admin_can_update_phone(admin_client, phone_mobile):
    response = update_phone(admin_client, phone_mobile)

    assert_status_ok(response)
    assert response.json()['label'] != phone_mobile.label


def test_user_without_permissions_cannot_update_phone(client, phone_mobile):
    assert_status_forbidden(update_phone(client, phone_mobile))


def test_user_with_permissions_can_update_phone(client, phone_mobile, user):
    add_permission(user, 'change_phone')

    response = update_phone(client, phone_mobile)

    assert_status_ok(response)
    assert response.json()['label'] != phone_mobile.label


def test_anonymous_cannot_update_phone(client, phone_mobile):
    client.logout()
    assert_status_forbidden(update_phone(client, phone_mobile))


def update_phone(client, phone):
    data = dict(
        label=Phone.LABEL.get_value('other'),
        number='+441234567384',
        contact=phone.contact.pk,
    )
    return client.put(reverse('phone-detail', kwargs=dict(pk=phone.pk)),
                      data=data, format='json')
