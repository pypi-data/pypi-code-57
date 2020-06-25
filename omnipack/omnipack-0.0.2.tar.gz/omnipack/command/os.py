import click
import omnipack

# -------- process -------- #


@click.command(help='Kill process with the same command')
@click.argument('cmd', type=str)
def kill_multiprocess(cmd):
    omnipack.kill_multiprocess(cmd)


@click.command(help='Kill process with pid')
@click.argument('pid', type=int)
def kill_process(pid):
    omnipack.kill_process(int(pid))


# -------- network -------- #

@click.command(help='Kill port connection')
@click.argument('port', type=int)
def kill_port(port):
    omnipack.kill_port(port)


@click.command(help='Check port availability')
@click.argument('port', type=int)
def is_port_available(port):
    avai = omnipack.is_port_available(port)
    print(avai)


@click.command(help='Get host of the machine')
def get_host():
    host = omnipack.get_host()
    print(host)


@click.command(help='Get hostname')
def get_hostname():
    hostname = omnipack.get_hostname()
    print(hostname)
