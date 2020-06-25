import email
import logging
import sys
try:
    from email import utils
except ImportError:
    import rfc822 as utils

from django.core.management.base import BaseCommand

from django.apps import apps


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    args = "<[Mailbox Name (optional)]>"
    help = "Receive incoming mail via stdin"

    def add_arguments(self, parser):
        parser.add_argument(
            'mailbox_name',
            nargs='?',
            help="The name of the mailbox that will receive the message"
        )
        parser.add_argument(
            'mailbox_model_name',
            help="The name of the inherited model of mailbox that will receive the message"
        )

    def handle(self, mailbox_name, mailbox_model_name=None, *args, **options):
        mailbox_model = apps.get_model(mailbox_model_name)
        message = email.message_from_string(sys.stdin.read())
        if message:
            if mailbox_name:
                mailbox = self.get_mailbox_by_name(mailbox_name, mailbox_model)
            else:
                mailbox = self.get_mailbox_for_message(message)
            mailbox.process_incoming_message(message)
            logger.info(
                "Message received from %s",
                message['from']
            )
        else:
            logger.warning("Message not processable.")

    def get_mailbox_by_name(self, name, mailbox_model_name):
        mailbox, created = mailbox_model_name.objects.get_or_create(
            name=name,
        )
        return mailbox

    def get_mailbox_for_message(self, message):
        email_address = utils.parseaddr(message['to'])[1][0:255]
        return self.get_mailbox_by_name(email_address)
