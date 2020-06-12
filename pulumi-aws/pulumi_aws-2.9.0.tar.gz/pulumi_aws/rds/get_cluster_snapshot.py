# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetClusterSnapshotResult:
    """
    A collection of values returned by getClusterSnapshot.
    """
    def __init__(__self__, allocated_storage=None, availability_zones=None, db_cluster_identifier=None, db_cluster_snapshot_arn=None, db_cluster_snapshot_identifier=None, engine=None, engine_version=None, id=None, include_public=None, include_shared=None, kms_key_id=None, license_model=None, most_recent=None, port=None, snapshot_create_time=None, snapshot_type=None, source_db_cluster_snapshot_arn=None, status=None, storage_encrypted=None, tags=None, vpc_id=None):
        if allocated_storage and not isinstance(allocated_storage, float):
            raise TypeError("Expected argument 'allocated_storage' to be a float")
        __self__.allocated_storage = allocated_storage
        """
        Specifies the allocated storage size in gigabytes (GB).
        """
        if availability_zones and not isinstance(availability_zones, list):
            raise TypeError("Expected argument 'availability_zones' to be a list")
        __self__.availability_zones = availability_zones
        """
        List of EC2 Availability Zones that instances in the DB cluster snapshot can be restored in.
        """
        if db_cluster_identifier and not isinstance(db_cluster_identifier, str):
            raise TypeError("Expected argument 'db_cluster_identifier' to be a str")
        __self__.db_cluster_identifier = db_cluster_identifier
        """
        Specifies the DB cluster identifier of the DB cluster that this DB cluster snapshot was created from.
        """
        if db_cluster_snapshot_arn and not isinstance(db_cluster_snapshot_arn, str):
            raise TypeError("Expected argument 'db_cluster_snapshot_arn' to be a str")
        __self__.db_cluster_snapshot_arn = db_cluster_snapshot_arn
        """
        The Amazon Resource Name (ARN) for the DB Cluster Snapshot.
        """
        if db_cluster_snapshot_identifier and not isinstance(db_cluster_snapshot_identifier, str):
            raise TypeError("Expected argument 'db_cluster_snapshot_identifier' to be a str")
        __self__.db_cluster_snapshot_identifier = db_cluster_snapshot_identifier
        if engine and not isinstance(engine, str):
            raise TypeError("Expected argument 'engine' to be a str")
        __self__.engine = engine
        """
        Specifies the name of the database engine.
        """
        if engine_version and not isinstance(engine_version, str):
            raise TypeError("Expected argument 'engine_version' to be a str")
        __self__.engine_version = engine_version
        """
        Version of the database engine for this DB cluster snapshot.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if include_public and not isinstance(include_public, bool):
            raise TypeError("Expected argument 'include_public' to be a bool")
        __self__.include_public = include_public
        if include_shared and not isinstance(include_shared, bool):
            raise TypeError("Expected argument 'include_shared' to be a bool")
        __self__.include_shared = include_shared
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        __self__.kms_key_id = kms_key_id
        """
        If storage_encrypted is true, the AWS KMS key identifier for the encrypted DB cluster snapshot.
        """
        if license_model and not isinstance(license_model, str):
            raise TypeError("Expected argument 'license_model' to be a str")
        __self__.license_model = license_model
        """
        License model information for the restored DB cluster.
        """
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        __self__.most_recent = most_recent
        if port and not isinstance(port, float):
            raise TypeError("Expected argument 'port' to be a float")
        __self__.port = port
        """
        Port that the DB cluster was listening on at the time of the snapshot.
        """
        if snapshot_create_time and not isinstance(snapshot_create_time, str):
            raise TypeError("Expected argument 'snapshot_create_time' to be a str")
        __self__.snapshot_create_time = snapshot_create_time
        """
        Time when the snapshot was taken, in Universal Coordinated Time (UTC).
        """
        if snapshot_type and not isinstance(snapshot_type, str):
            raise TypeError("Expected argument 'snapshot_type' to be a str")
        __self__.snapshot_type = snapshot_type
        if source_db_cluster_snapshot_arn and not isinstance(source_db_cluster_snapshot_arn, str):
            raise TypeError("Expected argument 'source_db_cluster_snapshot_arn' to be a str")
        __self__.source_db_cluster_snapshot_arn = source_db_cluster_snapshot_arn
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        __self__.status = status
        """
        The status of this DB Cluster Snapshot.
        """
        if storage_encrypted and not isinstance(storage_encrypted, bool):
            raise TypeError("Expected argument 'storage_encrypted' to be a bool")
        __self__.storage_encrypted = storage_encrypted
        """
        Specifies whether the DB cluster snapshot is encrypted.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A map of tags for the resource.
        """
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        __self__.vpc_id = vpc_id
        """
        The VPC ID associated with the DB cluster snapshot.
        """
class AwaitableGetClusterSnapshotResult(GetClusterSnapshotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterSnapshotResult(
            allocated_storage=self.allocated_storage,
            availability_zones=self.availability_zones,
            db_cluster_identifier=self.db_cluster_identifier,
            db_cluster_snapshot_arn=self.db_cluster_snapshot_arn,
            db_cluster_snapshot_identifier=self.db_cluster_snapshot_identifier,
            engine=self.engine,
            engine_version=self.engine_version,
            id=self.id,
            include_public=self.include_public,
            include_shared=self.include_shared,
            kms_key_id=self.kms_key_id,
            license_model=self.license_model,
            most_recent=self.most_recent,
            port=self.port,
            snapshot_create_time=self.snapshot_create_time,
            snapshot_type=self.snapshot_type,
            source_db_cluster_snapshot_arn=self.source_db_cluster_snapshot_arn,
            status=self.status,
            storage_encrypted=self.storage_encrypted,
            tags=self.tags,
            vpc_id=self.vpc_id)

def get_cluster_snapshot(db_cluster_identifier=None,db_cluster_snapshot_identifier=None,include_public=None,include_shared=None,most_recent=None,snapshot_type=None,tags=None,opts=None):
    """
    Use this data source to get information about a DB Cluster Snapshot for use when provisioning DB clusters.

    > **NOTE:** This data source does not apply to snapshots created on DB Instances. 
    See the `rds.Snapshot` data source for DB Instance snapshots.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_aws as aws

    development_final_snapshot = aws.rds.get_cluster_snapshot(db_cluster_identifier="development_cluster",
        most_recent=True)
    # Use the last snapshot of the dev database before it was destroyed to create
    # a new dev database.
    aurora_cluster = aws.rds.Cluster("auroraCluster",
        cluster_identifier="development_cluster",
        db_subnet_group_name="my_db_subnet_group",
        lifecycle={
            "ignoreChanges": ["snapshotIdentifier"],
        },
        snapshot_identifier=development_final_snapshot.id)
    aurora_cluster_instance = aws.rds.ClusterInstance("auroraClusterInstance",
        cluster_identifier=aurora_cluster.id,
        db_subnet_group_name="my_db_subnet_group",
        instance_class="db.t2.small")
    ```


    :param str db_cluster_identifier: Returns the list of snapshots created by the specific db_cluster
    :param str db_cluster_snapshot_identifier: Returns information on a specific snapshot_id.
    :param bool include_public: Set this value to true to include manual DB Cluster Snapshots that are public and can be
           copied or restored by any AWS account, otherwise set this value to false. The default is `false`.
    :param bool include_shared: Set this value to true to include shared manual DB Cluster Snapshots from other
           AWS accounts that this AWS account has been given permission to copy or restore, otherwise set this value to false.
           The default is `false`.
    :param bool most_recent: If more than one result is returned, use the most recent Snapshot.
    :param str snapshot_type: The type of snapshots to be returned. If you don't specify a SnapshotType
           value, then both automated and manual DB cluster snapshots are returned. Shared and public DB Cluster Snapshots are not
           included in the returned results by default. Possible values are, `automated`, `manual`, `shared` and `public`.
    :param dict tags: A map of tags for the resource.
    """
    __args__ = dict()


    __args__['dbClusterIdentifier'] = db_cluster_identifier
    __args__['dbClusterSnapshotIdentifier'] = db_cluster_snapshot_identifier
    __args__['includePublic'] = include_public
    __args__['includeShared'] = include_shared
    __args__['mostRecent'] = most_recent
    __args__['snapshotType'] = snapshot_type
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:rds/getClusterSnapshot:getClusterSnapshot', __args__, opts=opts).value

    return AwaitableGetClusterSnapshotResult(
        allocated_storage=__ret__.get('allocatedStorage'),
        availability_zones=__ret__.get('availabilityZones'),
        db_cluster_identifier=__ret__.get('dbClusterIdentifier'),
        db_cluster_snapshot_arn=__ret__.get('dbClusterSnapshotArn'),
        db_cluster_snapshot_identifier=__ret__.get('dbClusterSnapshotIdentifier'),
        engine=__ret__.get('engine'),
        engine_version=__ret__.get('engineVersion'),
        id=__ret__.get('id'),
        include_public=__ret__.get('includePublic'),
        include_shared=__ret__.get('includeShared'),
        kms_key_id=__ret__.get('kmsKeyId'),
        license_model=__ret__.get('licenseModel'),
        most_recent=__ret__.get('mostRecent'),
        port=__ret__.get('port'),
        snapshot_create_time=__ret__.get('snapshotCreateTime'),
        snapshot_type=__ret__.get('snapshotType'),
        source_db_cluster_snapshot_arn=__ret__.get('sourceDbClusterSnapshotArn'),
        status=__ret__.get('status'),
        storage_encrypted=__ret__.get('storageEncrypted'),
        tags=__ret__.get('tags'),
        vpc_id=__ret__.get('vpcId'))
