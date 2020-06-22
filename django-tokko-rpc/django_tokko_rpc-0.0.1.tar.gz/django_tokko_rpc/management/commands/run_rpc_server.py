import logging

from django.core.management.base import BaseCommand

from tokko_rpc.server import build_server as build_rpc_server


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start TokkoRPC server. '

    def handle(self, *args, **options):
        log.debug("Building server ...")
        server = build_rpc_server()
        log.info("Sever successfully built")
        server.serve_forever()
        log.info("Bye!")
