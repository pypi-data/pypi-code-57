import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53, Duration as _Duration_5170c158)
from ..aws_cloudfront import (IDistribution as _IDistribution_0af1f2d0)
from ..aws_iam import (IRole as _IRole_e69bbae4)
from ..aws_s3 import (IBucket as _IBucket_25bad983)
from ..aws_s3_assets import (AssetOptions as _AssetOptions_ed6c2956)


class BucketDeployment(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_s3_deployment.BucketDeployment"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, destination_bucket: _IBucket_25bad983, sources: typing.List["ISource"], cache_control: typing.Optional[typing.List["CacheControl"]]=None, content_disposition: typing.Optional[str]=None, content_encoding: typing.Optional[str]=None, content_language: typing.Optional[str]=None, content_type: typing.Optional[str]=None, destination_key_prefix: typing.Optional[str]=None, distribution: typing.Optional[_IDistribution_0af1f2d0]=None, distribution_paths: typing.Optional[typing.List[str]]=None, expires: typing.Optional["Expires"]=None, memory_limit: typing.Optional[jsii.Number]=None, metadata: typing.Optional["UserDefinedObjectMetadata"]=None, retain_on_delete: typing.Optional[bool]=None, role: typing.Optional[_IRole_e69bbae4]=None, server_side_encryption: typing.Optional["ServerSideEncryption"]=None, server_side_encryption_aws_kms_key_id: typing.Optional[str]=None, server_side_encryption_customer_algorithm: typing.Optional[str]=None, storage_class: typing.Optional["StorageClass"]=None, website_redirect_location: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param destination_bucket: The S3 bucket to sync the contents of the zip file to.
        :param sources: The sources from which to deploy the contents of this bucket.
        :param cache_control: System-defined cache-control metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_disposition: System-defined cache-disposition metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_encoding: System-defined content-encoding metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_language: System-defined content-language metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_type: System-defined content-type metadata to be set on all objects in the deployment. Default: - Not set.
        :param destination_key_prefix: Key prefix in the destination bucket. Default: "/" (unzip to root of the destination bucket)
        :param distribution: The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket. Default: - No invalidation occurs
        :param distribution_paths: The file paths to invalidate in the CloudFront distribution. Default: - All files under the destination bucket key prefix will be invalidated.
        :param expires: System-defined expires metadata to be set on all objects in the deployment. Default: - The objects in the distribution will not expire.
        :param memory_limit: The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: 128
        :param metadata: User-defined object metadata to be set on all objects in the deployment. Default: - No user metadata is set
        :param retain_on_delete: If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: if this is set to "false" and destination bucket/prefix is updated, all files in the previous destination will first be deleted and then uploaded to the new destination location. This could have availablity implications on your users. Default: true - when resource is deleted/updated, files are retained
        :param role: Execution role associated with this function. Default: - A role is automatically created
        :param server_side_encryption: System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment. Default: - Server side encryption is not used.
        :param server_side_encryption_aws_kms_key_id: System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment. Default: - Not set.
        :param server_side_encryption_customer_algorithm: System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment. Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080 Default: - Not set.
        :param storage_class: System-defined x-amz-storage-class metadata to be set on all objects in the deployment. Default: - Default storage-class for the bucket is used.
        :param website_redirect_location: System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment. Default: - No website redirection.

        stability
        :stability: experimental
        """
        props = BucketDeploymentProps(destination_bucket=destination_bucket, sources=sources, cache_control=cache_control, content_disposition=content_disposition, content_encoding=content_encoding, content_language=content_language, content_type=content_type, destination_key_prefix=destination_key_prefix, distribution=distribution, distribution_paths=distribution_paths, expires=expires, memory_limit=memory_limit, metadata=metadata, retain_on_delete=retain_on_delete, role=role, server_side_encryption=server_side_encryption, server_side_encryption_aws_kms_key_id=server_side_encryption_aws_kms_key_id, server_side_encryption_customer_algorithm=server_side_encryption_customer_algorithm, storage_class=storage_class, website_redirect_location=website_redirect_location)

        jsii.create(BucketDeployment, self, [scope, id, props])


@jsii.data_type(jsii_type="monocdk-experiment.aws_s3_deployment.BucketDeploymentProps", jsii_struct_bases=[], name_mapping={'destination_bucket': 'destinationBucket', 'sources': 'sources', 'cache_control': 'cacheControl', 'content_disposition': 'contentDisposition', 'content_encoding': 'contentEncoding', 'content_language': 'contentLanguage', 'content_type': 'contentType', 'destination_key_prefix': 'destinationKeyPrefix', 'distribution': 'distribution', 'distribution_paths': 'distributionPaths', 'expires': 'expires', 'memory_limit': 'memoryLimit', 'metadata': 'metadata', 'retain_on_delete': 'retainOnDelete', 'role': 'role', 'server_side_encryption': 'serverSideEncryption', 'server_side_encryption_aws_kms_key_id': 'serverSideEncryptionAwsKmsKeyId', 'server_side_encryption_customer_algorithm': 'serverSideEncryptionCustomerAlgorithm', 'storage_class': 'storageClass', 'website_redirect_location': 'websiteRedirectLocation'})
class BucketDeploymentProps():
    def __init__(self, *, destination_bucket: _IBucket_25bad983, sources: typing.List["ISource"], cache_control: typing.Optional[typing.List["CacheControl"]]=None, content_disposition: typing.Optional[str]=None, content_encoding: typing.Optional[str]=None, content_language: typing.Optional[str]=None, content_type: typing.Optional[str]=None, destination_key_prefix: typing.Optional[str]=None, distribution: typing.Optional[_IDistribution_0af1f2d0]=None, distribution_paths: typing.Optional[typing.List[str]]=None, expires: typing.Optional["Expires"]=None, memory_limit: typing.Optional[jsii.Number]=None, metadata: typing.Optional["UserDefinedObjectMetadata"]=None, retain_on_delete: typing.Optional[bool]=None, role: typing.Optional[_IRole_e69bbae4]=None, server_side_encryption: typing.Optional["ServerSideEncryption"]=None, server_side_encryption_aws_kms_key_id: typing.Optional[str]=None, server_side_encryption_customer_algorithm: typing.Optional[str]=None, storage_class: typing.Optional["StorageClass"]=None, website_redirect_location: typing.Optional[str]=None) -> None:
        """
        :param destination_bucket: The S3 bucket to sync the contents of the zip file to.
        :param sources: The sources from which to deploy the contents of this bucket.
        :param cache_control: System-defined cache-control metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_disposition: System-defined cache-disposition metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_encoding: System-defined content-encoding metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_language: System-defined content-language metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_type: System-defined content-type metadata to be set on all objects in the deployment. Default: - Not set.
        :param destination_key_prefix: Key prefix in the destination bucket. Default: "/" (unzip to root of the destination bucket)
        :param distribution: The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket. Default: - No invalidation occurs
        :param distribution_paths: The file paths to invalidate in the CloudFront distribution. Default: - All files under the destination bucket key prefix will be invalidated.
        :param expires: System-defined expires metadata to be set on all objects in the deployment. Default: - The objects in the distribution will not expire.
        :param memory_limit: The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: 128
        :param metadata: User-defined object metadata to be set on all objects in the deployment. Default: - No user metadata is set
        :param retain_on_delete: If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: if this is set to "false" and destination bucket/prefix is updated, all files in the previous destination will first be deleted and then uploaded to the new destination location. This could have availablity implications on your users. Default: true - when resource is deleted/updated, files are retained
        :param role: Execution role associated with this function. Default: - A role is automatically created
        :param server_side_encryption: System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment. Default: - Server side encryption is not used.
        :param server_side_encryption_aws_kms_key_id: System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment. Default: - Not set.
        :param server_side_encryption_customer_algorithm: System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment. Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080 Default: - Not set.
        :param storage_class: System-defined x-amz-storage-class metadata to be set on all objects in the deployment. Default: - Default storage-class for the bucket is used.
        :param website_redirect_location: System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment. Default: - No website redirection.

        stability
        :stability: experimental
        """
        if isinstance(metadata, dict): metadata = UserDefinedObjectMetadata(**metadata)
        self._values = {
            'destination_bucket': destination_bucket,
            'sources': sources,
        }
        if cache_control is not None: self._values["cache_control"] = cache_control
        if content_disposition is not None: self._values["content_disposition"] = content_disposition
        if content_encoding is not None: self._values["content_encoding"] = content_encoding
        if content_language is not None: self._values["content_language"] = content_language
        if content_type is not None: self._values["content_type"] = content_type
        if destination_key_prefix is not None: self._values["destination_key_prefix"] = destination_key_prefix
        if distribution is not None: self._values["distribution"] = distribution
        if distribution_paths is not None: self._values["distribution_paths"] = distribution_paths
        if expires is not None: self._values["expires"] = expires
        if memory_limit is not None: self._values["memory_limit"] = memory_limit
        if metadata is not None: self._values["metadata"] = metadata
        if retain_on_delete is not None: self._values["retain_on_delete"] = retain_on_delete
        if role is not None: self._values["role"] = role
        if server_side_encryption is not None: self._values["server_side_encryption"] = server_side_encryption
        if server_side_encryption_aws_kms_key_id is not None: self._values["server_side_encryption_aws_kms_key_id"] = server_side_encryption_aws_kms_key_id
        if server_side_encryption_customer_algorithm is not None: self._values["server_side_encryption_customer_algorithm"] = server_side_encryption_customer_algorithm
        if storage_class is not None: self._values["storage_class"] = storage_class
        if website_redirect_location is not None: self._values["website_redirect_location"] = website_redirect_location

    @builtins.property
    def destination_bucket(self) -> _IBucket_25bad983:
        """The S3 bucket to sync the contents of the zip file to.

        stability
        :stability: experimental
        """
        return self._values.get('destination_bucket')

    @builtins.property
    def sources(self) -> typing.List["ISource"]:
        """The sources from which to deploy the contents of this bucket.

        stability
        :stability: experimental
        """
        return self._values.get('sources')

    @builtins.property
    def cache_control(self) -> typing.Optional[typing.List["CacheControl"]]:
        """System-defined cache-control metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('cache_control')

    @builtins.property
    def content_disposition(self) -> typing.Optional[str]:
        """System-defined cache-disposition metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('content_disposition')

    @builtins.property
    def content_encoding(self) -> typing.Optional[str]:
        """System-defined content-encoding metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('content_encoding')

    @builtins.property
    def content_language(self) -> typing.Optional[str]:
        """System-defined content-language metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('content_language')

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        """System-defined content-type metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('content_type')

    @builtins.property
    def destination_key_prefix(self) -> typing.Optional[str]:
        """Key prefix in the destination bucket.

        default
        :default: "/" (unzip to root of the destination bucket)

        stability
        :stability: experimental
        """
        return self._values.get('destination_key_prefix')

    @builtins.property
    def distribution(self) -> typing.Optional[_IDistribution_0af1f2d0]:
        """The CloudFront distribution using the destination bucket as an origin.

        Files in the distribution's edge caches will be invalidated after
        files are uploaded to the destination bucket.

        default
        :default: - No invalidation occurs

        stability
        :stability: experimental
        """
        return self._values.get('distribution')

    @builtins.property
    def distribution_paths(self) -> typing.Optional[typing.List[str]]:
        """The file paths to invalidate in the CloudFront distribution.

        default
        :default: - All files under the destination bucket key prefix will be invalidated.

        stability
        :stability: experimental
        """
        return self._values.get('distribution_paths')

    @builtins.property
    def expires(self) -> typing.Optional["Expires"]:
        """System-defined expires metadata to be set on all objects in the deployment.

        default
        :default: - The objects in the distribution will not expire.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('expires')

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        """The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket.

        If you are deploying large files, you will need to increase this number
        accordingly.

        default
        :default: 128

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit')

    @builtins.property
    def metadata(self) -> typing.Optional["UserDefinedObjectMetadata"]:
        """User-defined object metadata to be set on all objects in the deployment.

        default
        :default: - No user metadata is set

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#UserMetadata
        stability
        :stability: experimental
        """
        return self._values.get('metadata')

    @builtins.property
    def retain_on_delete(self) -> typing.Optional[bool]:
        """If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated.

        NOTICE: if this is set to "false" and destination bucket/prefix is updated,
        all files in the previous destination will first be deleted and then
        uploaded to the new destination location. This could have availablity
        implications on your users.

        default
        :default: true - when resource is deleted/updated, files are retained

        stability
        :stability: experimental
        """
        return self._values.get('retain_on_delete')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Execution role associated with this function.

        default
        :default: - A role is automatically created

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def server_side_encryption(self) -> typing.Optional["ServerSideEncryption"]:
        """System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment.

        default
        :default: - Server side encryption is not used.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('server_side_encryption')

    @builtins.property
    def server_side_encryption_aws_kms_key_id(self) -> typing.Optional[str]:
        """System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('server_side_encryption_aws_kms_key_id')

    @builtins.property
    def server_side_encryption_customer_algorithm(self) -> typing.Optional[str]:
        """System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment.

        Warning: This is not a useful parameter until this bug is fixed: https://github.com/aws/aws-cdk/issues/6080

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html#sse-c-how-to-programmatically-intro
        stability
        :stability: experimental
        """
        return self._values.get('server_side_encryption_customer_algorithm')

    @builtins.property
    def storage_class(self) -> typing.Optional["StorageClass"]:
        """System-defined x-amz-storage-class metadata to be set on all objects in the deployment.

        default
        :default: - Default storage-class for the bucket is used.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('storage_class')

    @builtins.property
    def website_redirect_location(self) -> typing.Optional[str]:
        """System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment.

        default
        :default: - No website redirection.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('website_redirect_location')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BucketDeploymentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CacheControl(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_s3_deployment.CacheControl"):
    """Used for HTTP cache-control header, which influences downstream caches.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, s: str) -> "CacheControl":
        """
        :param s: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromString", [s])

    @jsii.member(jsii_name="maxAge")
    @builtins.classmethod
    def max_age(cls, t: _Duration_5170c158) -> "CacheControl":
        """
        :param t: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "maxAge", [t])

    @jsii.member(jsii_name="mustRevalidate")
    @builtins.classmethod
    def must_revalidate(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "mustRevalidate", [])

    @jsii.member(jsii_name="noCache")
    @builtins.classmethod
    def no_cache(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "noCache", [])

    @jsii.member(jsii_name="noTransform")
    @builtins.classmethod
    def no_transform(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "noTransform", [])

    @jsii.member(jsii_name="proxyRevalidate")
    @builtins.classmethod
    def proxy_revalidate(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "proxyRevalidate", [])

    @jsii.member(jsii_name="setPrivate")
    @builtins.classmethod
    def set_private(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setPrivate", [])

    @jsii.member(jsii_name="setPublic")
    @builtins.classmethod
    def set_public(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setPublic", [])

    @jsii.member(jsii_name="sMaxAge")
    @builtins.classmethod
    def s_max_age(cls, t: _Duration_5170c158) -> "CacheControl":
        """
        :param t: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "sMaxAge", [t])

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


@jsii.data_type(jsii_type="monocdk-experiment.aws_s3_deployment.DeploymentSourceContext", jsii_struct_bases=[], name_mapping={'handler_role': 'handlerRole'})
class DeploymentSourceContext():
    def __init__(self, *, handler_role: _IRole_e69bbae4) -> None:
        """Bind context for ISources.

        :param handler_role: The role for the handler.

        stability
        :stability: experimental
        """
        self._values = {
            'handler_role': handler_role,
        }

    @builtins.property
    def handler_role(self) -> _IRole_e69bbae4:
        """The role for the handler.

        stability
        :stability: experimental
        """
        return self._values.get('handler_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DeploymentSourceContext(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Expires(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_s3_deployment.Expires"):
    """Used for HTTP expires header, which influences downstream caches.

    Does NOT influence deletion of the object.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="after")
    @builtins.classmethod
    def after(cls, t: _Duration_5170c158) -> "Expires":
        """Expire once the specified duration has passed since deployment time.

        :param t: the duration to wait before expiring.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "after", [t])

    @jsii.member(jsii_name="atDate")
    @builtins.classmethod
    def at_date(cls, d: datetime.datetime) -> "Expires":
        """Expire at the specified date.

        :param d: date to expire at.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "atDate", [d])

    @jsii.member(jsii_name="atTimestamp")
    @builtins.classmethod
    def at_timestamp(cls, t: jsii.Number) -> "Expires":
        """Expire at the specified timestamp.

        :param t: timestamp in unix milliseconds.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "atTimestamp", [t])

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, s: str) -> "Expires":
        """
        :param s: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromString", [s])

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


@jsii.interface(jsii_type="monocdk-experiment.aws_s3_deployment.ISource")
class ISource(jsii.compat.Protocol):
    """Represents a source for bucket deployments.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISourceProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, *, handler_role: _IRole_e69bbae4) -> "SourceConfig":
        """Binds the source to a bucket deployment.

        :param scope: The construct tree context.
        :param handler_role: The role for the handler.

        stability
        :stability: experimental
        """
        ...


