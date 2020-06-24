import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53, CfnResource as _CfnResource_7760e8e4, IAsset as _IAsset_a3f13b15, AssetOptions as _AssetOptions_b07b0eef, AssetHashType as _AssetHashType_16f7047a, BundlingOptions as _BundlingOptions_0cab5223)
from ..assets import (CopyOptions as _CopyOptions_65085089, FollowMode as _FollowMode_f74e7125)
from ..aws_iam import (IGrantable as _IGrantable_0fcfc53a)
from ..aws_s3 import (IBucket as _IBucket_25bad983)


@jsii.implements(_IAsset_a3f13b15)
class Asset(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_s3_assets.Asset"):
    """An asset represents a local file or directory, which is automatically uploaded to S3 and then can be referenced within a CDK application.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, path: str, readers: typing.Optional[typing.List[_IGrantable_0fcfc53a]]=None, source_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional[_AssetHashType_16f7047a]=None, bundling: typing.Optional[_BundlingOptions_0cab5223]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.
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
        props = AssetProps(path=path, readers=readers, source_hash=source_hash, exclude=exclude, follow=follow, asset_hash=asset_hash, asset_hash_type=asset_hash_type, bundling=bundling)

        jsii.create(Asset, self, [scope, id, props])

    @jsii.member(jsii_name="addResourceMetadata")
    def add_resource_metadata(self, resource: _CfnResource_7760e8e4, resource_property: str) -> None:
        """Adds CloudFormation template metadata to the specified resource with information that indicates which resource property is mapped to this local asset.

        This can be used by tools such as SAM CLI to provide local
        experience such as local invocation and debugging of Lambda functions.

        Asset metadata will only be included if the stack is synthesized with the
        "aws:cdk:enable-asset-metadata" context key defined, which is the default
        behavior when synthesizing via the CDK Toolkit.

        :param resource: The CloudFormation resource which is using this asset [disable-awslint:ref-via-interface].
        :param resource_property: The property name where this asset is referenced (e.g. "Code" for AWS::Lambda::Function).

        see
        :see: https://github.com/aws/aws-cdk/issues/1432
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addResourceMetadata", [resource, resource_property])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> None:
        """Grants read permissions to the principal on the assets bucket.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @builtins.property
    @jsii.member(jsii_name="assetHash")
    def asset_hash(self) -> str:
        """A hash of this asset, which is available at construction time.

        As this is a plain string, it
        can be used in construct IDs in order to enforce creation of a new resource when the content
        hash has changed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assetHash")

    @builtins.property
    @jsii.member(jsii_name="assetPath")
    def asset_path(self) -> str:
        """The path to the asset (stringinfied token).

        If asset staging is disabled, this will just be the original path.
        If asset staging is enabled it will be the staged path.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assetPath")

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _IBucket_25bad983:
        """The S3 bucket in which this asset resides.

        stability
        :stability: experimental
        """
        return jsii.get(self, "bucket")

    @builtins.property
    @jsii.member(jsii_name="httpUrl")
    def http_url(self) -> str:
        """Attribute which represents the S3 HTTP URL of this asset.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return jsii.get(self, "httpUrl")

    @builtins.property
    @jsii.member(jsii_name="isZipArchive")
    def is_zip_archive(self) -> bool:
        """Indicates if this asset is a zip archive.

        Allows constructs to ensure that the
        correct file type was used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isZipArchive")

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> str:
        """Attribute that represents the name of the bucket this asset exists in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "s3BucketName")

    @builtins.property
    @jsii.member(jsii_name="s3ObjectKey")
    def s3_object_key(self) -> str:
        """Attribute which represents the S3 object key of this asset.

        stability
        :stability: experimental
        """
        return jsii.get(self, "s3ObjectKey")

    @builtins.property
    @jsii.member(jsii_name="s3ObjectUrl")
    def s3_object_url(self) -> str:
        """Attribute which represents the S3 URL of this asset.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            s3:
        """
        return jsii.get(self, "s3ObjectUrl")

    @builtins.property
    @jsii.member(jsii_name="s3Url")
    def s3_url(self) -> str:
        """Attribute which represents the S3 URL of this asset.

        deprecated
        :deprecated: use ``httpUrl``

        stability
        :stability: deprecated
        """
        return jsii.get(self, "s3Url")

    @builtins.property
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> str:
        """A cryptographic hash of the asset.

        deprecated
        :deprecated: see ``assetHash``

        stability
        :stability: deprecated
        """
        return jsii.get(self, "sourceHash")


