"""
## AWS::Cassandra Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cassandra as cassandra
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

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnKeyspace(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cassandra.CfnKeyspace"):
    """A CloudFormation ``AWS::Cassandra::Keyspace``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cassandra::Keyspace
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, keyspace_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Cassandra::Keyspace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param keyspace_name: ``AWS::Cassandra::Keyspace.KeyspaceName``.
        """
        props = CfnKeyspaceProps(keyspace_name=keyspace_name)

        jsii.create(CfnKeyspace, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnKeyspace":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="keyspaceName")
    def keyspace_name(self) -> typing.Optional[str]:
        """``AWS::Cassandra::Keyspace.KeyspaceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-keyspacename
        """
        return jsii.get(self, "keyspaceName")

    @keyspace_name.setter
    def keyspace_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "keyspaceName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-cassandra.CfnKeyspaceProps", jsii_struct_bases=[], name_mapping={'keyspace_name': 'keyspaceName'})
class CfnKeyspaceProps():
    def __init__(self, *, keyspace_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Cassandra::Keyspace``.

        :param keyspace_name: ``AWS::Cassandra::Keyspace.KeyspaceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html
        """
        self._values = {
        }
        if keyspace_name is not None: self._values["keyspace_name"] = keyspace_name

    @builtins.property
    def keyspace_name(self) -> typing.Optional[str]:
        """``AWS::Cassandra::Keyspace.KeyspaceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html#cfn-cassandra-keyspace-keyspacename
        """
        return self._values.get('keyspace_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnKeyspaceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTable(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cassandra.CfnTable"):
    """A CloudFormation ``AWS::Cassandra::Table``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html
    cloudformationResource:
    :cloudformationResource:: AWS::Cassandra::Table
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, keyspace_name: str, partition_key_columns: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ColumnProperty", aws_cdk.core.IResolvable]]], billing_mode: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "BillingModeProperty"]]=None, clustering_key_columns: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ClusteringKeyColumnProperty"]]]]=None, regular_columns: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ColumnProperty", aws_cdk.core.IResolvable]]]]=None, table_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Cassandra::Table``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param keyspace_name: ``AWS::Cassandra::Table.KeyspaceName``.
        :param partition_key_columns: ``AWS::Cassandra::Table.PartitionKeyColumns``.
        :param billing_mode: ``AWS::Cassandra::Table.BillingMode``.
        :param clustering_key_columns: ``AWS::Cassandra::Table.ClusteringKeyColumns``.
        :param regular_columns: ``AWS::Cassandra::Table.RegularColumns``.
        :param table_name: ``AWS::Cassandra::Table.TableName``.
        """
        props = CfnTableProps(keyspace_name=keyspace_name, partition_key_columns=partition_key_columns, billing_mode=billing_mode, clustering_key_columns=clustering_key_columns, regular_columns=regular_columns, table_name=table_name)

        jsii.create(CfnTable, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnTable":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="keyspaceName")
    def keyspace_name(self) -> str:
        """``AWS::Cassandra::Table.KeyspaceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-keyspacename
        """
        return jsii.get(self, "keyspaceName")

    @keyspace_name.setter
    def keyspace_name(self, value: str) -> None:
        jsii.set(self, "keyspaceName", value)

    @builtins.property
    @jsii.member(jsii_name="partitionKeyColumns")
    def partition_key_columns(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ColumnProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::Cassandra::Table.PartitionKeyColumns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-partitionkeycolumns
        """
        return jsii.get(self, "partitionKeyColumns")

    @partition_key_columns.setter
    def partition_key_columns(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ColumnProperty", aws_cdk.core.IResolvable]]]) -> None:
        jsii.set(self, "partitionKeyColumns", value)

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "BillingModeProperty"]]:
        """``AWS::Cassandra::Table.BillingMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-billingmode
        """
        return jsii.get(self, "billingMode")

    @billing_mode.setter
    def billing_mode(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "BillingModeProperty"]]) -> None:
        jsii.set(self, "billingMode", value)

    @builtins.property
    @jsii.member(jsii_name="clusteringKeyColumns")
    def clustering_key_columns(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ClusteringKeyColumnProperty"]]]]:
        """``AWS::Cassandra::Table.ClusteringKeyColumns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-clusteringkeycolumns
        """
        return jsii.get(self, "clusteringKeyColumns")

    @clustering_key_columns.setter
    def clustering_key_columns(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ClusteringKeyColumnProperty"]]]]) -> None:
        jsii.set(self, "clusteringKeyColumns", value)

    @builtins.property
    @jsii.member(jsii_name="regularColumns")
    def regular_columns(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ColumnProperty", aws_cdk.core.IResolvable]]]]:
        """``AWS::Cassandra::Table.RegularColumns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-regularcolumns
        """
        return jsii.get(self, "regularColumns")

    @regular_columns.setter
    def regular_columns(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ColumnProperty", aws_cdk.core.IResolvable]]]]) -> None:
        jsii.set(self, "regularColumns", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[str]:
        """``AWS::Cassandra::Table.TableName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-tablename
        """
        return jsii.get(self, "tableName")

    @table_name.setter
    def table_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "tableName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-cassandra.CfnTable.BillingModeProperty", jsii_struct_bases=[], name_mapping={'mode': 'mode', 'provisioned_throughput': 'provisionedThroughput'})
    class BillingModeProperty():
        def __init__(self, *, mode: str, provisioned_throughput: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTable.ProvisionedThroughputProperty"]]=None) -> None:
            """
            :param mode: ``CfnTable.BillingModeProperty.Mode``.
            :param provisioned_throughput: ``CfnTable.BillingModeProperty.ProvisionedThroughput``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html
            """
            self._values = {
                'mode': mode,
            }
            if provisioned_throughput is not None: self._values["provisioned_throughput"] = provisioned_throughput

        @builtins.property
        def mode(self) -> str:
            """``CfnTable.BillingModeProperty.Mode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html#cfn-cassandra-table-billingmode-mode
            """
            return self._values.get('mode')

        @builtins.property
        def provisioned_throughput(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTable.ProvisionedThroughputProperty"]]:
            """``CfnTable.BillingModeProperty.ProvisionedThroughput``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-billingmode.html#cfn-cassandra-table-billingmode-provisionedthroughput
            """
            return self._values.get('provisioned_throughput')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BillingModeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cassandra.CfnTable.ClusteringKeyColumnProperty", jsii_struct_bases=[], name_mapping={'column': 'column', 'order_by': 'orderBy'})
    class ClusteringKeyColumnProperty():
        def __init__(self, *, column: typing.Union["CfnTable.ColumnProperty", aws_cdk.core.IResolvable], order_by: typing.Optional[str]=None) -> None:
            """
            :param column: ``CfnTable.ClusteringKeyColumnProperty.Column``.
            :param order_by: ``CfnTable.ClusteringKeyColumnProperty.OrderBy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html
            """
            self._values = {
                'column': column,
            }
            if order_by is not None: self._values["order_by"] = order_by

        @builtins.property
        def column(self) -> typing.Union["CfnTable.ColumnProperty", aws_cdk.core.IResolvable]:
            """``CfnTable.ClusteringKeyColumnProperty.Column``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html#cfn-cassandra-table-clusteringkeycolumn-column
            """
            return self._values.get('column')

        @builtins.property
        def order_by(self) -> typing.Optional[str]:
            """``CfnTable.ClusteringKeyColumnProperty.OrderBy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-clusteringkeycolumn.html#cfn-cassandra-table-clusteringkeycolumn-orderby
            """
            return self._values.get('order_by')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ClusteringKeyColumnProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cassandra.CfnTable.ColumnProperty", jsii_struct_bases=[], name_mapping={'column_name': 'columnName', 'column_type': 'columnType'})
    class ColumnProperty():
        def __init__(self, *, column_name: str, column_type: str) -> None:
            """
            :param column_name: ``CfnTable.ColumnProperty.ColumnName``.
            :param column_type: ``CfnTable.ColumnProperty.ColumnType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html
            """
            self._values = {
                'column_name': column_name,
                'column_type': column_type,
            }

        @builtins.property
        def column_name(self) -> str:
            """``CfnTable.ColumnProperty.ColumnName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html#cfn-cassandra-table-column-columnname
            """
            return self._values.get('column_name')

        @builtins.property
        def column_type(self) -> str:
            """``CfnTable.ColumnProperty.ColumnType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-column.html#cfn-cassandra-table-column-columntype
            """
            return self._values.get('column_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ColumnProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-cassandra.CfnTable.ProvisionedThroughputProperty", jsii_struct_bases=[], name_mapping={'read_capacity_units': 'readCapacityUnits', 'write_capacity_units': 'writeCapacityUnits'})
    class ProvisionedThroughputProperty():
        def __init__(self, *, read_capacity_units: jsii.Number, write_capacity_units: jsii.Number) -> None:
            """
            :param read_capacity_units: ``CfnTable.ProvisionedThroughputProperty.ReadCapacityUnits``.
            :param write_capacity_units: ``CfnTable.ProvisionedThroughputProperty.WriteCapacityUnits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html
            """
            self._values = {
                'read_capacity_units': read_capacity_units,
                'write_capacity_units': write_capacity_units,
            }

        @builtins.property
        def read_capacity_units(self) -> jsii.Number:
            """``CfnTable.ProvisionedThroughputProperty.ReadCapacityUnits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html#cfn-cassandra-table-provisionedthroughput-readcapacityunits
            """
            return self._values.get('read_capacity_units')

        @builtins.property
        def write_capacity_units(self) -> jsii.Number:
            """``CfnTable.ProvisionedThroughputProperty.WriteCapacityUnits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cassandra-table-provisionedthroughput.html#cfn-cassandra-table-provisionedthroughput-writecapacityunits
            """
            return self._values.get('write_capacity_units')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProvisionedThroughputProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-cassandra.CfnTableProps", jsii_struct_bases=[], name_mapping={'keyspace_name': 'keyspaceName', 'partition_key_columns': 'partitionKeyColumns', 'billing_mode': 'billingMode', 'clustering_key_columns': 'clusteringKeyColumns', 'regular_columns': 'regularColumns', 'table_name': 'tableName'})
class CfnTableProps():
    def __init__(self, *, keyspace_name: str, partition_key_columns: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnTable.ColumnProperty", aws_cdk.core.IResolvable]]], billing_mode: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTable.BillingModeProperty"]]=None, clustering_key_columns: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTable.ClusteringKeyColumnProperty"]]]]=None, regular_columns: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnTable.ColumnProperty", aws_cdk.core.IResolvable]]]]=None, table_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Cassandra::Table``.

        :param keyspace_name: ``AWS::Cassandra::Table.KeyspaceName``.
        :param partition_key_columns: ``AWS::Cassandra::Table.PartitionKeyColumns``.
        :param billing_mode: ``AWS::Cassandra::Table.BillingMode``.
        :param clustering_key_columns: ``AWS::Cassandra::Table.ClusteringKeyColumns``.
        :param regular_columns: ``AWS::Cassandra::Table.RegularColumns``.
        :param table_name: ``AWS::Cassandra::Table.TableName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html
        """
        self._values = {
            'keyspace_name': keyspace_name,
            'partition_key_columns': partition_key_columns,
        }
        if billing_mode is not None: self._values["billing_mode"] = billing_mode
        if clustering_key_columns is not None: self._values["clustering_key_columns"] = clustering_key_columns
        if regular_columns is not None: self._values["regular_columns"] = regular_columns
        if table_name is not None: self._values["table_name"] = table_name

    @builtins.property
    def keyspace_name(self) -> str:
        """``AWS::Cassandra::Table.KeyspaceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-keyspacename
        """
        return self._values.get('keyspace_name')

    @builtins.property
    def partition_key_columns(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnTable.ColumnProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::Cassandra::Table.PartitionKeyColumns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-partitionkeycolumns
        """
        return self._values.get('partition_key_columns')

    @builtins.property
    def billing_mode(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTable.BillingModeProperty"]]:
        """``AWS::Cassandra::Table.BillingMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-billingmode
        """
        return self._values.get('billing_mode')

    @builtins.property
    def clustering_key_columns(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTable.ClusteringKeyColumnProperty"]]]]:
        """``AWS::Cassandra::Table.ClusteringKeyColumns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-clusteringkeycolumns
        """
        return self._values.get('clustering_key_columns')

    @builtins.property
    def regular_columns(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnTable.ColumnProperty", aws_cdk.core.IResolvable]]]]:
        """``AWS::Cassandra::Table.RegularColumns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-regularcolumns
        """
        return self._values.get('regular_columns')

    @builtins.property
    def table_name(self) -> typing.Optional[str]:
        """``AWS::Cassandra::Table.TableName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html#cfn-cassandra-table-tablename
        """
        return self._values.get('table_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTableProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnKeyspace",
    "CfnKeyspaceProps",
    "CfnTable",
    "CfnTableProps",
]

publication.publish()