class _ISourceProxy():
    """Represents a source for bucket deployments.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_s3_deployment.ISource"
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, *, handler_role: _IRole_e69bbae4) -> "SourceConfig":
        """Binds the source to a bucket deployment.

        :param scope: The construct tree context.
        :param handler_role: The role for the handler.

        stability
        :stability: experimental
        """
        context = DeploymentSourceContext(handler_role=handler_role)

        return jsii.invoke(self, "bind", [scope, context])


@jsii.enum(jsii_type="monocdk-experiment.aws_s3_deployment.ServerSideEncryption")
class ServerSideEncryption(enum.Enum):
    """Indicates whether server-side encryption is enabled for the object, and whether that encryption is from the AWS Key Management Service (AWS KMS) or from Amazon S3 managed encryption (SSE-S3).

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    stability
    :stability: experimental
    """
    AES_256 = "AES_256"
    """
    stability
    :stability: experimental
    """
    AWS_KMS = "AWS_KMS"
    """
    stability
    :stability: experimental
    """

class Source(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_s3_deployment.Source"):
    """Specifies bucket deployment source.

    Usage::

        Source.bucket(bucket, key)
        Source.asset('/local/path/to/directory')
        Source.asset('/local/path/to/a/file.zip')

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="asset")
    @builtins.classmethod
    def asset(cls, path: str, *, readers: typing.Optional[typing.List[_IGrantable_0fcfc53a]]=None, source_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional[_AssetHashType_16f7047a]=None, bundling: typing.Optional[_BundlingOptions_0cab5223]=None) -> "ISource":
        """Uses a local asset as the deployment source.

        :param path: The path to a local .zip file or a directory.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        options = _AssetOptions_ed6c2956(readers=readers, source_hash=source_hash, exclude=exclude, follow=follow, asset_hash=asset_hash, asset_hash_type=asset_hash_type, bundling=bundling)

        return jsii.sinvoke(cls, "asset", [path, options])

    @jsii.member(jsii_name="bucket")
    @builtins.classmethod
    def bucket(cls, bucket: _IBucket_25bad983, zip_object_key: str) -> "ISource":
        """Uses a .zip file stored in an S3 bucket as the source for the destination bucket contents.

        :param bucket: The S3 Bucket.
        :param zip_object_key: The S3 object key of the zip file with contents.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "bucket", [bucket, zip_object_key])


