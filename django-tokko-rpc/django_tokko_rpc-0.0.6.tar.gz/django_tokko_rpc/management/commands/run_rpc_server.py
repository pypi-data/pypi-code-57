import logging

from django.core.management.base import BaseCommand

from tokko_rpc.server import build_server as build_rpc_server


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start TokkoRPC server. '

    def add_arguments(self, parser):
        parser.add_argument("--port", type=int, default=9142, help="Server <int:PORT>")
        parser.add_argument("--host", type=str, default="localhost", help="Server <str:HOST>")
        parser.add_argument("--use-ssl", action="store_true", help="Use SSL")

    def handle(self, *args, **options):
        log.debug("Building server ...")
        server = build_rpc_server(
            port=options["port"],
            host=options["host"]
        )
        log.info("Sever successfully built")
        server.serve_forever()
        log.info("Bye!")
