from mailbox import Babyl
from django_mailbox_abstract.transports.generic import GenericFileMailbox


class BabylTransport(GenericFileMailbox):
    _variant = Babyl
