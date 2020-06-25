import click
from litenet.server import LiteNetServer
from litenet.client import LiteNetClient


@click.group()
def cli():
    pass


@click.argument()
@click.option("-h", "--host", required=True, type=str, help="The ip to run the server on. (Must have access to it.)")
@click.option("-p", "--port", default=5050, type=int, help="The port to run the server on. (Must be a valid port.)")
@click.option("--header", default=64, type=int, help="The size of the server message header. (Adjust as needed.)")
def server(host, port, header):
    litenet = LiteNetServer(host, port, header=header)
    litenet.start()

@click.argument()
@click.option("-h", "--host", required=True, type=str, help="The ip the server's running on. (Must have access to it.)")
@click.option("-p", "--port", default=5050, type=int, help="The port the server's running on. (Must be a valid port.)")
@click.option("--header", default=64, type=int, help="The size of the server message header. (Must match the server's.)")
def client(host, port, header):
    client = LiteNetClient(host, port, header)
    client.start()


cli.add_argument(server)
cli.add_argument(client)
