
import signal
from threading import Event

from kombunicator.ConsumerConfigurator import ConsumerConfigurator
from kombunicator.MessageProducer import MessageProducer
from kombunicator.RPCClient import RPCClient
from kombunicator.RPCServer import RPCServer

_consumer_container = list()


def shutdown_consumers():
    [t.stop() for t in _consumer_container]
    [t.join() for t in _consumer_container]


def _system_signal_handler(signum, frame):
    shutdown_consumers()


signal.signal(signal.SIGINT, _system_signal_handler)
signal.signal(signal.SIGTERM, _system_signal_handler)


def register_message_consumer(config_class):
    """
    Setup and starts a message consumer thread.

    :type config: Instance of kombunicator.ConsumerConfigurator
    """
    # import only intarnally
    from kombunicator.MessageConsumer import MessageConsumer

    config = config_class()
    _ready = Event()

    consumer_direct_params = {
        'connection_parameter': config.connection_parameter,
        'consumer_type': config.consumer_type,
        'binding_keys': config.binding_keys,
        '_thread_ready': _ready
    }

    if config.consumer_type == 'direct':
        consumer_thread = MessageConsumer(**consumer_direct_params)

    elif config.consumer_type == 'topic':
        consumer_thread = MessageConsumer(
            exchange_name=config.exchange_name,
            q_unique=config.q_unique,
            accept=config.accept,
            **consumer_direct_params
        )
    else:
        raise ValueError('consumer_type must be direct or topic.')

    def callback(obj, payload, headers, properties):
        '''obj will be occupied by self'''
        config.message_handler(payload, headers, properties)

    consumer_thread.register_message_handler(callback)
    try:
        consumer_thread.start()
    except RuntimeError:
        raise
    else:
        _consumer_container.append(consumer_thread)
        _ready.wait()
