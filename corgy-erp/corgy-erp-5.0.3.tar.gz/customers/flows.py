from viewflow import frontend
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from viewflow.flow import Start, Handler, View, If, End
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.base import this, Flow
from .models import SubscriptionProcess
from .models import UnsubscriptionProcess

@frontend.register
class SubscriptionFlow(Flow):
    process_class = SubscriptionProcess
    process_title = _('Ügyfél beléptetés')
    process_description = _('Új ügyfél regisztrációja és beléptetése.')

    start = (
        Start(CreateProcessView, fields=[
            'customer'
        ]).Permission(auto_create=True).Available(lambda user: user.pk is not None).Next(this.end)
    )

    end = End()

@frontend.register
class UnsubscriptionFlow(Flow):
    process_class = UnsubscriptionProcess
    process_title = _('Ügyfél kiléptetés')
    process_description = _('Meglévő ügyfél megszüntetése.')

    start = (
        Start(CreateProcessView, fields=[
            'customer'
        ]).Permission(auto_create=True).Available(lambda user: user.pk is not None).Next(this.end)
    )

    end = End()