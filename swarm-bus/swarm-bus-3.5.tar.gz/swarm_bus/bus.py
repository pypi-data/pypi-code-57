"""
Client to connect to AMQP.
"""
import logging
import os
import socket
import time
from datetime import datetime

from kombu import Connection
from kombu import Exchange
from kombu import Queue
from kombu.async.aws.ext import exception

from swarm_bus.patching import fix_libs


logger = logging.getLogger(__name__)


class AMQPConnector(object):
    _exchange = None
    _connection = None
    _queues = {}
    log_namespace = 'Swarm-Bus'

    def __init__(self, uri, transport, queues):
        """
        Ingest AMQP configuration.
        """
        self.uri = uri
        self.transport = transport.copy()
        self.queues = queues.copy()

        self.normalize_transport()
        self.normalize_queues()
        fix_libs(self)

    def connect(self):
        """
        Connects to the AMQP server and setup the exchange.
        """
        self._connection = Connection(
            self.uri,
            transport_options=self.transport
        )
        self._connection.connect()
        logger.debug(
            "[%s] Connected to %s, using '%s' prefix",
            self.log_namespace,
            self._connection.as_uri(),
            self.transport['queue_name_prefix']
        )

        self._exchange = Exchange(
            self.transport['exchange'],
            'topic'
        )
        self._exchange(self._connection).declare()

        self.declare_queues()

    def close(self):
        """
        Close the connection.
        """
        if self._connection:
            self._connection.release()
            self._connection = None
            logger.debug(
                '[%s] Disconnected',
                self.log_namespace
            )

    def get_hostname(self):
        """
        Method for having consistent hostname accross hosts.
        """
        default = socket.gethostname()
        hostname = os.getenv('AMQP_HOSTNAME', default)
        return hostname

    def normalize_transport(self):
        """
        Check and configure transport.
        """
        if 'queue_name_prefix' in self.transport:
            queue_prefix = self.transport['queue_name_prefix']
            queue_prefix = queue_prefix % {
                'hostname': self.get_hostname()
            }
            self.transport['queue_name_prefix'] = queue_prefix
        else:
            self.transport['queue_name_prefix'] = ''

        if 'region' not in self.transport:
            self.transport['region'] = 'eu-west-1'

        if 'exchange' not in self.transport:
            self.transport['exchange'] = 'swarm'

        if 'office_hours' not in self.transport:
            self.transport['office_hours'] = False

        if 'use_priorities' not in self.transport:
            self.transport['use_priorities'] = False

        if 'priorities' not in self.transport:
            self.transport['priorities'] = ['low', 'medium', 'high']

        if 'restore_at_shutdown' not in self.transport:
            self.transport['restore_at_shutdown'] = True

        if 'queue_living' not in self.transport:
            self.transport['queue_living'] = 864000  # 10 days

        if 'queue_sleeping' not in self.transport:
            self.transport['queue_sleeping'] = 0

        if 'queue_visibility' not in self.transport:
            self.transport['queue_visibility'] = 30

        if 'queue_waiting' not in self.transport:
            self.transport['queue_waiting'] = 10

    def normalize_queues(self):
        """
        Check and configure queues.
        """
        for queue_name, queue_attrs in self.queues.items():
            if 'route' not in queue_attrs:
                queue_attrs['route'] = queue_name.replace('_', '.').lower()
            if 'living' not in queue_attrs:
                queue_attrs['living'] = self.transport['queue_living']
            if 'sleep' not in queue_attrs:
                queue_attrs['sleep'] = self.transport['queue_sleeping']
            if 'visibility' not in queue_attrs:
                queue_attrs['visibility'] = self.transport['queue_visibility']
            if 'wait' not in queue_attrs:
                queue_attrs['wait'] = self.transport['queue_waiting']

    def declare_queues(self):
        """
        Declare all queues with routing keys.
        """
        suffixes = ['']
        if self.transport['use_priorities']:
            suffixes = self.transport['priorities']

        for queue_name, queue_attrs in self.queues.items():
            if queue_name in self._queues:
                continue
            routing_key = queue_attrs['route']
            for suffix in suffixes:
                if suffix:
                    queue_name_final = '%s-%s' % (queue_name, suffix)
                    routing_key_final = '%s.%s' % (routing_key, suffix)
                else:
                    queue_name_final = queue_name
                    routing_key_final = routing_key

                queue = Queue(
                    queue_name_final,
                    exchange=self._exchange,
                    routing_key=routing_key_final
                )
                queue_connected = queue(self._connection)
                queue_connected.declare()
                self._queues.setdefault(queue_name, [])
                self._queues[queue_name].append(queue_connected)
                logger.debug(
                    "[%s] Queue '%s' declared via '%s'",
                    self.log_namespace,
                    queue_name_final,
                    routing_key_final
                )

    def register_queue(self, queue_name, queue_attrs={}):
        """
        Register a new queue.
        """
        if queue_name not in self.queues:
            self.queues[queue_name] = queue_attrs.copy()
            self.normalize_queues()
            if self._connection:
                self.declare_queues()


class AMQPContextManager(object):
    """
    Context Manager features for AMQP.
    """
    def __del__(self):
        """
        Close the connection when garbage collected.
        """
        self.close()

    def __enter__(self):
        """
        Context manager establishing connection.
        """
        if self._connection is None:
            self.connect()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """
        Context manager closing connection.
        """
        self.close()