@jsii.data_type(jsii_type="monocdk-experiment.aws_s3_assets.AssetOptions", jsii_struct_bases=[_CopyOptions_65085089, _AssetOptions_b07b0eef], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'asset_hash': 'assetHash', 'asset_hash_type': 'assetHashType', 'bundling': 'bundling', 'readers': 'readers', 'source_hash': 'sourceHash'})
class AssetOptions(_CopyOptions_65085089, _AssetOptions_b07b0eef):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional[_AssetHashType_16f7047a]=None, bundling: typing.Optional[_BundlingOptions_0cab5223]=None, readers: typing.Optional[typing.List[_IGrantable_0fcfc53a]]=None, source_hash: typing.Optional[str]=None) -> None:
        """
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.

        stability
        :stability: experimental
        """
        if isinstance(bundling, dict): bundling = _BundlingOptions_0cab5223(**bundling)
        self._values = {
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if asset_hash is not None: self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None: self._values["asset_hash_type"] = asset_hash_type
        if bundling is not None: self._values["bundling"] = bundling
        if readers is not None: self._values["readers"] = readers
        if source_hash is not None: self._values["source_hash"] = source_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: deprecated
        """
        return self._values.get('exclude')

    @builtins.property
    def follow(self) -> typing.Optional[_FollowMode_f74e7125]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: deprecated
        """
        return self._values.get('follow')

    @builtins.property
    def asset_hash(self) -> typing.Optional[str]:
        """Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        default
        :default: - based on ``assetHashType``

        stability
        :stability: experimental
        """
        return self._values.get('asset_hash')

    @builtins.property
    def asset_hash_type(self) -> typing.Optional[_AssetHashType_16f7047a]:
        """Specifies the type of hash to calculate for this asset.

        If ``assetHash`` is configured, this option must be ``undefined`` or
        ``AssetHashType.CUSTOM``.

        default
        :default:

        - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is
          explicitly specified this value defaults to ``AssetHashType.CUSTOM``.

        stability
        :stability: experimental
        """
        return self._values.get('asset_hash_type')

    @builtins.property
    def bundling(self) -> typing.Optional[_BundlingOptions_0cab5223]:
        """Bundle the asset by executing a command in a Docker container.

        The asset path will be mounted at ``/asset-input``. The Docker
        container is responsible for putting content at ``/asset-output``.
        The content at ``/asset-output`` will be zipped and used as the
        final asset.

        default
        :default:

        - uploaded as-is to S3 if the asset is a regular file or a .zip file,
          archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        return self._values.get('bundling')

    @builtins.property
    def readers(self) -> typing.Optional[typing.List[_IGrantable_0fcfc53a]]:
        """A list of principals that should be able to read this asset from S3.

        You can use ``asset.grantRead(principal)`` to grant read permissions later.

        default
        :default: - No principals that can read file asset.

        stability
        :stability: experimental
        """
        return self._values.get('readers')

    @builtins.property
    def source_hash(self) -> typing.Optional[str]:
        """Custom hash to use when identifying the specific version of the asset.

        For consistency,
        this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be
        the asset hash.

        NOTE: the source hash is used in order to identify a specific revision of the asset,
        and used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the source hash,
        you will need to make sure it is updated every time the source changes, or otherwise
        it is possible that some deployments will not be invalidated.

        default
        :default:

        - automatically calculate source hash based on the contents
          of the source file or directory.

        deprecated
        :deprecated: see ``assetHash`` and ``assetHashType``

        stability
        :stability: deprecated
        """
        return self._values.get('source_hash')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_s3_assets.AssetProps", jsii_struct_bases=[AssetOptions], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'asset_hash': 'assetHash', 'asset_hash_type': 'assetHashType', 'bundling': 'bundling', 'readers': 'readers', 'source_hash': 'sourceHash', 'path': 'path'})
class AssetProps(AssetOptions):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional[_AssetHashType_16f7047a]=None, bundling: typing.Optional[_BundlingOptions_0cab5223]=None, readers: typing.Optional[typing.List[_IGrantable_0fcfc53a]]=None, source_hash: typing.Optional[str]=None, path: str) -> None:
        """
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param path: The disk location of the asset. The path should refer to one of the following: - A regular file or a .zip file, in which case the file will be uploaded as-is to S3. - A directory, in which case it will be archived into a .zip file and uploaded to S3.

        stability
        :stability: experimental
        """
        if isinstance(bundling, dict): bundling = _BundlingOptions_0cab5223(**bundling)
        self._values = {
            'path': path,
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if asset_hash is not None: self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None: self._values["asset_hash_type"] = asset_hash_type
        if bundling is not None: self._values["bundling"] = bundling
        if readers is not None: self._values["readers"] = readers
        if source_hash is not None: self._values["source_hash"] = source_hash

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: deprecated
        """
        return self._values.get('exclude')

    @builtins.property
    def follow(self) -> typing.Optional[_FollowMode_f74e7125]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: deprecated
        """
        return self._values.get('follow')

    @builtins.property
    def asset_hash(self) -> typing.Optional[str]:
        """Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        default
        :default: - based on ``assetHashType``

        stability
        :stability: experimental
        """
        return self._values.get('asset_hash')

    @builtins.property
    def asset_hash_type(self) -> typing.Optional[_AssetHashType_16f7047a]:
        """Specifies the type of hash to calculate for this asset.

        If ``assetHash`` is configured, this option must be ``undefined`` or
        ``AssetHashType.CUSTOM``.

        default
        :default:

        - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is
          explicitly specified this value defaults to ``AssetHashType.CUSTOM``.

        stability
        :stability: experimental
        """
        return self._values.get('asset_hash_type')

    @builtins.property
    def bundling(self) -> typing.Optional[_BundlingOptions_0cab5223]:
        """Bundle the asset by executing a command in a Docker container.

        The asset path will be mounted at ``/asset-input``. The Docker
        container is responsible for putting content at ``/asset-output``.
        The content at ``/asset-output`` will be zipped and used as the
        final asset.

        default
        :default:

        - uploaded as-is to S3 if the asset is a regular file or a .zip file,
          archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        return self._values.get('bundling')

    @builtins.property
    def readers(self) -> typing.Optional[typing.List[_IGrantable_0fcfc53a]]:
        """A list of principals that should be able to read this asset from S3.

        You can use ``asset.grantRead(principal)`` to grant read permissions later.

        default
        :default: - No principals that can read file asset.

        stability
        :stability: experimental
        """
        return self._values.get('readers')

    @builtins.property
    def source_hash(self) -> typing.Optional[str]:
        """Custom hash to use when identifying the specific version of the asset.

        For consistency,
        this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be
        the asset hash.

        NOTE: the source hash is used in order to identify a specific revision of the asset,
        and used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the source hash,
        you will need to make sure it is updated every time the source changes, or otherwise
        it is possible that some deployments will not be invalidated.

        default
        :default:

        - automatically calculate source hash based on the contents
          of the source file or directory.

        deprecated
        :deprecated: see ``assetHash`` and ``assetHashType``

        stability
        :stability: deprecated
        """
        return self._values.get('source_hash')

    @builtins.property
    def path(self) -> str:
        """The disk location of the asset.

        The path should refer to one of the following:

        - A regular file or a .zip file, in which case the file will be uploaded as-is to S3.
        - A directory, in which case it will be archived into a .zip file and uploaded to S3.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "Asset",
    "AssetOptions",
    "AssetProps",
]

publication.publish()
