"""
Patch and improve boto and kombu
"""
import logging

logger = logging.getLogger(__name__)


def fix_libs(instance):
    """
    Mock patching kombu 4.0.2 and boto 2.45
    """
    import boto.sqs.connection
    import kombu.transport.SQS

    from boto.sqs.queue import Queue as BotoQueue
    from kombu.five import Empty

    def drain_events_patched(self, timeout=None, **kwargs):
        """
        Override drain_events, by adding **kwargs argument.
        """
        if not self._consumers or not self.qos.can_consume():
            raise Empty()
        self._poll(self.cycle, self.connection._deliver, timeout=timeout)

    def create_queue_patched(self, queue_name, visibility_timeout=None):
        """
        Override create_queue, by configuring more parameters
        """
        base_queue_name = queue_name.replace(
            instance.transport['queue_name_prefix'],
            ''
        )
        if instance.transport['use_priorities']:
            for priority in instance.transport['priorities']:
                base_queue_name = base_queue_name.replace(
                    '-%s' % priority,
                    ''
                )

        queue = instance.queues[base_queue_name]

        params = {'QueueName': queue_name}
        params['Attribute.1.Name'] = 'VisibilityTimeout'
        params['Attribute.1.Value'] = queue['visibility']
        params['Attribute.2.Name'] = 'ReceiveMessageWaitTimeSeconds'
        params['Attribute.2.Value'] = queue['wait']
        params['Attribute.3.Name'] = 'MessageRetentionPeriod'
        params['Attribute.3.Value'] = queue['living']
        return self.get_object('CreateQueue', params, BotoQueue)

    def basic_ack_patched(self, delivery_tag, multiple=False):
        """
        Override basic_ack, to add logs
        """
        delivery_info = self.qos.get(delivery_tag).delivery_info
        try:
            queue = delivery_info['sqs_queue']
        except KeyError:
            pass
        else:
            queue.delete_message(delivery_info['sqs_message'])
        super(kombu.transport.SQS.Channel, self).basic_ack(delivery_tag)
        logger.debug(
            "[%s] [Message] '%s' on '%s' ACKNOWLEGED",
            instance.log_namespace,
            delivery_info['sqs_message'].id,
            delivery_info['routing_key']
        )

    def basic_reject_patched(self, delivery_tag, requeue=False):
        """
        Implement reject message in SQS
        """
        delivery_info = self.qos.get(delivery_tag).delivery_info
        try:
            queue = delivery_info['sqs_queue']
        except KeyError:
            pass
        else:
            queue.delete_message(delivery_info['sqs_message'])
        super(kombu.transport.SQS.Channel, self).basic_reject(
            delivery_tag, requeue=requeue
        )
        logger.debug(
            "[%s] [Message] '%s' on '%s' REJECTED",
            instance.log_namespace,
            delivery_info['sqs_message'].id,
            delivery_info['routing_key']
        )

    boto.sqs.connection.SQSConnection.create_queue = create_queue_patched
    kombu.transport.SQS.Channel.drain_events = drain_events_patched
    kombu.transport.SQS.Channel.basic_ack = basic_ack_patched
    kombu.transport.SQS.Channel.basic_reject = basic_reject_patched
