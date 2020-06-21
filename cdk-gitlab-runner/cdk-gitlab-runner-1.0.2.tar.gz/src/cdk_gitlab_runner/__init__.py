"""
[![NPM version](https://badge.fury.io/js/cdk-gitlab-runner.svg)](https://badge.fury.io/js/cdk-gitlab-runner)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab-runner.svg)](https://badge.fury.io/py/cdk-gitlab-runner)
![Release](https://github.com/guan840912/cdk-gitlab-runner/workflows/Release/badge.svg)

# Welcome to `cdk-gitlab-runner`

This repository template helps you create gitlab runner on your aws account via AWS CDK one line.

## Note

### Default will help you generate below services:

* VPC

  * Public Subnet (2)
* EC2 (1 T3.large)

## Before start you need gitlab runner token in your  `gitlab project` or   `gitlab group`

### In Group

Group > Settings > CI/CD
![group](image/group_runner_page.png)

### In Group

Project > Settings > CI/CD > Runners
![project](image/project_runner_page.png)

## Usage

Replace your gitlab runner token in `$GITLABTOKEN`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import InstanceType, InstanceClass, InstanceSize
from aws_cdk.aws_iam import ManagedPolicy

# If want change instance type to t3.large .
GitlabContainerRunner(stack, "testing", gitlabtoken="$GITLABTOKEN", ec2type=InstanceType.of(InstanceClass.T2, InstanceSize.LARGE))
# OR
# Just create a gitlab runner , by default instance type is t3.small .
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import InstanceType, InstanceClass, InstanceSize
from aws_cdk.aws_iam import ManagedPolicy

GitlabContainerRunner(stack, "testing", gitlabtoken="$GITLABTOKEN")

# If want change tags you want.
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import InstanceType, InstanceClass, InstanceSize
from aws_cdk.aws_iam import ManagedPolicy

GitlabContainerRunner(stack, "testing-have-type-tag", gitlabtoken="GITLABTOKEN", tag1="aa", tag2="bb", tag3="cc")

# If you want add runner other IAM Policy like s3-readonly-access.
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import InstanceType, InstanceClass, InstanceSize
from aws_cdk.aws_iam import ManagedPolicy

runner = GitlabContainerRunner(stack, "testing-have-type-tag", gitlabtoken="GITLABTOKEN", tag1="aa", tag2="bb", tag3="cc")
runner.runnerrole.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))
```

```python
# Example python instance type change to t3.small .
from aws_cdk import (
  core,
  aws_iam as iam,
)
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import InstanceType, InstanceClass, InstanceSize
runner = GitlabContainerRunner(self, 'gitlab-runner', gitlabtoken='$GITLABTOKEN',
                              ec2type=InstanceType.of(
                                  instance_class=InstanceClass.BURSTABLE3, instance_size=InstanceSize.SMALL), tag1='aa',tag2='bb',tag3='cc')

runner.runnerrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))
```

### see more instance class and size

[InstanceClass](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.InstanceClass.html)

[InstanceSize](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.InstanceSize.html)

## Wait about 6 mins , If success you will see your runner in that page .

![runner](image/group_runner2.png)

#### you can use tag `gitlab` , `runner` , `awscdk`  ,

## Example     *`gitlab-ci.yaml`*

[gitlab docs see more ...](https://docs.gitlab.com/ee/ci/yaml/README.html)

```yaml
dockerjob:
  image: docker:18.09-dind
  variables:
  tags:
    - runner
    - awscdk
    - gitlab
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker info
  script:
    - docker info;
    - echo 'test 123';
    - echo 'hello world 1228'
```

### If your want to debug you can go to aws console

# `In your runner region !!!`

## AWS Systems Manager  >  Session Manager  >  Start a session

![system manager](image/session.png)

#### click your `runner` and click `start session`

#### in the brower console in put `bash`

```bash
# become to root
sudo -i

# list runner container .
root# docker ps -a

# modify gitlab-runner/config.toml

root# cd /home/ec2-user/.gitlab-runner/ && ls
config.toml

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
import aws_cdk.aws_iam
import aws_cdk.core


class GitlabContainerRunner(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-gitlab-runner.GitlabContainerRunner"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, gitlabtoken: str, ec2type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, tag1: typing.Optional[str]=None, tag2: typing.Optional[str]=None, tag3: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param gitlabtoken: 
        :param ec2type: 
        :param tag1: 
        :param tag2: 
        :param tag3: 

        stability
        :stability: experimental
        """
        props = GitlabContainerRunnerProps(gitlabtoken=gitlabtoken, ec2type=ec2type, tag1=tag1, tag2=tag2, tag3=tag3)

        jsii.create(GitlabContainerRunner, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="runnerrole")
    def runnerrole(self) -> aws_cdk.aws_iam.IRole:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "runnerrole")


@jsii.data_type(jsii_type="cdk-gitlab-runner.GitlabContainerRunnerProps", jsii_struct_bases=[], name_mapping={'gitlabtoken': 'gitlabtoken', 'ec2type': 'ec2type', 'tag1': 'tag1', 'tag2': 'tag2', 'tag3': 'tag3'})
class GitlabContainerRunnerProps():
    def __init__(self, *, gitlabtoken: str, ec2type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, tag1: typing.Optional[str]=None, tag2: typing.Optional[str]=None, tag3: typing.Optional[str]=None) -> None:
        """
        :param gitlabtoken: 
        :param ec2type: 
        :param tag1: 
        :param tag2: 
        :param tag3: 

        stability
        :stability: experimental
        """
        self._values = {
            'gitlabtoken': gitlabtoken,
        }
        if ec2type is not None: self._values["ec2type"] = ec2type
        if tag1 is not None: self._values["tag1"] = tag1
        if tag2 is not None: self._values["tag2"] = tag2
        if tag3 is not None: self._values["tag3"] = tag3

    @builtins.property
    def gitlabtoken(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('gitlabtoken')

    @builtins.property
    def ec2type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('ec2type')

    @builtins.property
    def tag1(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('tag1')

    @builtins.property
    def tag2(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('tag2')

    @builtins.property
    def tag3(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('tag3')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitlabContainerRunnerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "GitlabContainerRunner",
    "GitlabContainerRunnerProps",
]

publication.publish()