class AMQPQueueManager(object):
    """
    Manager for queues.

    Use directly boto objects, because Kombu is bugged on delete.
    """

    @property
    def cache_queues(self):
        """
        Return a list of all Queues.
        """
        if self._connection:
            return self._connection._transport.channels[0]._queue_cache

        return {}

    def list_queues(self, prefix=''):
        """
        List all queues with details.
        """
        if prefix:
            prefix = '%s%s' % (
                self.transport['queue_name_prefix'],
                prefix
            )
        queues = {}

        for key, queue in self.cache_queues.items():
            if prefix and not key.startswith(prefix):
                continue
            try:
                queues[key] = queue.get_attributes()
            except exception.SQSError:
                pass

        return queues

    def purge_queue(self, queue_name, priority=''):
        """
        Purge a queue.
        """
        queue_name = '%s%s-%s' % (
            self.transport['queue_name_prefix'],
            queue_name,
            priority
        )
        if not priority:
            queue_name = queue_name[:-1]

        try:
            self.cache_queues[queue_name].purge()
            logger.info(
                "[%s] Queue '%s' is now purged",
                self.log_namespace,
                queue_name
            )
        except KeyError:
            logger.error(
                "[%s] Queue '%s' cannot be purged, does not exist",
                self.log_namespace,
                queue_name
            )
        except exception.SQSError:
            logger.error(
                "[%s] Queue '%s' cannot be purged, "
                "already done within the last minute",
                self.log_namespace,
                queue_name
            )

    def delete_queue(self, queue_name, priority=''):
        """
        Delete a queue.
        """
        queue_name = '%s%s-%s' % (
            self.transport['queue_name_prefix'],
            queue_name,
            priority
        )
        if not priority:
            queue_name = queue_name[:-1]

        try:
            self.cache_queues[queue_name].delete()
            logger.info(
                "[%s] Queue '%s' is now deleted",
                self.log_namespace,
                queue_name
            )
        except KeyError:
            logger.error(
                "[%s] Queue '%s' cannot be deleted, does not exist",
                self.log_namespace,
                queue_name
            )
        except exception.SQSError:
            logger.error(
                "[%s] Queue '%s' cannot be deleted, "
                "already done within the last minute",
                self.log_namespace,
                queue_name
            )


class AMQPConsumer(object):
    """
    Consumer feature for AMQP.
    """

    def consume(self, queue_name, callbacks=None, error_handler=None):
        """
        Starts consuming a queue.
        """
        if callbacks is None:
            raise ValueError(
                "callbacks parameter can not be empty"
            )
        try:
            iter(callbacks)
        except TypeError:
            callbacks = [callbacks]

        if queue_name not in self.queues:
            raise ValueError(
                "'%s' is an unknown queue" % queue_name
            )

        if self._connection is None:
            self.connect()

        callbacks = [
            self.callback_wrapper(cb, error_handler)
            for cb in callbacks
        ]
        queues = self._queues[queue_name]

        with self._connection.Consumer(queues=queues, callbacks=callbacks):
            logger.info(
                "[%s] Consuming messages on '%s' queue",
                self.log_namespace,
                queue_name
            )
            while True:
                if self.can_consume:
                    self._connection.drain_events()
                    sleeping_time = self.queues[queue_name]['sleep']
                else:
                    logger.debug(
                        '[%s] Consuming is on hold. Next fetch in 60s',
                        self.log_namespace
                    )
                    sleeping_time = 60
                time.sleep(sleeping_time)

    @property
    def can_consume(self):
        """
        Check a queue can be consumed.
        """
        if not self.transport['office_hours']:
            return True

        now = datetime.now()
        if now.weekday() in [5, 6]:  # Week-end
            return False

        hour = now.hour
        if hour >= 9 and hour < 20:
            return True

        return False

    def callback_wrapper(self, callback, error_handler):
        """
        Decorate the callback to log exceptions
        and send them to Senty later if possible.

        Also cancels the exception to avoid process to crash !
        """
        def exception_catcher(body, message):
            """
            Decorator around callback.
            """
            try:
                return callback(body, message)
            except Exception:
                logger.exception(
                    '[%s] Unhandled exception occured !',
                    self.log_namespace
                )
                if error_handler:
                    error_handler(body, message)
                    logger.debug(
                        '[%s] Error handler called',
                        self.log_namespace
                    )

        return exception_catcher


class AMQPPublisher(object):
    """
    Publisher feature for AMQP.
    """

    def publish(self, queue_name, datas=None, priority=0):
        """
        Publish datas on exchange using queue_name.
        """
        if datas is None:
            datas = {}

        if queue_name not in self.queues:
            raise ValueError(
                "'%s' is an unknown queue" % queue_name
            )
        routing_key = self.queues[queue_name]['route']

        if self.transport['use_priorities']:
            if priority not in range(len(self.transport)):
                raise ValueError(
                    "'%s' is an invalid priority" % priority
                )
            routing_key = '%s.%s' % (
                routing_key,
                self.transport['priorities'][priority]
            )

        if self._connection is None:
            self.connect()

        with self._connection.Producer() as producer:
            producer.publish(
                datas,
                exchange=self._exchange,
                routing_key=routing_key
            )
            logger.info(
                "[%s] Message published on '%s' queue",
                self.log_namespace,
                routing_key
            )


class AMQP(AMQPConnector,
           AMQPContextManager,
           AMQPQueueManager,
           AMQPPublisher,
           AMQPConsumer):
    """
    See https://bitbucket.org/monalgroup/swarm-bus
    """
    pass
