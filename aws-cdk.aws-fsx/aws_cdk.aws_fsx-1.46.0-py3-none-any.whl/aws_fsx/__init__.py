"""
## Amazon FSx Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[Amazon FSx](https://docs.aws.amazon.com/fsx/?id=docs_gateway) provides fully managed third-party file systems with the
native compatibility and feature sets for workloads such as Microsoft Windows–based storage, high-performance computing,
machine learning, and electronic design automation.

Amazon FSx supports two file system types: [Lustre](https://docs.aws.amazon.com/fsx/latest/LustreGuide/index.html) and
[Windows](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/index.html) File Server.

## FSx for Lustre

Amazon FSx for Lustre makes it easy and cost-effective to launch and run the popular, high-performance Lustre file
system. You use Lustre for workloads where speed matters, such as machine learning, high performance computing (HPC),
video processing, and financial modeling.

The open-source Lustre file system is designed for applications that require fast storage—where you want your storage
to keep up with your compute. Lustre was built to solve the problem of quickly and cheaply processing the world's
ever-growing datasets. It's a widely used file system designed for the fastest computers in the world. It provides
submillisecond latencies, up to hundreds of GBps of throughput, and up to millions of IOPS. For more information on
Lustre, see the [Lustre website](http://lustre.org/).

As a fully managed service, Amazon FSx makes it easier for you to use Lustre for workloads where storage speed matters.
Amazon FSx for Lustre eliminates the traditional complexity of setting up and managing Lustre file systems, enabling
you to spin up and run a battle-tested high-performance file system in minutes. It also provides multiple deployment
options so you can optimize cost for your needs.

Amazon FSx for Lustre is POSIX-compliant, so you can use your current Linux-based applications without having to make
any changes. Amazon FSx for Lustre provides a native file system interface and works as any file system does with your
Linux operating system. It also provides read-after-write consistency and supports file locking.

### Installation

Import to your project:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_fsx as fsx
```

### Basic Usage

Setup required properties and create:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stack = Stack(app, "Stack")
vpc = Vpc(stack, "VPC")

file_system = LustreFileSystem(stack, "FsxLustreFileSystem",
    lustre_configuration={"deployment_type": LustreDeploymentType.SCRATCH_2},
    storage_capacity_gi_b=1200,
    vpc=vpc,
    vpc_subnet=vpc.privateSubnets[0]
)
```

### Connecting

To control who can access the file system, use the `.connections` attribute. FSx has a fixed default port, so you don't
need to specify the port. This example allows an EC2 instance to connect to a file system:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
file_system.connections.allow_default_port_from(instance)
```

### Mounting

The LustreFileSystem Construct exposes both the DNS name of the file system as well as its mount name, which can be
used to mount the file system on an EC2 instance. The following example shows how to bring up a file system and EC2
instance, and then use User Data to mount the file system on the instance at start-up:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = App()
stack = Stack(app, "AwsCdkFsxLustre")
vpc = Vpc(stack, "VPC")

lustre_configuration = {
    "deployment_type": LustreDeploymentType.SCRATCH_2
}
fs = LustreFileSystem(stack, "FsxLustreFileSystem",
    lustre_configuration=lustre_configuration,
    storage_capacity_gi_b=1200,
    vpc=vpc,
    vpc_subnet=vpc.privateSubnets[0]
)

inst = Instance(stack, "inst",
    instance_type=InstanceType.of(InstanceClass.T2, InstanceSize.LARGE),
    machine_image=AmazonLinuxImage(
        generation=AmazonLinuxGeneration.AMAZON_LINUX_2
    ),
    vpc=vpc,
    vpc_subnets={
        "subnet_type": SubnetType.PUBLIC
    }
)
fs.connections.allow_default_port_from(inst)

# Need to give the instance access to read information about FSx to determine the file system's mount name.
inst.role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AmazonFSxReadOnlyAccess"))

mount_path = "/mnt/fsx"
dns_name = fs.dns_name
mount_name = fs.mount_name

inst.user_data.add_commands("set -eux", "yum update -y", "amazon-linux-extras install -y lustre2.10", f"mkdir -p {mountPath}", f"chmod 777 {mountPath}", f"chown ec2-user:ec2-user {mountPath}", f"echo \"{dnsName}@tcp:/{mountName} {mountPath} lustre defaults,noatime,flock,_netdev 0 0\" >> /etc/fstab", "mount -a")
```

### Importing

An FSx for Lustre file system can be imported with `fromLustreFileSystemAttributes(stack, id, attributes)`. The
following example lays out how you could import the SecurityGroup a file system belongs to, use that to import the file
system, and then also import the VPC the file system is in and add an EC2 instance to it, giving it access to the file
system.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = App()
stack = Stack(app, "AwsCdkFsxLustreImport")

sg = SecurityGroup.from_security_group_id(stack, "FsxSecurityGroup", "{SECURITY-GROUP-ID}")
fs = LustreFileSystem.from_lustre_file_system_attributes(stack, "FsxLustreFileSystem",
    dns_name="{FILE-SYSTEM-DNS-NAME}",
    file_system_id="{FILE-SYSTEM-ID}",
    security_group=sg
)

vpc = Vpc.from_vpc_attributes(stack, "Vpc",
    availability_zones=["us-west-2a", "us-west-2b"],
    public_subnet_ids=["{US-WEST-2A-SUBNET-ID}", "{US-WEST-2B-SUBNET-ID}"],
    vpc_id="{VPC-ID}"
)
inst = Instance(stack, "inst",
    instance_type=InstanceType.of(InstanceClass.T2, InstanceSize.LARGE),
    machine_image=AmazonLinuxImage(
        generation=AmazonLinuxGeneration.AMAZON_LINUX_2
    ),
    vpc=vpc,
    vpc_subnets={
        "subnet_type": SubnetType.PUBLIC
    }
)
fs.connections.allow_default_port_from(inst)
```

## FSx for Windows File Server

The L2 construct for the FSx for Windows File Server has not yet been implemented. To instantiate an FSx for Windows
file system, the L1 constructs can be used as defined by CloudFormation.
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
import aws_cdk.aws_kms
import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnFileSystem(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-fsx.CfnFileSystem"):
    """A CloudFormation ``AWS::FSx::FileSystem``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html
    cloudformationResource:
    :cloudformationResource:: AWS::FSx::FileSystem
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, file_system_type: str, subnet_ids: typing.List[str], backup_id: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, lustre_configuration: typing.Optional[typing.Union["LustreConfigurationProperty", aws_cdk.core.IResolvable]]=None, security_group_ids: typing.Optional[typing.List[str]]=None, storage_capacity: typing.Optional[jsii.Number]=None, storage_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, windows_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "WindowsConfigurationProperty"]]=None) -> None:
        """Create a new ``AWS::FSx::FileSystem``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_type: ``AWS::FSx::FileSystem.FileSystemType``.
        :param subnet_ids: ``AWS::FSx::FileSystem.SubnetIds``.
        :param backup_id: ``AWS::FSx::FileSystem.BackupId``.
        :param kms_key_id: ``AWS::FSx::FileSystem.KmsKeyId``.
        :param lustre_configuration: ``AWS::FSx::FileSystem.LustreConfiguration``.
        :param security_group_ids: ``AWS::FSx::FileSystem.SecurityGroupIds``.
        :param storage_capacity: ``AWS::FSx::FileSystem.StorageCapacity``.
        :param storage_type: ``AWS::FSx::FileSystem.StorageType``.
        :param tags: ``AWS::FSx::FileSystem.Tags``.
        :param windows_configuration: ``AWS::FSx::FileSystem.WindowsConfiguration``.
        """
        props = CfnFileSystemProps(file_system_type=file_system_type, subnet_ids=subnet_ids, backup_id=backup_id, kms_key_id=kms_key_id, lustre_configuration=lustre_configuration, security_group_ids=security_group_ids, storage_capacity=storage_capacity, storage_type=storage_type, tags=tags, windows_configuration=windows_configuration)

        jsii.create(CfnFileSystem, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnFileSystem":
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
    @jsii.member(jsii_name="attrLustreMountName")
    def attr_lustre_mount_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: LustreMountName
        """
        return jsii.get(self, "attrLustreMountName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::FSx::FileSystem.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="fileSystemType")
    def file_system_type(self) -> str:
        """``AWS::FSx::FileSystem.FileSystemType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-filesystemtype
        """
        return jsii.get(self, "fileSystemType")

    @file_system_type.setter
    def file_system_type(self, value: str) -> None:
        jsii.set(self, "fileSystemType", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::FSx::FileSystem.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="backupId")
    def backup_id(self) -> typing.Optional[str]:
        """``AWS::FSx::FileSystem.BackupId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-backupid
        """
        return jsii.get(self, "backupId")

    @backup_id.setter
    def backup_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "backupId", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::FSx::FileSystem.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="lustreConfiguration")
    def lustre_configuration(self) -> typing.Optional[typing.Union["LustreConfigurationProperty", aws_cdk.core.IResolvable]]:
        """``AWS::FSx::FileSystem.LustreConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-lustreconfiguration
        """
        return jsii.get(self, "lustreConfiguration")

    @lustre_configuration.setter
    def lustre_configuration(self, value: typing.Optional[typing.Union["LustreConfigurationProperty", aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "lustreConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::FSx::FileSystem.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter
    def security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="storageCapacity")
    def storage_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::FSx::FileSystem.StorageCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-storagecapacity
        """
        return jsii.get(self, "storageCapacity")

    @storage_capacity.setter
    def storage_capacity(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "storageCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> typing.Optional[str]:
        """``AWS::FSx::FileSystem.StorageType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-storagetype
        """
        return jsii.get(self, "storageType")

    @storage_type.setter
    def storage_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "storageType", value)

    @builtins.property
    @jsii.member(jsii_name="windowsConfiguration")
    def windows_configuration(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "WindowsConfigurationProperty"]]:
        """``AWS::FSx::FileSystem.WindowsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-windowsconfiguration
        """
        return jsii.get(self, "windowsConfiguration")

    @windows_configuration.setter
    def windows_configuration(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "WindowsConfigurationProperty"]]) -> None:
        jsii.set(self, "windowsConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-fsx.CfnFileSystem.LustreConfigurationProperty", jsii_struct_bases=[], name_mapping={'deployment_type': 'deploymentType', 'export_path': 'exportPath', 'imported_file_chunk_size': 'importedFileChunkSize', 'import_path': 'importPath', 'per_unit_storage_throughput': 'perUnitStorageThroughput', 'weekly_maintenance_start_time': 'weeklyMaintenanceStartTime'})
    class LustreConfigurationProperty():
        def __init__(self, *, deployment_type: typing.Optional[str]=None, export_path: typing.Optional[str]=None, imported_file_chunk_size: typing.Optional[jsii.Number]=None, import_path: typing.Optional[str]=None, per_unit_storage_throughput: typing.Optional[jsii.Number]=None, weekly_maintenance_start_time: typing.Optional[str]=None) -> None:
            """
            :param deployment_type: ``CfnFileSystem.LustreConfigurationProperty.DeploymentType``.
            :param export_path: ``CfnFileSystem.LustreConfigurationProperty.ExportPath``.
            :param imported_file_chunk_size: ``CfnFileSystem.LustreConfigurationProperty.ImportedFileChunkSize``.
            :param import_path: ``CfnFileSystem.LustreConfigurationProperty.ImportPath``.
            :param per_unit_storage_throughput: ``CfnFileSystem.LustreConfigurationProperty.PerUnitStorageThroughput``.
            :param weekly_maintenance_start_time: ``CfnFileSystem.LustreConfigurationProperty.WeeklyMaintenanceStartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html
            """
            self._values = {
            }
            if deployment_type is not None: self._values["deployment_type"] = deployment_type
            if export_path is not None: self._values["export_path"] = export_path
            if imported_file_chunk_size is not None: self._values["imported_file_chunk_size"] = imported_file_chunk_size
            if import_path is not None: self._values["import_path"] = import_path
            if per_unit_storage_throughput is not None: self._values["per_unit_storage_throughput"] = per_unit_storage_throughput
            if weekly_maintenance_start_time is not None: self._values["weekly_maintenance_start_time"] = weekly_maintenance_start_time

        @builtins.property
        def deployment_type(self) -> typing.Optional[str]:
            """``CfnFileSystem.LustreConfigurationProperty.DeploymentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-deploymenttype
            """
            return self._values.get('deployment_type')

        @builtins.property
        def export_path(self) -> typing.Optional[str]:
            """``CfnFileSystem.LustreConfigurationProperty.ExportPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-exportpath
            """
            return self._values.get('export_path')

        @builtins.property
        def imported_file_chunk_size(self) -> typing.Optional[jsii.Number]:
            """``CfnFileSystem.LustreConfigurationProperty.ImportedFileChunkSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-importedfilechunksize
            """
            return self._values.get('imported_file_chunk_size')

        @builtins.property
        def import_path(self) -> typing.Optional[str]:
            """``CfnFileSystem.LustreConfigurationProperty.ImportPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-importpath
            """
            return self._values.get('import_path')

        @builtins.property
        def per_unit_storage_throughput(self) -> typing.Optional[jsii.Number]:
            """``CfnFileSystem.LustreConfigurationProperty.PerUnitStorageThroughput``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-perunitstoragethroughput
            """
            return self._values.get('per_unit_storage_throughput')

        @builtins.property
        def weekly_maintenance_start_time(self) -> typing.Optional[str]:
            """``CfnFileSystem.LustreConfigurationProperty.WeeklyMaintenanceStartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-weeklymaintenancestarttime
            """
            return self._values.get('weekly_maintenance_start_time')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LustreConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-fsx.CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty", jsii_struct_bases=[], name_mapping={'dns_ips': 'dnsIps', 'domain_name': 'domainName', 'file_system_administrators_group': 'fileSystemAdministratorsGroup', 'organizational_unit_distinguished_name': 'organizationalUnitDistinguishedName', 'password': 'password', 'user_name': 'userName'})
    class SelfManagedActiveDirectoryConfigurationProperty():
        def __init__(self, *, dns_ips: typing.Optional[typing.List[str]]=None, domain_name: typing.Optional[str]=None, file_system_administrators_group: typing.Optional[str]=None, organizational_unit_distinguished_name: typing.Optional[str]=None, password: typing.Optional[str]=None, user_name: typing.Optional[str]=None) -> None:
            """
            :param dns_ips: ``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.DnsIps``.
            :param domain_name: ``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.DomainName``.
            :param file_system_administrators_group: ``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.FileSystemAdministratorsGroup``.
            :param organizational_unit_distinguished_name: ``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.OrganizationalUnitDistinguishedName``.
            :param password: ``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.Password``.
            :param user_name: ``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.UserName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration.html
            """
            self._values = {
            }
            if dns_ips is not None: self._values["dns_ips"] = dns_ips
            if domain_name is not None: self._values["domain_name"] = domain_name
            if file_system_administrators_group is not None: self._values["file_system_administrators_group"] = file_system_administrators_group
            if organizational_unit_distinguished_name is not None: self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name
            if password is not None: self._values["password"] = password
            if user_name is not None: self._values["user_name"] = user_name

        @builtins.property
        def dns_ips(self) -> typing.Optional[typing.List[str]]:
            """``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.DnsIps``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration-dnsips
            """
            return self._values.get('dns_ips')

        @builtins.property
        def domain_name(self) -> typing.Optional[str]:
            """``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.DomainName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration-domainname
            """
            return self._values.get('domain_name')

        @builtins.property
        def file_system_administrators_group(self) -> typing.Optional[str]:
            """``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.FileSystemAdministratorsGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration-filesystemadministratorsgroup
            """
            return self._values.get('file_system_administrators_group')

        @builtins.property
        def organizational_unit_distinguished_name(self) -> typing.Optional[str]:
            """``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.OrganizationalUnitDistinguishedName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration-organizationalunitdistinguishedname
            """
            return self._values.get('organizational_unit_distinguished_name')

        @builtins.property
        def password(self) -> typing.Optional[str]:
            """``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.Password``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration-password
            """
            return self._values.get('password')

        @builtins.property
        def user_name(self) -> typing.Optional[str]:
            """``CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty.UserName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration-username
            """
            return self._values.get('user_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SelfManagedActiveDirectoryConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-fsx.CfnFileSystem.WindowsConfigurationProperty", jsii_struct_bases=[], name_mapping={'active_directory_id': 'activeDirectoryId', 'automatic_backup_retention_days': 'automaticBackupRetentionDays', 'copy_tags_to_backups': 'copyTagsToBackups', 'daily_automatic_backup_start_time': 'dailyAutomaticBackupStartTime', 'deployment_type': 'deploymentType', 'preferred_subnet_id': 'preferredSubnetId', 'self_managed_active_directory_configuration': 'selfManagedActiveDirectoryConfiguration', 'throughput_capacity': 'throughputCapacity', 'weekly_maintenance_start_time': 'weeklyMaintenanceStartTime'})
    class WindowsConfigurationProperty():
        def __init__(self, *, active_directory_id: typing.Optional[str]=None, automatic_backup_retention_days: typing.Optional[jsii.Number]=None, copy_tags_to_backups: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, daily_automatic_backup_start_time: typing.Optional[str]=None, deployment_type: typing.Optional[str]=None, preferred_subnet_id: typing.Optional[str]=None, self_managed_active_directory_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty"]]=None, throughput_capacity: typing.Optional[jsii.Number]=None, weekly_maintenance_start_time: typing.Optional[str]=None) -> None:
            """
            :param active_directory_id: ``CfnFileSystem.WindowsConfigurationProperty.ActiveDirectoryId``.
            :param automatic_backup_retention_days: ``CfnFileSystem.WindowsConfigurationProperty.AutomaticBackupRetentionDays``.
            :param copy_tags_to_backups: ``CfnFileSystem.WindowsConfigurationProperty.CopyTagsToBackups``.
            :param daily_automatic_backup_start_time: ``CfnFileSystem.WindowsConfigurationProperty.DailyAutomaticBackupStartTime``.
            :param deployment_type: ``CfnFileSystem.WindowsConfigurationProperty.DeploymentType``.
            :param preferred_subnet_id: ``CfnFileSystem.WindowsConfigurationProperty.PreferredSubnetId``.
            :param self_managed_active_directory_configuration: ``CfnFileSystem.WindowsConfigurationProperty.SelfManagedActiveDirectoryConfiguration``.
            :param throughput_capacity: ``CfnFileSystem.WindowsConfigurationProperty.ThroughputCapacity``.
            :param weekly_maintenance_start_time: ``CfnFileSystem.WindowsConfigurationProperty.WeeklyMaintenanceStartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html
            """
            self._values = {
            }
            if active_directory_id is not None: self._values["active_directory_id"] = active_directory_id
            if automatic_backup_retention_days is not None: self._values["automatic_backup_retention_days"] = automatic_backup_retention_days
            if copy_tags_to_backups is not None: self._values["copy_tags_to_backups"] = copy_tags_to_backups
            if daily_automatic_backup_start_time is not None: self._values["daily_automatic_backup_start_time"] = daily_automatic_backup_start_time
            if deployment_type is not None: self._values["deployment_type"] = deployment_type
            if preferred_subnet_id is not None: self._values["preferred_subnet_id"] = preferred_subnet_id
            if self_managed_active_directory_configuration is not None: self._values["self_managed_active_directory_configuration"] = self_managed_active_directory_configuration
            if throughput_capacity is not None: self._values["throughput_capacity"] = throughput_capacity
            if weekly_maintenance_start_time is not None: self._values["weekly_maintenance_start_time"] = weekly_maintenance_start_time

        @builtins.property
        def active_directory_id(self) -> typing.Optional[str]:
            """``CfnFileSystem.WindowsConfigurationProperty.ActiveDirectoryId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-activedirectoryid
            """
            return self._values.get('active_directory_id')

        @builtins.property
        def automatic_backup_retention_days(self) -> typing.Optional[jsii.Number]:
            """``CfnFileSystem.WindowsConfigurationProperty.AutomaticBackupRetentionDays``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-automaticbackupretentiondays
            """
            return self._values.get('automatic_backup_retention_days')

        @builtins.property
        def copy_tags_to_backups(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnFileSystem.WindowsConfigurationProperty.CopyTagsToBackups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-copytagstobackups
            """
            return self._values.get('copy_tags_to_backups')

        @builtins.property
        def daily_automatic_backup_start_time(self) -> typing.Optional[str]:
            """``CfnFileSystem.WindowsConfigurationProperty.DailyAutomaticBackupStartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-dailyautomaticbackupstarttime
            """
            return self._values.get('daily_automatic_backup_start_time')

        @builtins.property
        def deployment_type(self) -> typing.Optional[str]:
            """``CfnFileSystem.WindowsConfigurationProperty.DeploymentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-deploymenttype
            """
            return self._values.get('deployment_type')

        @builtins.property
        def preferred_subnet_id(self) -> typing.Optional[str]:
            """``CfnFileSystem.WindowsConfigurationProperty.PreferredSubnetId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-preferredsubnetid
            """
            return self._values.get('preferred_subnet_id')

        @builtins.property
        def self_managed_active_directory_configuration(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty"]]:
            """``CfnFileSystem.WindowsConfigurationProperty.SelfManagedActiveDirectoryConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration
            """
            return self._values.get('self_managed_active_directory_configuration')

        @builtins.property
        def throughput_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnFileSystem.WindowsConfigurationProperty.ThroughputCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-throughputcapacity
            """
            return self._values.get('throughput_capacity')

        @builtins.property
        def weekly_maintenance_start_time(self) -> typing.Optional[str]:
            """``CfnFileSystem.WindowsConfigurationProperty.WeeklyMaintenanceStartTime``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-weeklymaintenancestarttime
            """
            return self._values.get('weekly_maintenance_start_time')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WindowsConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-fsx.CfnFileSystemProps", jsii_struct_bases=[], name_mapping={'file_system_type': 'fileSystemType', 'subnet_ids': 'subnetIds', 'backup_id': 'backupId', 'kms_key_id': 'kmsKeyId', 'lustre_configuration': 'lustreConfiguration', 'security_group_ids': 'securityGroupIds', 'storage_capacity': 'storageCapacity', 'storage_type': 'storageType', 'tags': 'tags', 'windows_configuration': 'windowsConfiguration'})
class CfnFileSystemProps():
    def __init__(self, *, file_system_type: str, subnet_ids: typing.List[str], backup_id: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, lustre_configuration: typing.Optional[typing.Union["CfnFileSystem.LustreConfigurationProperty", aws_cdk.core.IResolvable]]=None, security_group_ids: typing.Optional[typing.List[str]]=None, storage_capacity: typing.Optional[jsii.Number]=None, storage_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, windows_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.WindowsConfigurationProperty"]]=None) -> None:
        """Properties for defining a ``AWS::FSx::FileSystem``.

        :param file_system_type: ``AWS::FSx::FileSystem.FileSystemType``.
        :param subnet_ids: ``AWS::FSx::FileSystem.SubnetIds``.
        :param backup_id: ``AWS::FSx::FileSystem.BackupId``.
        :param kms_key_id: ``AWS::FSx::FileSystem.KmsKeyId``.
        :param lustre_configuration: ``AWS::FSx::FileSystem.LustreConfiguration``.
        :param security_group_ids: ``AWS::FSx::FileSystem.SecurityGroupIds``.
        :param storage_capacity: ``AWS::FSx::FileSystem.StorageCapacity``.
        :param storage_type: ``AWS::FSx::FileSystem.StorageType``.
        :param tags: ``AWS::FSx::FileSystem.Tags``.
        :param windows_configuration: ``AWS::FSx::FileSystem.WindowsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html
        """
        self._values = {
            'file_system_type': file_system_type,
            'subnet_ids': subnet_ids,
        }
        if backup_id is not None: self._values["backup_id"] = backup_id
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if lustre_configuration is not None: self._values["lustre_configuration"] = lustre_configuration
        if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids
        if storage_capacity is not None: self._values["storage_capacity"] = storage_capacity
        if storage_type is not None: self._values["storage_type"] = storage_type
        if tags is not None: self._values["tags"] = tags
        if windows_configuration is not None: self._values["windows_configuration"] = windows_configuration

    @builtins.property
    def file_system_type(self) -> str:
        """``AWS::FSx::FileSystem.FileSystemType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-filesystemtype
        """
        return self._values.get('file_system_type')

    @builtins.property
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::FSx::FileSystem.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-subnetids
        """
        return self._values.get('subnet_ids')

    @builtins.property
    def backup_id(self) -> typing.Optional[str]:
        """``AWS::FSx::FileSystem.BackupId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-backupid
        """
        return self._values.get('backup_id')

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::FSx::FileSystem.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-kmskeyid
        """
        return self._values.get('kms_key_id')

    @builtins.property
    def lustre_configuration(self) -> typing.Optional[typing.Union["CfnFileSystem.LustreConfigurationProperty", aws_cdk.core.IResolvable]]:
        """``AWS::FSx::FileSystem.LustreConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-lustreconfiguration
        """
        return self._values.get('lustre_configuration')

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::FSx::FileSystem.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-securitygroupids
        """
        return self._values.get('security_group_ids')

    @builtins.property
    def storage_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::FSx::FileSystem.StorageCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-storagecapacity
        """
        return self._values.get('storage_capacity')

    @builtins.property
    def storage_type(self) -> typing.Optional[str]:
        """``AWS::FSx::FileSystem.StorageType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-storagetype
        """
        return self._values.get('storage_type')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::FSx::FileSystem.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-tags
        """
        return self._values.get('tags')

    @builtins.property
    def windows_configuration(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.WindowsConfigurationProperty"]]:
        """``AWS::FSx::FileSystem.WindowsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-windowsconfiguration
        """
        return self._values.get('windows_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnFileSystemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-fsx.FileSystemAttributes", jsii_struct_bases=[], name_mapping={'dns_name': 'dnsName', 'file_system_id': 'fileSystemId', 'security_group': 'securityGroup'})
class FileSystemAttributes():
    def __init__(self, *, dns_name: str, file_system_id: str, security_group: aws_cdk.aws_ec2.ISecurityGroup) -> None:
        """Properties that describe an existing FSx file system.

        :param dns_name: The DNS name assigned to this file system.
        :param file_system_id: The ID of the file system, assigned by Amazon FSx.
        :param security_group: The security group of the file system.

        stability
        :stability: experimental
        """
        self._values = {
            'dns_name': dns_name,
            'file_system_id': file_system_id,
            'security_group': security_group,
        }

    @builtins.property
    def dns_name(self) -> str:
        """The DNS name assigned to this file system.

        stability
        :stability: experimental
        """
        return self._values.get('dns_name')

    @builtins.property
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon FSx.

        stability
        :stability: experimental
        """
        return self._values.get('file_system_id')

    @builtins.property
    def security_group(self) -> aws_cdk.aws_ec2.ISecurityGroup:
        """The security group of the file system.

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileSystemAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-fsx.FileSystemProps", jsii_struct_bases=[], name_mapping={'storage_capacity_gib': 'storageCapacityGiB', 'vpc': 'vpc', 'backup_id': 'backupId', 'kms_key': 'kmsKey', 'security_group': 'securityGroup'})
class FileSystemProps():
    def __init__(self, *, storage_capacity_gib: jsii.Number, vpc: aws_cdk.aws_ec2.IVpc, backup_id: typing.Optional[str]=None, kms_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None) -> None:
        """Properties for the FSx file system.

        :param storage_capacity_gib: The storage capacity of the file system being created. For Windows file systems, valid values are 32 GiB to 65,536 GiB. For SCRATCH_1 deployment types, valid values are 1,200, 2,400, 3,600, then continuing in increments of 3,600 GiB. For SCRATCH_2 and PERSISTENT_1 types, valid values are 1,200, 2,400, then continuing in increments of 2,400 GiB.
        :param vpc: The VPC to launch the file system in.
        :param backup_id: The ID of the backup. Specifies the backup to use if you're creating a file system from an existing backup. Default: - no backup will be used.
        :param kms_key: The KMS key used for encryption to protect your data at rest. Default: - the aws/fsx default KMS key for the AWS account being deployed into.
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html
        stability
        :stability: experimental
        """
        self._values = {
            'storage_capacity_gib': storage_capacity_gib,
            'vpc': vpc,
        }
        if backup_id is not None: self._values["backup_id"] = backup_id
        if kms_key is not None: self._values["kms_key"] = kms_key
        if security_group is not None: self._values["security_group"] = security_group

    @builtins.property
    def storage_capacity_gib(self) -> jsii.Number:
        """The storage capacity of the file system being created.

        For Windows file systems, valid values are 32 GiB to 65,536 GiB.
        For SCRATCH_1 deployment types, valid values are 1,200, 2,400, 3,600, then continuing in increments of 3,600 GiB.
        For SCRATCH_2 and PERSISTENT_1 types, valid values are 1,200, 2,400, then continuing in increments of 2,400 GiB.

        stability
        :stability: experimental
        """
        return self._values.get('storage_capacity_gib')

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC to launch the file system in.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def backup_id(self) -> typing.Optional[str]:
        """The ID of the backup.

        Specifies the backup to use if you're creating a file system from an existing backup.

        default
        :default: - no backup will be used.

        stability
        :stability: experimental
        """
        return self._values.get('backup_id')

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The KMS key used for encryption to protect your data at rest.

        default
        :default: - the aws/fsx default KMS key for the AWS account being deployed into.

        stability
        :stability: experimental
        """
        return self._values.get('kms_key')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security Group to assign to this file system.

        default
        :default: - creates new security group which allows all outbound traffic.

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileSystemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-fsx.IFileSystem")
class IFileSystem(aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    """Interface to implement FSx File Systems.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFileSystemProxy

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon FSx.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IFileSystemProxy(jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    """Interface to implement FSx File Systems.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-fsx.IFileSystem"
    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon FSx.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fileSystemId")


@jsii.data_type(jsii_type="@aws-cdk/aws-fsx.LustreConfiguration", jsii_struct_bases=[], name_mapping={'deployment_type': 'deploymentType', 'export_path': 'exportPath', 'imported_file_chunk_size_mib': 'importedFileChunkSizeMiB', 'import_path': 'importPath', 'per_unit_storage_throughput': 'perUnitStorageThroughput', 'weekly_maintenance_start_time': 'weeklyMaintenanceStartTime'})
class LustreConfiguration():
    def __init__(self, *, deployment_type: "LustreDeploymentType", export_path: typing.Optional[str]=None, imported_file_chunk_size_mib: typing.Optional[jsii.Number]=None, import_path: typing.Optional[str]=None, per_unit_storage_throughput: typing.Optional[jsii.Number]=None, weekly_maintenance_start_time: typing.Optional["LustreMaintenanceTime"]=None) -> None:
        """The configuration for the Amazon FSx for Lustre file system.

        :param deployment_type: The type of backing file system deployment used by FSx.
        :param export_path: The path in Amazon S3 where the root of your Amazon FSx file system is exported. The path must use the same Amazon S3 bucket as specified in ImportPath. If you only specify a bucket name, such as s3://import-bucket, you get a 1:1 mapping of file system objects to S3 bucket objects. This mapping means that the input data in S3 is overwritten on export. If you provide a custom prefix in the export path, such as s3://import-bucket/[custom-optional-prefix], Amazon FSx exports the contents of your file system to that export prefix in the Amazon S3 bucket. Default: s3://import-bucket/FSxLustre[creation-timestamp]
        :param imported_file_chunk_size_mib: For files imported from a data repository, this value determines the stripe count and maximum amount of data per file (in MiB) stored on a single physical disk. Allowed values are between 1 and 512,000. Default: 1024
        :param import_path: The path to the Amazon S3 bucket (including the optional prefix) that you're using as the data repository for your Amazon FSx for Lustre file system. Must be of the format "s3://{bucketName}/optional-prefix" and cannot exceed 900 characters. Default: - no bucket is imported
        :param per_unit_storage_throughput: Required for the PERSISTENT_1 deployment type, describes the amount of read and write throughput for each 1 tebibyte of storage, in MB/s/TiB. Valid values are 50, 100, 200. Default: - no default, conditionally required for PERSISTENT_1 deployment type
        :param weekly_maintenance_start_time: The preferred day and time to perform weekly maintenance. The first digit is the day of the week, starting at 0 for Sunday, then the following are hours and minutes in the UTC time zone, 24 hour clock. For example: '2:20:30' is Tuesdays at 20:30. Default: - no preference

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html
        stability
        :stability: experimental
        """
        self._values = {
            'deployment_type': deployment_type,
        }
        if export_path is not None: self._values["export_path"] = export_path
        if imported_file_chunk_size_mib is not None: self._values["imported_file_chunk_size_mib"] = imported_file_chunk_size_mib
        if import_path is not None: self._values["import_path"] = import_path
        if per_unit_storage_throughput is not None: self._values["per_unit_storage_throughput"] = per_unit_storage_throughput
        if weekly_maintenance_start_time is not None: self._values["weekly_maintenance_start_time"] = weekly_maintenance_start_time

    @builtins.property
    def deployment_type(self) -> "LustreDeploymentType":
        """The type of backing file system deployment used by FSx.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_type')

    @builtins.property
    def export_path(self) -> typing.Optional[str]:
        """The path in Amazon S3 where the root of your Amazon FSx file system is exported.

        The path must use the same
        Amazon S3 bucket as specified in ImportPath. If you only specify a bucket name, such as s3://import-bucket, you
        get a 1:1 mapping of file system objects to S3 bucket objects. This mapping means that the input data in S3 is
        overwritten on export. If you provide a custom prefix in the export path, such as
        s3://import-bucket/[custom-optional-prefix], Amazon FSx exports the contents of your file system to that export
        prefix in the Amazon S3 bucket.

        default
        :default: s3://import-bucket/FSxLustre[creation-timestamp]

        stability
        :stability: experimental
        """
        return self._values.get('export_path')

    @builtins.property
    def imported_file_chunk_size_mib(self) -> typing.Optional[jsii.Number]:
        """For files imported from a data repository, this value determines the stripe count and maximum amount of data per file (in MiB) stored on a single physical disk.

        Allowed values are between 1 and 512,000.

        default
        :default: 1024

        stability
        :stability: experimental
        """
        return self._values.get('imported_file_chunk_size_mib')

    @builtins.property
    def import_path(self) -> typing.Optional[str]:
        """The path to the Amazon S3 bucket (including the optional prefix) that you're using as the data repository for your Amazon FSx for Lustre file system.

        Must be of the format "s3://{bucketName}/optional-prefix" and cannot
        exceed 900 characters.

        default
        :default: - no bucket is imported

        stability
        :stability: experimental
        """
        return self._values.get('import_path')

    @builtins.property
    def per_unit_storage_throughput(self) -> typing.Optional[jsii.Number]:
        """Required for the PERSISTENT_1 deployment type, describes the amount of read and write throughput for each 1 tebibyte of storage, in MB/s/TiB.

        Valid values are 50, 100, 200.

        default
        :default: - no default, conditionally required for PERSISTENT_1 deployment type

        stability
        :stability: experimental
        """
        return self._values.get('per_unit_storage_throughput')

    @builtins.property
    def weekly_maintenance_start_time(self) -> typing.Optional["LustreMaintenanceTime"]:
        """The preferred day and time to perform weekly maintenance.

        The first digit is the day of the week, starting at 0
        for Sunday, then the following are hours and minutes in the UTC time zone, 24 hour clock. For example: '2:20:30'
        is Tuesdays at 20:30.

        default
        :default: - no preference

        stability
        :stability: experimental
        """
        return self._values.get('weekly_maintenance_start_time')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LustreConfiguration(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-fsx.LustreDeploymentType")
class LustreDeploymentType(enum.Enum):
    """The different kinds of file system deployments used by Lustre.

    stability
    :stability: experimental
    """
    SCRATCH_1 = "SCRATCH_1"
    """Original type for shorter term data processing.

    Data is not replicated and does not persist on server fail.

    stability
    :stability: experimental
    """
    SCRATCH_2 = "SCRATCH_2"
    """Newer type for shorter term data processing.

    Data is not replicated and does not persist on server fail.
    Provides better support for spiky workloads.

    stability
    :stability: experimental
    """
    PERSISTENT_1 = "PERSISTENT_1"
    """Long term storage.

    Data is replicated and file servers are replaced if they fail.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-fsx.LustreFileSystemProps", jsii_struct_bases=[FileSystemProps], name_mapping={'storage_capacity_gib': 'storageCapacityGiB', 'vpc': 'vpc', 'backup_id': 'backupId', 'kms_key': 'kmsKey', 'security_group': 'securityGroup', 'lustre_configuration': 'lustreConfiguration', 'vpc_subnet': 'vpcSubnet'})
class LustreFileSystemProps(FileSystemProps):
    def __init__(self, *, storage_capacity_gib: jsii.Number, vpc: aws_cdk.aws_ec2.IVpc, backup_id: typing.Optional[str]=None, kms_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, lustre_configuration: "LustreConfiguration", vpc_subnet: aws_cdk.aws_ec2.ISubnet) -> None:
        """Properties specific to the Lustre version of the FSx file system.

        :param storage_capacity_gib: The storage capacity of the file system being created. For Windows file systems, valid values are 32 GiB to 65,536 GiB. For SCRATCH_1 deployment types, valid values are 1,200, 2,400, 3,600, then continuing in increments of 3,600 GiB. For SCRATCH_2 and PERSISTENT_1 types, valid values are 1,200, 2,400, then continuing in increments of 2,400 GiB.
        :param vpc: The VPC to launch the file system in.
        :param backup_id: The ID of the backup. Specifies the backup to use if you're creating a file system from an existing backup. Default: - no backup will be used.
        :param kms_key: The KMS key used for encryption to protect your data at rest. Default: - the aws/fsx default KMS key for the AWS account being deployed into.
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic.
        :param lustre_configuration: Additional configuration for FSx specific to Lustre.
        :param vpc_subnet: The subnet that the file system will be accessible from.

        stability
        :stability: experimental
        """
        if isinstance(lustre_configuration, dict): lustre_configuration = LustreConfiguration(**lustre_configuration)
        self._values = {
            'storage_capacity_gib': storage_capacity_gib,
            'vpc': vpc,
            'lustre_configuration': lustre_configuration,
            'vpc_subnet': vpc_subnet,
        }
        if backup_id is not None: self._values["backup_id"] = backup_id
        if kms_key is not None: self._values["kms_key"] = kms_key
        if security_group is not None: self._values["security_group"] = security_group

    @builtins.property
    def storage_capacity_gib(self) -> jsii.Number:
        """The storage capacity of the file system being created.

        For Windows file systems, valid values are 32 GiB to 65,536 GiB.
        For SCRATCH_1 deployment types, valid values are 1,200, 2,400, 3,600, then continuing in increments of 3,600 GiB.
        For SCRATCH_2 and PERSISTENT_1 types, valid values are 1,200, 2,400, then continuing in increments of 2,400 GiB.

        stability
        :stability: experimental
        """
        return self._values.get('storage_capacity_gib')

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC to launch the file system in.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def backup_id(self) -> typing.Optional[str]:
        """The ID of the backup.

        Specifies the backup to use if you're creating a file system from an existing backup.

        default
        :default: - no backup will be used.

        stability
        :stability: experimental
        """
        return self._values.get('backup_id')

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The KMS key used for encryption to protect your data at rest.

        default
        :default: - the aws/fsx default KMS key for the AWS account being deployed into.

        stability
        :stability: experimental
        """
        return self._values.get('kms_key')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security Group to assign to this file system.

        default
        :default: - creates new security group which allows all outbound traffic.

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def lustre_configuration(self) -> "LustreConfiguration":
        """Additional configuration for FSx specific to Lustre.

        stability
        :stability: experimental
        """
        return self._values.get('lustre_configuration')

    @builtins.property
    def vpc_subnet(self) -> aws_cdk.aws_ec2.ISubnet:
        """The subnet that the file system will be accessible from.

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnet')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LustreFileSystemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LustreMaintenanceTime(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-fsx.LustreMaintenanceTime"):
    """Class for scheduling a weekly manitenance time.

    stability
    :stability: experimental
    """
    def __init__(self, *, day: "Weekday", hour: jsii.Number, minute: jsii.Number) -> None:
        """
        :param day: The day of the week for maintenance to be performed.
        :param hour: The hour of the day (from 0-24) for maintenance to be performed.
        :param minute: The minute of the hour (from 0-59) for maintenance to be performed.

        stability
        :stability: experimental
        """
        props = LustreMaintenanceTimeProps(day=day, hour=hour, minute=minute)

        jsii.create(LustreMaintenanceTime, self, [props])

    @jsii.member(jsii_name="toTimestamp")
    def to_timestamp(self) -> str:
        """Converts a day, hour, and minute into a timestamp as used by FSx for Lustre's weeklyMaintenanceStartTime field.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTimestamp", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-fsx.LustreMaintenanceTimeProps", jsii_struct_bases=[], name_mapping={'day': 'day', 'hour': 'hour', 'minute': 'minute'})
class LustreMaintenanceTimeProps():
    def __init__(self, *, day: "Weekday", hour: jsii.Number, minute: jsii.Number) -> None:
        """Properties required for setting up a weekly maintenance time.

        :param day: The day of the week for maintenance to be performed.
        :param hour: The hour of the day (from 0-24) for maintenance to be performed.
        :param minute: The minute of the hour (from 0-59) for maintenance to be performed.

        stability
        :stability: experimental
        """
        self._values = {
            'day': day,
            'hour': hour,
            'minute': minute,
        }

    @builtins.property
    def day(self) -> "Weekday":
        """The day of the week for maintenance to be performed.

        stability
        :stability: experimental
        """
        return self._values.get('day')

    @builtins.property
    def hour(self) -> jsii.Number:
        """The hour of the day (from 0-24) for maintenance to be performed.

        stability
        :stability: experimental
        """
        return self._values.get('hour')

    @builtins.property
    def minute(self) -> jsii.Number:
        """The minute of the hour (from 0-59) for maintenance to be performed.

        stability
        :stability: experimental
        """
        return self._values.get('minute')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LustreMaintenanceTimeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-fsx.Weekday")
class Weekday(enum.Enum):
    """Enum for representing all the days of the week.

    stability
    :stability: experimental
    """
    SUNDAY = "SUNDAY"
    """Sunday.

    stability
    :stability: experimental
    """
    MONDAY = "MONDAY"
    """Monday.

    stability
    :stability: experimental
    """
    TUESDAY = "TUESDAY"
    """Tuesday.

    stability
    :stability: experimental
    """
    WEDNESDAY = "WEDNESDAY"
    """Wednesday.

    stability
    :stability: experimental
    """
    THURSDAY = "THURSDAY"
    """Thursday.

    stability
    :stability: experimental
    """
    FRIDAY = "FRIDAY"
    """Friday.

    stability
    :stability: experimental
    """
    SATURDAY = "SATURDAY"
    """Saturday.

    stability
    :stability: experimental
    """

@jsii.implements(IFileSystem)
class FileSystemBase(aws_cdk.core.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-fsx.FileSystemBase"):
    """A new or imported FSx file system.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _FileSystemBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = aws_cdk.core.ResourceProps(physical_name=physical_name)

        jsii.create(FileSystemBase, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="connections")
    @abc.abstractmethod
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The security groups/rules used to allow network connections to the file system.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    @abc.abstractmethod
    def dns_name(self) -> str:
        """The DNS name assigned to this file system.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    @abc.abstractmethod
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon FSx.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _FileSystemBaseProxy(FileSystemBase, jsii.proxy_for(aws_cdk.core.Resource)):
    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The security groups/rules used to allow network connections to the file system.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> str:
        """The DNS name assigned to this file system.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "dnsName")

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon FSx.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fileSystemId")


class LustreFileSystem(FileSystemBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-fsx.LustreFileSystem"):
    """The FSx for Lustre File System implementation of IFileSystem.

    see
    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html
    stability
    :stability: experimental
    resource:
    :resource:: AWS::FSx::FileSystem
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, lustre_configuration: "LustreConfiguration", vpc_subnet: aws_cdk.aws_ec2.ISubnet, storage_capacity_gib: jsii.Number, vpc: aws_cdk.aws_ec2.IVpc, backup_id: typing.Optional[str]=None, kms_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param lustre_configuration: Additional configuration for FSx specific to Lustre.
        :param vpc_subnet: The subnet that the file system will be accessible from.
        :param storage_capacity_gib: The storage capacity of the file system being created. For Windows file systems, valid values are 32 GiB to 65,536 GiB. For SCRATCH_1 deployment types, valid values are 1,200, 2,400, 3,600, then continuing in increments of 3,600 GiB. For SCRATCH_2 and PERSISTENT_1 types, valid values are 1,200, 2,400, then continuing in increments of 2,400 GiB.
        :param vpc: The VPC to launch the file system in.
        :param backup_id: The ID of the backup. Specifies the backup to use if you're creating a file system from an existing backup. Default: - no backup will be used.
        :param kms_key: The KMS key used for encryption to protect your data at rest. Default: - the aws/fsx default KMS key for the AWS account being deployed into.
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic.

        stability
        :stability: experimental
        """
        props = LustreFileSystemProps(lustre_configuration=lustre_configuration, vpc_subnet=vpc_subnet, storage_capacity_gib=storage_capacity_gib, vpc=vpc, backup_id=backup_id, kms_key=kms_key, security_group=security_group)

        jsii.create(LustreFileSystem, self, [scope, id, props])

    @jsii.member(jsii_name="fromLustreFileSystemAttributes")
    @builtins.classmethod
    def from_lustre_file_system_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, dns_name: str, file_system_id: str, security_group: aws_cdk.aws_ec2.ISecurityGroup) -> "IFileSystem":
        """Import an existing FSx for Lustre file system from the given properties.

        :param scope: -
        :param id: -
        :param dns_name: The DNS name assigned to this file system.
        :param file_system_id: The ID of the file system, assigned by Amazon FSx.
        :param security_group: The security group of the file system.

        stability
        :stability: experimental
        """
        attrs = FileSystemAttributes(dns_name=dns_name, file_system_id=file_system_id, security_group=security_group)

        return jsii.sinvoke(cls, "fromLustreFileSystemAttributes", [scope, id, attrs])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The security groups/rules used to allow network connections to the file system.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> str:
        """The DNS name assigned to this file system.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dnsName")

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID that AWS assigns to the file system.

        stability
        :stability: experimental
        """
        return jsii.get(self, "fileSystemId")

    @builtins.property
    @jsii.member(jsii_name="mountName")
    def mount_name(self) -> str:
        """The mount name of the file system, generated by FSx.

        stability
        :stability: experimental
        attribute:
        :attribute:: LustreMountName
        """
        return jsii.get(self, "mountName")


__all__ = [
    "CfnFileSystem",
    "CfnFileSystemProps",
    "FileSystemAttributes",
    "FileSystemBase",
    "FileSystemProps",
    "IFileSystem",
    "LustreConfiguration",
    "LustreDeploymentType",
    "LustreFileSystem",
    "LustreFileSystemProps",
    "LustreMaintenanceTime",
    "LustreMaintenanceTimeProps",
    "Weekday",
]

publication.publish()
