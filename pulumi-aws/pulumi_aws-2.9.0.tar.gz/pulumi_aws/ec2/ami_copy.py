# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class AmiCopy(pulumi.CustomResource):
    architecture: pulumi.Output[str]
    """
    Machine architecture for created instances. Defaults to "x86_64".
    """
    description: pulumi.Output[str]
    """
    A longer, human-readable description for the AMI.
    """
    ebs_block_devices: pulumi.Output[list]
    """
    Nested block describing an EBS block device that should be
    attached to created instances. The structure of this block is described below.

      * `deleteOnTermination` (`bool`) - Boolean controlling whether the EBS volumes created to
        support each created instance will be deleted once that instance is terminated.
      * `device_name` (`str`) - The path at which the device is exposed to created instances.
      * `encrypted` (`bool`) - Boolean controlling whether the created EBS volumes will be encrypted. Can't be used with `snapshot_id`.
      * `iops` (`float`) - Number of I/O operations per second the
        created volumes will support.
      * `snapshot_id` (`str`) - The id of an EBS snapshot that will be used to initialize the created
        EBS volumes. If set, the `volume_size` attribute must be at least as large as the referenced
        snapshot.
      * `volume_size` (`float`) - The size of created volumes in GiB.
        If `snapshot_id` is set and `volume_size` is omitted then the volume will have the same size
        as the selected snapshot.
      * `volumeType` (`str`) - The type of EBS volume to create. Can be one of "standard" (the
        default), "io1" or "gp2".
    """
    ena_support: pulumi.Output[bool]
    """
    Specifies whether enhanced networking with ENA is enabled. Defaults to `false`.
    """
    encrypted: pulumi.Output[bool]
    """
    Boolean controlling whether the created EBS volumes will be encrypted. Can't be used with `snapshot_id`.
    """
    ephemeral_block_devices: pulumi.Output[list]
    """
    Nested block describing an ephemeral block device that
    should be attached to created instances. The structure of this block is described below.

      * `device_name` (`str`) - The path at which the device is exposed to created instances.
      * `virtualName` (`str`) - A name for the ephemeral device, of the form "ephemeralN" where
        *N* is a volume number starting from zero.
    """
    image_location: pulumi.Output[str]
    """
    Path to an S3 object containing an image manifest, e.g. created
    by the `ec2-upload-bundle` command in the EC2 command line tools.
    """
    kernel_id: pulumi.Output[str]
    """
    The id of the kernel image (AKI) that will be used as the paravirtual
    kernel in created instances.
    """
    kms_key_id: pulumi.Output[str]
    """
    The full ARN of the AWS Key Management Service (AWS KMS) CMK to use when encrypting the snapshots of
    an image during a copy operation. This parameter is only required if you want to use a non-default CMK;
    if this parameter is not specified, the default CMK for EBS is used
    """
    manage_ebs_snapshots: pulumi.Output[bool]
    name: pulumi.Output[str]
    """
    A region-unique name for the AMI.
    """
    ramdisk_id: pulumi.Output[str]
    """
    The id of an initrd image (ARI) that will be used when booting the
    created instances.
    """
    root_device_name: pulumi.Output[str]
    """
    The name of the root device (for example, `/dev/sda1`, or `/dev/xvda`).
    """
    root_snapshot_id: pulumi.Output[str]
    source_ami_id: pulumi.Output[str]
    """
    The id of the AMI to copy. This id must be valid in the region
    given by `source_ami_region`.
    """
    source_ami_region: pulumi.Output[str]
    """
    The region from which the AMI will be copied. This may be the
    same as the AWS provider region in order to create a copy within the same region.
    """
    sriov_net_support: pulumi.Output[str]
    """
    When set to "simple" (the default), enables enhanced networking
    for created instances. No other value is supported at this time.
    """
    tags: pulumi.Output[dict]
    """
    A map of tags to assign to the resource.
    """
    virtualization_type: pulumi.Output[str]
    """
    Keyword to choose what virtualization mode created instances
    will use. Can be either "paravirtual" (the default) or "hvm". The choice of virtualization type
    changes the set of further arguments that are required, as described below.
    """
    def __init__(__self__, resource_name, opts=None, description=None, ebs_block_devices=None, encrypted=None, ephemeral_block_devices=None, kms_key_id=None, name=None, source_ami_id=None, source_ami_region=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        The "AMI copy" resource allows duplication of an Amazon Machine Image (AMI),
        including cross-region copies.

        If the source AMI has associated EBS snapshots, those will also be duplicated
        along with the AMI.

        This is useful for taking a single AMI provisioned in one region and making
        it available in another for a multi-region deployment.

        Copying an AMI can take several minutes. The creation of this resource will
        block until the new AMI is available for use on new instances.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.AmiCopy("example",
            description="A copy of ami-xxxxxxxx",
            source_ami_id="ami-xxxxxxxx",
            source_ami_region="us-west-1",
            tags={
                "Name": "HelloWorld",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A longer, human-readable description for the AMI.
        :param pulumi.Input[list] ebs_block_devices: Nested block describing an EBS block device that should be
               attached to created instances. The structure of this block is described below.
        :param pulumi.Input[bool] encrypted: Boolean controlling whether the created EBS volumes will be encrypted. Can't be used with `snapshot_id`.
        :param pulumi.Input[list] ephemeral_block_devices: Nested block describing an ephemeral block device that
               should be attached to created instances. The structure of this block is described below.
        :param pulumi.Input[str] kms_key_id: The full ARN of the AWS Key Management Service (AWS KMS) CMK to use when encrypting the snapshots of
               an image during a copy operation. This parameter is only required if you want to use a non-default CMK;
               if this parameter is not specified, the default CMK for EBS is used
        :param pulumi.Input[str] name: A region-unique name for the AMI.
        :param pulumi.Input[str] source_ami_id: The id of the AMI to copy. This id must be valid in the region
               given by `source_ami_region`.
        :param pulumi.Input[str] source_ami_region: The region from which the AMI will be copied. This may be the
               same as the AWS provider region in order to create a copy within the same region.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.

        The **ebs_block_devices** object supports the following:

          * `deleteOnTermination` (`pulumi.Input[bool]`) - Boolean controlling whether the EBS volumes created to
            support each created instance will be deleted once that instance is terminated.
          * `device_name` (`pulumi.Input[str]`) - The path at which the device is exposed to created instances.
          * `encrypted` (`pulumi.Input[bool]`) - Boolean controlling whether the created EBS volumes will be encrypted. Can't be used with `snapshot_id`.
          * `iops` (`pulumi.Input[float]`) - Number of I/O operations per second the
            created volumes will support.
          * `snapshot_id` (`pulumi.Input[str]`) - The id of an EBS snapshot that will be used to initialize the created
            EBS volumes. If set, the `volume_size` attribute must be at least as large as the referenced
            snapshot.
          * `volume_size` (`pulumi.Input[float]`) - The size of created volumes in GiB.
            If `snapshot_id` is set and `volume_size` is omitted then the volume will have the same size
            as the selected snapshot.
          * `volumeType` (`pulumi.Input[str]`) - The type of EBS volume to create. Can be one of "standard" (the
            default), "io1" or "gp2".

        The **ephemeral_block_devices** object supports the following:

          * `device_name` (`pulumi.Input[str]`) - The path at which the device is exposed to created instances.
          * `virtualName` (`pulumi.Input[str]`) - A name for the ephemeral device, of the form "ephemeralN" where
            *N* is a volume number starting from zero.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['description'] = description
            __props__['ebs_block_devices'] = ebs_block_devices
            __props__['encrypted'] = encrypted
            __props__['ephemeral_block_devices'] = ephemeral_block_devices
            __props__['kms_key_id'] = kms_key_id
            __props__['name'] = name
            if source_ami_id is None:
                raise TypeError("Missing required property 'source_ami_id'")
            __props__['source_ami_id'] = source_ami_id
            if source_ami_region is None:
                raise TypeError("Missing required property 'source_ami_region'")
            __props__['source_ami_region'] = source_ami_region
            __props__['tags'] = tags
            __props__['architecture'] = None
            __props__['ena_support'] = None
            __props__['image_location'] = None
            __props__['kernel_id'] = None
            __props__['manage_ebs_snapshots'] = None
            __props__['ramdisk_id'] = None
            __props__['root_device_name'] = None
            __props__['root_snapshot_id'] = None
            __props__['sriov_net_support'] = None
            __props__['virtualization_type'] = None
        super(AmiCopy, __self__).__init__(
            'aws:ec2/amiCopy:AmiCopy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, architecture=None, description=None, ebs_block_devices=None, ena_support=None, encrypted=None, ephemeral_block_devices=None, image_location=None, kernel_id=None, kms_key_id=None, manage_ebs_snapshots=None, name=None, ramdisk_id=None, root_device_name=None, root_snapshot_id=None, source_ami_id=None, source_ami_region=None, sriov_net_support=None, tags=None, virtualization_type=None):
        """
        Get an existing AmiCopy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] architecture: Machine architecture for created instances. Defaults to "x86_64".
        :param pulumi.Input[str] description: A longer, human-readable description for the AMI.
        :param pulumi.Input[list] ebs_block_devices: Nested block describing an EBS block device that should be
               attached to created instances. The structure of this block is described below.
        :param pulumi.Input[bool] ena_support: Specifies whether enhanced networking with ENA is enabled. Defaults to `false`.
        :param pulumi.Input[bool] encrypted: Boolean controlling whether the created EBS volumes will be encrypted. Can't be used with `snapshot_id`.
        :param pulumi.Input[list] ephemeral_block_devices: Nested block describing an ephemeral block device that
               should be attached to created instances. The structure of this block is described below.
        :param pulumi.Input[str] image_location: Path to an S3 object containing an image manifest, e.g. created
               by the `ec2-upload-bundle` command in the EC2 command line tools.
        :param pulumi.Input[str] kernel_id: The id of the kernel image (AKI) that will be used as the paravirtual
               kernel in created instances.
        :param pulumi.Input[str] kms_key_id: The full ARN of the AWS Key Management Service (AWS KMS) CMK to use when encrypting the snapshots of
               an image during a copy operation. This parameter is only required if you want to use a non-default CMK;
               if this parameter is not specified, the default CMK for EBS is used
        :param pulumi.Input[str] name: A region-unique name for the AMI.
        :param pulumi.Input[str] ramdisk_id: The id of an initrd image (ARI) that will be used when booting the
               created instances.
        :param pulumi.Input[str] root_device_name: The name of the root device (for example, `/dev/sda1`, or `/dev/xvda`).
        :param pulumi.Input[str] source_ami_id: The id of the AMI to copy. This id must be valid in the region
               given by `source_ami_region`.
        :param pulumi.Input[str] source_ami_region: The region from which the AMI will be copied. This may be the
               same as the AWS provider region in order to create a copy within the same region.
        :param pulumi.Input[str] sriov_net_support: When set to "simple" (the default), enables enhanced networking
               for created instances. No other value is supported at this time.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] virtualization_type: Keyword to choose what virtualization mode created instances
               will use. Can be either "paravirtual" (the default) or "hvm". The choice of virtualization type
               changes the set of further arguments that are required, as described below.

        The **ebs_block_devices** object supports the following:

          * `deleteOnTermination` (`pulumi.Input[bool]`) - Boolean controlling whether the EBS volumes created to
            support each created instance will be deleted once that instance is terminated.
          * `device_name` (`pulumi.Input[str]`) - The path at which the device is exposed to created instances.
          * `encrypted` (`pulumi.Input[bool]`) - Boolean controlling whether the created EBS volumes will be encrypted. Can't be used with `snapshot_id`.
          * `iops` (`pulumi.Input[float]`) - Number of I/O operations per second the
            created volumes will support.
          * `snapshot_id` (`pulumi.Input[str]`) - The id of an EBS snapshot that will be used to initialize the created
            EBS volumes. If set, the `volume_size` attribute must be at least as large as the referenced
            snapshot.
          * `volume_size` (`pulumi.Input[float]`) - The size of created volumes in GiB.
            If `snapshot_id` is set and `volume_size` is omitted then the volume will have the same size
            as the selected snapshot.
          * `volumeType` (`pulumi.Input[str]`) - The type of EBS volume to create. Can be one of "standard" (the
            default), "io1" or "gp2".

        The **ephemeral_block_devices** object supports the following:

          * `device_name` (`pulumi.Input[str]`) - The path at which the device is exposed to created instances.
          * `virtualName` (`pulumi.Input[str]`) - A name for the ephemeral device, of the form "ephemeralN" where
            *N* is a volume number starting from zero.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["architecture"] = architecture
        __props__["description"] = description
        __props__["ebs_block_devices"] = ebs_block_devices
        __props__["ena_support"] = ena_support
        __props__["encrypted"] = encrypted
        __props__["ephemeral_block_devices"] = ephemeral_block_devices
        __props__["image_location"] = image_location
        __props__["kernel_id"] = kernel_id
        __props__["kms_key_id"] = kms_key_id
        __props__["manage_ebs_snapshots"] = manage_ebs_snapshots
        __props__["name"] = name
        __props__["ramdisk_id"] = ramdisk_id
        __props__["root_device_name"] = root_device_name
        __props__["root_snapshot_id"] = root_snapshot_id
        __props__["source_ami_id"] = source_ami_id
        __props__["source_ami_region"] = source_ami_region
        __props__["sriov_net_support"] = sriov_net_support
        __props__["tags"] = tags
        __props__["virtualization_type"] = virtualization_type
        return AmiCopy(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

