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
from ..aws_kinesis import (IStream as _IStream_c7ff3ed6)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc)
from ..aws_logs import (LogSubscriptionDestinationConfig as _LogSubscriptionDestinationConfig_1075ffd8, ILogGroup as _ILogGroup_6b54c8e1, ILogSubscriptionDestination as _ILogSubscriptionDestination_d006367a)


@jsii.implements(_ILogSubscriptionDestination_d006367a)
class KinesisDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs_destinations.KinesisDestination"):
    """Use a Kinesis stream as the destination for a log subscription.

    stability
    :stability: experimental
    """
    def __init__(self, stream: _IStream_c7ff3ed6) -> None:
        """
        :param stream: -

        stability
        :stability: experimental
        """
        jsii.create(KinesisDestination, self, [stream])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, _source_log_group: _ILogGroup_6b54c8e1) -> _LogSubscriptionDestinationConfig_1075ffd8:
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param _source_log_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, _source_log_group])


@jsii.implements(_ILogSubscriptionDestination_d006367a)
class LambdaDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs_destinations.LambdaDestination"):
    """Use a Lamda Function as the destination for a log subscription.

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
    def bind(self, scope: _Construct_f50a3f53, log_group: _ILogGroup_6b54c8e1) -> _LogSubscriptionDestinationConfig_1075ffd8:
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param log_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, log_group])


__all__ = [
    "KinesisDestination",
    "LambdaDestination",
]

publication.publish()
