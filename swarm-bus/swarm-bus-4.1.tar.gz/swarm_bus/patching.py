"""
Patch and improve boto and kombu
"""
import logging

logger = logging.getLogger(__name__)


def fix_libs(instance):
    """
    Mock patching kombu 4.6.8
    """
    import kombu.transport.SQS
    import kombu.transport.virtual.base
    from kombu.utils.div import emergency_dump_state

    def create_queue_patched(self, queue_name, attributes):
        """
        Override create_queue, by configuring more parameters
        """
        if self.predefined_queues:
            return None

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

        attributes.update(
            {
                'MessageRetentionPeriod': str(queue['living']),
                'ReceiveMessageWaitTimeSeconds': str(queue['wait']),
                'VisibilityTimeout': str(queue['visibility']),
            }
        )

        return self.sqs(queue=queue_name).create_queue(
            QueueName=queue_name,
            Attributes=attributes
        )

    def basic_ack_patched(self, delivery_tag, multiple=False):
        """
        Override basic_ack, to add logs
        """
        try:
            message = self.qos.get(delivery_tag).delivery_info
            sqs_message = message['sqs_message']
        except KeyError:
            pass
        else:
            queue = None
            if 'routing_key' in message:
                queue = self.canonical_queue_name(message['routing_key'])

            self.sqs(queue=queue).delete_message(
                QueueUrl=message['sqs_queue'],
                ReceiptHandle=sqs_message['ReceiptHandle'],
            )

        super(kombu.transport.SQS.Channel, self).basic_ack(delivery_tag)
        logger.debug(
            "[%s] [Message] '%s' on '%s' ACKNOWLEGED",
            instance.log_namespace,
            message['sqs_message']['MessageId'],
            message['routing_key']
        )

    def basic_reject_patched(self, delivery_tag, requeue=False):
        """
        Implement reject message in SQS, with logs
        """
        try:
            message = self.qos.get(delivery_tag).delivery_info
            sqs_message = message['sqs_message']
        except KeyError:
            pass
        else:
            queue = None
            if 'routing_key' in message:
                queue = self.canonical_queue_name(message['routing_key'])

            self.sqs(queue=queue).delete_message(
                QueueUrl=message['sqs_queue'],
                ReceiptHandle=sqs_message['ReceiptHandle'],
            )

        super(kombu.transport.SQS.Channel, self).basic_reject(delivery_tag)
        logger.debug(
            "[%s] [Message] '%s' on '%s' REJECTED",
            instance.log_namespace,
            message['sqs_message']['MessageId'],
            message['routing_key']
        )

    def restore_unacked_once_patched(self, stderr=None):
        """
        Adapt this function to replace print with useful logs
        """
        self._on_collect.cancel()
        self._flush()
        state = self._delivered

        logger.info(
            '[%s] Interruption detected, cleaning...',
            instance.log_namespace
        )

        if (not instance.transport['restore_at_shutdown']
                or not self.restore_at_shutdown
                or not self.channel.do_restore):
            return
        if getattr(state, 'restored', None):
            assert not state
            return
        try:
            if state:
                logger.warning(
                    '[%s] Restoring %d unacknowledged message(s)...',
                    instance.log_namespace,
                    len(self._delivered)
                )
                unrestored = self.restore_unacked()

                if unrestored:
                    errors, messages = list(zip(*unrestored))
                    logger.warning(
                        '[%s] UNABLE TO RESTORE %d MESSAGES: %s',
                        instance.log_namespace,
                        len(errors),
                        errors
                    )
                    emergency_dump_state(messages)
        finally:
            state.restored = True

    kombu.transport.SQS.Channel._create_queue = create_queue_patched
    kombu.transport.SQS.Channel.basic_ack = basic_ack_patched
    kombu.transport.SQS.Channel.basic_reject = basic_reject_patched
    kombu.transport.virtual.base.QoS.restore_unacked_once = restore_unacked_once_patched  # noqa
