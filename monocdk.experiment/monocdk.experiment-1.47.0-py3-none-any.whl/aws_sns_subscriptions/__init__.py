import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from ..aws_lambda import (IFunction as _IFunction_1c1de0bc)
from ..aws_sns import (TopicSubscriptionConfig as _TopicSubscriptionConfig_2ddb92c9, ITopic as _ITopic_ef0ebe0e, ITopicSubscription as _ITopicSubscription_5303fec1, SubscriptionFilter as _SubscriptionFilter_91537200, SubscriptionProtocol as _SubscriptionProtocol_3d1a4bcf)
from ..aws_sqs import (IQueue as _IQueue_b743f559)


@jsii.implements(_ITopicSubscription_5303fec1)
class EmailSubscription(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_sns_subscriptions.EmailSubscription"):
    """Use an email address as a subscription target.

    Email subscriptions require confirmation.

    stability
    :stability: experimental
    """
    def __init__(self, email_address: str, *, json: typing.Optional[bool]=None, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None) -> None:
        """
        :param email_address: -
        :param json: Indicates if the full notification JSON should be sent to the email address or just the message text. Default: false (Message text)
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        stability
        :stability: experimental
        """
        props = EmailSubscriptionProps(json=json, dead_letter_queue=dead_letter_queue, filter_policy=filter_policy)

        jsii.create(EmailSubscription, self, [email_address, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_ef0ebe0e) -> _TopicSubscriptionConfig_2ddb92c9:
        """Returns a configuration for an email address to subscribe to an SNS topic.

        :param _topic: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_topic])


@jsii.implements(_ITopicSubscription_5303fec1)
class LambdaSubscription(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_sns_subscriptions.LambdaSubscription"):
    """Use a Lambda function as a subscription target.

    stability
    :stability: experimental
    """
    def __init__(self, fn: _IFunction_1c1de0bc, *, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None) -> None:
        """
        :param fn: -
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        stability
        :stability: experimental
        """
        props = LambdaSubscriptionProps(dead_letter_queue=dead_letter_queue, filter_policy=filter_policy)

        jsii.create(LambdaSubscription, self, [fn, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic: _ITopic_ef0ebe0e) -> _TopicSubscriptionConfig_2ddb92c9:
        """Returns a configuration for a Lambda function to subscribe to an SNS topic.

        :param topic: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [topic])


@jsii.implements(_ITopicSubscription_5303fec1)
class SmsSubscription(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_sns_subscriptions.SmsSubscription"):
    """Use an sms address as a subscription target.

    stability
    :stability: experimental
    """
    def __init__(self, phone_number: str, *, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None) -> None:
        """
        :param phone_number: -
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        stability
        :stability: experimental
        """
        props = SmsSubscriptionProps(dead_letter_queue=dead_letter_queue, filter_policy=filter_policy)

        jsii.create(SmsSubscription, self, [phone_number, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_ef0ebe0e) -> _TopicSubscriptionConfig_2ddb92c9:
        """Returns a configuration used to subscribe to an SNS topic.

        :param _topic: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_topic])


@jsii.implements(_ITopicSubscription_5303fec1)
class SqsSubscription(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_sns_subscriptions.SqsSubscription"):
    """Use an SQS queue as a subscription target.

    stability
    :stability: experimental
    """
    def __init__(self, queue: _IQueue_b743f559, *, raw_message_delivery: typing.Optional[bool]=None, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None) -> None:
        """
        :param queue: -
        :param raw_message_delivery: The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        stability
        :stability: experimental
        """
        props = SqsSubscriptionProps(raw_message_delivery=raw_message_delivery, dead_letter_queue=dead_letter_queue, filter_policy=filter_policy)

        jsii.create(SqsSubscription, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic: _ITopic_ef0ebe0e) -> _TopicSubscriptionConfig_2ddb92c9:
        """Returns a configuration for an SQS queue to subscribe to an SNS topic.

        :param topic: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [topic])


@jsii.data_type(jsii_type="monocdk-experiment.aws_sns_subscriptions.SubscriptionProps", jsii_struct_bases=[], name_mapping={'dead_letter_queue': 'deadLetterQueue', 'filter_policy': 'filterPolicy'})
class SubscriptionProps():
    def __init__(self, *, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None) -> None:
        """Options to subscribing to an SNS topic.

        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        stability
        :stability: experimental
        """
        self._values = {
        }
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None: self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        return self._values.get('filter_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_ITopicSubscription_5303fec1)
class UrlSubscription(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_sns_subscriptions.UrlSubscription"):
    """Use a URL as a subscription target.

    The message will be POSTed to the given URL.

    see
    :see: https://docs.aws.amazon.com/sns/latest/dg/sns-http-https-endpoint-as-subscriber.html
    stability
    :stability: experimental
    """
    def __init__(self, url: str, *, protocol: typing.Optional[_SubscriptionProtocol_3d1a4bcf]=None, raw_message_delivery: typing.Optional[bool]=None, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None) -> None:
        """
        :param url: -
        :param protocol: The subscription's protocol. Default: - Protocol is derived from url
        :param raw_message_delivery: The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        stability
        :stability: experimental
        """
        props = UrlSubscriptionProps(protocol=protocol, raw_message_delivery=raw_message_delivery, dead_letter_queue=dead_letter_queue, filter_policy=filter_policy)

        jsii.create(UrlSubscription, self, [url, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_ef0ebe0e) -> _TopicSubscriptionConfig_2ddb92c9:
        """Returns a configuration for a URL to subscribe to an SNS topic.

        :param _topic: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_topic])


@jsii.data_type(jsii_type="monocdk-experiment.aws_sns_subscriptions.UrlSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'dead_letter_queue': 'deadLetterQueue', 'filter_policy': 'filterPolicy', 'protocol': 'protocol', 'raw_message_delivery': 'rawMessageDelivery'})
class UrlSubscriptionProps(SubscriptionProps):
    def __init__(self, *, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None, protocol: typing.Optional[_SubscriptionProtocol_3d1a4bcf]=None, raw_message_delivery: typing.Optional[bool]=None) -> None:
        """Options for URL subscriptions.

        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param protocol: The subscription's protocol. Default: - Protocol is derived from url
        :param raw_message_delivery: The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if protocol is not None: self._values["protocol"] = protocol
        if raw_message_delivery is not None: self._values["raw_message_delivery"] = raw_message_delivery

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        return self._values.get('filter_policy')

    @builtins.property
    def protocol(self) -> typing.Optional[_SubscriptionProtocol_3d1a4bcf]:
        """The subscription's protocol.

        default
        :default: - Protocol is derived from url

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[bool]:
        """The message to the queue is the same as it was sent to the topic.

        If false, the message will be wrapped in an SNS envelope.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('raw_message_delivery')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UrlSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_sns_subscriptions.EmailSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'dead_letter_queue': 'deadLetterQueue', 'filter_policy': 'filterPolicy', 'json': 'json'})
class EmailSubscriptionProps(SubscriptionProps):
    def __init__(self, *, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None, json: typing.Optional[bool]=None) -> None:
        """Options for email subscriptions.

        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param json: Indicates if the full notification JSON should be sent to the email address or just the message text. Default: false (Message text)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if json is not None: self._values["json"] = json

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        return self._values.get('filter_policy')

    @builtins.property
    def json(self) -> typing.Optional[bool]:
        """Indicates if the full notification JSON should be sent to the email address or just the message text.

        default
        :default: false (Message text)

        stability
        :stability: experimental
        """
        return self._values.get('json')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EmailSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_sns_subscriptions.LambdaSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'dead_letter_queue': 'deadLetterQueue', 'filter_policy': 'filterPolicy'})
class LambdaSubscriptionProps(SubscriptionProps):
    def __init__(self, *, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None) -> None:
        """Properties for a Lambda subscription.

        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        stability
        :stability: experimental
        """
        self._values = {
        }
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None: self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        return self._values.get('filter_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_sns_subscriptions.SmsSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'dead_letter_queue': 'deadLetterQueue', 'filter_policy': 'filterPolicy'})
class SmsSubscriptionProps(SubscriptionProps):
    def __init__(self, *, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None) -> None:
        """Options for SMS subscriptions.

        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered

        stability
        :stability: experimental
        """
        self._values = {
        }
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None: self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        return self._values.get('filter_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SmsSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_sns_subscriptions.SqsSubscriptionProps", jsii_struct_bases=[SubscriptionProps], name_mapping={'dead_letter_queue': 'deadLetterQueue', 'filter_policy': 'filterPolicy', 'raw_message_delivery': 'rawMessageDelivery'})
class SqsSubscriptionProps(SubscriptionProps):
    def __init__(self, *, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, filter_policy: typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]=None, raw_message_delivery: typing.Optional[bool]=None) -> None:
        """Properties for an SQS subscription.

        :param dead_letter_queue: Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None: self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None: self._values["raw_message_delivery"] = raw_message_delivery

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        default
        :default: - No dead letter queue enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def filter_policy(self) -> typing.Optional[typing.Mapping[str, _SubscriptionFilter_91537200]]:
        """The filter policy.

        default
        :default: - all messages are delivered

        stability
        :stability: experimental
        """
        return self._values.get('filter_policy')

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[bool]:
        """The message to the queue is the same as it was sent to the topic.

        If false, the message will be wrapped in an SNS envelope.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('raw_message_delivery')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SqsSubscriptionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "EmailSubscription",
    "EmailSubscriptionProps",
    "LambdaSubscription",
    "LambdaSubscriptionProps",
    "SmsSubscription",
    "SmsSubscriptionProps",
    "SqsSubscription",
    "SqsSubscriptionProps",
    "SubscriptionProps",
    "UrlSubscription",
    "UrlSubscriptionProps",
]

publication.publish()
