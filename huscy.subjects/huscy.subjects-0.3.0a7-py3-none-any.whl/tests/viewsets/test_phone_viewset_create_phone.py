from model_bakery import baker
from rest_framework.reverse import reverse

from utils.asserts import assert_status_created, assert_status_forbidden
from utils.helper import add_permission


def test_admin_can_create_phone(admin_client):
    contact = baker.make('subjects.Contact')
    response = create_phone(admin_client, baker.prepare('subjects.Phone', contact=contact))
    assert_status_created(response)


def test_anonymous_cannot_create_phone(client):
    client.logout()
    contact = baker.make('subjects.Contact')
    response = create_phone(client, baker.prepare('subjects.Phone', contact=contact))
    assert_status_forbidden(response)


def test_user_with_permissions_can_create_phone(client, user):
    add_permission(user, 'add_phone')
    contact = baker.make('subjects.Contact')
    response = create_phone(client, baker.prepare('subjects.Phone', contact=contact))
    assert_status_created(response)


def test_user_without_permissions_cannot_create_phone(client):
    contact = baker.make('subjects.Contact')
    response = create_phone(client, baker.prepare('subjects.Phone', contact=contact))
    assert_status_forbidden(response)


def create_phone(client, phone):
    data = dict(
        label=phone.label,
        number=phone.number,
        contact=phone.contact.pk,
    )
    return client.post(reverse('phone-list'), data=data)
