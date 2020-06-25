from mailbox import MMDF
from django_mailbox_abstract.transports.generic import GenericFileMailbox


class MMDFTransport(GenericFileMailbox):
    _variant = MMDF
