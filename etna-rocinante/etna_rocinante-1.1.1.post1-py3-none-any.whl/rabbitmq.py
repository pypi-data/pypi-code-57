"""
Module providing helpers to deal with RabbitMQ
"""

import pika
import ssl


def get_blocking_connection(
        *,
        username: str,
        password: str,
        host: str,
        port: int,
        virtual_host: str = None,
        ssl_context: ssl.SSLContext = None,
) -> pika.BlockingConnection:
    """
    Obtain a blocking connection to RabbitMQ

    :param username:                the username to use to connect to the RabbitMQ server
    :param password:                the password to use to connect to the RabbitMQ server
    :param host:                    the host to connect to
    :param port:                    the port to use when connecting
    :param virtual_host:            the virtual host to use (default is None)
    :param ssl_context:             the SSL context to use (default is None, to use no encryption)
    :return:                        the configured connection
    """

    credentials = pika.PlainCredentials(username, password)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE
    extra_params = {}

    # pika does not accept None as default argument, so we must not pass anything if the argument is not there
    if virtual_host is not None:
        extra_params["virtual_host"] = virtual_host
    if ssl_context is not None:
        extra_params["ssl_options"] = pika.SSLOptions(context)

    params = pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=credentials,
        **extra_params
    )
    return pika.BlockingConnection(params)
