import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Resource as _Resource_884d0774, Construct as _Construct_f50a3f53, SecretValue as _SecretValue_99478b8b, CfnResource as _CfnResource_7760e8e4, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a, IResource as _IResource_72f7ee7e)
from ..aws_codebuild import (BuildSpec as _BuildSpec_2207fbc6)
from ..aws_codecommit import (IRepository as _IRepository_91f381de)
from ..aws_iam import (IPrincipal as _IPrincipal_97126874, IGrantable as _IGrantable_0fcfc53a, IRole as _IRole_e69bbae4)
from ..aws_kms import (IKey as _IKey_3336c79d)


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.AppProps", jsii_struct_bases=[], name_mapping={'app_name': 'appName', 'auto_branch_creation': 'autoBranchCreation', 'basic_auth': 'basicAuth', 'build_spec': 'buildSpec', 'custom_rules': 'customRules', 'description': 'description', 'environment_variables': 'environmentVariables', 'role': 'role', 'source_code_provider': 'sourceCodeProvider'})
class AppProps():
    def __init__(self, *, app_name: typing.Optional[str]=None, auto_branch_creation: typing.Optional["AutoBranchCreation"]=None, basic_auth: typing.Optional["BasicAuth"]=None, build_spec: typing.Optional[_BuildSpec_2207fbc6]=None, custom_rules: typing.Optional[typing.List["CustomRule"]]=None, description: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Mapping[str, str]]=None, role: typing.Optional[_IRole_e69bbae4]=None, source_code_provider: typing.Optional["ISourceCodeProvider"]=None) -> None:
        """Properties for an App.

        :param app_name: The name for the application. Default: - a CDK generated name
        :param auto_branch_creation: The auto branch creation configuration. Use this to automatically create branches that match a certain pattern. Default: - no auto branch creation
        :param basic_auth: The Basic Auth configuration. Use this to set password protection at an app level to all your branches. Default: - no password protection
        :param build_spec: BuildSpec for the application. Alternatively, add a ``amplify.yml`` file to the repository. Default: - no build spec
        :param custom_rules: Custom rewrite/redirect rules for the application. Default: - no custom rewrite/redirect rules
        :param description: A description for the application. Default: - no description
        :param environment_variables: Environment variables for the application. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - no environment variables
        :param role: The IAM service role to associate with the application. The App implements IGrantable. Default: - a new role is created
        :param source_code_provider: The source code provider for this application. Default: - not connected to a source code provider

        stability
        :stability: experimental
        """
        if isinstance(auto_branch_creation, dict): auto_branch_creation = AutoBranchCreation(**auto_branch_creation)
        self._values = {
        }
        if app_name is not None: self._values["app_name"] = app_name
        if auto_branch_creation is not None: self._values["auto_branch_creation"] = auto_branch_creation
        if basic_auth is not None: self._values["basic_auth"] = basic_auth
        if build_spec is not None: self._values["build_spec"] = build_spec
        if custom_rules is not None: self._values["custom_rules"] = custom_rules
        if description is not None: self._values["description"] = description
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if role is not None: self._values["role"] = role
        if source_code_provider is not None: self._values["source_code_provider"] = source_code_provider

    @builtins.property
    def app_name(self) -> typing.Optional[str]:
        """The name for the application.

        default
        :default: - a CDK generated name

        stability
        :stability: experimental
        """
        return self._values.get('app_name')

    @builtins.property
    def auto_branch_creation(self) -> typing.Optional["AutoBranchCreation"]:
        """The auto branch creation configuration.

        Use this to automatically create
        branches that match a certain pattern.

        default
        :default: - no auto branch creation

        stability
        :stability: experimental
        """
        return self._values.get('auto_branch_creation')

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        """The Basic Auth configuration.

        Use this to set password protection at an
        app level to all your branches.

        default
        :default: - no password protection

        stability
        :stability: experimental
        """
        return self._values.get('basic_auth')

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_2207fbc6]:
        """BuildSpec for the application.

        Alternatively, add a ``amplify.yml``
        file to the repository.

        default
        :default: - no build spec

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        stability
        :stability: experimental
        """
        return self._values.get('build_spec')

    @builtins.property
    def custom_rules(self) -> typing.Optional[typing.List["CustomRule"]]:
        """Custom rewrite/redirect rules for the application.

        default
        :default: - no custom rewrite/redirect rules

        stability
        :stability: experimental
        """
        return self._values.get('custom_rules')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description for the application.

        default
        :default: - no description

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables for the application.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        default
        :default: - no environment variables

        stability
        :stability: experimental
        """
        return self._values.get('environment_variables')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM service role to associate with the application.

        The App
        implements IGrantable.

        default
        :default: - a new role is created

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def source_code_provider(self) -> typing.Optional["ISourceCodeProvider"]:
        """The source code provider for this application.

        default
        :default: - not connected to a source code provider

        stability
        :stability: experimental
        """
        return self._values.get('source_code_provider')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.AutoBranchCreation", jsii_struct_bases=[], name_mapping={'auto_build': 'autoBuild', 'basic_auth': 'basicAuth', 'build_spec': 'buildSpec', 'environment_variables': 'environmentVariables', 'patterns': 'patterns', 'pull_request_environment_name': 'pullRequestEnvironmentName', 'pull_request_preview': 'pullRequestPreview', 'stage': 'stage'})
class AutoBranchCreation():
    def __init__(self, *, auto_build: typing.Optional[bool]=None, basic_auth: typing.Optional["BasicAuth"]=None, build_spec: typing.Optional[_BuildSpec_2207fbc6]=None, environment_variables: typing.Optional[typing.Mapping[str, str]]=None, patterns: typing.Optional[typing.List[str]]=None, pull_request_environment_name: typing.Optional[str]=None, pull_request_preview: typing.Optional[bool]=None, stage: typing.Optional[str]=None) -> None:
        """Auto branch creation configuration.

        :param auto_build: Whether to enable auto building for the auto created branch. Default: true
        :param basic_auth: The Basic Auth configuration. Use this to set password protection for the auto created branch. Default: - no password protection
        :param build_spec: Build spec for the auto created branch. Default: - application build spec
        :param environment_variables: Environment variables for the auto created branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param patterns: Automated branch creation glob patterns. Default: - all repository branches
        :param pull_request_environment_name: The dedicated backend environment for the pull request previews of the auto created branch. Default: - automatically provision a temporary backend
        :param pull_request_preview: Whether to enable pull request preview for the auto created branch. Default: true
        :param stage: Stage for the auto created branch. Default: - no stage

        stability
        :stability: experimental
        """
        self._values = {
        }
        if auto_build is not None: self._values["auto_build"] = auto_build
        if basic_auth is not None: self._values["basic_auth"] = basic_auth
        if build_spec is not None: self._values["build_spec"] = build_spec
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if patterns is not None: self._values["patterns"] = patterns
        if pull_request_environment_name is not None: self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None: self._values["pull_request_preview"] = pull_request_preview
        if stage is not None: self._values["stage"] = stage

    @builtins.property
    def auto_build(self) -> typing.Optional[bool]:
        """Whether to enable auto building for the auto created branch.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('auto_build')

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        """The Basic Auth configuration.

        Use this to set password protection for
        the auto created branch.

        default
        :default: - no password protection

        stability
        :stability: experimental
        """
        return self._values.get('basic_auth')

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_2207fbc6]:
        """Build spec for the auto created branch.

        default
        :default: - application build spec

        stability
        :stability: experimental
        """
        return self._values.get('build_spec')

    @builtins.property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables for the auto created branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        default
        :default: - application environment variables

        stability
        :stability: experimental
        """
        return self._values.get('environment_variables')

    @builtins.property
    def patterns(self) -> typing.Optional[typing.List[str]]:
        """Automated branch creation glob patterns.

        default
        :default: - all repository branches

        stability
        :stability: experimental
        """
        return self._values.get('patterns')

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[str]:
        """The dedicated backend environment for the pull request previews of the auto created branch.

        default
        :default: - automatically provision a temporary backend

        stability
        :stability: experimental
        """
        return self._values.get('pull_request_environment_name')

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[bool]:
        """Whether to enable pull request preview for the auto created branch.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('pull_request_preview')

    @builtins.property
    def stage(self) -> typing.Optional[str]:
        """Stage for the auto created branch.

        default
        :default: - no stage

        stability
        :stability: experimental
        """
        return self._values.get('stage')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AutoBranchCreation(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class BasicAuth(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.BasicAuth"):
    """Basic Auth configuration.

    stability
    :stability: experimental
    """
    def __init__(self, *, username: str, encryption_key: typing.Optional[_IKey_3336c79d]=None, password: typing.Optional[_SecretValue_99478b8b]=None) -> None:
        """
        :param username: The username.
        :param encryption_key: The encryption key to use to encrypt the password when it's generated in Secrets Manager. Default: - default master key
        :param password: The password. Default: - A Secrets Manager generated password

        stability
        :stability: experimental
        """
        props = BasicAuthProps(username=username, encryption_key=encryption_key, password=password)

        jsii.create(BasicAuth, self, [props])

    @jsii.member(jsii_name="fromCredentials")
    @builtins.classmethod
    def from_credentials(cls, username: str, password: _SecretValue_99478b8b) -> "BasicAuth":
        """Creates a Basic Auth configuration from a username and a password.

        :param username: The username.
        :param password: The password.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCredentials", [username, password])

    @jsii.member(jsii_name="fromGeneratedPassword")
    @builtins.classmethod
    def from_generated_password(cls, username: str, encryption_key: typing.Optional[_IKey_3336c79d]=None) -> "BasicAuth":
        """Creates a Basic Auth configuration with a password generated in Secrets Manager.

        :param username: The username.
        :param encryption_key: The encryption key to use to encrypt the password in Secrets Manager.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromGeneratedPassword", [username, encryption_key])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, id: str) -> "BasicAuthConfig":
        """Binds this Basic Auth configuration to an App.

        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, id])


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.BasicAuthConfig", jsii_struct_bases=[], name_mapping={'enable_basic_auth': 'enableBasicAuth', 'password': 'password', 'username': 'username'})
class BasicAuthConfig():
    def __init__(self, *, enable_basic_auth: bool, password: str, username: str) -> None:
        """A Basic Auth configuration.

        :param enable_basic_auth: Whether to enable Basic Auth.
        :param password: The password.
        :param username: The username.

        stability
        :stability: experimental
        """
        self._values = {
            'enable_basic_auth': enable_basic_auth,
            'password': password,
            'username': username,
        }

    @builtins.property
    def enable_basic_auth(self) -> bool:
        """Whether to enable Basic Auth.

        stability
        :stability: experimental
        """
        return self._values.get('enable_basic_auth')

    @builtins.property
    def password(self) -> str:
        """The password.

        stability
        :stability: experimental
        """
        return self._values.get('password')

    @builtins.property
    def username(self) -> str:
        """The username.

        stability
        :stability: experimental
        """
        return self._values.get('username')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasicAuthConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.BasicAuthProps", jsii_struct_bases=[], name_mapping={'username': 'username', 'encryption_key': 'encryptionKey', 'password': 'password'})
class BasicAuthProps():
    def __init__(self, *, username: str, encryption_key: typing.Optional[_IKey_3336c79d]=None, password: typing.Optional[_SecretValue_99478b8b]=None) -> None:
        """Properties for a BasicAuth.

        :param username: The username.
        :param encryption_key: The encryption key to use to encrypt the password when it's generated in Secrets Manager. Default: - default master key
        :param password: The password. Default: - A Secrets Manager generated password

        stability
        :stability: experimental
        """
        self._values = {
            'username': username,
        }
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if password is not None: self._values["password"] = password

    @builtins.property
    def username(self) -> str:
        """The username.

        stability
        :stability: experimental
        """
        return self._values.get('username')

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The encryption key to use to encrypt the password when it's generated in Secrets Manager.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    @builtins.property
    def password(self) -> typing.Optional[_SecretValue_99478b8b]:
        """The password.

        default
        :default: - A Secrets Manager generated password

        stability
        :stability: experimental
        """
        return self._values.get('password')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BasicAuthProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.BranchOptions", jsii_struct_bases=[], name_mapping={'auto_build': 'autoBuild', 'basic_auth': 'basicAuth', 'branch_name': 'branchName', 'build_spec': 'buildSpec', 'description': 'description', 'environment_variables': 'environmentVariables', 'pull_request_environment_name': 'pullRequestEnvironmentName', 'pull_request_preview': 'pullRequestPreview', 'stage': 'stage'})
class BranchOptions():
    def __init__(self, *, auto_build: typing.Optional[bool]=None, basic_auth: typing.Optional["BasicAuth"]=None, branch_name: typing.Optional[str]=None, build_spec: typing.Optional[_BuildSpec_2207fbc6]=None, description: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Mapping[str, str]]=None, pull_request_environment_name: typing.Optional[str]=None, pull_request_preview: typing.Optional[bool]=None, stage: typing.Optional[str]=None) -> None:
        """Options to add a branch to an application.

        :param auto_build: Whether to enable auto building for the branch. Default: true
        :param basic_auth: The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: The name of the branch. Default: - the construct's id
        :param build_spec: BuildSpec for the branch. Default: - no build spec
        :param description: A description for the branch. Default: - no description
        :param environment_variables: Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param pull_request_environment_name: The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: Whether to enable pull request preview for the branch. Default: true
        :param stage: Stage for the branch. Default: - no stage

        stability
        :stability: experimental
        """
        self._values = {
        }
        if auto_build is not None: self._values["auto_build"] = auto_build
        if basic_auth is not None: self._values["basic_auth"] = basic_auth
        if branch_name is not None: self._values["branch_name"] = branch_name
        if build_spec is not None: self._values["build_spec"] = build_spec
        if description is not None: self._values["description"] = description
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if pull_request_environment_name is not None: self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None: self._values["pull_request_preview"] = pull_request_preview
        if stage is not None: self._values["stage"] = stage

    @builtins.property
    def auto_build(self) -> typing.Optional[bool]:
        """Whether to enable auto building for the branch.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('auto_build')

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        """The Basic Auth configuration.

        Use this to set password protection for
        the branch

        default
        :default: - no password protection

        stability
        :stability: experimental
        """
        return self._values.get('basic_auth')

    @builtins.property
    def branch_name(self) -> typing.Optional[str]:
        """The name of the branch.

        default
        :default: - the construct's id

        stability
        :stability: experimental
        """
        return self._values.get('branch_name')

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_2207fbc6]:
        """BuildSpec for the branch.

        default
        :default: - no build spec

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        stability
        :stability: experimental
        """
        return self._values.get('build_spec')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description for the branch.

        default
        :default: - no description

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables for the branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        default
        :default: - application environment variables

        stability
        :stability: experimental
        """
        return self._values.get('environment_variables')

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[str]:
        """The dedicated backend environment for the pull request previews.

        default
        :default: - automatically provision a temporary backend

        stability
        :stability: experimental
        """
        return self._values.get('pull_request_environment_name')

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[bool]:
        """Whether to enable pull request preview for the branch.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('pull_request_preview')

    @builtins.property
    def stage(self) -> typing.Optional[str]:
        """Stage for the branch.

        default
        :default: - no stage

        stability
        :stability: experimental
        """
        return self._values.get('stage')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BranchOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.BranchProps", jsii_struct_bases=[BranchOptions], name_mapping={'auto_build': 'autoBuild', 'basic_auth': 'basicAuth', 'branch_name': 'branchName', 'build_spec': 'buildSpec', 'description': 'description', 'environment_variables': 'environmentVariables', 'pull_request_environment_name': 'pullRequestEnvironmentName', 'pull_request_preview': 'pullRequestPreview', 'stage': 'stage', 'app': 'app'})
class BranchProps(BranchOptions):
    def __init__(self, *, auto_build: typing.Optional[bool]=None, basic_auth: typing.Optional["BasicAuth"]=None, branch_name: typing.Optional[str]=None, build_spec: typing.Optional[_BuildSpec_2207fbc6]=None, description: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Mapping[str, str]]=None, pull_request_environment_name: typing.Optional[str]=None, pull_request_preview: typing.Optional[bool]=None, stage: typing.Optional[str]=None, app: "IApp") -> None:
        """Properties for a Branch.

        :param auto_build: Whether to enable auto building for the branch. Default: true
        :param basic_auth: The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: The name of the branch. Default: - the construct's id
        :param build_spec: BuildSpec for the branch. Default: - no build spec
        :param description: A description for the branch. Default: - no description
        :param environment_variables: Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param pull_request_environment_name: The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: Whether to enable pull request preview for the branch. Default: true
        :param stage: Stage for the branch. Default: - no stage
        :param app: The application within which the branch must be created.

        stability
        :stability: experimental
        """
        self._values = {
            'app': app,
        }
        if auto_build is not None: self._values["auto_build"] = auto_build
        if basic_auth is not None: self._values["basic_auth"] = basic_auth
        if branch_name is not None: self._values["branch_name"] = branch_name
        if build_spec is not None: self._values["build_spec"] = build_spec
        if description is not None: self._values["description"] = description
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if pull_request_environment_name is not None: self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None: self._values["pull_request_preview"] = pull_request_preview
        if stage is not None: self._values["stage"] = stage

    @builtins.property
    def auto_build(self) -> typing.Optional[bool]:
        """Whether to enable auto building for the branch.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('auto_build')

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        """The Basic Auth configuration.

        Use this to set password protection for
        the branch

        default
        :default: - no password protection

        stability
        :stability: experimental
        """
        return self._values.get('basic_auth')

    @builtins.property
    def branch_name(self) -> typing.Optional[str]:
        """The name of the branch.

        default
        :default: - the construct's id

        stability
        :stability: experimental
        """
        return self._values.get('branch_name')

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_2207fbc6]:
        """BuildSpec for the branch.

        default
        :default: - no build spec

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        stability
        :stability: experimental
        """
        return self._values.get('build_spec')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description for the branch.

        default
        :default: - no description

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def environment_variables(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables for the branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        default
        :default: - application environment variables

        stability
        :stability: experimental
        """
        return self._values.get('environment_variables')

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[str]:
        """The dedicated backend environment for the pull request previews.

        default
        :default: - automatically provision a temporary backend

        stability
        :stability: experimental
        """
        return self._values.get('pull_request_environment_name')

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[bool]:
        """Whether to enable pull request preview for the branch.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('pull_request_preview')

    @builtins.property
    def stage(self) -> typing.Optional[str]:
        """Stage for the branch.

        default
        :default: - no stage

        stability
        :stability: experimental
        """
        return self._values.get('stage')

    @builtins.property
    def app(self) -> "IApp":
        """The application within which the branch must be created.

        stability
        :stability: experimental
        """
        return self._values.get('app')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BranchProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnApp(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.CfnApp"):
    """A CloudFormation ``AWS::Amplify::App``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html
    cloudformationResource:
    :cloudformationResource:: AWS::Amplify::App
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, access_token: typing.Optional[str]=None, auto_branch_creation_config: typing.Optional[typing.Union["AutoBranchCreationConfigProperty", _IResolvable_9ceae33e]]=None, basic_auth_config: typing.Optional[typing.Union["BasicAuthConfigProperty", _IResolvable_9ceae33e]]=None, build_spec: typing.Optional[str]=None, custom_rules: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CustomRuleProperty", _IResolvable_9ceae33e]]]]=None, description: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]=None, iam_service_role: typing.Optional[str]=None, oauth_token: typing.Optional[str]=None, repository: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::Amplify::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Amplify::App.Name``.
        :param access_token: ``AWS::Amplify::App.AccessToken``.
        :param auto_branch_creation_config: ``AWS::Amplify::App.AutoBranchCreationConfig``.
        :param basic_auth_config: ``AWS::Amplify::App.BasicAuthConfig``.
        :param build_spec: ``AWS::Amplify::App.BuildSpec``.
        :param custom_rules: ``AWS::Amplify::App.CustomRules``.
        :param description: ``AWS::Amplify::App.Description``.
        :param environment_variables: ``AWS::Amplify::App.EnvironmentVariables``.
        :param iam_service_role: ``AWS::Amplify::App.IAMServiceRole``.
        :param oauth_token: ``AWS::Amplify::App.OauthToken``.
        :param repository: ``AWS::Amplify::App.Repository``.
        :param tags: ``AWS::Amplify::App.Tags``.
        """
        props = CfnAppProps(name=name, access_token=access_token, auto_branch_creation_config=auto_branch_creation_config, basic_auth_config=basic_auth_config, build_spec=build_spec, custom_rules=custom_rules, description=description, environment_variables=environment_variables, iam_service_role=iam_service_role, oauth_token=oauth_token, repository=repository, tags=tags)

        jsii.create(CfnApp, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnApp":
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
    @jsii.member(jsii_name="attrAppId")
    def attr_app_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: AppId
        """
        return jsii.get(self, "attrAppId")

    @builtins.property
    @jsii.member(jsii_name="attrAppName")
    def attr_app_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: AppName
        """
        return jsii.get(self, "attrAppName")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrDefaultDomain")
    def attr_default_domain(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DefaultDomain
        """
        return jsii.get(self, "attrDefaultDomain")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Amplify::App.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Amplify::App.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.AccessToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-accesstoken
        """
        return jsii.get(self, "accessToken")

    @access_token.setter
    def access_token(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "accessToken", value)

    @builtins.property
    @jsii.member(jsii_name="autoBranchCreationConfig")
    def auto_branch_creation_config(self) -> typing.Optional[typing.Union["AutoBranchCreationConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Amplify::App.AutoBranchCreationConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-autobranchcreationconfig
        """
        return jsii.get(self, "autoBranchCreationConfig")

    @auto_branch_creation_config.setter
    def auto_branch_creation_config(self, value: typing.Optional[typing.Union["AutoBranchCreationConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "autoBranchCreationConfig", value)

    @builtins.property
    @jsii.member(jsii_name="basicAuthConfig")
    def basic_auth_config(self) -> typing.Optional[typing.Union["BasicAuthConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Amplify::App.BasicAuthConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-basicauthconfig
        """
        return jsii.get(self, "basicAuthConfig")

    @basic_auth_config.setter
    def basic_auth_config(self, value: typing.Optional[typing.Union["BasicAuthConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "basicAuthConfig", value)

    @builtins.property
    @jsii.member(jsii_name="buildSpec")
    def build_spec(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.BuildSpec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-buildspec
        """
        return jsii.get(self, "buildSpec")

    @build_spec.setter
    def build_spec(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "buildSpec", value)

    @builtins.property
    @jsii.member(jsii_name="customRules")
    def custom_rules(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CustomRuleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Amplify::App.CustomRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customrules
        """
        return jsii.get(self, "customRules")

    @custom_rules.setter
    def custom_rules(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CustomRuleProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "customRules", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Amplify::App.EnvironmentVariables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-environmentvariables
        """
        return jsii.get(self, "environmentVariables")

    @environment_variables.setter
    def environment_variables(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="iamServiceRole")
    def iam_service_role(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.IAMServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-iamservicerole
        """
        return jsii.get(self, "iamServiceRole")

    @iam_service_role.setter
    def iam_service_role(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "iamServiceRole", value)

    @builtins.property
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.OauthToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-oauthtoken
        """
        return jsii.get(self, "oauthToken")

    @oauth_token.setter
    def oauth_token(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "oauthToken", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.Repository``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-repository
        """
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "repository", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnApp.AutoBranchCreationConfigProperty", jsii_struct_bases=[], name_mapping={'auto_branch_creation_patterns': 'autoBranchCreationPatterns', 'basic_auth_config': 'basicAuthConfig', 'build_spec': 'buildSpec', 'enable_auto_branch_creation': 'enableAutoBranchCreation', 'enable_auto_build': 'enableAutoBuild', 'enable_pull_request_preview': 'enablePullRequestPreview', 'environment_variables': 'environmentVariables', 'pull_request_environment_name': 'pullRequestEnvironmentName', 'stage': 'stage'})
    class AutoBranchCreationConfigProperty():
        def __init__(self, *, auto_branch_creation_patterns: typing.Optional[typing.List[str]]=None, basic_auth_config: typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_9ceae33e]]=None, build_spec: typing.Optional[str]=None, enable_auto_branch_creation: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, enable_auto_build: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, enable_pull_request_preview: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, environment_variables: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]=None, pull_request_environment_name: typing.Optional[str]=None, stage: typing.Optional[str]=None) -> None:
            """
            :param auto_branch_creation_patterns: ``CfnApp.AutoBranchCreationConfigProperty.AutoBranchCreationPatterns``.
            :param basic_auth_config: ``CfnApp.AutoBranchCreationConfigProperty.BasicAuthConfig``.
            :param build_spec: ``CfnApp.AutoBranchCreationConfigProperty.BuildSpec``.
            :param enable_auto_branch_creation: ``CfnApp.AutoBranchCreationConfigProperty.EnableAutoBranchCreation``.
            :param enable_auto_build: ``CfnApp.AutoBranchCreationConfigProperty.EnableAutoBuild``.
            :param enable_pull_request_preview: ``CfnApp.AutoBranchCreationConfigProperty.EnablePullRequestPreview``.
            :param environment_variables: ``CfnApp.AutoBranchCreationConfigProperty.EnvironmentVariables``.
            :param pull_request_environment_name: ``CfnApp.AutoBranchCreationConfigProperty.PullRequestEnvironmentName``.
            :param stage: ``CfnApp.AutoBranchCreationConfigProperty.Stage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html
            """
            self._values = {
            }
            if auto_branch_creation_patterns is not None: self._values["auto_branch_creation_patterns"] = auto_branch_creation_patterns
            if basic_auth_config is not None: self._values["basic_auth_config"] = basic_auth_config
            if build_spec is not None: self._values["build_spec"] = build_spec
            if enable_auto_branch_creation is not None: self._values["enable_auto_branch_creation"] = enable_auto_branch_creation
            if enable_auto_build is not None: self._values["enable_auto_build"] = enable_auto_build
            if enable_pull_request_preview is not None: self._values["enable_pull_request_preview"] = enable_pull_request_preview
            if environment_variables is not None: self._values["environment_variables"] = environment_variables
            if pull_request_environment_name is not None: self._values["pull_request_environment_name"] = pull_request_environment_name
            if stage is not None: self._values["stage"] = stage

        @builtins.property
        def auto_branch_creation_patterns(self) -> typing.Optional[typing.List[str]]:
            """``CfnApp.AutoBranchCreationConfigProperty.AutoBranchCreationPatterns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-autobranchcreationpatterns
            """
            return self._values.get('auto_branch_creation_patterns')

        @builtins.property
        def basic_auth_config(self) -> typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_9ceae33e]]:
            """``CfnApp.AutoBranchCreationConfigProperty.BasicAuthConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-basicauthconfig
            """
            return self._values.get('basic_auth_config')

        @builtins.property
        def build_spec(self) -> typing.Optional[str]:
            """``CfnApp.AutoBranchCreationConfigProperty.BuildSpec``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-buildspec
            """
            return self._values.get('build_spec')

        @builtins.property
        def enable_auto_branch_creation(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnApp.AutoBranchCreationConfigProperty.EnableAutoBranchCreation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableautobranchcreation
            """
            return self._values.get('enable_auto_branch_creation')

        @builtins.property
        def enable_auto_build(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnApp.AutoBranchCreationConfigProperty.EnableAutoBuild``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableautobuild
            """
            return self._values.get('enable_auto_build')

        @builtins.property
        def enable_pull_request_preview(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnApp.AutoBranchCreationConfigProperty.EnablePullRequestPreview``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enablepullrequestpreview
            """
            return self._values.get('enable_pull_request_preview')

        @builtins.property
        def environment_variables(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]:
            """``CfnApp.AutoBranchCreationConfigProperty.EnvironmentVariables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-environmentvariables
            """
            return self._values.get('environment_variables')

        @builtins.property
        def pull_request_environment_name(self) -> typing.Optional[str]:
            """``CfnApp.AutoBranchCreationConfigProperty.PullRequestEnvironmentName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-pullrequestenvironmentname
            """
            return self._values.get('pull_request_environment_name')

        @builtins.property
        def stage(self) -> typing.Optional[str]:
            """``CfnApp.AutoBranchCreationConfigProperty.Stage``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-stage
            """
            return self._values.get('stage')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AutoBranchCreationConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnApp.BasicAuthConfigProperty", jsii_struct_bases=[], name_mapping={'enable_basic_auth': 'enableBasicAuth', 'password': 'password', 'username': 'username'})
    class BasicAuthConfigProperty():
        def __init__(self, *, enable_basic_auth: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, password: typing.Optional[str]=None, username: typing.Optional[str]=None) -> None:
            """
            :param enable_basic_auth: ``CfnApp.BasicAuthConfigProperty.EnableBasicAuth``.
            :param password: ``CfnApp.BasicAuthConfigProperty.Password``.
            :param username: ``CfnApp.BasicAuthConfigProperty.Username``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html
            """
            self._values = {
            }
            if enable_basic_auth is not None: self._values["enable_basic_auth"] = enable_basic_auth
            if password is not None: self._values["password"] = password
            if username is not None: self._values["username"] = username

        @builtins.property
        def enable_basic_auth(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnApp.BasicAuthConfigProperty.EnableBasicAuth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-enablebasicauth
            """
            return self._values.get('enable_basic_auth')

        @builtins.property
        def password(self) -> typing.Optional[str]:
            """``CfnApp.BasicAuthConfigProperty.Password``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-password
            """
            return self._values.get('password')

        @builtins.property
        def username(self) -> typing.Optional[str]:
            """``CfnApp.BasicAuthConfigProperty.Username``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-username
            """
            return self._values.get('username')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BasicAuthConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnApp.CustomRuleProperty", jsii_struct_bases=[], name_mapping={'source': 'source', 'target': 'target', 'condition': 'condition', 'status': 'status'})
    class CustomRuleProperty():
        def __init__(self, *, source: str, target: str, condition: typing.Optional[str]=None, status: typing.Optional[str]=None) -> None:
            """
            :param source: ``CfnApp.CustomRuleProperty.Source``.
            :param target: ``CfnApp.CustomRuleProperty.Target``.
            :param condition: ``CfnApp.CustomRuleProperty.Condition``.
            :param status: ``CfnApp.CustomRuleProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html
            """
            self._values = {
                'source': source,
                'target': target,
            }
            if condition is not None: self._values["condition"] = condition
            if status is not None: self._values["status"] = status

        @builtins.property
        def source(self) -> str:
            """``CfnApp.CustomRuleProperty.Source``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-source
            """
            return self._values.get('source')

        @builtins.property
        def target(self) -> str:
            """``CfnApp.CustomRuleProperty.Target``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-target
            """
            return self._values.get('target')

        @builtins.property
        def condition(self) -> typing.Optional[str]:
            """``CfnApp.CustomRuleProperty.Condition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-condition
            """
            return self._values.get('condition')

        @builtins.property
        def status(self) -> typing.Optional[str]:
            """``CfnApp.CustomRuleProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-status
            """
            return self._values.get('status')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CustomRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnApp.EnvironmentVariableProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class EnvironmentVariableProperty():
        def __init__(self, *, name: str, value: str) -> None:
            """
            :param name: ``CfnApp.EnvironmentVariableProperty.Name``.
            :param value: ``CfnApp.EnvironmentVariableProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html
            """
            self._values = {
                'name': name,
                'value': value,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnApp.EnvironmentVariableProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html#cfn-amplify-app-environmentvariable-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> str:
            """``CfnApp.EnvironmentVariableProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html#cfn-amplify-app-environmentvariable-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EnvironmentVariableProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnAppProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'access_token': 'accessToken', 'auto_branch_creation_config': 'autoBranchCreationConfig', 'basic_auth_config': 'basicAuthConfig', 'build_spec': 'buildSpec', 'custom_rules': 'customRules', 'description': 'description', 'environment_variables': 'environmentVariables', 'iam_service_role': 'iamServiceRole', 'oauth_token': 'oauthToken', 'repository': 'repository', 'tags': 'tags'})
class CfnAppProps():
    def __init__(self, *, name: str, access_token: typing.Optional[str]=None, auto_branch_creation_config: typing.Optional[typing.Union["CfnApp.AutoBranchCreationConfigProperty", _IResolvable_9ceae33e]]=None, basic_auth_config: typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_9ceae33e]]=None, build_spec: typing.Optional[str]=None, custom_rules: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnApp.CustomRuleProperty", _IResolvable_9ceae33e]]]]=None, description: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]=None, iam_service_role: typing.Optional[str]=None, oauth_token: typing.Optional[str]=None, repository: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::Amplify::App``.

        :param name: ``AWS::Amplify::App.Name``.
        :param access_token: ``AWS::Amplify::App.AccessToken``.
        :param auto_branch_creation_config: ``AWS::Amplify::App.AutoBranchCreationConfig``.
        :param basic_auth_config: ``AWS::Amplify::App.BasicAuthConfig``.
        :param build_spec: ``AWS::Amplify::App.BuildSpec``.
        :param custom_rules: ``AWS::Amplify::App.CustomRules``.
        :param description: ``AWS::Amplify::App.Description``.
        :param environment_variables: ``AWS::Amplify::App.EnvironmentVariables``.
        :param iam_service_role: ``AWS::Amplify::App.IAMServiceRole``.
        :param oauth_token: ``AWS::Amplify::App.OauthToken``.
        :param repository: ``AWS::Amplify::App.Repository``.
        :param tags: ``AWS::Amplify::App.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html
        """
        self._values = {
            'name': name,
        }
        if access_token is not None: self._values["access_token"] = access_token
        if auto_branch_creation_config is not None: self._values["auto_branch_creation_config"] = auto_branch_creation_config
        if basic_auth_config is not None: self._values["basic_auth_config"] = basic_auth_config
        if build_spec is not None: self._values["build_spec"] = build_spec
        if custom_rules is not None: self._values["custom_rules"] = custom_rules
        if description is not None: self._values["description"] = description
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if iam_service_role is not None: self._values["iam_service_role"] = iam_service_role
        if oauth_token is not None: self._values["oauth_token"] = oauth_token
        if repository is not None: self._values["repository"] = repository
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def name(self) -> str:
        """``AWS::Amplify::App.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-name
        """
        return self._values.get('name')

    @builtins.property
    def access_token(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.AccessToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-accesstoken
        """
        return self._values.get('access_token')

    @builtins.property
    def auto_branch_creation_config(self) -> typing.Optional[typing.Union["CfnApp.AutoBranchCreationConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Amplify::App.AutoBranchCreationConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-autobranchcreationconfig
        """
        return self._values.get('auto_branch_creation_config')

    @builtins.property
    def basic_auth_config(self) -> typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Amplify::App.BasicAuthConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-basicauthconfig
        """
        return self._values.get('basic_auth_config')

    @builtins.property
    def build_spec(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.BuildSpec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-buildspec
        """
        return self._values.get('build_spec')

    @builtins.property
    def custom_rules(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnApp.CustomRuleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Amplify::App.CustomRules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customrules
        """
        return self._values.get('custom_rules')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-description
        """
        return self._values.get('description')

    @builtins.property
    def environment_variables(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Amplify::App.EnvironmentVariables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-environmentvariables
        """
        return self._values.get('environment_variables')

    @builtins.property
    def iam_service_role(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.IAMServiceRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-iamservicerole
        """
        return self._values.get('iam_service_role')

    @builtins.property
    def oauth_token(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.OauthToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-oauthtoken
        """
        return self._values.get('oauth_token')

    @builtins.property
    def repository(self) -> typing.Optional[str]:
        """``AWS::Amplify::App.Repository``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-repository
        """
        return self._values.get('repository')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Amplify::App.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAppProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnBranch(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.CfnBranch"):
    """A CloudFormation ``AWS::Amplify::Branch``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html
    cloudformationResource:
    :cloudformationResource:: AWS::Amplify::Branch
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, app_id: str, branch_name: str, basic_auth_config: typing.Optional[typing.Union["BasicAuthConfigProperty", _IResolvable_9ceae33e]]=None, build_spec: typing.Optional[str]=None, description: typing.Optional[str]=None, enable_auto_build: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, enable_pull_request_preview: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, environment_variables: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]=None, pull_request_environment_name: typing.Optional[str]=None, stage: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::Amplify::Branch``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_id: ``AWS::Amplify::Branch.AppId``.
        :param branch_name: ``AWS::Amplify::Branch.BranchName``.
        :param basic_auth_config: ``AWS::Amplify::Branch.BasicAuthConfig``.
        :param build_spec: ``AWS::Amplify::Branch.BuildSpec``.
        :param description: ``AWS::Amplify::Branch.Description``.
        :param enable_auto_build: ``AWS::Amplify::Branch.EnableAutoBuild``.
        :param enable_pull_request_preview: ``AWS::Amplify::Branch.EnablePullRequestPreview``.
        :param environment_variables: ``AWS::Amplify::Branch.EnvironmentVariables``.
        :param pull_request_environment_name: ``AWS::Amplify::Branch.PullRequestEnvironmentName``.
        :param stage: ``AWS::Amplify::Branch.Stage``.
        :param tags: ``AWS::Amplify::Branch.Tags``.
        """
        props = CfnBranchProps(app_id=app_id, branch_name=branch_name, basic_auth_config=basic_auth_config, build_spec=build_spec, description=description, enable_auto_build=enable_auto_build, enable_pull_request_preview=enable_pull_request_preview, environment_variables=environment_variables, pull_request_environment_name=pull_request_environment_name, stage=stage, tags=tags)

        jsii.create(CfnBranch, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnBranch":
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
    @jsii.member(jsii_name="attrBranchName")
    def attr_branch_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: BranchName
        """
        return jsii.get(self, "attrBranchName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Amplify::Branch.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> str:
        """``AWS::Amplify::Branch.AppId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-appid
        """
        return jsii.get(self, "appId")

    @app_id.setter
    def app_id(self, value: str) -> None:
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> str:
        """``AWS::Amplify::Branch.BranchName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-branchname
        """
        return jsii.get(self, "branchName")

    @branch_name.setter
    def branch_name(self, value: str) -> None:
        jsii.set(self, "branchName", value)

    @builtins.property
    @jsii.member(jsii_name="basicAuthConfig")
    def basic_auth_config(self) -> typing.Optional[typing.Union["BasicAuthConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Amplify::Branch.BasicAuthConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-basicauthconfig
        """
        return jsii.get(self, "basicAuthConfig")

    @basic_auth_config.setter
    def basic_auth_config(self, value: typing.Optional[typing.Union["BasicAuthConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "basicAuthConfig", value)

    @builtins.property
    @jsii.member(jsii_name="buildSpec")
    def build_spec(self) -> typing.Optional[str]:
        """``AWS::Amplify::Branch.BuildSpec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-buildspec
        """
        return jsii.get(self, "buildSpec")

    @build_spec.setter
    def build_spec(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "buildSpec", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Amplify::Branch.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enableAutoBuild")
    def enable_auto_build(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Amplify::Branch.EnableAutoBuild``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableautobuild
        """
        return jsii.get(self, "enableAutoBuild")

    @enable_auto_build.setter
    def enable_auto_build(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "enableAutoBuild", value)

    @builtins.property
    @jsii.member(jsii_name="enablePullRequestPreview")
    def enable_pull_request_preview(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Amplify::Branch.EnablePullRequestPreview``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enablepullrequestpreview
        """
        return jsii.get(self, "enablePullRequestPreview")

    @enable_pull_request_preview.setter
    def enable_pull_request_preview(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "enablePullRequestPreview", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Amplify::Branch.EnvironmentVariables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-environmentvariables
        """
        return jsii.get(self, "environmentVariables")

    @environment_variables.setter
    def environment_variables(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> typing.Optional[str]:
        """``AWS::Amplify::Branch.PullRequestEnvironmentName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-pullrequestenvironmentname
        """
        return jsii.get(self, "pullRequestEnvironmentName")

    @pull_request_environment_name.setter
    def pull_request_environment_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "pullRequestEnvironmentName", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional[str]:
        """``AWS::Amplify::Branch.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-stage
        """
        return jsii.get(self, "stage")

    @stage.setter
    def stage(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "stage", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnBranch.BasicAuthConfigProperty", jsii_struct_bases=[], name_mapping={'password': 'password', 'username': 'username', 'enable_basic_auth': 'enableBasicAuth'})
    class BasicAuthConfigProperty():
        def __init__(self, *, password: str, username: str, enable_basic_auth: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param password: ``CfnBranch.BasicAuthConfigProperty.Password``.
            :param username: ``CfnBranch.BasicAuthConfigProperty.Username``.
            :param enable_basic_auth: ``CfnBranch.BasicAuthConfigProperty.EnableBasicAuth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html
            """
            self._values = {
                'password': password,
                'username': username,
            }
            if enable_basic_auth is not None: self._values["enable_basic_auth"] = enable_basic_auth

        @builtins.property
        def password(self) -> str:
            """``CfnBranch.BasicAuthConfigProperty.Password``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-password
            """
            return self._values.get('password')

        @builtins.property
        def username(self) -> str:
            """``CfnBranch.BasicAuthConfigProperty.Username``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-username
            """
            return self._values.get('username')

        @builtins.property
        def enable_basic_auth(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnBranch.BasicAuthConfigProperty.EnableBasicAuth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-enablebasicauth
            """
            return self._values.get('enable_basic_auth')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BasicAuthConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnBranch.EnvironmentVariableProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class EnvironmentVariableProperty():
        def __init__(self, *, name: str, value: str) -> None:
            """
            :param name: ``CfnBranch.EnvironmentVariableProperty.Name``.
            :param value: ``CfnBranch.EnvironmentVariableProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html
            """
            self._values = {
                'name': name,
                'value': value,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnBranch.EnvironmentVariableProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html#cfn-amplify-branch-environmentvariable-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> str:
            """``CfnBranch.EnvironmentVariableProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html#cfn-amplify-branch-environmentvariable-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EnvironmentVariableProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnBranchProps", jsii_struct_bases=[], name_mapping={'app_id': 'appId', 'branch_name': 'branchName', 'basic_auth_config': 'basicAuthConfig', 'build_spec': 'buildSpec', 'description': 'description', 'enable_auto_build': 'enableAutoBuild', 'enable_pull_request_preview': 'enablePullRequestPreview', 'environment_variables': 'environmentVariables', 'pull_request_environment_name': 'pullRequestEnvironmentName', 'stage': 'stage', 'tags': 'tags'})
class CfnBranchProps():
    def __init__(self, *, app_id: str, branch_name: str, basic_auth_config: typing.Optional[typing.Union["CfnBranch.BasicAuthConfigProperty", _IResolvable_9ceae33e]]=None, build_spec: typing.Optional[str]=None, description: typing.Optional[str]=None, enable_auto_build: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, enable_pull_request_preview: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, environment_variables: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnBranch.EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]=None, pull_request_environment_name: typing.Optional[str]=None, stage: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::Amplify::Branch``.

        :param app_id: ``AWS::Amplify::Branch.AppId``.
        :param branch_name: ``AWS::Amplify::Branch.BranchName``.
        :param basic_auth_config: ``AWS::Amplify::Branch.BasicAuthConfig``.
        :param build_spec: ``AWS::Amplify::Branch.BuildSpec``.
        :param description: ``AWS::Amplify::Branch.Description``.
        :param enable_auto_build: ``AWS::Amplify::Branch.EnableAutoBuild``.
        :param enable_pull_request_preview: ``AWS::Amplify::Branch.EnablePullRequestPreview``.
        :param environment_variables: ``AWS::Amplify::Branch.EnvironmentVariables``.
        :param pull_request_environment_name: ``AWS::Amplify::Branch.PullRequestEnvironmentName``.
        :param stage: ``AWS::Amplify::Branch.Stage``.
        :param tags: ``AWS::Amplify::Branch.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html
        """
        self._values = {
            'app_id': app_id,
            'branch_name': branch_name,
        }
        if basic_auth_config is not None: self._values["basic_auth_config"] = basic_auth_config
        if build_spec is not None: self._values["build_spec"] = build_spec
        if description is not None: self._values["description"] = description
        if enable_auto_build is not None: self._values["enable_auto_build"] = enable_auto_build
        if enable_pull_request_preview is not None: self._values["enable_pull_request_preview"] = enable_pull_request_preview
        if environment_variables is not None: self._values["environment_variables"] = environment_variables
        if pull_request_environment_name is not None: self._values["pull_request_environment_name"] = pull_request_environment_name
        if stage is not None: self._values["stage"] = stage
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def app_id(self) -> str:
        """``AWS::Amplify::Branch.AppId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-appid
        """
        return self._values.get('app_id')

    @builtins.property
    def branch_name(self) -> str:
        """``AWS::Amplify::Branch.BranchName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-branchname
        """
        return self._values.get('branch_name')

    @builtins.property
    def basic_auth_config(self) -> typing.Optional[typing.Union["CfnBranch.BasicAuthConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Amplify::Branch.BasicAuthConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-basicauthconfig
        """
        return self._values.get('basic_auth_config')

    @builtins.property
    def build_spec(self) -> typing.Optional[str]:
        """``AWS::Amplify::Branch.BuildSpec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-buildspec
        """
        return self._values.get('build_spec')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Amplify::Branch.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-description
        """
        return self._values.get('description')

    @builtins.property
    def enable_auto_build(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Amplify::Branch.EnableAutoBuild``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableautobuild
        """
        return self._values.get('enable_auto_build')

    @builtins.property
    def enable_pull_request_preview(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Amplify::Branch.EnablePullRequestPreview``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enablepullrequestpreview
        """
        return self._values.get('enable_pull_request_preview')

    @builtins.property
    def environment_variables(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnBranch.EnvironmentVariableProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Amplify::Branch.EnvironmentVariables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-environmentvariables
        """
        return self._values.get('environment_variables')

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[str]:
        """``AWS::Amplify::Branch.PullRequestEnvironmentName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-pullrequestenvironmentname
        """
        return self._values.get('pull_request_environment_name')

    @builtins.property
    def stage(self) -> typing.Optional[str]:
        """``AWS::Amplify::Branch.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-stage
        """
        return self._values.get('stage')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Amplify::Branch.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnBranchProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDomain(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.CfnDomain"):
    """A CloudFormation ``AWS::Amplify::Domain``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html
    cloudformationResource:
    :cloudformationResource:: AWS::Amplify::Domain
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, app_id: str, domain_name: str, sub_domain_settings: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SubDomainSettingProperty", _IResolvable_9ceae33e]]]) -> None:
        """Create a new ``AWS::Amplify::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_id: ``AWS::Amplify::Domain.AppId``.
        :param domain_name: ``AWS::Amplify::Domain.DomainName``.
        :param sub_domain_settings: ``AWS::Amplify::Domain.SubDomainSettings``.
        """
        props = CfnDomainProps(app_id=app_id, domain_name=domain_name, sub_domain_settings=sub_domain_settings)

        jsii.create(CfnDomain, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDomain":
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
    @jsii.member(jsii_name="attrCertificateRecord")
    def attr_certificate_record(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CertificateRecord
        """
        return jsii.get(self, "attrCertificateRecord")

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DomainName
        """
        return jsii.get(self, "attrDomainName")

    @builtins.property
    @jsii.member(jsii_name="attrDomainStatus")
    def attr_domain_status(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DomainStatus
        """
        return jsii.get(self, "attrDomainStatus")

    @builtins.property
    @jsii.member(jsii_name="attrStatusReason")
    def attr_status_reason(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: StatusReason
        """
        return jsii.get(self, "attrStatusReason")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> str:
        """``AWS::Amplify::Domain.AppId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-appid
        """
        return jsii.get(self, "appId")

    @app_id.setter
    def app_id(self, value: str) -> None:
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::Amplify::Domain.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="subDomainSettings")
    def sub_domain_settings(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SubDomainSettingProperty", _IResolvable_9ceae33e]]]:
        """``AWS::Amplify::Domain.SubDomainSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-subdomainsettings
        """
        return jsii.get(self, "subDomainSettings")

    @sub_domain_settings.setter
    def sub_domain_settings(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["SubDomainSettingProperty", _IResolvable_9ceae33e]]]) -> None:
        jsii.set(self, "subDomainSettings", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnDomain.SubDomainSettingProperty", jsii_struct_bases=[], name_mapping={'branch_name': 'branchName', 'prefix': 'prefix'})
    class SubDomainSettingProperty():
        def __init__(self, *, branch_name: str, prefix: str) -> None:
            """
            :param branch_name: ``CfnDomain.SubDomainSettingProperty.BranchName``.
            :param prefix: ``CfnDomain.SubDomainSettingProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html
            """
            self._values = {
                'branch_name': branch_name,
                'prefix': prefix,
            }

        @builtins.property
        def branch_name(self) -> str:
            """``CfnDomain.SubDomainSettingProperty.BranchName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html#cfn-amplify-domain-subdomainsetting-branchname
            """
            return self._values.get('branch_name')

        @builtins.property
        def prefix(self) -> str:
            """``CfnDomain.SubDomainSettingProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html#cfn-amplify-domain-subdomainsetting-prefix
            """
            return self._values.get('prefix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SubDomainSettingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CfnDomainProps", jsii_struct_bases=[], name_mapping={'app_id': 'appId', 'domain_name': 'domainName', 'sub_domain_settings': 'subDomainSettings'})
class CfnDomainProps():
    def __init__(self, *, app_id: str, domain_name: str, sub_domain_settings: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDomain.SubDomainSettingProperty", _IResolvable_9ceae33e]]]) -> None:
        """Properties for defining a ``AWS::Amplify::Domain``.

        :param app_id: ``AWS::Amplify::Domain.AppId``.
        :param domain_name: ``AWS::Amplify::Domain.DomainName``.
        :param sub_domain_settings: ``AWS::Amplify::Domain.SubDomainSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html
        """
        self._values = {
            'app_id': app_id,
            'domain_name': domain_name,
            'sub_domain_settings': sub_domain_settings,
        }

    @builtins.property
    def app_id(self) -> str:
        """``AWS::Amplify::Domain.AppId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-appid
        """
        return self._values.get('app_id')

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::Amplify::Domain.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-domainname
        """
        return self._values.get('domain_name')

    @builtins.property
    def sub_domain_settings(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDomain.SubDomainSettingProperty", _IResolvable_9ceae33e]]]:
        """``AWS::Amplify::Domain.SubDomainSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-subdomainsettings
        """
        return self._values.get('sub_domain_settings')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDomainProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CodeCommitSourceCodeProviderProps", jsii_struct_bases=[], name_mapping={'repository': 'repository'})
class CodeCommitSourceCodeProviderProps():
    def __init__(self, *, repository: _IRepository_91f381de) -> None:
        """Properties for a CodeCommit source code provider.

        :param repository: The CodeCommit repository.

        stability
        :stability: experimental
        """
        self._values = {
            'repository': repository,
        }

    @builtins.property
    def repository(self) -> _IRepository_91f381de:
        """The CodeCommit repository.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeCommitSourceCodeProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CustomRule(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.CustomRule"):
    """Custom rewrite/redirect rule for an Amplify App.

    see
    :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
    stability
    :stability: experimental
    """
    def __init__(self, *, source: str, target: str, condition: typing.Optional[str]=None, status: typing.Optional["RedirectStatus"]=None) -> None:
        """
        :param source: The source pattern for a URL rewrite or redirect rule.
        :param target: The target pattern for a URL rewrite or redirect rule.
        :param condition: The condition for a URL rewrite or redirect rule, e.g. country code. Default: - no condition
        :param status: The status code for a URL rewrite or redirect rule. Default: PERMANENT_REDIRECT

        stability
        :stability: experimental
        """
        options = CustomRuleOptions(source=source, target=target, condition=condition, status=status)

        jsii.create(CustomRule, self, [options])

    @jsii.python.classproperty
    @jsii.member(jsii_name="SINGLE_PAGE_APPLICATION_REDIRECT")
    def SINGLE_PAGE_APPLICATION_REDIRECT(cls) -> "CustomRule":
        """Sets up a 200 rewrite for all paths to ``index.html`` except for path containing a file extension.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "SINGLE_PAGE_APPLICATION_REDIRECT")

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> str:
        """The source pattern for a URL rewrite or redirect rule.

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        stability
        :stability: experimental
        """
        return jsii.get(self, "source")

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> str:
        """The target pattern for a URL rewrite or redirect rule.

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        stability
        :stability: experimental
        """
        return jsii.get(self, "target")

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional[str]:
        """The condition for a URL rewrite or redirect rule, e.g. country code.

        default
        :default: - no condition

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        stability
        :stability: experimental
        """
        return jsii.get(self, "condition")

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional["RedirectStatus"]:
        """The status code for a URL rewrite or redirect rule.

        default
        :default: PERMANENT_REDIRECT

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        stability
        :stability: experimental
        """
        return jsii.get(self, "status")


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.CustomRuleOptions", jsii_struct_bases=[], name_mapping={'source': 'source', 'target': 'target', 'condition': 'condition', 'status': 'status'})
class CustomRuleOptions():
    def __init__(self, *, source: str, target: str, condition: typing.Optional[str]=None, status: typing.Optional["RedirectStatus"]=None) -> None:
        """Options for a custom rewrite/redirect rule for an Amplify App.

        :param source: The source pattern for a URL rewrite or redirect rule.
        :param target: The target pattern for a URL rewrite or redirect rule.
        :param condition: The condition for a URL rewrite or redirect rule, e.g. country code. Default: - no condition
        :param status: The status code for a URL rewrite or redirect rule. Default: PERMANENT_REDIRECT

        stability
        :stability: experimental
        """
        self._values = {
            'source': source,
            'target': target,
        }
        if condition is not None: self._values["condition"] = condition
        if status is not None: self._values["status"] = status

    @builtins.property
    def source(self) -> str:
        """The source pattern for a URL rewrite or redirect rule.

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        stability
        :stability: experimental
        """
        return self._values.get('source')

    @builtins.property
    def target(self) -> str:
        """The target pattern for a URL rewrite or redirect rule.

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        stability
        :stability: experimental
        """
        return self._values.get('target')

    @builtins.property
    def condition(self) -> typing.Optional[str]:
        """The condition for a URL rewrite or redirect rule, e.g. country code.

        default
        :default: - no condition

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        stability
        :stability: experimental
        """
        return self._values.get('condition')

    @builtins.property
    def status(self) -> typing.Optional["RedirectStatus"]:
        """The status code for a URL rewrite or redirect rule.

        default
        :default: PERMANENT_REDIRECT

        see
        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        stability
        :stability: experimental
        """
        return self._values.get('status')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CustomRuleOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Domain(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.Domain"):
    """An Amplify Console domain.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, app: "IApp", domain_name: typing.Optional[str]=None, sub_domains: typing.Optional[typing.List["SubDomain"]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param app: The application to which the domain must be connected.
        :param domain_name: The name of the domain. Default: - the construct's id
        :param sub_domains: Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        stability
        :stability: experimental
        """
        props = DomainProps(app=app, domain_name=domain_name, sub_domains=sub_domains)

        jsii.create(Domain, self, [scope, id, props])

    @jsii.member(jsii_name="mapRoot")
    def map_root(self, branch: "IBranch") -> "Domain":
        """Maps a branch to the domain root.

        :param branch: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapRoot", [branch])

    @jsii.member(jsii_name="mapSubDomain")
    def map_sub_domain(self, branch: "IBranch", prefix: typing.Optional[str]=None) -> "Domain":
        """Maps a branch to a sub domain.

        :param branch: The branch.
        :param prefix: The prefix. Use '' to map to the root of the domain. Defaults to branch name.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapSubDomain", [branch, prefix])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> str:
        """The ARN of the domain.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "arn")

    @builtins.property
    @jsii.member(jsii_name="certificateRecord")
    def certificate_record(self) -> str:
        """The DNS Record for certificate verification.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "certificateRecord")

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The name of the domain.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "domainName")

    @builtins.property
    @jsii.member(jsii_name="domainStatus")
    def domain_status(self) -> str:
        """The status of the domain association.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "domainStatus")

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> str:
        """The reason for the current status of the domain.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "statusReason")


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.DomainOptions", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'sub_domains': 'subDomains'})
class DomainOptions():
    def __init__(self, *, domain_name: typing.Optional[str]=None, sub_domains: typing.Optional[typing.List["SubDomain"]]=None) -> None:
        """Options to add a domain to an application.

        :param domain_name: The name of the domain. Default: - the construct's id
        :param sub_domains: Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        stability
        :stability: experimental
        """
        self._values = {
        }
        if domain_name is not None: self._values["domain_name"] = domain_name
        if sub_domains is not None: self._values["sub_domains"] = sub_domains

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The name of the domain.

        default
        :default: - the construct's id

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomain"]]:
        """Subdomains.

        default
        :default: - use ``addSubDomain()`` to add subdomains

        stability
        :stability: experimental
        """
        return self._values.get('sub_domains')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DomainOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.DomainProps", jsii_struct_bases=[DomainOptions], name_mapping={'domain_name': 'domainName', 'sub_domains': 'subDomains', 'app': 'app'})
class DomainProps(DomainOptions):
    def __init__(self, *, domain_name: typing.Optional[str]=None, sub_domains: typing.Optional[typing.List["SubDomain"]]=None, app: "IApp") -> None:
        """Properties for a Domain.

        :param domain_name: The name of the domain. Default: - the construct's id
        :param sub_domains: Subdomains. Default: - use ``addSubDomain()`` to add subdomains
        :param app: The application to which the domain must be connected.

        stability
        :stability: experimental
        """
        self._values = {
            'app': app,
        }
        if domain_name is not None: self._values["domain_name"] = domain_name
        if sub_domains is not None: self._values["sub_domains"] = sub_domains

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The name of the domain.

        default
        :default: - the construct's id

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomain"]]:
        """Subdomains.

        default
        :default: - use ``addSubDomain()`` to add subdomains

        stability
        :stability: experimental
        """
        return self._values.get('sub_domains')

    @builtins.property
    def app(self) -> "IApp":
        """The application to which the domain must be connected.

        stability
        :stability: experimental
        """
        return self._values.get('app')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DomainProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.GitHubSourceCodeProviderProps", jsii_struct_bases=[], name_mapping={'oauth_token': 'oauthToken', 'owner': 'owner', 'repository': 'repository'})
class GitHubSourceCodeProviderProps():
    def __init__(self, *, oauth_token: _SecretValue_99478b8b, owner: str, repository: str) -> None:
        """Properties for a GitHub source code provider.

        :param oauth_token: A personal access token with the ``repo`` scope.
        :param owner: The user or organization owning the repository.
        :param repository: The name of the repository.

        stability
        :stability: experimental
        """
        self._values = {
            'oauth_token': oauth_token,
            'owner': owner,
            'repository': repository,
        }

    @builtins.property
    def oauth_token(self) -> _SecretValue_99478b8b:
        """A personal access token with the ``repo`` scope.

        stability
        :stability: experimental
        """
        return self._values.get('oauth_token')

    @builtins.property
    def owner(self) -> str:
        """The user or organization owning the repository.

        stability
        :stability: experimental
        """
        return self._values.get('owner')

    @builtins.property
    def repository(self) -> str:
        """The name of the repository.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitHubSourceCodeProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.GitLabSourceCodeProviderProps", jsii_struct_bases=[], name_mapping={'oauth_token': 'oauthToken', 'owner': 'owner', 'repository': 'repository'})
class GitLabSourceCodeProviderProps():
    def __init__(self, *, oauth_token: _SecretValue_99478b8b, owner: str, repository: str) -> None:
        """Properties for a GitLab source code provider.

        :param oauth_token: A personal access token with the ``repo`` scope.
        :param owner: The user or organization owning the repository.
        :param repository: The name of the repository.

        stability
        :stability: experimental
        """
        self._values = {
            'oauth_token': oauth_token,
            'owner': owner,
            'repository': repository,
        }

    @builtins.property
    def oauth_token(self) -> _SecretValue_99478b8b:
        """A personal access token with the ``repo`` scope.

        stability
        :stability: experimental
        """
        return self._values.get('oauth_token')

    @builtins.property
    def owner(self) -> str:
        """The user or organization owning the repository.

        stability
        :stability: experimental
        """
        return self._values.get('owner')

    @builtins.property
    def repository(self) -> str:
        """The name of the repository.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitLabSourceCodeProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_amplify.IApp")
class IApp(_IResource_72f7ee7e, jsii.compat.Protocol):
    """An Amplify Console application.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAppProxy

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> str:
        """The application id.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IAppProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """An Amplify Console application.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_amplify.IApp"
    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> str:
        """The application id.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "appId")


@jsii.interface(jsii_type="monocdk-experiment.aws_amplify.IBranch")
class IBranch(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A branch.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBranchProxy

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> str:
        """The name of the branch.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IBranchProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A branch.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_amplify.IBranch"
    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> str:
        """The name of the branch.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "branchName")


@jsii.interface(jsii_type="monocdk-experiment.aws_amplify.ISourceCodeProvider")
class ISourceCodeProvider(jsii.compat.Protocol):
    """A source code provider.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISourceCodeProviderProxy

    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        """Binds the source code provider to an app.

        :param app: The app [disable-awslint:ref-via-interface].

        stability
        :stability: experimental
        """
        ...


class _ISourceCodeProviderProxy():
    """A source code provider.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_amplify.ISourceCodeProvider"
    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        """Binds the source code provider to an app.

        :param app: The app [disable-awslint:ref-via-interface].

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [app])


@jsii.enum(jsii_type="monocdk-experiment.aws_amplify.RedirectStatus")
class RedirectStatus(enum.Enum):
    """The status code for a URL rewrite or redirect rule.

    stability
    :stability: experimental
    """
    REWRITE = "REWRITE"
    """Rewrite (200).

    stability
    :stability: experimental
    """
    PERMANENT_REDIRECT = "PERMANENT_REDIRECT"
    """Permanent redirect (301).

    stability
    :stability: experimental
    """
    TEMPORARY_REDIRECT = "TEMPORARY_REDIRECT"
    """Temporary redirect (302).

    stability
    :stability: experimental
    """
    NOT_FOUND = "NOT_FOUND"
    """Not found (404).

    stability
    :stability: experimental
    """
    NOT_FOUND_REWRITE = "NOT_FOUND_REWRITE"
    """Not found rewrite (404).

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.SourceCodeProviderConfig", jsii_struct_bases=[], name_mapping={'repository': 'repository', 'access_token': 'accessToken', 'oauth_token': 'oauthToken'})
class SourceCodeProviderConfig():
    def __init__(self, *, repository: str, access_token: typing.Optional[_SecretValue_99478b8b]=None, oauth_token: typing.Optional[_SecretValue_99478b8b]=None) -> None:
        """Configuration for the source code provider.

        :param repository: The repository for the application. Must use the ``HTTPS`` protocol.
        :param access_token: Personal Access token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key. Token is not stored. Either ``accessToken`` or ``oauthToken`` must be specified if ``repository`` is sepcified. Default: - do not use a token
        :param oauth_token: OAuth token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key. OAuth token is not stored. Either ``accessToken`` or ``oauthToken`` must be specified if ``repository`` is sepcified. Default: - do not use a token

        stability
        :stability: experimental
        """
        self._values = {
            'repository': repository,
        }
        if access_token is not None: self._values["access_token"] = access_token
        if oauth_token is not None: self._values["oauth_token"] = oauth_token

    @builtins.property
    def repository(self) -> str:
        """The repository for the application.

        Must use the ``HTTPS`` protocol.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return self._values.get('repository')

    @builtins.property
    def access_token(self) -> typing.Optional[_SecretValue_99478b8b]:
        """Personal Access token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key.

        Token is not stored.

        Either ``accessToken`` or ``oauthToken`` must be specified if ``repository``
        is sepcified.

        default
        :default: - do not use a token

        stability
        :stability: experimental
        """
        return self._values.get('access_token')

    @builtins.property
    def oauth_token(self) -> typing.Optional[_SecretValue_99478b8b]:
        """OAuth token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key.

        OAuth token is not stored.

        Either ``accessToken`` or ``oauthToken`` must be specified if ``repository``
        is sepcified.

        default
        :default: - do not use a token

        stability
        :stability: experimental
        """
        return self._values.get('oauth_token')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SourceCodeProviderConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_amplify.SubDomain", jsii_struct_bases=[], name_mapping={'branch': 'branch', 'prefix': 'prefix'})
class SubDomain():
    def __init__(self, *, branch: "IBranch", prefix: typing.Optional[str]=None) -> None:
        """Sub domain settings.

        :param branch: The branch.
        :param prefix: The prefix. Use '' to map to the root of the domain Default: - the branch name

        stability
        :stability: experimental
        """
        self._values = {
            'branch': branch,
        }
        if prefix is not None: self._values["prefix"] = prefix

    @builtins.property
    def branch(self) -> "IBranch":
        """The branch.

        stability
        :stability: experimental
        """
        return self._values.get('branch')

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """The prefix.

        Use '' to map to the root of the domain

        default
        :default: - the branch name

        stability
        :stability: experimental
        """
        return self._values.get('prefix')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubDomain(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IApp, _IGrantable_0fcfc53a)
class App(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.App"):
    """An Amplify Console application.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, app_name: typing.Optional[str]=None, auto_branch_creation: typing.Optional["AutoBranchCreation"]=None, basic_auth: typing.Optional["BasicAuth"]=None, build_spec: typing.Optional[_BuildSpec_2207fbc6]=None, custom_rules: typing.Optional[typing.List["CustomRule"]]=None, description: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Mapping[str, str]]=None, role: typing.Optional[_IRole_e69bbae4]=None, source_code_provider: typing.Optional["ISourceCodeProvider"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param app_name: The name for the application. Default: - a CDK generated name
        :param auto_branch_creation: The auto branch creation configuration. Use this to automatically create branches that match a certain pattern. Default: - no auto branch creation
        :param basic_auth: The Basic Auth configuration. Use this to set password protection at an app level to all your branches. Default: - no password protection
        :param build_spec: BuildSpec for the application. Alternatively, add a ``amplify.yml`` file to the repository. Default: - no build spec
        :param custom_rules: Custom rewrite/redirect rules for the application. Default: - no custom rewrite/redirect rules
        :param description: A description for the application. Default: - no description
        :param environment_variables: Environment variables for the application. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - no environment variables
        :param role: The IAM service role to associate with the application. The App implements IGrantable. Default: - a new role is created
        :param source_code_provider: The source code provider for this application. Default: - not connected to a source code provider

        stability
        :stability: experimental
        """
        props = AppProps(app_name=app_name, auto_branch_creation=auto_branch_creation, basic_auth=basic_auth, build_spec=build_spec, custom_rules=custom_rules, description=description, environment_variables=environment_variables, role=role, source_code_provider=source_code_provider)

        jsii.create(App, self, [scope, id, props])

    @jsii.member(jsii_name="fromAppId")
    @builtins.classmethod
    def from_app_id(cls, scope: _Construct_f50a3f53, id: str, app_id: str) -> "IApp":
        """Import an existing application.

        :param scope: -
        :param id: -
        :param app_id: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromAppId", [scope, id, app_id])

    @jsii.member(jsii_name="addAutoBranchEnvironment")
    def add_auto_branch_environment(self, name: str, value: str) -> "App":
        """Adds an environment variable to the auto created branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAutoBranchEnvironment", [name, value])

    @jsii.member(jsii_name="addBranch")
    def add_branch(self, id: str, *, auto_build: typing.Optional[bool]=None, basic_auth: typing.Optional["BasicAuth"]=None, branch_name: typing.Optional[str]=None, build_spec: typing.Optional[_BuildSpec_2207fbc6]=None, description: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Mapping[str, str]]=None, pull_request_environment_name: typing.Optional[str]=None, pull_request_preview: typing.Optional[bool]=None, stage: typing.Optional[str]=None) -> "Branch":
        """Adds a branch to this application.

        :param id: -
        :param auto_build: Whether to enable auto building for the branch. Default: true
        :param basic_auth: The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: The name of the branch. Default: - the construct's id
        :param build_spec: BuildSpec for the branch. Default: - no build spec
        :param description: A description for the branch. Default: - no description
        :param environment_variables: Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param pull_request_environment_name: The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: Whether to enable pull request preview for the branch. Default: true
        :param stage: Stage for the branch. Default: - no stage

        stability
        :stability: experimental
        """
        options = BranchOptions(auto_build=auto_build, basic_auth=basic_auth, branch_name=branch_name, build_spec=build_spec, description=description, environment_variables=environment_variables, pull_request_environment_name=pull_request_environment_name, pull_request_preview=pull_request_preview, stage=stage)

        return jsii.invoke(self, "addBranch", [id, options])

    @jsii.member(jsii_name="addCustomRule")
    def add_custom_rule(self, rule: "CustomRule") -> "App":
        """Adds a custom rewrite/redirect rule to this application.

        :param rule: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addCustomRule", [rule])

    @jsii.member(jsii_name="addDomain")
    def add_domain(self, id: str, *, domain_name: typing.Optional[str]=None, sub_domains: typing.Optional[typing.List["SubDomain"]]=None) -> "Domain":
        """Adds a domain to this application.

        :param id: -
        :param domain_name: The name of the domain. Default: - the construct's id
        :param sub_domains: Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        stability
        :stability: experimental
        """
        options = DomainOptions(domain_name=domain_name, sub_domains=sub_domains)

        return jsii.invoke(self, "addDomain", [id, options])

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: str, value: str) -> "App":
        """Adds an environment variable to this application.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addEnvironment", [name, value])

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> str:
        """The application id.

        stability
        :stability: experimental
        """
        return jsii.get(self, "appId")

    @builtins.property
    @jsii.member(jsii_name="appName")
    def app_name(self) -> str:
        """The name of the application.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "appName")

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> str:
        """The ARN of the application.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "arn")

    @builtins.property
    @jsii.member(jsii_name="defaultDomain")
    def default_domain(self) -> str:
        """The default domain of the application.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "defaultDomain")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")


@jsii.implements(IBranch)
class Branch(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.Branch"):
    """An Amplify Console branch.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, app: "IApp", auto_build: typing.Optional[bool]=None, basic_auth: typing.Optional["BasicAuth"]=None, branch_name: typing.Optional[str]=None, build_spec: typing.Optional[_BuildSpec_2207fbc6]=None, description: typing.Optional[str]=None, environment_variables: typing.Optional[typing.Mapping[str, str]]=None, pull_request_environment_name: typing.Optional[str]=None, pull_request_preview: typing.Optional[bool]=None, stage: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param app: The application within which the branch must be created.
        :param auto_build: Whether to enable auto building for the branch. Default: true
        :param basic_auth: The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: The name of the branch. Default: - the construct's id
        :param build_spec: BuildSpec for the branch. Default: - no build spec
        :param description: A description for the branch. Default: - no description
        :param environment_variables: Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param pull_request_environment_name: The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: Whether to enable pull request preview for the branch. Default: true
        :param stage: Stage for the branch. Default: - no stage

        stability
        :stability: experimental
        """
        props = BranchProps(app=app, auto_build=auto_build, basic_auth=basic_auth, branch_name=branch_name, build_spec=build_spec, description=description, environment_variables=environment_variables, pull_request_environment_name=pull_request_environment_name, pull_request_preview=pull_request_preview, stage=stage)

        jsii.create(Branch, self, [scope, id, props])

    @jsii.member(jsii_name="fromBranchName")
    @builtins.classmethod
    def from_branch_name(cls, scope: _Construct_f50a3f53, id: str, branch_name: str) -> "IBranch":
        """Import an existing branch.

        :param scope: -
        :param id: -
        :param branch_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromBranchName", [scope, id, branch_name])

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: str, value: str) -> "Branch":
        """Adds an environment variable to this branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addEnvironment", [name, value])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> str:
        """The ARN of the branch.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "arn")

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> str:
        """The name of the branch.

        stability
        :stability: experimental
        """
        return jsii.get(self, "branchName")


@jsii.implements(ISourceCodeProvider)
class CodeCommitSourceCodeProvider(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.CodeCommitSourceCodeProvider"):
    """CodeCommit source code provider.

    stability
    :stability: experimental
    """
    def __init__(self, *, repository: _IRepository_91f381de) -> None:
        """
        :param repository: The CodeCommit repository.

        stability
        :stability: experimental
        """
        props = CodeCommitSourceCodeProviderProps(repository=repository)

        jsii.create(CodeCommitSourceCodeProvider, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        """Binds the source code provider to an app.

        :param app: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [app])


@jsii.implements(ISourceCodeProvider)
class GitHubSourceCodeProvider(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.GitHubSourceCodeProvider"):
    """GitHub source code provider.

    stability
    :stability: experimental
    """
    def __init__(self, *, oauth_token: _SecretValue_99478b8b, owner: str, repository: str) -> None:
        """
        :param oauth_token: A personal access token with the ``repo`` scope.
        :param owner: The user or organization owning the repository.
        :param repository: The name of the repository.

        stability
        :stability: experimental
        """
        props = GitHubSourceCodeProviderProps(oauth_token=oauth_token, owner=owner, repository=repository)

        jsii.create(GitHubSourceCodeProvider, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _app: "App") -> "SourceCodeProviderConfig":
        """Binds the source code provider to an app.

        :param _app: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_app])


@jsii.implements(ISourceCodeProvider)
class GitLabSourceCodeProvider(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_amplify.GitLabSourceCodeProvider"):
    """GitLab source code provider.

    stability
    :stability: experimental
    """
    def __init__(self, *, oauth_token: _SecretValue_99478b8b, owner: str, repository: str) -> None:
        """
        :param oauth_token: A personal access token with the ``repo`` scope.
        :param owner: The user or organization owning the repository.
        :param repository: The name of the repository.

        stability
        :stability: experimental
        """
        props = GitLabSourceCodeProviderProps(oauth_token=oauth_token, owner=owner, repository=repository)

        jsii.create(GitLabSourceCodeProvider, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _app: "App") -> "SourceCodeProviderConfig":
        """Binds the source code provider to an app.

        :param _app: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_app])


__all__ = [
    "App",
    "AppProps",
    "AutoBranchCreation",
    "BasicAuth",
    "BasicAuthConfig",
    "BasicAuthProps",
    "Branch",
    "BranchOptions",
    "BranchProps",
    "CfnApp",
    "CfnAppProps",
    "CfnBranch",
    "CfnBranchProps",
    "CfnDomain",
    "CfnDomainProps",
    "CodeCommitSourceCodeProvider",
    "CodeCommitSourceCodeProviderProps",
    "CustomRule",
    "CustomRuleOptions",
    "Domain",
    "DomainOptions",
    "DomainProps",
    "GitHubSourceCodeProvider",
    "GitHubSourceCodeProviderProps",
    "GitLabSourceCodeProvider",
    "GitLabSourceCodeProviderProps",
    "IApp",
    "IBranch",
    "ISourceCodeProvider",
    "RedirectStatus",
    "SourceCodeProviderConfig",
    "SubDomain",
]

publication.publish()
