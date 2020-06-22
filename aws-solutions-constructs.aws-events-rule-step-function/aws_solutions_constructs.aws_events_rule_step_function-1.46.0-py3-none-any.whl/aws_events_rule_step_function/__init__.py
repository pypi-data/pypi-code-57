"""
# aws-events-rule-step-function module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_events_rule_step_function`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-events-rule-step-function`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.eventsrulestepfunction`|

This AWS Solutions Construct implements an AWS Events rule and an AWS Step function.

Here is a minimal deployable pattern definition:

```javascript
const { EventsRuleToStepFunction, EventsRuleToStepFunctionProps } = require('@aws-solutions-constructs/aws-events-rule-step-function');

const startState = new stepfunctions.Pass(stack, 'StartState');

const props: EventsRuleToStepFunctionProps = {
    stateMachineProps: {
      definition: startState
    },
    eventRuleProps: {
      schedule: events.Schedule.rate(Duration.minutes(5))
    }
};

new EventsRuleToStepFunction(stack, 'test-events-rule-step-function-stack', props);
```

## Initializer

```text
new EventsRuleToStepFunction(scope: Construct, id: string, props: EventsRuleToStepFunctionProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`EventsRuleToStepFunctionProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|stateMachineProps|[`sfn.StateMachineProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-stepfunctions.StateMachineProps.html)|Optional user provided props to override the default props for sfn.StateMachine|
|eventRuleProps|[`events.RuleProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.RuleProps.html)|User provided eventRuleProps to override the defaults|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventsRule|[`events.Rule`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.Rule.html)|Returns an instance of events.Rule created by the construct|
|stateMachine|[`sfn.StateMachine`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-stepfunctions.StateMachine.html)|Returns an instance of sfn.StateMachine created by the construct|
|cloudwatchAlarms|[`cloudwatch.Alarm[]`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudwatch.Alarm.html)|Returns a list of cloudwatch.Alarm created by the construct|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon CloudWatch Events Rule

* Grant least privilege permissions to CloudWatch Events to trigger the Lambda Function

### AWS Step Function

* Enable CloudWatch logging for API Gateway
* Deploy best practices CloudWatch Alarms for the Step Function

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_events
import aws_cdk.aws_stepfunctions
import aws_cdk.core


class EventsRuleToStepFunction(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-events-rule-step-function.EventsRuleToStepFunction"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, event_rule_props: aws_cdk.aws_events.RuleProps, state_machine_props: aws_cdk.aws_stepfunctions.StateMachineProps) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param state_machine_props: User provided StateMachineProps to override the defaults. Default: - None

        access:
        :access:: public
        since:
        :since:: 0.9.0
        summary:
        :summary:: Constructs a new instance of the EventsRuleToStepFunction class.
        """
        props = EventsRuleToStepFunctionProps(event_rule_props=event_rule_props, state_machine_props=state_machine_props)

        jsii.create(EventsRuleToStepFunction, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarms")
    def cloudwatch_alarms(self) -> typing.List[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "cloudwatchAlarms")

    @builtins.property
    @jsii.member(jsii_name="eventsRule")
    def events_rule(self) -> aws_cdk.aws_events.Rule:
        return jsii.get(self, "eventsRule")

    @builtins.property
    @jsii.member(jsii_name="stateMachine")
    def state_machine(self) -> aws_cdk.aws_stepfunctions.StateMachine:
        return jsii.get(self, "stateMachine")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-events-rule-step-function.EventsRuleToStepFunctionProps", jsii_struct_bases=[], name_mapping={'event_rule_props': 'eventRuleProps', 'state_machine_props': 'stateMachineProps'})
class EventsRuleToStepFunctionProps():
    def __init__(self, *, event_rule_props: aws_cdk.aws_events.RuleProps, state_machine_props: aws_cdk.aws_stepfunctions.StateMachineProps) -> None:
        """
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param state_machine_props: User provided StateMachineProps to override the defaults. Default: - None

        summary:
        :summary:: The properties for the EventsRuleToStepFunction Construct
        """
        if isinstance(event_rule_props, dict): event_rule_props = aws_cdk.aws_events.RuleProps(**event_rule_props)
        if isinstance(state_machine_props, dict): state_machine_props = aws_cdk.aws_stepfunctions.StateMachineProps(**state_machine_props)
        self._values = {
            'event_rule_props': event_rule_props,
            'state_machine_props': state_machine_props,
        }

    @builtins.property
    def event_rule_props(self) -> aws_cdk.aws_events.RuleProps:
        """User provided eventRuleProps to override the defaults.

        default
        :default: - None
        """
        return self._values.get('event_rule_props')

    @builtins.property
    def state_machine_props(self) -> aws_cdk.aws_stepfunctions.StateMachineProps:
        """User provided StateMachineProps to override the defaults.

        default
        :default: - None
        """
        return self._values.get('state_machine_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EventsRuleToStepFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "EventsRuleToStepFunction",
    "EventsRuleToStepFunctionProps",
]

publication.publish()
