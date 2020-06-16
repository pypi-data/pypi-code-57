from viewflow import frontend
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from viewflow.base import this, Flow
from .models import SubscriptionProcess
from .models import UnsubscriptionProcess

@frontend.register
class SubscriptionFlow(Flow):
    process_class = SubscriptionProcess
    process_title = _('Ügyfél beléptetés')
    process_description = _('Új ügyfél regisztrációja és beléptetése.')

@frontend.register
class UnsubscriptionFlow(Flow):
    process_class = UnsubscriptionProcess
    process_title = _('Ügyfél kiléptetés')
    process_description = _('Meglévő ügyfél megszüntetése.')