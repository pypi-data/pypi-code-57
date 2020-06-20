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
from ..aws_autoscaling import (LifecycleHookTargetConfig as _LifecycleHookTargetConfig_83c58429, ILifecycleHook as _ILifecycleHook_04206686, ILifecycleHookTarget as _ILifecycleHookTarget_d52ce7b2)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)
from ..aws_sqs import (IQueue as _IQueue_b743f559)


@jsii.implements(_ILifecycleHookTarget_d52ce7b2)
class FunctionHook(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_autoscaling_hooktargets.FunctionHook"):
    """Use a Lambda Function as a hook target.

    Internally creates a Topic to make the connection.

    stability
    :stability: experimental
    """
    def __init__(self, fn: _IFunction_1c1de0bc) -> None:
        """
        :param fn: -

        stability
        :stability: experimental
        """
        jsii.create(FunctionHook, self, [fn])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, lifecycle_hook: _ILifecycleHook_04206686) -> _LifecycleHookTargetConfig_83c58429:
        """Called when this object is used as the target of a lifecycle hook.

        :param scope: -
        :param lifecycle_hook: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, lifecycle_hook])


@jsii.implements(_ILifecycleHookTarget_d52ce7b2)
class QueueHook(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_autoscaling_hooktargets.QueueHook"):
    """Use an SQS queue as a hook target.

    stability
    :stability: experimental
    """
    def __init__(self, queue: _IQueue_b743f559) -> None:
        """
        :param queue: -

        stability
        :stability: experimental
        """
        jsii.create(QueueHook, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, lifecycle_hook: _ILifecycleHook_04206686) -> _LifecycleHookTargetConfig_83c58429:
        """Called when this object is used as the target of a lifecycle hook.

        :param _scope: -
        :param lifecycle_hook: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, lifecycle_hook])


@jsii.implements(_ILifecycleHookTarget_d52ce7b2)
class TopicHook(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_autoscaling_hooktargets.TopicHook"):
    """Use an SNS topic as a hook target.

    stability
    :stability: experimental
    """
    def __init__(self, topic: _ITopic_ef0ebe0e) -> None:
        """
        :param topic: -

        stability
        :stability: experimental
        """
        jsii.create(TopicHook, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, lifecycle_hook: _ILifecycleHook_04206686) -> _LifecycleHookTargetConfig_83c58429:
        """Called when this object is used as the target of a lifecycle hook.

        :param _scope: -
        :param lifecycle_hook: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, lifecycle_hook])


__all__ = [
    "FunctionHook",
    "QueueHook",
    "TopicHook",
]

publication.publish()
