import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc)
from ..aws_s3 import (BucketNotificationDestinationConfig as _BucketNotificationDestinationConfig_f2b78ed5, IBucket as _IBucket_25bad983, IBucketNotificationDestination as _IBucketNotificationDestination_de4b916c)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)
from ..aws_sqs import (IQueue as _IQueue_b743f559)


@jsii.implements(_IBucketNotificationDestination_de4b916c)
class LambdaDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_s3_notifications.LambdaDestination"):
    """Use a Lambda function as a bucket notification destination.

    stability
    :stability: experimental
    """
    def __init__(self, fn: _IFunction_1c1de0bc) -> None:
        """
        :param fn: -

        stability
        :stability: experimental
        """
        jsii.create(LambdaDestination, self, [fn])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, bucket: _IBucket_25bad983) -> _BucketNotificationDestinationConfig_f2b78ed5:
        """Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param _scope: -
        :param bucket: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, bucket])


@jsii.implements(_IBucketNotificationDestination_de4b916c)
class SnsDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_s3_notifications.SnsDestination"):
    """Use an SNS topic as a bucket notification destination.

    stability
    :stability: experimental
    """
    def __init__(self, topic: _ITopic_ef0ebe0e) -> None:
        """
        :param topic: -

        stability
        :stability: experimental
        """
        jsii.create(SnsDestination, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, bucket: _IBucket_25bad983) -> _BucketNotificationDestinationConfig_f2b78ed5:
        """Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param _scope: -
        :param bucket: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, bucket])


@jsii.implements(_IBucketNotificationDestination_de4b916c)
class SqsDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_s3_notifications.SqsDestination"):
    """Use an SQS queue as a bucket notification destination.

    stability
    :stability: experimental
    """
    def __init__(self, queue: _IQueue_b743f559) -> None:
        """
        :param queue: -

        stability
        :stability: experimental
        """
        jsii.create(SqsDestination, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, bucket: _IBucket_25bad983) -> _BucketNotificationDestinationConfig_f2b78ed5:
        """Allows using SQS queues as destinations for bucket notifications.

        Use ``bucket.onEvent(event, queue)`` to subscribe.

        :param _scope: -
        :param bucket: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, bucket])


__all__ = [
    "LambdaDestination",
    "SnsDestination",
    "SqsDestination",
]

publication.publish()
