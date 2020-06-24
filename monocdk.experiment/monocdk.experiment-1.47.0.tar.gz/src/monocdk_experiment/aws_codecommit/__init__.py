import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a, IResource as _IResource_72f7ee7e, Resource as _Resource_884d0774)
from ..aws_events import (Rule as _Rule_c38e0b39, OnEventOptions as _OnEventOptions_926fbcf9, EventPattern as _EventPattern_8aa7b781, IRuleTarget as _IRuleTarget_41800a77)
from ..aws_iam import (Grant as _Grant_96af6d2d, IGrantable as _IGrantable_0fcfc53a)


@jsii.implements(_IInspectable_051e6ed8)
class CfnRepository(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codecommit.CfnRepository"):
    """A CloudFormation ``AWS::CodeCommit::Repository``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeCommit::Repository
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, repository_name: str, code: typing.Optional[typing.Union["CodeProperty", _IResolvable_9ceae33e]]=None, repository_description: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, triggers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["RepositoryTriggerProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Create a new ``AWS::CodeCommit::Repository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param repository_name: ``AWS::CodeCommit::Repository.RepositoryName``.
        :param code: ``AWS::CodeCommit::Repository.Code``.
        :param repository_description: ``AWS::CodeCommit::Repository.RepositoryDescription``.
        :param tags: ``AWS::CodeCommit::Repository.Tags``.
        :param triggers: ``AWS::CodeCommit::Repository.Triggers``.
        """
        props = CfnRepositoryProps(repository_name=repository_name, code=code, repository_description=repository_description, tags=tags, triggers=triggers)

        jsii.create(CfnRepository, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnRepository":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrCloneUrlHttp")
    def attr_clone_url_http(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CloneUrlHttp
        """
        return jsii.get(self, "attrCloneUrlHttp")

    @builtins.property
    @jsii.member(jsii_name="attrCloneUrlSsh")
    def attr_clone_url_ssh(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CloneUrlSsh
        """
        return jsii.get(self, "attrCloneUrlSsh")

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::CodeCommit::Repository.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """``AWS::CodeCommit::Repository.RepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositoryname
        """
        return jsii.get(self, "repositoryName")

    @repository_name.setter
    def repository_name(self, value: str) -> None:
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> typing.Optional[typing.Union["CodeProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeCommit::Repository.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-code
        """
        return jsii.get(self, "code")

    @code.setter
    def code(self, value: typing.Optional[typing.Union["CodeProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryDescription")
    def repository_description(self) -> typing.Optional[str]:
        """``AWS::CodeCommit::Repository.RepositoryDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositorydescription
        """
        return jsii.get(self, "repositoryDescription")

    @repository_description.setter
    def repository_description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "repositoryDescription", value)

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["RepositoryTriggerProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeCommit::Repository.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-triggers
        """
        return jsii.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["RepositoryTriggerProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "triggers", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_codecommit.CfnRepository.CodeProperty", jsii_struct_bases=[], name_mapping={'s3': 's3'})
    class CodeProperty():
        def __init__(self, *, s3: typing.Union["CfnRepository.S3Property", _IResolvable_9ceae33e]) -> None:
            """
            :param s3: ``CfnRepository.CodeProperty.S3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-code.html
            """
            self._values = {
                's3': s3,
            }

        @builtins.property
        def s3(self) -> typing.Union["CfnRepository.S3Property", _IResolvable_9ceae33e]:
            """``CfnRepository.CodeProperty.S3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-code.html#cfn-codecommit-repository-code-s3
            """
            return self._values.get('s3')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CodeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codecommit.CfnRepository.RepositoryTriggerProperty", jsii_struct_bases=[], name_mapping={'destination_arn': 'destinationArn', 'events': 'events', 'name': 'name', 'branches': 'branches', 'custom_data': 'customData'})
    class RepositoryTriggerProperty():
        def __init__(self, *, destination_arn: str, events: typing.List[str], name: str, branches: typing.Optional[typing.List[str]]=None, custom_data: typing.Optional[str]=None) -> None:
            """
            :param destination_arn: ``CfnRepository.RepositoryTriggerProperty.DestinationArn``.
            :param events: ``CfnRepository.RepositoryTriggerProperty.Events``.
            :param name: ``CfnRepository.RepositoryTriggerProperty.Name``.
            :param branches: ``CfnRepository.RepositoryTriggerProperty.Branches``.
            :param custom_data: ``CfnRepository.RepositoryTriggerProperty.CustomData``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html
            """
            self._values = {
                'destination_arn': destination_arn,
                'events': events,
                'name': name,
            }
            if branches is not None: self._values["branches"] = branches
            if custom_data is not None: self._values["custom_data"] = custom_data

        @builtins.property
        def destination_arn(self) -> str:
            """``CfnRepository.RepositoryTriggerProperty.DestinationArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-destinationarn
            """
            return self._values.get('destination_arn')

        @builtins.property
        def events(self) -> typing.List[str]:
            """``CfnRepository.RepositoryTriggerProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-events
            """
            return self._values.get('events')

        @builtins.property
        def name(self) -> str:
            """``CfnRepository.RepositoryTriggerProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-name
            """
            return self._values.get('name')

        @builtins.property
        def branches(self) -> typing.Optional[typing.List[str]]:
            """``CfnRepository.RepositoryTriggerProperty.Branches``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-branches
            """
            return self._values.get('branches')

        @builtins.property
        def custom_data(self) -> typing.Optional[str]:
            """``CfnRepository.RepositoryTriggerProperty.CustomData``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-customdata
            """
            return self._values.get('custom_data')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RepositoryTriggerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codecommit.CfnRepository.S3Property", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'key': 'key', 'object_version': 'objectVersion'})
    class S3Property():
        def __init__(self, *, bucket: str, key: str, object_version: typing.Optional[str]=None) -> None:
            """
            :param bucket: ``CfnRepository.S3Property.Bucket``.
            :param key: ``CfnRepository.S3Property.Key``.
            :param object_version: ``CfnRepository.S3Property.ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html
            """
            self._values = {
                'bucket': bucket,
                'key': key,
            }
            if object_version is not None: self._values["object_version"] = object_version

        @builtins.property
        def bucket(self) -> str:
            """``CfnRepository.S3Property.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-bucket
            """
            return self._values.get('bucket')

        @builtins.property
        def key(self) -> str:
            """``CfnRepository.S3Property.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-key
            """
            return self._values.get('key')

        @builtins.property
        def object_version(self) -> typing.Optional[str]:
            """``CfnRepository.S3Property.ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-objectversion
            """
            return self._values.get('object_version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3Property(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_codecommit.CfnRepositoryProps", jsii_struct_bases=[], name_mapping={'repository_name': 'repositoryName', 'code': 'code', 'repository_description': 'repositoryDescription', 'tags': 'tags', 'triggers': 'triggers'})
class CfnRepositoryProps():
    def __init__(self, *, repository_name: str, code: typing.Optional[typing.Union["CfnRepository.CodeProperty", _IResolvable_9ceae33e]]=None, repository_description: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, triggers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRepository.RepositoryTriggerProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Properties for defining a ``AWS::CodeCommit::Repository``.

        :param repository_name: ``AWS::CodeCommit::Repository.RepositoryName``.
        :param code: ``AWS::CodeCommit::Repository.Code``.
        :param repository_description: ``AWS::CodeCommit::Repository.RepositoryDescription``.
        :param tags: ``AWS::CodeCommit::Repository.Tags``.
        :param triggers: ``AWS::CodeCommit::Repository.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html
        """
        self._values = {
            'repository_name': repository_name,
        }
        if code is not None: self._values["code"] = code
        if repository_description is not None: self._values["repository_description"] = repository_description
        if tags is not None: self._values["tags"] = tags
        if triggers is not None: self._values["triggers"] = triggers

    @builtins.property
    def repository_name(self) -> str:
        """``AWS::CodeCommit::Repository.RepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositoryname
        """
        return self._values.get('repository_name')

    @builtins.property
    def code(self) -> typing.Optional[typing.Union["CfnRepository.CodeProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeCommit::Repository.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-code
        """
        return self._values.get('code')

    @builtins.property
    def repository_description(self) -> typing.Optional[str]:
        """``AWS::CodeCommit::Repository.RepositoryDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositorydescription
        """
        return self._values.get('repository_description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::CodeCommit::Repository.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-tags
        """
        return self._values.get('tags')

    @builtins.property
    def triggers(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRepository.RepositoryTriggerProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeCommit::Repository.Triggers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-triggers
        """
        return self._values.get('triggers')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRepositoryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_codecommit.IRepository")
class IRepository(_IResource_72f7ee7e, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRepositoryProxy

    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of this Repository.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        """The HTTP clone URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        """The SSH clone URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The human-visible name of this Repository.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: _IGrantable_0fcfc53a, *actions: str) -> _Grant_96af6d2d:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to pull this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to pull and push this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to read this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, id: str, *, branches: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        :param id: -
        :param branches: The branch to monitor. Default: - All branches
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a pull request state is changed.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...


class _IRepositoryProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codecommit.IRepository"
    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of this Repository.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "repositoryArn")

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        """The HTTP clone URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "repositoryCloneUrlHttp")

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        """The SSH clone URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "repositoryCloneUrlSsh")

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The human-visible name of this Repository.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "repositoryName")

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: _IGrantable_0fcfc53a, *actions: str) -> _Grant_96af6d2d:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to pull this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to pull and push this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to read this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCommentOnCommit", [id, options])

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCommentOnPullRequest", [id, options])

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, id: str, *, branches: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        :param id: -
        :param branches: The branch to monitor. Default: - All branches
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = OnCommitOptions(branches=branches, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCommit", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a pull request state is changed.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onPullRequestStateChange", [id, options])

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onReferenceCreated", [id, options])

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onReferenceDeleted", [id, options])

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onReferenceUpdated", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onStateChange", [id, options])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codecommit.OnCommitOptions", jsii_struct_bases=[_OnEventOptions_926fbcf9], name_mapping={'description': 'description', 'event_pattern': 'eventPattern', 'rule_name': 'ruleName', 'target': 'target', 'branches': 'branches'})
class OnCommitOptions(_OnEventOptions_926fbcf9):
    def __init__(self, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None, branches: typing.Optional[typing.List[str]]=None) -> None:
        """Options for the onCommit() method.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param branches: The branch to monitor. Default: - All branches

        stability
        :stability: experimental
        """
        if isinstance(event_pattern, dict): event_pattern = _EventPattern_8aa7b781(**event_pattern)
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if event_pattern is not None: self._values["event_pattern"] = event_pattern
        if rule_name is not None: self._values["rule_name"] = rule_name
        if target is not None: self._values["target"] = target
        if branches is not None: self._values["branches"] = branches

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the rule's purpose.

        default
        :default: - No description

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def event_pattern(self) -> typing.Optional[_EventPattern_8aa7b781]:
        """Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        default
        :default: - No additional filtering based on an event pattern.

        see
        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        stability
        :stability: experimental
        """
        return self._values.get('event_pattern')

    @builtins.property
    def rule_name(self) -> typing.Optional[str]:
        """A name for the rule.

        default
        :default: AWS CloudFormation generates a unique physical ID.

        stability
        :stability: experimental
        """
        return self._values.get('rule_name')

    @builtins.property
    def target(self) -> typing.Optional[_IRuleTarget_41800a77]:
        """The target to register for the event.

        default
        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        return self._values.get('target')

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[str]]:
        """The branch to monitor.

        default
        :default: - All branches

        stability
        :stability: experimental
        """
        return self._values.get('branches')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'OnCommitOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ReferenceEvent(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codecommit.ReferenceEvent"):
    """Fields of CloudWatch Events that change references.

    see
    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#codebuild_event_type
    stability
    :stability: experimental
    """
    @jsii.python.classproperty
    @jsii.member(jsii_name="commitId")
    def commit_id(cls) -> str:
        """Commit id this reference now points to.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "commitId")

    @jsii.python.classproperty
    @jsii.member(jsii_name="eventType")
    def event_type(cls) -> str:
        """The type of reference event.

        'referenceCreated', 'referenceUpdated' or 'referenceDeleted'

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "eventType")

    @jsii.python.classproperty
    @jsii.member(jsii_name="referenceFullName")
    def reference_full_name(cls) -> str:
        """Full reference name.

        For example, 'refs/tags/myTag'

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "referenceFullName")

    @jsii.python.classproperty
    @jsii.member(jsii_name="referenceName")
    def reference_name(cls) -> str:
        """Name of reference changed (branch or tag name).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "referenceName")

    @jsii.python.classproperty
    @jsii.member(jsii_name="referenceType")
    def reference_type(cls) -> str:
        """Type of reference changed.

        'branch' or 'tag'

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "referenceType")

    @jsii.python.classproperty
    @jsii.member(jsii_name="repositoryId")
    def repository_id(cls) -> str:
        """Id of the CodeCommit repository.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "repositoryId")

    @jsii.python.classproperty
    @jsii.member(jsii_name="repositoryName")
    def repository_name(cls) -> str:
        """Name of the CodeCommit repository.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "repositoryName")


