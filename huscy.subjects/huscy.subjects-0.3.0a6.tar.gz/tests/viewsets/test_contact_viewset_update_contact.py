from rest_framework.reverse import reverse

from huscy.subjects.models import Contact

from utils.asserts import assert_status_forbidden, assert_status_ok
from utils.helper import add_permission


def test_admin_can_update_contact(admin_client, contact):
    response = update_contact(admin_client, contact)

    assert_status_ok(response)
    assert response.json()['email'] != contact.email


def test_user_without_permissions_cannot_update_contact(client, contact):
    assert_status_forbidden(update_contact(client, contact))


def test_user_with_permissions_can_update_contact(client, contact, user):
    add_permission(user, 'change_contact')

    response = update_contact(client, contact)

    assert_status_ok(response)
    assert response.json()['email'] != contact.email


def test_anonymous_cannot_update_contact(client, contact):
    client.logout()
    assert_status_forbidden(update_contact(client, contact))


def update_contact(client, contact):
    data = dict(
        first_name='Klaus',
        last_name='Nadarkan',
        display_name='Sensei Wu',
        gender=Contact.GENDER.get_value('male'),
        date_of_birth='0999-09-09',
        email='wu@never.realm.com',
    )
    return client.put(reverse('contact-detail', kwargs=dict(pk=contact.pk)),
                      data=data, format='json')
