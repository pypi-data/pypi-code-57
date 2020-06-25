from mailbox import MH
from django_mailbox_abstract.transports.generic import GenericFileMailbox


class MHTransport(GenericFileMailbox):
    _variant = MH
