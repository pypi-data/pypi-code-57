from django.db.models.signals import post_save

from whisperer.events import WhispererEvent, registry
from whisperer.tasks import deliver_event
from whisperer.tests.models import Order
from whisperer.tests.serializers import OrderSerializer


class OrderCreateEvent(WhispererEvent):
    serializer_class = OrderSerializer
    event_type = 'order-created'


registry.register(OrderCreateEvent)


def signal_receiver(instance, created=False, **kwargs):
    if created:
        deliver_event(instance, 'order-created')


post_save.connect(signal_receiver, Order)
