import logging

from django.core.management.base import BaseCommand

from django.apps import apps

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'mailbox_model_name',
            help="The name of the inherited model of mailbox that will receive the message"
        )

    def handle(self, mailbox_model_name, *args, **options):
        mailbox_model = apps.get_model(mailbox_model_name)
        mailboxes = mailbox_model.active_mailboxes.all()
        if args:
            mailboxes = mailboxes.filter(
                name=' '.join(args)
            )
        for mailbox in mailboxes:
            logger.info(
                'Gathering messages for %s',
                mailbox.name
            )
            messages = mailbox.get_new_mail()
            for message in messages:
                logger.info(
                    'Received %s (from %s)',
                    message.subject,
                    message.from_address
                )