@jsii.implements(IRepository)
class Repository(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codecommit.Repository"):
    """Provides a CodeCommit Repository.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, repository_name: str, description: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param repository_name: Name of the repository. This property is required for all CodeCommit repositories.
        :param description: A description of the repository. Use the description to identify the purpose of the repository. Default: - No description.

        stability
        :stability: experimental
        """
        props = RepositoryProps(repository_name=repository_name, description=description)

        jsii.create(Repository, self, [scope, id, props])

    @jsii.member(jsii_name="fromRepositoryArn")
    @builtins.classmethod
    def from_repository_arn(cls, scope: _Construct_f50a3f53, id: str, repository_arn: str) -> "IRepository":
        """Imports a codecommit repository.

        :param scope: -
        :param id: -
        :param repository_arn: (e.g. ``arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo``).

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRepositoryArn", [scope, id, repository_arn])

    @jsii.member(jsii_name="fromRepositoryName")
    @builtins.classmethod
    def from_repository_name(cls, scope: _Construct_f50a3f53, id: str, repository_name: str) -> "IRepository":
        """
        :param scope: -
        :param id: -
        :param repository_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRepositoryName", [scope, id, repository_name])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: _IGrantable_0fcfc53a, *actions: str) -> _Grant_96af6d2d:
        """Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to pull this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to pull and push this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to read this repository.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="notify")
    def notify(self, arn: str, *, branches: typing.Optional[typing.List[str]]=None, custom_data: typing.Optional[str]=None, events: typing.Optional[typing.List["RepositoryEventTrigger"]]=None, name: typing.Optional[str]=None) -> "Repository":
        """Create a trigger to notify another service to run actions on repository events.

        :param arn: Arn of the resource that repository events will notify.
        :param branches: The names of the branches in the AWS CodeCommit repository that contain events that you want to include in the trigger. If you don't specify at least one branch, the trigger applies to all branches.
        :param custom_data: When an event is triggered, additional information that AWS CodeCommit includes when it sends information to the target.
        :param events: The repository events for which AWS CodeCommit sends information to the target, which you specified in the DestinationArn property.If you don't specify events, the trigger runs for all repository events.
        :param name: A name for the trigger.Triggers on a repository must have unique names.

        stability
        :stability: experimental
        """
        options = RepositoryTriggerOptions(branches=branches, custom_data=custom_data, events=events, name=name)

        return jsii.invoke(self, "notify", [arn, options])

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCommentOnCommit", [id, options])

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCommentOnPullRequest", [id, options])

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, id: str, *, branches: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        :param id: -
        :param branches: The branch to monitor. Default: - All branches
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = OnCommitOptions(branches=branches, description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onCommit", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a pull request state is changed.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onPullRequestStateChange", [id, options])

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onReferenceCreated", [id, options])

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onReferenceDeleted", [id, options])

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onReferenceUpdated", [id, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[_EventPattern_8aa7b781]=None, rule_name: typing.Optional[str]=None, target: typing.Optional[_IRuleTarget_41800a77]=None) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(description=description, event_pattern=event_pattern, rule_name=rule_name, target=target)

        return jsii.invoke(self, "onStateChange", [id, options])

    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of this Repository.

        stability
        :stability: experimental
        """
        return jsii.get(self, "repositoryArn")

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        """The HTTP clone URL.

        stability
        :stability: experimental
        """
        return jsii.get(self, "repositoryCloneUrlHttp")

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        """The SSH clone URL.

        stability
        :stability: experimental
        """
        return jsii.get(self, "repositoryCloneUrlSsh")

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The human-visible name of this Repository.

        stability
        :stability: experimental
        """
        return jsii.get(self, "repositoryName")


@jsii.enum(jsii_type="monocdk-experiment.aws_codecommit.RepositoryEventTrigger")
class RepositoryEventTrigger(enum.Enum):
    """Repository events that will cause the trigger to run actions in another service.

    stability
    :stability: experimental
    """
    ALL = "ALL"
    """
    stability
    :stability: experimental
    """
    UPDATE_REF = "UPDATE_REF"
    """
    stability
    :stability: experimental
    """
    CREATE_REF = "CREATE_REF"
    """
    stability
    :stability: experimental
    """
    DELETE_REF = "DELETE_REF"
    """
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_codecommit.RepositoryProps", jsii_struct_bases=[], name_mapping={'repository_name': 'repositoryName', 'description': 'description'})
class RepositoryProps():
    def __init__(self, *, repository_name: str, description: typing.Optional[str]=None) -> None:
        """
        :param repository_name: Name of the repository. This property is required for all CodeCommit repositories.
        :param description: A description of the repository. Use the description to identify the purpose of the repository. Default: - No description.

        stability
        :stability: experimental
        """
        self._values = {
            'repository_name': repository_name,
        }
        if description is not None: self._values["description"] = description

    @builtins.property
    def repository_name(self) -> str:
        """Name of the repository.

        This property is required for all CodeCommit repositories.

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the repository.

        Use the description to identify the
        purpose of the repository.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RepositoryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codecommit.RepositoryTriggerOptions", jsii_struct_bases=[], name_mapping={'branches': 'branches', 'custom_data': 'customData', 'events': 'events', 'name': 'name'})
class RepositoryTriggerOptions():
    def __init__(self, *, branches: typing.Optional[typing.List[str]]=None, custom_data: typing.Optional[str]=None, events: typing.Optional[typing.List["RepositoryEventTrigger"]]=None, name: typing.Optional[str]=None) -> None:
        """Creates for a repository trigger to an SNS topic or Lambda function.

        :param branches: The names of the branches in the AWS CodeCommit repository that contain events that you want to include in the trigger. If you don't specify at least one branch, the trigger applies to all branches.
        :param custom_data: When an event is triggered, additional information that AWS CodeCommit includes when it sends information to the target.
        :param events: The repository events for which AWS CodeCommit sends information to the target, which you specified in the DestinationArn property.If you don't specify events, the trigger runs for all repository events.
        :param name: A name for the trigger.Triggers on a repository must have unique names.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if branches is not None: self._values["branches"] = branches
        if custom_data is not None: self._values["custom_data"] = custom_data
        if events is not None: self._values["events"] = events
        if name is not None: self._values["name"] = name

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[str]]:
        """The names of the branches in the AWS CodeCommit repository that contain events that you want to include in the trigger.

        If you don't specify at
        least one branch, the trigger applies to all branches.

        stability
        :stability: experimental
        """
        return self._values.get('branches')

    @builtins.property
    def custom_data(self) -> typing.Optional[str]:
        """When an event is triggered, additional information that AWS CodeCommit includes when it sends information to the target.

        stability
        :stability: experimental
        """
        return self._values.get('custom_data')

    @builtins.property
    def events(self) -> typing.Optional[typing.List["RepositoryEventTrigger"]]:
        """The repository events for which AWS CodeCommit sends information to the target, which you specified in the DestinationArn property.If you don't specify events, the trigger runs for all repository events.

        stability
        :stability: experimental
        """
        return self._values.get('events')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """A name for the trigger.Triggers on a repository must have unique names.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RepositoryTriggerOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnRepository",
    "CfnRepositoryProps",
    "IRepository",
    "OnCommitOptions",
    "ReferenceEvent",
    "Repository",
    "RepositoryEventTrigger",
    "RepositoryProps",
    "RepositoryTriggerOptions",
]

publication.publish()
