import datetime

import pytest

from huscy.subjects.models import Inactivity
from huscy.subjects.services import set_inactivity

pytestmark = pytest.mark.django_db


@pytest.fixture
def until():
    return datetime.date.today() + datetime.timedelta(days=20)


def test_raise_exception_if_until_is_in_the_past(subject):
    until = datetime.date.today() - datetime.timedelta(days=1)
    with pytest.raises(ValueError) as e:
        set_inactivity(subject, until)

    assert str(e.value) == f'Until ({until}) cannot be in the past.'


def test_set_inactivity_with_specific_end_date(subject, inactivity, until):
    set_inactivity(subject, until)

    inactivity.refresh_from_db()
    assert inactivity.subject == subject
    assert inactivity.until == until


def test_set_inactivity_for_forever(subject, inactivity):
    set_inactivity(subject)

    inactivity.refresh_from_db()
    assert inactivity.subject == subject
    assert inactivity.until is None


def test_create_new_inactivity_if_none_exists(subject, until):
    assert not Inactivity.objects.exists()

    inactivity = set_inactivity(subject, until)

    assert Inactivity.objects.exists()
    assert inactivity.subject == subject
    assert inactivity.until == until
