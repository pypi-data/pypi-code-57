import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnDataLakeSettings(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lakeformation.CfnDataLakeSettings"):
    """A CloudFormation ``AWS::LakeFormation::DataLakeSettings``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html
    cloudformationResource:
    :cloudformationResource:: AWS::LakeFormation::DataLakeSettings
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, admins: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DataLakePrincipalProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Create a new ``AWS::LakeFormation::DataLakeSettings``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param admins: ``AWS::LakeFormation::DataLakeSettings.Admins``.
        """
        props = CfnDataLakeSettingsProps(admins=admins)

        jsii.create(CfnDataLakeSettings, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDataLakeSettings":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="admins")
    def admins(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DataLakePrincipalProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::LakeFormation::DataLakeSettings.Admins``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-admins
        """
        return jsii.get(self, "admins")

    @admins.setter
    def admins(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DataLakePrincipalProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "admins", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnDataLakeSettings.DataLakePrincipalProperty", jsii_struct_bases=[], name_mapping={'data_lake_principal_identifier': 'dataLakePrincipalIdentifier'})
    class DataLakePrincipalProperty():
        def __init__(self, *, data_lake_principal_identifier: typing.Optional[str]=None) -> None:
            """
            :param data_lake_principal_identifier: ``CfnDataLakeSettings.DataLakePrincipalProperty.DataLakePrincipalIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datalakesettings-datalakeprincipal.html
            """
            self._values = {
            }
            if data_lake_principal_identifier is not None: self._values["data_lake_principal_identifier"] = data_lake_principal_identifier

        @builtins.property
        def data_lake_principal_identifier(self) -> typing.Optional[str]:
            """``CfnDataLakeSettings.DataLakePrincipalProperty.DataLakePrincipalIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datalakesettings-datalakeprincipal.html#cfn-lakeformation-datalakesettings-datalakeprincipal-datalakeprincipalidentifier
            """
            return self._values.get('data_lake_principal_identifier')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DataLakePrincipalProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnDataLakeSettingsProps", jsii_struct_bases=[], name_mapping={'admins': 'admins'})
class CfnDataLakeSettingsProps():
    def __init__(self, *, admins: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataLakeSettings.DataLakePrincipalProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Properties for defining a ``AWS::LakeFormation::DataLakeSettings``.

        :param admins: ``AWS::LakeFormation::DataLakeSettings.Admins``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html
        """
        self._values = {
        }
        if admins is not None: self._values["admins"] = admins

    @builtins.property
    def admins(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDataLakeSettings.DataLakePrincipalProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::LakeFormation::DataLakeSettings.Admins``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-admins
        """
        return self._values.get('admins')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDataLakeSettingsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnPermissions(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissions"):
    """A CloudFormation ``AWS::LakeFormation::Permissions``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html
    cloudformationResource:
    :cloudformationResource:: AWS::LakeFormation::Permissions
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, data_lake_principal: typing.Union["DataLakePrincipalProperty", _IResolvable_9ceae33e], resource: typing.Union["ResourceProperty", _IResolvable_9ceae33e], permissions: typing.Optional[typing.List[str]]=None, permissions_with_grant_option: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::LakeFormation::Permissions``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_lake_principal: ``AWS::LakeFormation::Permissions.DataLakePrincipal``.
        :param resource: ``AWS::LakeFormation::Permissions.Resource``.
        :param permissions: ``AWS::LakeFormation::Permissions.Permissions``.
        :param permissions_with_grant_option: ``AWS::LakeFormation::Permissions.PermissionsWithGrantOption``.
        """
        props = CfnPermissionsProps(data_lake_principal=data_lake_principal, resource=resource, permissions=permissions, permissions_with_grant_option=permissions_with_grant_option)

        jsii.create(CfnPermissions, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnPermissions":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="dataLakePrincipal")
    def data_lake_principal(self) -> typing.Union["DataLakePrincipalProperty", _IResolvable_9ceae33e]:
        """``AWS::LakeFormation::Permissions.DataLakePrincipal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-datalakeprincipal
        """
        return jsii.get(self, "dataLakePrincipal")

    @data_lake_principal.setter
    def data_lake_principal(self, value: typing.Union["DataLakePrincipalProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "dataLakePrincipal", value)

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> typing.Union["ResourceProperty", _IResolvable_9ceae33e]:
        """``AWS::LakeFormation::Permissions.Resource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-resource
        """
        return jsii.get(self, "resource")

    @resource.setter
    def resource(self, value: typing.Union["ResourceProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "resource", value)

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> typing.Optional[typing.List[str]]:
        """``AWS::LakeFormation::Permissions.Permissions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-permissions
        """
        return jsii.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "permissions", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsWithGrantOption")
    def permissions_with_grant_option(self) -> typing.Optional[typing.List[str]]:
        """``AWS::LakeFormation::Permissions.PermissionsWithGrantOption``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-permissionswithgrantoption
        """
        return jsii.get(self, "permissionsWithGrantOption")

    @permissions_with_grant_option.setter
    def permissions_with_grant_option(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "permissionsWithGrantOption", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissions.ColumnWildcardProperty", jsii_struct_bases=[], name_mapping={'excluded_column_names': 'excludedColumnNames'})
    class ColumnWildcardProperty():
        def __init__(self, *, excluded_column_names: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param excluded_column_names: ``CfnPermissions.ColumnWildcardProperty.ExcludedColumnNames``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-columnwildcard.html
            """
            self._values = {
            }
            if excluded_column_names is not None: self._values["excluded_column_names"] = excluded_column_names

        @builtins.property
        def excluded_column_names(self) -> typing.Optional[typing.List[str]]:
            """``CfnPermissions.ColumnWildcardProperty.ExcludedColumnNames``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-columnwildcard.html#cfn-lakeformation-permissions-columnwildcard-excludedcolumnnames
            """
            return self._values.get('excluded_column_names')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ColumnWildcardProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissions.DataLakePrincipalProperty", jsii_struct_bases=[], name_mapping={'data_lake_principal_identifier': 'dataLakePrincipalIdentifier'})
    class DataLakePrincipalProperty():
        def __init__(self, *, data_lake_principal_identifier: typing.Optional[str]=None) -> None:
            """
            :param data_lake_principal_identifier: ``CfnPermissions.DataLakePrincipalProperty.DataLakePrincipalIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalakeprincipal.html
            """
            self._values = {
            }
            if data_lake_principal_identifier is not None: self._values["data_lake_principal_identifier"] = data_lake_principal_identifier

        @builtins.property
        def data_lake_principal_identifier(self) -> typing.Optional[str]:
            """``CfnPermissions.DataLakePrincipalProperty.DataLakePrincipalIdentifier``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalakeprincipal.html#cfn-lakeformation-permissions-datalakeprincipal-datalakeprincipalidentifier
            """
            return self._values.get('data_lake_principal_identifier')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DataLakePrincipalProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissions.DataLocationResourceProperty", jsii_struct_bases=[], name_mapping={'s3_resource': 's3Resource'})
    class DataLocationResourceProperty():
        def __init__(self, *, s3_resource: typing.Optional[str]=None) -> None:
            """
            :param s3_resource: ``CfnPermissions.DataLocationResourceProperty.S3Resource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalocationresource.html
            """
            self._values = {
            }
            if s3_resource is not None: self._values["s3_resource"] = s3_resource

        @builtins.property
        def s3_resource(self) -> typing.Optional[str]:
            """``CfnPermissions.DataLocationResourceProperty.S3Resource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalocationresource.html#cfn-lakeformation-permissions-datalocationresource-s3resource
            """
            return self._values.get('s3_resource')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DataLocationResourceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissions.DatabaseResourceProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class DatabaseResourceProperty():
        def __init__(self, *, name: typing.Optional[str]=None) -> None:
            """
            :param name: ``CfnPermissions.DatabaseResourceProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-databaseresource.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPermissions.DatabaseResourceProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-databaseresource.html#cfn-lakeformation-permissions-databaseresource-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DatabaseResourceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissions.ResourceProperty", jsii_struct_bases=[], name_mapping={'database_resource': 'databaseResource', 'data_location_resource': 'dataLocationResource', 'table_resource': 'tableResource', 'table_with_columns_resource': 'tableWithColumnsResource'})
    class ResourceProperty():
        def __init__(self, *, database_resource: typing.Optional[typing.Union["CfnPermissions.DatabaseResourceProperty", _IResolvable_9ceae33e]]=None, data_location_resource: typing.Optional[typing.Union["CfnPermissions.DataLocationResourceProperty", _IResolvable_9ceae33e]]=None, table_resource: typing.Optional[typing.Union["CfnPermissions.TableResourceProperty", _IResolvable_9ceae33e]]=None, table_with_columns_resource: typing.Optional[typing.Union["CfnPermissions.TableWithColumnsResourceProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param database_resource: ``CfnPermissions.ResourceProperty.DatabaseResource``.
            :param data_location_resource: ``CfnPermissions.ResourceProperty.DataLocationResource``.
            :param table_resource: ``CfnPermissions.ResourceProperty.TableResource``.
            :param table_with_columns_resource: ``CfnPermissions.ResourceProperty.TableWithColumnsResource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html
            """
            self._values = {
            }
            if database_resource is not None: self._values["database_resource"] = database_resource
            if data_location_resource is not None: self._values["data_location_resource"] = data_location_resource
            if table_resource is not None: self._values["table_resource"] = table_resource
            if table_with_columns_resource is not None: self._values["table_with_columns_resource"] = table_with_columns_resource

        @builtins.property
        def database_resource(self) -> typing.Optional[typing.Union["CfnPermissions.DatabaseResourceProperty", _IResolvable_9ceae33e]]:
            """``CfnPermissions.ResourceProperty.DatabaseResource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html#cfn-lakeformation-permissions-resource-databaseresource
            """
            return self._values.get('database_resource')

        @builtins.property
        def data_location_resource(self) -> typing.Optional[typing.Union["CfnPermissions.DataLocationResourceProperty", _IResolvable_9ceae33e]]:
            """``CfnPermissions.ResourceProperty.DataLocationResource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html#cfn-lakeformation-permissions-resource-datalocationresource
            """
            return self._values.get('data_location_resource')

        @builtins.property
        def table_resource(self) -> typing.Optional[typing.Union["CfnPermissions.TableResourceProperty", _IResolvable_9ceae33e]]:
            """``CfnPermissions.ResourceProperty.TableResource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html#cfn-lakeformation-permissions-resource-tableresource
            """
            return self._values.get('table_resource')

        @builtins.property
        def table_with_columns_resource(self) -> typing.Optional[typing.Union["CfnPermissions.TableWithColumnsResourceProperty", _IResolvable_9ceae33e]]:
            """``CfnPermissions.ResourceProperty.TableWithColumnsResource``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html#cfn-lakeformation-permissions-resource-tablewithcolumnsresource
            """
            return self._values.get('table_with_columns_resource')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResourceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissions.TableResourceProperty", jsii_struct_bases=[], name_mapping={'database_name': 'databaseName', 'name': 'name'})
    class TableResourceProperty():
        def __init__(self, *, database_name: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
            """
            :param database_name: ``CfnPermissions.TableResourceProperty.DatabaseName``.
            :param name: ``CfnPermissions.TableResourceProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tableresource.html
            """
            self._values = {
            }
            if database_name is not None: self._values["database_name"] = database_name
            if name is not None: self._values["name"] = name

        @builtins.property
        def database_name(self) -> typing.Optional[str]:
            """``CfnPermissions.TableResourceProperty.DatabaseName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tableresource.html#cfn-lakeformation-permissions-tableresource-databasename
            """
            return self._values.get('database_name')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPermissions.TableResourceProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tableresource.html#cfn-lakeformation-permissions-tableresource-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TableResourceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissions.TableWithColumnsResourceProperty", jsii_struct_bases=[], name_mapping={'column_names': 'columnNames', 'column_wildcard': 'columnWildcard', 'database_name': 'databaseName', 'name': 'name'})
    class TableWithColumnsResourceProperty():
        def __init__(self, *, column_names: typing.Optional[typing.List[str]]=None, column_wildcard: typing.Optional[typing.Union["CfnPermissions.ColumnWildcardProperty", _IResolvable_9ceae33e]]=None, database_name: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
            """
            :param column_names: ``CfnPermissions.TableWithColumnsResourceProperty.ColumnNames``.
            :param column_wildcard: ``CfnPermissions.TableWithColumnsResourceProperty.ColumnWildcard``.
            :param database_name: ``CfnPermissions.TableWithColumnsResourceProperty.DatabaseName``.
            :param name: ``CfnPermissions.TableWithColumnsResourceProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html
            """
            self._values = {
            }
            if column_names is not None: self._values["column_names"] = column_names
            if column_wildcard is not None: self._values["column_wildcard"] = column_wildcard
            if database_name is not None: self._values["database_name"] = database_name
            if name is not None: self._values["name"] = name

        @builtins.property
        def column_names(self) -> typing.Optional[typing.List[str]]:
            """``CfnPermissions.TableWithColumnsResourceProperty.ColumnNames``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-columnnames
            """
            return self._values.get('column_names')

        @builtins.property
        def column_wildcard(self) -> typing.Optional[typing.Union["CfnPermissions.ColumnWildcardProperty", _IResolvable_9ceae33e]]:
            """``CfnPermissions.TableWithColumnsResourceProperty.ColumnWildcard``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-columnwildcard
            """
            return self._values.get('column_wildcard')

        @builtins.property
        def database_name(self) -> typing.Optional[str]:
            """``CfnPermissions.TableWithColumnsResourceProperty.DatabaseName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-databasename
            """
            return self._values.get('database_name')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnPermissions.TableWithColumnsResourceProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TableWithColumnsResourceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnPermissionsProps", jsii_struct_bases=[], name_mapping={'data_lake_principal': 'dataLakePrincipal', 'resource': 'resource', 'permissions': 'permissions', 'permissions_with_grant_option': 'permissionsWithGrantOption'})
class CfnPermissionsProps():
    def __init__(self, *, data_lake_principal: typing.Union["CfnPermissions.DataLakePrincipalProperty", _IResolvable_9ceae33e], resource: typing.Union["CfnPermissions.ResourceProperty", _IResolvable_9ceae33e], permissions: typing.Optional[typing.List[str]]=None, permissions_with_grant_option: typing.Optional[typing.List[str]]=None) -> None:
        """Properties for defining a ``AWS::LakeFormation::Permissions``.

        :param data_lake_principal: ``AWS::LakeFormation::Permissions.DataLakePrincipal``.
        :param resource: ``AWS::LakeFormation::Permissions.Resource``.
        :param permissions: ``AWS::LakeFormation::Permissions.Permissions``.
        :param permissions_with_grant_option: ``AWS::LakeFormation::Permissions.PermissionsWithGrantOption``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html
        """
        self._values = {
            'data_lake_principal': data_lake_principal,
            'resource': resource,
        }
        if permissions is not None: self._values["permissions"] = permissions
        if permissions_with_grant_option is not None: self._values["permissions_with_grant_option"] = permissions_with_grant_option

    @builtins.property
    def data_lake_principal(self) -> typing.Union["CfnPermissions.DataLakePrincipalProperty", _IResolvable_9ceae33e]:
        """``AWS::LakeFormation::Permissions.DataLakePrincipal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-datalakeprincipal
        """
        return self._values.get('data_lake_principal')

    @builtins.property
    def resource(self) -> typing.Union["CfnPermissions.ResourceProperty", _IResolvable_9ceae33e]:
        """``AWS::LakeFormation::Permissions.Resource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-resource
        """
        return self._values.get('resource')

    @builtins.property
    def permissions(self) -> typing.Optional[typing.List[str]]:
        """``AWS::LakeFormation::Permissions.Permissions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-permissions
        """
        return self._values.get('permissions')

    @builtins.property
    def permissions_with_grant_option(self) -> typing.Optional[typing.List[str]]:
        """``AWS::LakeFormation::Permissions.PermissionsWithGrantOption``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-permissionswithgrantoption
        """
        return self._values.get('permissions_with_grant_option')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPermissionsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnResource(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lakeformation.CfnResource"):
    """A CloudFormation ``AWS::LakeFormation::Resource``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html
    cloudformationResource:
    :cloudformationResource:: AWS::LakeFormation::Resource
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, resource_arn: str, use_service_linked_role: typing.Union[bool, _IResolvable_9ceae33e], role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::LakeFormation::Resource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_arn: ``AWS::LakeFormation::Resource.ResourceArn``.
        :param use_service_linked_role: ``AWS::LakeFormation::Resource.UseServiceLinkedRole``.
        :param role_arn: ``AWS::LakeFormation::Resource.RoleArn``.
        """
        props = CfnResourceProps(resource_arn=resource_arn, use_service_linked_role=use_service_linked_role, role_arn=role_arn)

        jsii.create(CfnResource, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnResource":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> str:
        """``AWS::LakeFormation::Resource.ResourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-resourcearn
        """
        return jsii.get(self, "resourceArn")

    @resource_arn.setter
    def resource_arn(self, value: str) -> None:
        jsii.set(self, "resourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="useServiceLinkedRole")
    def use_service_linked_role(self) -> typing.Union[bool, _IResolvable_9ceae33e]:
        """``AWS::LakeFormation::Resource.UseServiceLinkedRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-useservicelinkedrole
        """
        return jsii.get(self, "useServiceLinkedRole")

    @use_service_linked_role.setter
    def use_service_linked_role(self, value: typing.Union[bool, _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "useServiceLinkedRole", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::LakeFormation::Resource.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "roleArn", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_lakeformation.CfnResourceProps", jsii_struct_bases=[], name_mapping={'resource_arn': 'resourceArn', 'use_service_linked_role': 'useServiceLinkedRole', 'role_arn': 'roleArn'})
class CfnResourceProps():
    def __init__(self, *, resource_arn: str, use_service_linked_role: typing.Union[bool, _IResolvable_9ceae33e], role_arn: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::LakeFormation::Resource``.

        :param resource_arn: ``AWS::LakeFormation::Resource.ResourceArn``.
        :param use_service_linked_role: ``AWS::LakeFormation::Resource.UseServiceLinkedRole``.
        :param role_arn: ``AWS::LakeFormation::Resource.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html
        """
        self._values = {
            'resource_arn': resource_arn,
            'use_service_linked_role': use_service_linked_role,
        }
        if role_arn is not None: self._values["role_arn"] = role_arn

    @builtins.property
    def resource_arn(self) -> str:
        """``AWS::LakeFormation::Resource.ResourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-resourcearn
        """
        return self._values.get('resource_arn')

    @builtins.property
    def use_service_linked_role(self) -> typing.Union[bool, _IResolvable_9ceae33e]:
        """``AWS::LakeFormation::Resource.UseServiceLinkedRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-useservicelinkedrole
        """
        return self._values.get('use_service_linked_role')

    @builtins.property
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::LakeFormation::Resource.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-rolearn
        """
        return self._values.get('role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnDataLakeSettings",
    "CfnDataLakeSettingsProps",
    "CfnPermissions",
    "CfnPermissionsProps",
    "CfnResource",
    "CfnResourceProps",
]

publication.publish()
