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
from ..aws_applicationautoscaling import (StepScalingAction as _StepScalingAction_e6a08ac3)
from ..aws_autoscaling import (StepScalingAction as _StepScalingAction_24342ebd)
from ..aws_cloudwatch import (AlarmActionConfig as _AlarmActionConfig_280e5eed, IAlarm as _IAlarm_478ec33c, IAlarmAction as _IAlarmAction_4b9cf0b4)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)


@jsii.implements(_IAlarmAction_4b9cf0b4)
class ApplicationScalingAction(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_cloudwatch_actions.ApplicationScalingAction"):
    """Use an ApplicationAutoScaling StepScalingAction as an Alarm Action.

    stability
    :stability: experimental
    """
    def __init__(self, step_scaling_action: _StepScalingAction_e6a08ac3) -> None:
        """
        :param step_scaling_action: -

        stability
        :stability: experimental
        """
        jsii.create(ApplicationScalingAction, self, [step_scaling_action])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _alarm: _IAlarm_478ec33c) -> _AlarmActionConfig_280e5eed:
        """Returns an alarm action configuration to use an ApplicationScaling StepScalingAction as an alarm action.

        :param _scope: -
        :param _alarm: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _alarm])


@jsii.implements(_IAlarmAction_4b9cf0b4)
class AutoScalingAction(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_cloudwatch_actions.AutoScalingAction"):
    """Use an AutoScaling StepScalingAction as an Alarm Action.

    stability
    :stability: experimental
    """
    def __init__(self, step_scaling_action: _StepScalingAction_24342ebd) -> None:
        """
        :param step_scaling_action: -

        stability
        :stability: experimental
        """
        jsii.create(AutoScalingAction, self, [step_scaling_action])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _alarm: _IAlarm_478ec33c) -> _AlarmActionConfig_280e5eed:
        """Returns an alarm action configuration to use an AutoScaling StepScalingAction as an alarm action.

        :param _scope: -
        :param _alarm: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _alarm])


@jsii.implements(_IAlarmAction_4b9cf0b4)
class SnsAction(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_cloudwatch_actions.SnsAction"):
    """Use an SNS topic as an alarm action.

    stability
    :stability: experimental
    """
    def __init__(self, topic: _ITopic_ef0ebe0e) -> None:
        """
        :param topic: -

        stability
        :stability: experimental
        """
        jsii.create(SnsAction, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _alarm: _IAlarm_478ec33c) -> _AlarmActionConfig_280e5eed:
        """Returns an alarm action configuration to use an SNS topic as an alarm action.

        :param _scope: -
        :param _alarm: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _alarm])


__all__ = [
    "ApplicationScalingAction",
    "AutoScalingAction",
    "SnsAction",
]

publication.publish()
