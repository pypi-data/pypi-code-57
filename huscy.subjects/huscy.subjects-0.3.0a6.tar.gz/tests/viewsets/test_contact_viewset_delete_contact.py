from rest_framework.reverse import reverse

from huscy.subjects.models import Address, Phone

from utils.asserts import assert_status_forbidden, assert_status_no_content
from utils.helper import add_permission


def test_admin_can_delete_contact(admin_client, contact):
    assert_status_no_content(delete_contact(admin_client, contact))
    assert_all_contact_phones_have_gone(contact)
    assert_contact_address_has_gone(contact)


def test_user_with_permission_can_delete_contact(client, user, contact):
    add_permission(user, 'delete_contact')
    assert_status_no_content(delete_contact(client, contact))
    assert_all_contact_phones_have_gone(contact)
    assert_contact_address_has_gone(contact)


def test_user_without_permission_cannot_delete_contact(client, contact):
    assert_status_forbidden(delete_contact(client, contact))


def test_anonymous_cannot_delete_contact(client, contact):
    client.logout()
    assert_status_forbidden(delete_contact(client, contact))


def delete_contact(client, contact):
    return client.delete(reverse('contact-detail', kwargs=dict(pk=contact.pk)))


def assert_all_contact_phones_have_gone(contact):
    assert not Phone.objects.filter(contact=contact).exists()


def assert_contact_address_has_gone(contact):
    assert not Address.objects.filter(contact=contact.pk).exists()
