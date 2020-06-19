import logging

from django.db import IntegrityError
from django.utils import timezone

from huscy.subjects.models import Inactivity, Subject

logger = logging.getLogger('huscy.subjects')


def create_subject(contact, guardians):
    try:
        subject = Subject.objects.create(
            contact=contact,
        )
    except IntegrityError:
        # try again if generated uuid is already taken
        return create_subject(contact, guardians)

    logger.info('Subject id:%d has been created', subject.id)

    for guardian in guardians:
        subject.guardians.add(guardian)

    return subject


def set_inactivity(subject, until=None):
    if until and until < timezone.now().date():
        raise ValueError(f'Until ({until}) cannot be in the past.')

    inactivity, created = Inactivity.objects.get_or_create(subject=subject,
                                                           defaults={'until': until})
    if not created:
        inactivity.until = until
        inactivity.save()

    return inactivity


def unset_inactivity(subject):
    subject.inactivity_set.all().delete()
