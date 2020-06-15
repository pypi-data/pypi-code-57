import socket

import click

from src.config.global_config import compile_ip, compile_host_mame


def net_test(host, port):
    try:
        remote_ip = host
        if compile_host_mame.match(host):
            remote_ip = socket.gethostbyname(host)
        elif compile_ip.match(host):
            remote_ip = socket.gethostbyaddr(host)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((remote_ip, port))
        click.echo("{}的{}端口连接成功!".format(host, port))
        sock.close()
    except socket.error as e:
        click.echo("{}的{}端口连接失败,原因:{}".format(host, port, e))
