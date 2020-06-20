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
from ..aws_events import (IEventBus as _IEventBus_ed4f1700)
from ..aws_lambda import (DestinationConfig as _DestinationConfig_ab93b607, IFunction as _IFunction_1c1de0bc, DestinationOptions as _DestinationOptions_4bc6a3c7, IDestination as _IDestination_7081f282)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)
from ..aws_sqs import (IQueue as _IQueue_b743f559)


@jsii.implements(_IDestination_7081f282)
class EventBridgeDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_destinations.EventBridgeDestination"):
    """Use an Event Bridge event bus as a Lambda destination.

    If no event bus is specified, the default event bus is used.

    stability
    :stability: experimental
    """
    def __init__(self, event_bus: typing.Optional[_IEventBus_ed4f1700]=None) -> None:
        """
        :param event_bus: -

        default
        :default: - use the default event bus

        stability
        :stability: experimental
        """
        jsii.create(EventBridgeDestination, self, [event_bus])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, fn: _IFunction_1c1de0bc, *, type: _DestinationType_644824de) -> _DestinationConfig_ab93b607:
        """Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: The destination type.

        stability
        :stability: experimental
        """
        _options = _DestinationOptions_4bc6a3c7(type=type)

        return jsii.invoke(self, "bind", [_scope, fn, _options])


@jsii.implements(_IDestination_7081f282)
class LambdaDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_destinations.LambdaDestination"):
    """Use a Lambda function as a Lambda destination.

    stability
    :stability: experimental
    """
    def __init__(self, fn: _IFunction_1c1de0bc, *, response_only: typing.Optional[bool]=None) -> None:
        """
        :param fn: -
        :param response_only: Whether the destination function receives only the ``responsePayload`` of the source function. When set to ``true`` and used as ``onSuccess`` destination, the destination function will be invoked with the payload returned by the source function. When set to ``true`` and used as ``onFailure`` destination, the destination function will be invoked with the error object returned by source function. See the README of this module to see a full explanation of this option. Default: false The destination function receives the full invocation record.

        stability
        :stability: experimental
        """
        options = LambdaDestinationOptions(response_only=response_only)

        jsii.create(LambdaDestination, self, [fn, options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, fn: _IFunction_1c1de0bc, *, type: _DestinationType_644824de) -> _DestinationConfig_ab93b607:
        """Returns a destination configuration.

        :param scope: -
        :param fn: -
        :param type: The destination type.

        stability
        :stability: experimental
        """
        options = _DestinationOptions_4bc6a3c7(type=type)

        return jsii.invoke(self, "bind", [scope, fn, options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda_destinations.LambdaDestinationOptions", jsii_struct_bases=[], name_mapping={'response_only': 'responseOnly'})
class LambdaDestinationOptions():
    def __init__(self, *, response_only: typing.Optional[bool]=None) -> None:
        """Options for a Lambda destination.

        :param response_only: Whether the destination function receives only the ``responsePayload`` of the source function. When set to ``true`` and used as ``onSuccess`` destination, the destination function will be invoked with the payload returned by the source function. When set to ``true`` and used as ``onFailure`` destination, the destination function will be invoked with the error object returned by source function. See the README of this module to see a full explanation of this option. Default: false The destination function receives the full invocation record.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if response_only is not None: self._values["response_only"] = response_only

    @builtins.property
    def response_only(self) -> typing.Optional[bool]:
        """Whether the destination function receives only the ``responsePayload`` of the source function.

        When set to ``true`` and used as ``onSuccess`` destination, the destination
        function will be invoked with the payload returned by the source function.

        When set to ``true`` and used as ``onFailure`` destination, the destination
        function will be invoked with the error object returned by source function.

        See the README of this module to see a full explanation of this option.

        default
        :default: false The destination function receives the full invocation record.

        stability
        :stability: experimental
        """
        return self._values.get('response_only')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaDestinationOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IDestination_7081f282)
class SnsDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_destinations.SnsDestination"):
    """Use a SNS topic as a Lambda destination.

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
    def bind(self, _scope: _Construct_f50a3f53, fn: _IFunction_1c1de0bc, *, type: _DestinationType_644824de) -> _DestinationConfig_ab93b607:
        """Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: The destination type.

        stability
        :stability: experimental
        """
        _options = _DestinationOptions_4bc6a3c7(type=type)

        return jsii.invoke(self, "bind", [_scope, fn, _options])


@jsii.implements(_IDestination_7081f282)
class SqsDestination(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_destinations.SqsDestination"):
    """Use a SQS queue as a Lambda destination.

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
    def bind(self, _scope: _Construct_f50a3f53, fn: _IFunction_1c1de0bc, *, type: _DestinationType_644824de) -> _DestinationConfig_ab93b607:
        """Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: The destination type.

        stability
        :stability: experimental
        """
        _options = _DestinationOptions_4bc6a3c7(type=type)

        return jsii.invoke(self, "bind", [_scope, fn, _options])


__all__ = [
    "EventBridgeDestination",
    "LambdaDestination",
    "LambdaDestinationOptions",
    "SnsDestination",
    "SqsDestination",
]

publication.publish()
