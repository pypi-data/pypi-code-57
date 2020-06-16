"""
Main interface for appmesh service type definitions.

Usage::

    ```python
    from mypy_boto3_appmesh.type_defs import AccessLogTypeDef

    data: AccessLogTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccessLogTypeDef",
    "AwsCloudMapInstanceAttributeTypeDef",
    "AwsCloudMapServiceDiscoveryTypeDef",
    "BackendDefaultsTypeDef",
    "BackendTypeDef",
    "ClientPolicyTlsTypeDef",
    "ClientPolicyTypeDef",
    "DnsServiceDiscoveryTypeDef",
    "DurationTypeDef",
    "EgressFilterTypeDef",
    "FileAccessLogTypeDef",
    "GrpcRetryPolicyTypeDef",
    "GrpcRouteActionTypeDef",
    "GrpcRouteMatchTypeDef",
    "GrpcRouteMetadataMatchMethodTypeDef",
    "GrpcRouteMetadataTypeDef",
    "GrpcRouteTypeDef",
    "HeaderMatchMethodTypeDef",
    "HealthCheckPolicyTypeDef",
    "HttpRetryPolicyTypeDef",
    "HttpRouteActionTypeDef",
    "HttpRouteHeaderTypeDef",
    "HttpRouteMatchTypeDef",
    "HttpRouteTypeDef",
    "ListenerTlsAcmCertificateTypeDef",
    "ListenerTlsCertificateTypeDef",
    "ListenerTlsFileCertificateTypeDef",
    "ListenerTlsTypeDef",
    "ListenerTypeDef",
    "LoggingTypeDef",
    "MatchRangeTypeDef",
    "MeshDataTypeDef",
    "MeshRefTypeDef",
    "MeshSpecTypeDef",
    "MeshStatusTypeDef",
    "PortMappingTypeDef",
    "ResourceMetadataTypeDef",
    "RouteDataTypeDef",
    "RouteRefTypeDef",
    "RouteSpecTypeDef",
    "RouteStatusTypeDef",
    "ServiceDiscoveryTypeDef",
    "TagRefTypeDef",
    "TcpRouteActionTypeDef",
    "TcpRouteTypeDef",
    "TlsValidationContextAcmTrustTypeDef",
    "TlsValidationContextFileTrustTypeDef",
    "TlsValidationContextTrustTypeDef",
    "TlsValidationContextTypeDef",
    "VirtualNodeDataTypeDef",
    "VirtualNodeRefTypeDef",
    "VirtualNodeServiceProviderTypeDef",
    "VirtualNodeSpecTypeDef",
    "VirtualNodeStatusTypeDef",
    "VirtualRouterDataTypeDef",
    "VirtualRouterListenerTypeDef",
    "VirtualRouterRefTypeDef",
    "VirtualRouterServiceProviderTypeDef",
    "VirtualRouterSpecTypeDef",
    "VirtualRouterStatusTypeDef",
    "VirtualServiceBackendTypeDef",
    "VirtualServiceDataTypeDef",
    "VirtualServiceProviderTypeDef",
    "VirtualServiceRefTypeDef",
    "VirtualServiceSpecTypeDef",
    "VirtualServiceStatusTypeDef",
    "WeightedTargetTypeDef",
    "CreateMeshOutputTypeDef",
    "CreateRouteOutputTypeDef",
    "CreateVirtualNodeOutputTypeDef",
    "CreateVirtualRouterOutputTypeDef",
    "CreateVirtualServiceOutputTypeDef",
    "DeleteMeshOutputTypeDef",
    "DeleteRouteOutputTypeDef",
    "DeleteVirtualNodeOutputTypeDef",
    "DeleteVirtualRouterOutputTypeDef",
    "DeleteVirtualServiceOutputTypeDef",
    "DescribeMeshOutputTypeDef",
    "DescribeRouteOutputTypeDef",
    "DescribeVirtualNodeOutputTypeDef",
    "DescribeVirtualRouterOutputTypeDef",
    "DescribeVirtualServiceOutputTypeDef",
    "ListMeshesOutputTypeDef",
    "ListRoutesOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListVirtualNodesOutputTypeDef",
    "ListVirtualRoutersOutputTypeDef",
    "ListVirtualServicesOutputTypeDef",
    "PaginatorConfigTypeDef",
    "UpdateMeshOutputTypeDef",
    "UpdateRouteOutputTypeDef",
    "UpdateVirtualNodeOutputTypeDef",
    "UpdateVirtualRouterOutputTypeDef",
    "UpdateVirtualServiceOutputTypeDef",
)

AccessLogTypeDef = TypedDict("AccessLogTypeDef", {"file": "FileAccessLogTypeDef"}, total=False)

AwsCloudMapInstanceAttributeTypeDef = TypedDict(
    "AwsCloudMapInstanceAttributeTypeDef", {"key": str, "value": str}
)

_RequiredAwsCloudMapServiceDiscoveryTypeDef = TypedDict(
    "_RequiredAwsCloudMapServiceDiscoveryTypeDef", {"namespaceName": str, "serviceName": str}
)
_OptionalAwsCloudMapServiceDiscoveryTypeDef = TypedDict(
    "_OptionalAwsCloudMapServiceDiscoveryTypeDef",
    {"attributes": List["AwsCloudMapInstanceAttributeTypeDef"]},
    total=False,
)


class AwsCloudMapServiceDiscoveryTypeDef(
    _RequiredAwsCloudMapServiceDiscoveryTypeDef, _OptionalAwsCloudMapServiceDiscoveryTypeDef
):
    pass


BackendDefaultsTypeDef = TypedDict(
    "BackendDefaultsTypeDef", {"clientPolicy": "ClientPolicyTypeDef"}, total=False
)

BackendTypeDef = TypedDict(
    "BackendTypeDef", {"virtualService": "VirtualServiceBackendTypeDef"}, total=False
)

_RequiredClientPolicyTlsTypeDef = TypedDict(
    "_RequiredClientPolicyTlsTypeDef", {"validation": "TlsValidationContextTypeDef"}
)
_OptionalClientPolicyTlsTypeDef = TypedDict(
    "_OptionalClientPolicyTlsTypeDef", {"enforce": bool, "ports": List[int]}, total=False
)


class ClientPolicyTlsTypeDef(_RequiredClientPolicyTlsTypeDef, _OptionalClientPolicyTlsTypeDef):
    pass


ClientPolicyTypeDef = TypedDict(
    "ClientPolicyTypeDef", {"tls": "ClientPolicyTlsTypeDef"}, total=False
)

DnsServiceDiscoveryTypeDef = TypedDict("DnsServiceDiscoveryTypeDef", {"hostname": str})

DurationTypeDef = TypedDict(
    "DurationTypeDef", {"unit": Literal["ms", "s"], "value": int}, total=False
)

EgressFilterTypeDef = TypedDict("EgressFilterTypeDef", {"type": Literal["ALLOW_ALL", "DROP_ALL"]})

FileAccessLogTypeDef = TypedDict("FileAccessLogTypeDef", {"path": str})

_RequiredGrpcRetryPolicyTypeDef = TypedDict(
    "_RequiredGrpcRetryPolicyTypeDef", {"maxRetries": int, "perRetryTimeout": "DurationTypeDef"}
)
_OptionalGrpcRetryPolicyTypeDef = TypedDict(
    "_OptionalGrpcRetryPolicyTypeDef",
    {
        "grpcRetryEvents": List[
            Literal[
                "cancelled", "deadline-exceeded", "internal", "resource-exhausted", "unavailable"
            ]
        ],
        "httpRetryEvents": List[str],
        "tcpRetryEvents": List[Literal["connection-error"]],
    },
    total=False,
)


class GrpcRetryPolicyTypeDef(_RequiredGrpcRetryPolicyTypeDef, _OptionalGrpcRetryPolicyTypeDef):
    pass


GrpcRouteActionTypeDef = TypedDict(
    "GrpcRouteActionTypeDef", {"weightedTargets": List["WeightedTargetTypeDef"]}
)

GrpcRouteMatchTypeDef = TypedDict(
    "GrpcRouteMatchTypeDef",
    {"metadata": List["GrpcRouteMetadataTypeDef"], "methodName": str, "serviceName": str},
    total=False,
)

GrpcRouteMetadataMatchMethodTypeDef = TypedDict(
    "GrpcRouteMetadataMatchMethodTypeDef",
    {"exact": str, "prefix": str, "range": "MatchRangeTypeDef", "regex": str, "suffix": str},
    total=False,
)

_RequiredGrpcRouteMetadataTypeDef = TypedDict("_RequiredGrpcRouteMetadataTypeDef", {"name": str})
_OptionalGrpcRouteMetadataTypeDef = TypedDict(
    "_OptionalGrpcRouteMetadataTypeDef",
    {"invert": bool, "match": "GrpcRouteMetadataMatchMethodTypeDef"},
    total=False,
)


class GrpcRouteMetadataTypeDef(
    _RequiredGrpcRouteMetadataTypeDef, _OptionalGrpcRouteMetadataTypeDef
):
    pass


_RequiredGrpcRouteTypeDef = TypedDict(
    "_RequiredGrpcRouteTypeDef",
    {"action": "GrpcRouteActionTypeDef", "match": "GrpcRouteMatchTypeDef"},
)
_OptionalGrpcRouteTypeDef = TypedDict(
    "_OptionalGrpcRouteTypeDef", {"retryPolicy": "GrpcRetryPolicyTypeDef"}, total=False
)


class GrpcRouteTypeDef(_RequiredGrpcRouteTypeDef, _OptionalGrpcRouteTypeDef):
    pass


HeaderMatchMethodTypeDef = TypedDict(
    "HeaderMatchMethodTypeDef",
    {"exact": str, "prefix": str, "range": "MatchRangeTypeDef", "regex": str, "suffix": str},
    total=False,
)

_RequiredHealthCheckPolicyTypeDef = TypedDict(
    "_RequiredHealthCheckPolicyTypeDef",
    {
        "healthyThreshold": int,
        "intervalMillis": int,
        "protocol": Literal["grpc", "http", "http2", "tcp"],
        "timeoutMillis": int,
        "unhealthyThreshold": int,
    },
)
_OptionalHealthCheckPolicyTypeDef = TypedDict(
    "_OptionalHealthCheckPolicyTypeDef", {"path": str, "port": int}, total=False
)


class HealthCheckPolicyTypeDef(
    _RequiredHealthCheckPolicyTypeDef, _OptionalHealthCheckPolicyTypeDef
):
    pass


_RequiredHttpRetryPolicyTypeDef = TypedDict(
    "_RequiredHttpRetryPolicyTypeDef", {"maxRetries": int, "perRetryTimeout": "DurationTypeDef"}
)
_OptionalHttpRetryPolicyTypeDef = TypedDict(
    "_OptionalHttpRetryPolicyTypeDef",
    {"httpRetryEvents": List[str], "tcpRetryEvents": List[Literal["connection-error"]]},
    total=False,
)


class HttpRetryPolicyTypeDef(_RequiredHttpRetryPolicyTypeDef, _OptionalHttpRetryPolicyTypeDef):
    pass


HttpRouteActionTypeDef = TypedDict(
    "HttpRouteActionTypeDef", {"weightedTargets": List["WeightedTargetTypeDef"]}
)

_RequiredHttpRouteHeaderTypeDef = TypedDict("_RequiredHttpRouteHeaderTypeDef", {"name": str})
_OptionalHttpRouteHeaderTypeDef = TypedDict(
    "_OptionalHttpRouteHeaderTypeDef",
    {"invert": bool, "match": "HeaderMatchMethodTypeDef"},
    total=False,
)


class HttpRouteHeaderTypeDef(_RequiredHttpRouteHeaderTypeDef, _OptionalHttpRouteHeaderTypeDef):
    pass


_RequiredHttpRouteMatchTypeDef = TypedDict("_RequiredHttpRouteMatchTypeDef", {"prefix": str})
_OptionalHttpRouteMatchTypeDef = TypedDict(
    "_OptionalHttpRouteMatchTypeDef",
    {
        "headers": List["HttpRouteHeaderTypeDef"],
        "method": Literal[
            "CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"
        ],
        "scheme": Literal["http", "https"],
    },
    total=False,
)


class HttpRouteMatchTypeDef(_RequiredHttpRouteMatchTypeDef, _OptionalHttpRouteMatchTypeDef):
    pass


_RequiredHttpRouteTypeDef = TypedDict(
    "_RequiredHttpRouteTypeDef",
    {"action": "HttpRouteActionTypeDef", "match": "HttpRouteMatchTypeDef"},
)
_OptionalHttpRouteTypeDef = TypedDict(
    "_OptionalHttpRouteTypeDef", {"retryPolicy": "HttpRetryPolicyTypeDef"}, total=False
)


class HttpRouteTypeDef(_RequiredHttpRouteTypeDef, _OptionalHttpRouteTypeDef):
    pass


ListenerTlsAcmCertificateTypeDef = TypedDict(
    "ListenerTlsAcmCertificateTypeDef", {"certificateArn": str}
)

ListenerTlsCertificateTypeDef = TypedDict(
    "ListenerTlsCertificateTypeDef",
    {"acm": "ListenerTlsAcmCertificateTypeDef", "file": "ListenerTlsFileCertificateTypeDef"},
    total=False,
)

ListenerTlsFileCertificateTypeDef = TypedDict(
    "ListenerTlsFileCertificateTypeDef", {"certificateChain": str, "privateKey": str}
)

ListenerTlsTypeDef = TypedDict(
    "ListenerTlsTypeDef",
    {
        "certificate": "ListenerTlsCertificateTypeDef",
        "mode": Literal["DISABLED", "PERMISSIVE", "STRICT"],
    },
)

_RequiredListenerTypeDef = TypedDict(
    "_RequiredListenerTypeDef", {"portMapping": "PortMappingTypeDef"}
)
_OptionalListenerTypeDef = TypedDict(
    "_OptionalListenerTypeDef",
    {"healthCheck": "HealthCheckPolicyTypeDef", "tls": "ListenerTlsTypeDef"},
    total=False,
)


class ListenerTypeDef(_RequiredListenerTypeDef, _OptionalListenerTypeDef):
    pass


LoggingTypeDef = TypedDict("LoggingTypeDef", {"accessLog": "AccessLogTypeDef"}, total=False)

MatchRangeTypeDef = TypedDict("MatchRangeTypeDef", {"end": int, "start": int})

MeshDataTypeDef = TypedDict(
    "MeshDataTypeDef",
    {
        "meshName": str,
        "metadata": "ResourceMetadataTypeDef",
        "spec": "MeshSpecTypeDef",
        "status": "MeshStatusTypeDef",
    },
)

MeshRefTypeDef = TypedDict(
    "MeshRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
    },
)

MeshSpecTypeDef = TypedDict("MeshSpecTypeDef", {"egressFilter": "EgressFilterTypeDef"}, total=False)

MeshStatusTypeDef = TypedDict(
    "MeshStatusTypeDef", {"status": Literal["ACTIVE", "DELETED", "INACTIVE"]}, total=False
)

PortMappingTypeDef = TypedDict(
    "PortMappingTypeDef", {"port": int, "protocol": Literal["grpc", "http", "http2", "tcp"]}
)

ResourceMetadataTypeDef = TypedDict(
    "ResourceMetadataTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshOwner": str,
        "resourceOwner": str,
        "uid": str,
        "version": int,
    },
)

RouteDataTypeDef = TypedDict(
    "RouteDataTypeDef",
    {
        "meshName": str,
        "metadata": "ResourceMetadataTypeDef",
        "routeName": str,
        "spec": "RouteSpecTypeDef",
        "status": "RouteStatusTypeDef",
        "virtualRouterName": str,
    },
)

RouteRefTypeDef = TypedDict(
    "RouteRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "routeName": str,
        "version": int,
        "virtualRouterName": str,
    },
)

RouteSpecTypeDef = TypedDict(
    "RouteSpecTypeDef",
    {
        "grpcRoute": "GrpcRouteTypeDef",
        "http2Route": "HttpRouteTypeDef",
        "httpRoute": "HttpRouteTypeDef",
        "priority": int,
        "tcpRoute": "TcpRouteTypeDef",
    },
    total=False,
)

RouteStatusTypeDef = TypedDict(
    "RouteStatusTypeDef", {"status": Literal["ACTIVE", "DELETED", "INACTIVE"]}
)

ServiceDiscoveryTypeDef = TypedDict(
    "ServiceDiscoveryTypeDef",
    {"awsCloudMap": "AwsCloudMapServiceDiscoveryTypeDef", "dns": "DnsServiceDiscoveryTypeDef"},
    total=False,
)

_RequiredTagRefTypeDef = TypedDict("_RequiredTagRefTypeDef", {"key": str})
_OptionalTagRefTypeDef = TypedDict("_OptionalTagRefTypeDef", {"value": str}, total=False)


class TagRefTypeDef(_RequiredTagRefTypeDef, _OptionalTagRefTypeDef):
    pass


TcpRouteActionTypeDef = TypedDict(
    "TcpRouteActionTypeDef", {"weightedTargets": List["WeightedTargetTypeDef"]}
)

TcpRouteTypeDef = TypedDict("TcpRouteTypeDef", {"action": "TcpRouteActionTypeDef"})

TlsValidationContextAcmTrustTypeDef = TypedDict(
    "TlsValidationContextAcmTrustTypeDef", {"certificateAuthorityArns": List[str]}
)

TlsValidationContextFileTrustTypeDef = TypedDict(
    "TlsValidationContextFileTrustTypeDef", {"certificateChain": str}
)

TlsValidationContextTrustTypeDef = TypedDict(
    "TlsValidationContextTrustTypeDef",
    {"acm": "TlsValidationContextAcmTrustTypeDef", "file": "TlsValidationContextFileTrustTypeDef"},
    total=False,
)

TlsValidationContextTypeDef = TypedDict(
    "TlsValidationContextTypeDef", {"trust": "TlsValidationContextTrustTypeDef"}
)

VirtualNodeDataTypeDef = TypedDict(
    "VirtualNodeDataTypeDef",
    {
        "meshName": str,
        "metadata": "ResourceMetadataTypeDef",
        "spec": "VirtualNodeSpecTypeDef",
        "status": "VirtualNodeStatusTypeDef",
        "virtualNodeName": str,
    },
)

VirtualNodeRefTypeDef = TypedDict(
    "VirtualNodeRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
        "virtualNodeName": str,
    },
)

VirtualNodeServiceProviderTypeDef = TypedDict(
    "VirtualNodeServiceProviderTypeDef", {"virtualNodeName": str}
)

VirtualNodeSpecTypeDef = TypedDict(
    "VirtualNodeSpecTypeDef",
    {
        "backendDefaults": "BackendDefaultsTypeDef",
        "backends": List["BackendTypeDef"],
        "listeners": List["ListenerTypeDef"],
        "logging": "LoggingTypeDef",
        "serviceDiscovery": "ServiceDiscoveryTypeDef",
    },
    total=False,
)

VirtualNodeStatusTypeDef = TypedDict(
    "VirtualNodeStatusTypeDef", {"status": Literal["ACTIVE", "DELETED", "INACTIVE"]}
)

VirtualRouterDataTypeDef = TypedDict(
    "VirtualRouterDataTypeDef",
    {
        "meshName": str,
        "metadata": "ResourceMetadataTypeDef",
        "spec": "VirtualRouterSpecTypeDef",
        "status": "VirtualRouterStatusTypeDef",
        "virtualRouterName": str,
    },
)

VirtualRouterListenerTypeDef = TypedDict(
    "VirtualRouterListenerTypeDef", {"portMapping": "PortMappingTypeDef"}
)

VirtualRouterRefTypeDef = TypedDict(
    "VirtualRouterRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
        "virtualRouterName": str,
    },
)

VirtualRouterServiceProviderTypeDef = TypedDict(
    "VirtualRouterServiceProviderTypeDef", {"virtualRouterName": str}
)

VirtualRouterSpecTypeDef = TypedDict(
    "VirtualRouterSpecTypeDef", {"listeners": List["VirtualRouterListenerTypeDef"]}, total=False
)

VirtualRouterStatusTypeDef = TypedDict(
    "VirtualRouterStatusTypeDef", {"status": Literal["ACTIVE", "DELETED", "INACTIVE"]}
)

_RequiredVirtualServiceBackendTypeDef = TypedDict(
    "_RequiredVirtualServiceBackendTypeDef", {"virtualServiceName": str}
)
_OptionalVirtualServiceBackendTypeDef = TypedDict(
    "_OptionalVirtualServiceBackendTypeDef", {"clientPolicy": "ClientPolicyTypeDef"}, total=False
)


class VirtualServiceBackendTypeDef(
    _RequiredVirtualServiceBackendTypeDef, _OptionalVirtualServiceBackendTypeDef
):
    pass


VirtualServiceDataTypeDef = TypedDict(
    "VirtualServiceDataTypeDef",
    {
        "meshName": str,
        "metadata": "ResourceMetadataTypeDef",
        "spec": "VirtualServiceSpecTypeDef",
        "status": "VirtualServiceStatusTypeDef",
        "virtualServiceName": str,
    },
)

VirtualServiceProviderTypeDef = TypedDict(
    "VirtualServiceProviderTypeDef",
    {
        "virtualNode": "VirtualNodeServiceProviderTypeDef",
        "virtualRouter": "VirtualRouterServiceProviderTypeDef",
    },
    total=False,
)

VirtualServiceRefTypeDef = TypedDict(
    "VirtualServiceRefTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "meshName": str,
        "meshOwner": str,
        "resourceOwner": str,
        "version": int,
        "virtualServiceName": str,
    },
)

VirtualServiceSpecTypeDef = TypedDict(
    "VirtualServiceSpecTypeDef", {"provider": "VirtualServiceProviderTypeDef"}, total=False
)

VirtualServiceStatusTypeDef = TypedDict(
    "VirtualServiceStatusTypeDef", {"status": Literal["ACTIVE", "DELETED", "INACTIVE"]}
)

WeightedTargetTypeDef = TypedDict("WeightedTargetTypeDef", {"virtualNode": str, "weight": int})

CreateMeshOutputTypeDef = TypedDict("CreateMeshOutputTypeDef", {"mesh": "MeshDataTypeDef"})

CreateRouteOutputTypeDef = TypedDict("CreateRouteOutputTypeDef", {"route": "RouteDataTypeDef"})

CreateVirtualNodeOutputTypeDef = TypedDict(
    "CreateVirtualNodeOutputTypeDef", {"virtualNode": "VirtualNodeDataTypeDef"}
)

CreateVirtualRouterOutputTypeDef = TypedDict(
    "CreateVirtualRouterOutputTypeDef", {"virtualRouter": "VirtualRouterDataTypeDef"}
)

CreateVirtualServiceOutputTypeDef = TypedDict(
    "CreateVirtualServiceOutputTypeDef", {"virtualService": "VirtualServiceDataTypeDef"}
)

DeleteMeshOutputTypeDef = TypedDict("DeleteMeshOutputTypeDef", {"mesh": "MeshDataTypeDef"})

DeleteRouteOutputTypeDef = TypedDict("DeleteRouteOutputTypeDef", {"route": "RouteDataTypeDef"})

DeleteVirtualNodeOutputTypeDef = TypedDict(
    "DeleteVirtualNodeOutputTypeDef", {"virtualNode": "VirtualNodeDataTypeDef"}
)

DeleteVirtualRouterOutputTypeDef = TypedDict(
    "DeleteVirtualRouterOutputTypeDef", {"virtualRouter": "VirtualRouterDataTypeDef"}
)

DeleteVirtualServiceOutputTypeDef = TypedDict(
    "DeleteVirtualServiceOutputTypeDef", {"virtualService": "VirtualServiceDataTypeDef"}
)

DescribeMeshOutputTypeDef = TypedDict("DescribeMeshOutputTypeDef", {"mesh": "MeshDataTypeDef"})

DescribeRouteOutputTypeDef = TypedDict("DescribeRouteOutputTypeDef", {"route": "RouteDataTypeDef"})

DescribeVirtualNodeOutputTypeDef = TypedDict(
    "DescribeVirtualNodeOutputTypeDef", {"virtualNode": "VirtualNodeDataTypeDef"}
)

DescribeVirtualRouterOutputTypeDef = TypedDict(
    "DescribeVirtualRouterOutputTypeDef", {"virtualRouter": "VirtualRouterDataTypeDef"}
)

DescribeVirtualServiceOutputTypeDef = TypedDict(
    "DescribeVirtualServiceOutputTypeDef", {"virtualService": "VirtualServiceDataTypeDef"}
)

_RequiredListMeshesOutputTypeDef = TypedDict(
    "_RequiredListMeshesOutputTypeDef", {"meshes": List["MeshRefTypeDef"]}
)
_OptionalListMeshesOutputTypeDef = TypedDict(
    "_OptionalListMeshesOutputTypeDef", {"nextToken": str}, total=False
)


class ListMeshesOutputTypeDef(_RequiredListMeshesOutputTypeDef, _OptionalListMeshesOutputTypeDef):
    pass


_RequiredListRoutesOutputTypeDef = TypedDict(
    "_RequiredListRoutesOutputTypeDef", {"routes": List["RouteRefTypeDef"]}
)
_OptionalListRoutesOutputTypeDef = TypedDict(
    "_OptionalListRoutesOutputTypeDef", {"nextToken": str}, total=False
)


class ListRoutesOutputTypeDef(_RequiredListRoutesOutputTypeDef, _OptionalListRoutesOutputTypeDef):
    pass


_RequiredListTagsForResourceOutputTypeDef = TypedDict(
    "_RequiredListTagsForResourceOutputTypeDef", {"tags": List["TagRefTypeDef"]}
)
_OptionalListTagsForResourceOutputTypeDef = TypedDict(
    "_OptionalListTagsForResourceOutputTypeDef", {"nextToken": str}, total=False
)


class ListTagsForResourceOutputTypeDef(
    _RequiredListTagsForResourceOutputTypeDef, _OptionalListTagsForResourceOutputTypeDef
):
    pass


_RequiredListVirtualNodesOutputTypeDef = TypedDict(
    "_RequiredListVirtualNodesOutputTypeDef", {"virtualNodes": List["VirtualNodeRefTypeDef"]}
)
_OptionalListVirtualNodesOutputTypeDef = TypedDict(
    "_OptionalListVirtualNodesOutputTypeDef", {"nextToken": str}, total=False
)


class ListVirtualNodesOutputTypeDef(
    _RequiredListVirtualNodesOutputTypeDef, _OptionalListVirtualNodesOutputTypeDef
):
    pass


_RequiredListVirtualRoutersOutputTypeDef = TypedDict(
    "_RequiredListVirtualRoutersOutputTypeDef", {"virtualRouters": List["VirtualRouterRefTypeDef"]}
)
_OptionalListVirtualRoutersOutputTypeDef = TypedDict(
    "_OptionalListVirtualRoutersOutputTypeDef", {"nextToken": str}, total=False
)


class ListVirtualRoutersOutputTypeDef(
    _RequiredListVirtualRoutersOutputTypeDef, _OptionalListVirtualRoutersOutputTypeDef
):
    pass


_RequiredListVirtualServicesOutputTypeDef = TypedDict(
    "_RequiredListVirtualServicesOutputTypeDef",
    {"virtualServices": List["VirtualServiceRefTypeDef"]},
)
_OptionalListVirtualServicesOutputTypeDef = TypedDict(
    "_OptionalListVirtualServicesOutputTypeDef", {"nextToken": str}, total=False
)


class ListVirtualServicesOutputTypeDef(
    _RequiredListVirtualServicesOutputTypeDef, _OptionalListVirtualServicesOutputTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

UpdateMeshOutputTypeDef = TypedDict("UpdateMeshOutputTypeDef", {"mesh": "MeshDataTypeDef"})

UpdateRouteOutputTypeDef = TypedDict("UpdateRouteOutputTypeDef", {"route": "RouteDataTypeDef"})

UpdateVirtualNodeOutputTypeDef = TypedDict(
    "UpdateVirtualNodeOutputTypeDef", {"virtualNode": "VirtualNodeDataTypeDef"}
)

UpdateVirtualRouterOutputTypeDef = TypedDict(
    "UpdateVirtualRouterOutputTypeDef", {"virtualRouter": "VirtualRouterDataTypeDef"}
)

UpdateVirtualServiceOutputTypeDef = TypedDict(
    "UpdateVirtualServiceOutputTypeDef", {"virtualService": "VirtualServiceDataTypeDef"}
)
