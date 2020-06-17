from django.conf import settings

from register.forms.personal import PersonalInformationForm
from register.models.attendee import Attendee
from register.models.queue import Queue
from register.views.core import RegisterStep


class PersonalInformationView(RegisterStep):
    title = 'Personal Information'
    form_class = PersonalInformationForm

    def get_initial(self):
        user = self.request.user
        initial = {}

        attendee = user.attendee
        for field in attendee._meta.get_fields():
            if field.is_relation:
                continue
            initial[field.name] = getattr(attendee, field.name)

        return initial

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data

        user.attendee  # We should never be creating, here
        user.attendee, created = Attendee.objects.update_or_create(
            user=user, defaults=data)

        if form.cleaned_data['pgp_fingerprints'] and settings.ISSUE_KSP_ID:
            queue, created = Queue.objects.get_or_create(
                name='PGP Keysigning')
            queue.slots.get_or_create(attendee=user.attendee)

        return super().form_valid(form)
