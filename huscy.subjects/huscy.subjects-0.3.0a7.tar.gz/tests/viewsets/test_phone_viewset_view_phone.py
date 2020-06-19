from rest_framework.reverse import reverse

from huscy.subjects.serializers import PhoneSerializer

from utils.asserts import assert_status_forbidden, assert_status_not_allowed, \
                          assert_status_ok, debug_response
from utils.helper import add_permission


def test_admin_cannot_list_phones(admin_client, phone_mobile):
    assert_status_not_allowed(list_phones(admin_client))


def test_user_cannot_list_phones(client, user, phone_mobile):
    add_permission(user, 'view_phone')
    assert_status_not_allowed(list_phones(client))


def test_user_without_permission_cannot_list_phones(client, user):
    assert_status_not_allowed(list_phones(client))


def test_admin_cannot_retrieve_phone(admin_client, phone_mobile):
    assert_status_not_allowed(retrieve_phone(admin_client, phone_mobile))


def test_user_cannot_retrieve_phone(client, user, phone_mobile):
    add_permission(user, 'view_phone')
    assert_status_not_allowed(retrieve_phone(client, phone_mobile))


def test_user_without_permission_cannot_retrieve_phone(client, phone_mobile):
    assert_status_not_allowed(retrieve_phone(client, phone_mobile))


def test_admin_can_get_phonenumbers_from_contact(admin_client, contact, phone_mobile, phone_home):
    response = admin_client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk)))
    assert_status_ok(response)
    assert_phone_numbers_inside_contact_response([phone_mobile, phone_home], response)


def test_user_without_permissions_cannot_get_phonenumbers_from_contact(client, contact,
                                                                       phone_mobile, phone_home):
    response = client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk)))
    assert_status_forbidden(response)


def test_user_can_get_phonenumbers_from_contact(client, user, contact, phone_mobile, phone_home):
    add_permission(user, 'view_contact')
    response = client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk)))
    assert_status_ok(response)
    assert_phone_numbers_inside_contact_response([phone_mobile, phone_home], response)


def test_anonymous_cannot_get_phonenumbers(client, contact, phone_mobile, phone_home):
    client.logout()
    assert_status_forbidden(client.get(reverse('contact-detail', kwargs=dict(pk=contact.pk))))


def assert_phone_numbers_inside_contact_response(phones, response):
    assert 'phones' in response.json()

    def phone_number(phone):
        return phone['number']

    expected = sorted(PhoneSerializer(phones, many=True).data, key=phone_number)

    assert sorted(response.json()['phones'], key=phone_number) == expected, debug_response(response)


def list_phones(client):
    return client.get(reverse('phone-list'))


def retrieve_phone(client, phone):
    return client.get(reverse('phone-detail', kwargs=dict(pk=phone.pk)))