@jsii.data_type(jsii_type="monocdk-experiment.aws_s3_deployment.SourceConfig", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'zip_object_key': 'zipObjectKey'})
class SourceConfig():
    def __init__(self, *, bucket: _IBucket_25bad983, zip_object_key: str) -> None:
        """
        :param bucket: The source bucket to deploy from.
        :param zip_object_key: An S3 object key in the source bucket that points to a zip file.

        stability
        :stability: experimental
        """
        self._values = {
            'bucket': bucket,
            'zip_object_key': zip_object_key,
        }

    @builtins.property
    def bucket(self) -> _IBucket_25bad983:
        """The source bucket to deploy from.

        stability
        :stability: experimental
        """
        return self._values.get('bucket')

    @builtins.property
    def zip_object_key(self) -> str:
        """An S3 object key in the source bucket that points to a zip file.

        stability
        :stability: experimental
        """
        return self._values.get('zip_object_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SourceConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_s3_deployment.StorageClass")
class StorageClass(enum.Enum):
    """Storage class used for storing the object.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    stability
    :stability: experimental
    """
    STANDARD = "STANDARD"
    """
    stability
    :stability: experimental
    """
    REDUCED_REDUNDANCY = "REDUCED_REDUNDANCY"
    """
    stability
    :stability: experimental
    """
    STANDARD_IA = "STANDARD_IA"
    """
    stability
    :stability: experimental
    """
    ONEZONE_IA = "ONEZONE_IA"
    """
    stability
    :stability: experimental
    """
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    """
    stability
    :stability: experimental
    """
    GLACIER = "GLACIER"
    """
    stability
    :stability: experimental
    """
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    """
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_s3_deployment.UserDefinedObjectMetadata", jsii_struct_bases=[], name_mapping={})
class UserDefinedObjectMetadata():
    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        self._values = {
        }

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserDefinedObjectMetadata(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "BucketDeployment",
    "BucketDeploymentProps",
    "CacheControl",
    "DeploymentSourceContext",
    "Expires",
    "ISource",
    "ServerSideEncryption",
    "Source",
    "SourceConfig",
    "StorageClass",
    "UserDefinedObjectMetadata",
]

publication.publish()
