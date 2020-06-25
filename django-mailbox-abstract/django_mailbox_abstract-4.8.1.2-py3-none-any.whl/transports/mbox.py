from mailbox import mbox
from django_mailbox_abstract.transports.generic import GenericFileMailbox


class MboxTransport(GenericFileMailbox):
    _variant = mbox
