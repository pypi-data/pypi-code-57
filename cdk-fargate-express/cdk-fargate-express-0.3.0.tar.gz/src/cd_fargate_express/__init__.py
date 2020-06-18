"""
# cdk-fargate-express

Deploy your serverless Express app in AWS with AWS CDK

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_fargate_express import ExpressService

ExpressService(stack, "testing",
    vpc=vpc,
    # define your local express assets directory containing the Dockerfile
    docker_assets=path.join(__dirname, "../express.d")
)
```
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

import aws_cdk.aws_ec2
import aws_cdk.aws_ecs_patterns
import aws_cdk.core


class ExpressService(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-fargate-express.ExpressService"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, docker_assets: typing.Optional[str]=None, service_options: typing.Optional[aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateServiceProps]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param docker_assets: local path to the docker assets directory.
        :param service_options: options to customize the servide.
        :param vpc: The VPC.

        stability
        :stability: experimental
        """
        props = ExpressServiceProps(docker_assets=docker_assets, service_options=service_options, vpc=vpc)

        jsii.create(ExpressService, self, [scope, id, props])


@jsii.data_type(jsii_type="cdk-fargate-express.ExpressServiceProps", jsii_struct_bases=[], name_mapping={'docker_assets': 'dockerAssets', 'service_options': 'serviceOptions', 'vpc': 'vpc'})
class ExpressServiceProps():
    def __init__(self, *, docker_assets: typing.Optional[str]=None, service_options: typing.Optional[aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateServiceProps]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """
        :param docker_assets: local path to the docker assets directory.
        :param service_options: options to customize the servide.
        :param vpc: The VPC.

        stability
        :stability: experimental
        """
        if isinstance(service_options, dict): service_options = aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateServiceProps(**service_options)
        self._values = {
        }
        if docker_assets is not None: self._values["docker_assets"] = docker_assets
        if service_options is not None: self._values["service_options"] = service_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def docker_assets(self) -> typing.Optional[str]:
        """local path to the docker assets directory.

        stability
        :stability: experimental
        """
        return self._values.get('docker_assets')

    @builtins.property
    def service_options(self) -> typing.Optional[aws_cdk.aws_ecs_patterns.ApplicationLoadBalancedFargateServiceProps]:
        """options to customize the servide.

        stability
        :stability: experimental
        """
        return self._values.get('service_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ExpressServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "ExpressService",
    "ExpressServiceProps",
]

publication.publish()
