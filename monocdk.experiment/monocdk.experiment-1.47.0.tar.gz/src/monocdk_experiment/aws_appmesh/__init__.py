import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a, Duration as _Duration_5170c158, IResource as _IResource_72f7ee7e, Resource as _Resource_884d0774)
from ..aws_servicediscovery import (IService as _IService_f28ba3c9)


@jsii.implements(_IInspectable_051e6ed8)
class CfnMesh(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.CfnMesh"):
    """A CloudFormation ``AWS::AppMesh::Mesh``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppMesh::Mesh
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh_name: str, spec: typing.Optional[typing.Union["MeshSpecProperty", _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::AppMesh::Mesh``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::Mesh.MeshName``.
        :param spec: ``AWS::AppMesh::Mesh.Spec``.
        :param tags: ``AWS::AppMesh::Mesh.Tags``.
        """
        props = CfnMeshProps(mesh_name=mesh_name, spec=spec, tags=tags)

        jsii.create(CfnMesh, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnMesh":
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
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshName
        """
        return jsii.get(self, "attrMeshName")

    @builtins.property
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshOwner
        """
        return jsii.get(self, "attrMeshOwner")

    @builtins.property
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ResourceOwner
        """
        return jsii.get(self, "attrResourceOwner")

    @builtins.property
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Uid
        """
        return jsii.get(self, "attrUid")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::AppMesh::Mesh.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """``AWS::AppMesh::Mesh.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-meshname
        """
        return jsii.get(self, "meshName")

    @mesh_name.setter
    def mesh_name(self, value: str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> typing.Optional[typing.Union["MeshSpecProperty", _IResolvable_9ceae33e]]:
        """``AWS::AppMesh::Mesh.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-spec
        """
        return jsii.get(self, "spec")

    @spec.setter
    def spec(self, value: typing.Optional[typing.Union["MeshSpecProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "spec", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnMesh.EgressFilterProperty", jsii_struct_bases=[], name_mapping={'type': 'type'})
    class EgressFilterProperty():
        def __init__(self, *, type: str) -> None:
            """
            :param type: ``CfnMesh.EgressFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html
            """
            self._values = {
                'type': type,
            }

        @builtins.property
        def type(self) -> str:
            """``CfnMesh.EgressFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html#cfn-appmesh-mesh-egressfilter-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EgressFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnMesh.MeshSpecProperty", jsii_struct_bases=[], name_mapping={'egress_filter': 'egressFilter'})
    class MeshSpecProperty():
        def __init__(self, *, egress_filter: typing.Optional[typing.Union["CfnMesh.EgressFilterProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param egress_filter: ``CfnMesh.MeshSpecProperty.EgressFilter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html
            """
            self._values = {
            }
            if egress_filter is not None: self._values["egress_filter"] = egress_filter

        @builtins.property
        def egress_filter(self) -> typing.Optional[typing.Union["CfnMesh.EgressFilterProperty", _IResolvable_9ceae33e]]:
            """``CfnMesh.MeshSpecProperty.EgressFilter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-meshspec.html#cfn-appmesh-mesh-meshspec-egressfilter
            """
            return self._values.get('egress_filter')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MeshSpecProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnMeshProps", jsii_struct_bases=[], name_mapping={'mesh_name': 'meshName', 'spec': 'spec', 'tags': 'tags'})
class CfnMeshProps():
    def __init__(self, *, mesh_name: str, spec: typing.Optional[typing.Union["CfnMesh.MeshSpecProperty", _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::AppMesh::Mesh``.

        :param mesh_name: ``AWS::AppMesh::Mesh.MeshName``.
        :param spec: ``AWS::AppMesh::Mesh.Spec``.
        :param tags: ``AWS::AppMesh::Mesh.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html
        """
        self._values = {
            'mesh_name': mesh_name,
        }
        if spec is not None: self._values["spec"] = spec
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> str:
        """``AWS::AppMesh::Mesh.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-meshname
        """
        return self._values.get('mesh_name')

    @builtins.property
    def spec(self) -> typing.Optional[typing.Union["CfnMesh.MeshSpecProperty", _IResolvable_9ceae33e]]:
        """``AWS::AppMesh::Mesh.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-spec
        """
        return self._values.get('spec')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::AppMesh::Mesh.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html#cfn-appmesh-mesh-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMeshProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnRoute(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.CfnRoute"):
    """A CloudFormation ``AWS::AppMesh::Route``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppMesh::Route
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh_name: str, route_name: str, spec: typing.Union["RouteSpecProperty", _IResolvable_9ceae33e], virtual_router_name: str, mesh_owner: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::AppMesh::Route``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::Route.MeshName``.
        :param route_name: ``AWS::AppMesh::Route.RouteName``.
        :param spec: ``AWS::AppMesh::Route.Spec``.
        :param virtual_router_name: ``AWS::AppMesh::Route.VirtualRouterName``.
        :param mesh_owner: ``AWS::AppMesh::Route.MeshOwner``.
        :param tags: ``AWS::AppMesh::Route.Tags``.
        """
        props = CfnRouteProps(mesh_name=mesh_name, route_name=route_name, spec=spec, virtual_router_name=virtual_router_name, mesh_owner=mesh_owner, tags=tags)

        jsii.create(CfnRoute, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnRoute":
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
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshName
        """
        return jsii.get(self, "attrMeshName")

    @builtins.property
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshOwner
        """
        return jsii.get(self, "attrMeshOwner")

    @builtins.property
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ResourceOwner
        """
        return jsii.get(self, "attrResourceOwner")

    @builtins.property
    @jsii.member(jsii_name="attrRouteName")
    def attr_route_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RouteName
        """
        return jsii.get(self, "attrRouteName")

    @builtins.property
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Uid
        """
        return jsii.get(self, "attrUid")

    @builtins.property
    @jsii.member(jsii_name="attrVirtualRouterName")
    def attr_virtual_router_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: VirtualRouterName
        """
        return jsii.get(self, "attrVirtualRouterName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::AppMesh::Route.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """``AWS::AppMesh::Route.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshname
        """
        return jsii.get(self, "meshName")

    @mesh_name.setter
    def mesh_name(self, value: str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> str:
        """``AWS::AppMesh::Route.RouteName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-routename
        """
        return jsii.get(self, "routeName")

    @route_name.setter
    def route_name(self, value: str) -> None:
        jsii.set(self, "routeName", value)

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> typing.Union["RouteSpecProperty", _IResolvable_9ceae33e]:
        """``AWS::AppMesh::Route.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-spec
        """
        return jsii.get(self, "spec")

    @spec.setter
    def spec(self, value: typing.Union["RouteSpecProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "spec", value)

    @builtins.property
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> str:
        """``AWS::AppMesh::Route.VirtualRouterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-virtualroutername
        """
        return jsii.get(self, "virtualRouterName")

    @virtual_router_name.setter
    def virtual_router_name(self, value: str) -> None:
        jsii.set(self, "virtualRouterName", value)

    @builtins.property
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[str]:
        """``AWS::AppMesh::Route.MeshOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshowner
        """
        return jsii.get(self, "meshOwner")

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "meshOwner", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.DurationProperty", jsii_struct_bases=[], name_mapping={'unit': 'unit', 'value': 'value'})
    class DurationProperty():
        def __init__(self, *, unit: str, value: jsii.Number) -> None:
            """
            :param unit: ``CfnRoute.DurationProperty.Unit``.
            :param value: ``CfnRoute.DurationProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html
            """
            self._values = {
                'unit': unit,
                'value': value,
            }

        @builtins.property
        def unit(self) -> str:
            """``CfnRoute.DurationProperty.Unit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html#cfn-appmesh-route-duration-unit
            """
            return self._values.get('unit')

        @builtins.property
        def value(self) -> jsii.Number:
            """``CfnRoute.DurationProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-duration.html#cfn-appmesh-route-duration-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.GrpcRetryPolicyProperty", jsii_struct_bases=[], name_mapping={'max_retries': 'maxRetries', 'per_retry_timeout': 'perRetryTimeout', 'grpc_retry_events': 'grpcRetryEvents', 'http_retry_events': 'httpRetryEvents', 'tcp_retry_events': 'tcpRetryEvents'})
    class GrpcRetryPolicyProperty():
        def __init__(self, *, max_retries: jsii.Number, per_retry_timeout: typing.Union["CfnRoute.DurationProperty", _IResolvable_9ceae33e], grpc_retry_events: typing.Optional[typing.List[str]]=None, http_retry_events: typing.Optional[typing.List[str]]=None, tcp_retry_events: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param max_retries: ``CfnRoute.GrpcRetryPolicyProperty.MaxRetries``.
            :param per_retry_timeout: ``CfnRoute.GrpcRetryPolicyProperty.PerRetryTimeout``.
            :param grpc_retry_events: ``CfnRoute.GrpcRetryPolicyProperty.GrpcRetryEvents``.
            :param http_retry_events: ``CfnRoute.GrpcRetryPolicyProperty.HttpRetryEvents``.
            :param tcp_retry_events: ``CfnRoute.GrpcRetryPolicyProperty.TcpRetryEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html
            """
            self._values = {
                'max_retries': max_retries,
                'per_retry_timeout': per_retry_timeout,
            }
            if grpc_retry_events is not None: self._values["grpc_retry_events"] = grpc_retry_events
            if http_retry_events is not None: self._values["http_retry_events"] = http_retry_events
            if tcp_retry_events is not None: self._values["tcp_retry_events"] = tcp_retry_events

        @builtins.property
        def max_retries(self) -> jsii.Number:
            """``CfnRoute.GrpcRetryPolicyProperty.MaxRetries``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-maxretries
            """
            return self._values.get('max_retries')

        @builtins.property
        def per_retry_timeout(self) -> typing.Union["CfnRoute.DurationProperty", _IResolvable_9ceae33e]:
            """``CfnRoute.GrpcRetryPolicyProperty.PerRetryTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-perretrytimeout
            """
            return self._values.get('per_retry_timeout')

        @builtins.property
        def grpc_retry_events(self) -> typing.Optional[typing.List[str]]:
            """``CfnRoute.GrpcRetryPolicyProperty.GrpcRetryEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-grpcretryevents
            """
            return self._values.get('grpc_retry_events')

        @builtins.property
        def http_retry_events(self) -> typing.Optional[typing.List[str]]:
            """``CfnRoute.GrpcRetryPolicyProperty.HttpRetryEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-httpretryevents
            """
            return self._values.get('http_retry_events')

        @builtins.property
        def tcp_retry_events(self) -> typing.Optional[typing.List[str]]:
            """``CfnRoute.GrpcRetryPolicyProperty.TcpRetryEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcretrypolicy.html#cfn-appmesh-route-grpcretrypolicy-tcpretryevents
            """
            return self._values.get('tcp_retry_events')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GrpcRetryPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.GrpcRouteActionProperty", jsii_struct_bases=[], name_mapping={'weighted_targets': 'weightedTargets'})
    class GrpcRouteActionProperty():
        def __init__(self, *, weighted_targets: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.WeightedTargetProperty", _IResolvable_9ceae33e]]]) -> None:
            """
            :param weighted_targets: ``CfnRoute.GrpcRouteActionProperty.WeightedTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcrouteaction.html
            """
            self._values = {
                'weighted_targets': weighted_targets,
            }

        @builtins.property
        def weighted_targets(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.WeightedTargetProperty", _IResolvable_9ceae33e]]]:
            """``CfnRoute.GrpcRouteActionProperty.WeightedTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcrouteaction.html#cfn-appmesh-route-grpcrouteaction-weightedtargets
            """
            return self._values.get('weighted_targets')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GrpcRouteActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.GrpcRouteMatchProperty", jsii_struct_bases=[], name_mapping={'metadata': 'metadata', 'method_name': 'methodName', 'service_name': 'serviceName'})
    class GrpcRouteMatchProperty():
        def __init__(self, *, metadata: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.GrpcRouteMetadataProperty", _IResolvable_9ceae33e]]]]=None, method_name: typing.Optional[str]=None, service_name: typing.Optional[str]=None) -> None:
            """
            :param metadata: ``CfnRoute.GrpcRouteMatchProperty.Metadata``.
            :param method_name: ``CfnRoute.GrpcRouteMatchProperty.MethodName``.
            :param service_name: ``CfnRoute.GrpcRouteMatchProperty.ServiceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html
            """
            self._values = {
            }
            if metadata is not None: self._values["metadata"] = metadata
            if method_name is not None: self._values["method_name"] = method_name
            if service_name is not None: self._values["service_name"] = service_name

        @builtins.property
        def metadata(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.GrpcRouteMetadataProperty", _IResolvable_9ceae33e]]]]:
            """``CfnRoute.GrpcRouteMatchProperty.Metadata``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-metadata
            """
            return self._values.get('metadata')

        @builtins.property
        def method_name(self) -> typing.Optional[str]:
            """``CfnRoute.GrpcRouteMatchProperty.MethodName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-methodname
            """
            return self._values.get('method_name')

        @builtins.property
        def service_name(self) -> typing.Optional[str]:
            """``CfnRoute.GrpcRouteMatchProperty.ServiceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutematch.html#cfn-appmesh-route-grpcroutematch-servicename
            """
            return self._values.get('service_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GrpcRouteMatchProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.GrpcRouteMetadataMatchMethodProperty", jsii_struct_bases=[], name_mapping={'exact': 'exact', 'prefix': 'prefix', 'range': 'range', 'regex': 'regex', 'suffix': 'suffix'})
    class GrpcRouteMetadataMatchMethodProperty():
        def __init__(self, *, exact: typing.Optional[str]=None, prefix: typing.Optional[str]=None, range: typing.Optional[typing.Union["CfnRoute.MatchRangeProperty", _IResolvable_9ceae33e]]=None, regex: typing.Optional[str]=None, suffix: typing.Optional[str]=None) -> None:
            """
            :param exact: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Exact``.
            :param prefix: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Prefix``.
            :param range: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Range``.
            :param regex: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Regex``.
            :param suffix: ``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Suffix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html
            """
            self._values = {
            }
            if exact is not None: self._values["exact"] = exact
            if prefix is not None: self._values["prefix"] = prefix
            if range is not None: self._values["range"] = range
            if regex is not None: self._values["regex"] = regex
            if suffix is not None: self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[str]:
            """``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Exact``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-exact
            """
            return self._values.get('exact')

        @builtins.property
        def prefix(self) -> typing.Optional[str]:
            """``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-prefix
            """
            return self._values.get('prefix')

        @builtins.property
        def range(self) -> typing.Optional[typing.Union["CfnRoute.MatchRangeProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Range``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-range
            """
            return self._values.get('range')

        @builtins.property
        def regex(self) -> typing.Optional[str]:
            """``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Regex``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-regex
            """
            return self._values.get('regex')

        @builtins.property
        def suffix(self) -> typing.Optional[str]:
            """``CfnRoute.GrpcRouteMetadataMatchMethodProperty.Suffix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadatamatchmethod.html#cfn-appmesh-route-grpcroutemetadatamatchmethod-suffix
            """
            return self._values.get('suffix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GrpcRouteMetadataMatchMethodProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.GrpcRouteMetadataProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'invert': 'invert', 'match': 'match'})
    class GrpcRouteMetadataProperty():
        def __init__(self, *, name: str, invert: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, match: typing.Optional[typing.Union["CfnRoute.GrpcRouteMetadataMatchMethodProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param name: ``CfnRoute.GrpcRouteMetadataProperty.Name``.
            :param invert: ``CfnRoute.GrpcRouteMetadataProperty.Invert``.
            :param match: ``CfnRoute.GrpcRouteMetadataProperty.Match``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html
            """
            self._values = {
                'name': name,
            }
            if invert is not None: self._values["invert"] = invert
            if match is not None: self._values["match"] = match

        @builtins.property
        def name(self) -> str:
            """``CfnRoute.GrpcRouteMetadataProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-name
            """
            return self._values.get('name')

        @builtins.property
        def invert(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnRoute.GrpcRouteMetadataProperty.Invert``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-invert
            """
            return self._values.get('invert')

        @builtins.property
        def match(self) -> typing.Optional[typing.Union["CfnRoute.GrpcRouteMetadataMatchMethodProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.GrpcRouteMetadataProperty.Match``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroutemetadata.html#cfn-appmesh-route-grpcroutemetadata-match
            """
            return self._values.get('match')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GrpcRouteMetadataProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.GrpcRouteProperty", jsii_struct_bases=[], name_mapping={'action': 'action', 'match': 'match', 'retry_policy': 'retryPolicy'})
    class GrpcRouteProperty():
        def __init__(self, *, action: typing.Union["CfnRoute.GrpcRouteActionProperty", _IResolvable_9ceae33e], match: typing.Union["CfnRoute.GrpcRouteMatchProperty", _IResolvable_9ceae33e], retry_policy: typing.Optional[typing.Union["CfnRoute.GrpcRetryPolicyProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param action: ``CfnRoute.GrpcRouteProperty.Action``.
            :param match: ``CfnRoute.GrpcRouteProperty.Match``.
            :param retry_policy: ``CfnRoute.GrpcRouteProperty.RetryPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html
            """
            self._values = {
                'action': action,
                'match': match,
            }
            if retry_policy is not None: self._values["retry_policy"] = retry_policy

        @builtins.property
        def action(self) -> typing.Union["CfnRoute.GrpcRouteActionProperty", _IResolvable_9ceae33e]:
            """``CfnRoute.GrpcRouteProperty.Action``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-action
            """
            return self._values.get('action')

        @builtins.property
        def match(self) -> typing.Union["CfnRoute.GrpcRouteMatchProperty", _IResolvable_9ceae33e]:
            """``CfnRoute.GrpcRouteProperty.Match``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-match
            """
            return self._values.get('match')

        @builtins.property
        def retry_policy(self) -> typing.Optional[typing.Union["CfnRoute.GrpcRetryPolicyProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.GrpcRouteProperty.RetryPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-grpcroute.html#cfn-appmesh-route-grpcroute-retrypolicy
            """
            return self._values.get('retry_policy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GrpcRouteProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.HeaderMatchMethodProperty", jsii_struct_bases=[], name_mapping={'exact': 'exact', 'prefix': 'prefix', 'range': 'range', 'regex': 'regex', 'suffix': 'suffix'})
    class HeaderMatchMethodProperty():
        def __init__(self, *, exact: typing.Optional[str]=None, prefix: typing.Optional[str]=None, range: typing.Optional[typing.Union["CfnRoute.MatchRangeProperty", _IResolvable_9ceae33e]]=None, regex: typing.Optional[str]=None, suffix: typing.Optional[str]=None) -> None:
            """
            :param exact: ``CfnRoute.HeaderMatchMethodProperty.Exact``.
            :param prefix: ``CfnRoute.HeaderMatchMethodProperty.Prefix``.
            :param range: ``CfnRoute.HeaderMatchMethodProperty.Range``.
            :param regex: ``CfnRoute.HeaderMatchMethodProperty.Regex``.
            :param suffix: ``CfnRoute.HeaderMatchMethodProperty.Suffix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html
            """
            self._values = {
            }
            if exact is not None: self._values["exact"] = exact
            if prefix is not None: self._values["prefix"] = prefix
            if range is not None: self._values["range"] = range
            if regex is not None: self._values["regex"] = regex
            if suffix is not None: self._values["suffix"] = suffix

        @builtins.property
        def exact(self) -> typing.Optional[str]:
            """``CfnRoute.HeaderMatchMethodProperty.Exact``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-exact
            """
            return self._values.get('exact')

        @builtins.property
        def prefix(self) -> typing.Optional[str]:
            """``CfnRoute.HeaderMatchMethodProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-prefix
            """
            return self._values.get('prefix')

        @builtins.property
        def range(self) -> typing.Optional[typing.Union["CfnRoute.MatchRangeProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.HeaderMatchMethodProperty.Range``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-range
            """
            return self._values.get('range')

        @builtins.property
        def regex(self) -> typing.Optional[str]:
            """``CfnRoute.HeaderMatchMethodProperty.Regex``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-regex
            """
            return self._values.get('regex')

        @builtins.property
        def suffix(self) -> typing.Optional[str]:
            """``CfnRoute.HeaderMatchMethodProperty.Suffix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-headermatchmethod.html#cfn-appmesh-route-headermatchmethod-suffix
            """
            return self._values.get('suffix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HeaderMatchMethodProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.HttpRetryPolicyProperty", jsii_struct_bases=[], name_mapping={'max_retries': 'maxRetries', 'per_retry_timeout': 'perRetryTimeout', 'http_retry_events': 'httpRetryEvents', 'tcp_retry_events': 'tcpRetryEvents'})
    class HttpRetryPolicyProperty():
        def __init__(self, *, max_retries: jsii.Number, per_retry_timeout: typing.Union["CfnRoute.DurationProperty", _IResolvable_9ceae33e], http_retry_events: typing.Optional[typing.List[str]]=None, tcp_retry_events: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param max_retries: ``CfnRoute.HttpRetryPolicyProperty.MaxRetries``.
            :param per_retry_timeout: ``CfnRoute.HttpRetryPolicyProperty.PerRetryTimeout``.
            :param http_retry_events: ``CfnRoute.HttpRetryPolicyProperty.HttpRetryEvents``.
            :param tcp_retry_events: ``CfnRoute.HttpRetryPolicyProperty.TcpRetryEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html
            """
            self._values = {
                'max_retries': max_retries,
                'per_retry_timeout': per_retry_timeout,
            }
            if http_retry_events is not None: self._values["http_retry_events"] = http_retry_events
            if tcp_retry_events is not None: self._values["tcp_retry_events"] = tcp_retry_events

        @builtins.property
        def max_retries(self) -> jsii.Number:
            """``CfnRoute.HttpRetryPolicyProperty.MaxRetries``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-maxretries
            """
            return self._values.get('max_retries')

        @builtins.property
        def per_retry_timeout(self) -> typing.Union["CfnRoute.DurationProperty", _IResolvable_9ceae33e]:
            """``CfnRoute.HttpRetryPolicyProperty.PerRetryTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-perretrytimeout
            """
            return self._values.get('per_retry_timeout')

        @builtins.property
        def http_retry_events(self) -> typing.Optional[typing.List[str]]:
            """``CfnRoute.HttpRetryPolicyProperty.HttpRetryEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-httpretryevents
            """
            return self._values.get('http_retry_events')

        @builtins.property
        def tcp_retry_events(self) -> typing.Optional[typing.List[str]]:
            """``CfnRoute.HttpRetryPolicyProperty.TcpRetryEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httpretrypolicy.html#cfn-appmesh-route-httpretrypolicy-tcpretryevents
            """
            return self._values.get('tcp_retry_events')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpRetryPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.HttpRouteActionProperty", jsii_struct_bases=[], name_mapping={'weighted_targets': 'weightedTargets'})
    class HttpRouteActionProperty():
        def __init__(self, *, weighted_targets: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.WeightedTargetProperty", _IResolvable_9ceae33e]]]) -> None:
            """
            :param weighted_targets: ``CfnRoute.HttpRouteActionProperty.WeightedTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteaction.html
            """
            self._values = {
                'weighted_targets': weighted_targets,
            }

        @builtins.property
        def weighted_targets(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.WeightedTargetProperty", _IResolvable_9ceae33e]]]:
            """``CfnRoute.HttpRouteActionProperty.WeightedTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteaction.html#cfn-appmesh-route-httprouteaction-weightedtargets
            """
            return self._values.get('weighted_targets')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpRouteActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.HttpRouteHeaderProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'invert': 'invert', 'match': 'match'})
    class HttpRouteHeaderProperty():
        def __init__(self, *, name: str, invert: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, match: typing.Optional[typing.Union["CfnRoute.HeaderMatchMethodProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param name: ``CfnRoute.HttpRouteHeaderProperty.Name``.
            :param invert: ``CfnRoute.HttpRouteHeaderProperty.Invert``.
            :param match: ``CfnRoute.HttpRouteHeaderProperty.Match``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html
            """
            self._values = {
                'name': name,
            }
            if invert is not None: self._values["invert"] = invert
            if match is not None: self._values["match"] = match

        @builtins.property
        def name(self) -> str:
            """``CfnRoute.HttpRouteHeaderProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-name
            """
            return self._values.get('name')

        @builtins.property
        def invert(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnRoute.HttpRouteHeaderProperty.Invert``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-invert
            """
            return self._values.get('invert')

        @builtins.property
        def match(self) -> typing.Optional[typing.Union["CfnRoute.HeaderMatchMethodProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.HttpRouteHeaderProperty.Match``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httprouteheader.html#cfn-appmesh-route-httprouteheader-match
            """
            return self._values.get('match')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpRouteHeaderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.HttpRouteMatchProperty", jsii_struct_bases=[], name_mapping={'prefix': 'prefix', 'headers': 'headers', 'method': 'method', 'scheme': 'scheme'})
    class HttpRouteMatchProperty():
        def __init__(self, *, prefix: str, headers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.HttpRouteHeaderProperty", _IResolvable_9ceae33e]]]]=None, method: typing.Optional[str]=None, scheme: typing.Optional[str]=None) -> None:
            """
            :param prefix: ``CfnRoute.HttpRouteMatchProperty.Prefix``.
            :param headers: ``CfnRoute.HttpRouteMatchProperty.Headers``.
            :param method: ``CfnRoute.HttpRouteMatchProperty.Method``.
            :param scheme: ``CfnRoute.HttpRouteMatchProperty.Scheme``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html
            """
            self._values = {
                'prefix': prefix,
            }
            if headers is not None: self._values["headers"] = headers
            if method is not None: self._values["method"] = method
            if scheme is not None: self._values["scheme"] = scheme

        @builtins.property
        def prefix(self) -> str:
            """``CfnRoute.HttpRouteMatchProperty.Prefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-prefix
            """
            return self._values.get('prefix')

        @builtins.property
        def headers(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.HttpRouteHeaderProperty", _IResolvable_9ceae33e]]]]:
            """``CfnRoute.HttpRouteMatchProperty.Headers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-headers
            """
            return self._values.get('headers')

        @builtins.property
        def method(self) -> typing.Optional[str]:
            """``CfnRoute.HttpRouteMatchProperty.Method``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-method
            """
            return self._values.get('method')

        @builtins.property
        def scheme(self) -> typing.Optional[str]:
            """``CfnRoute.HttpRouteMatchProperty.Scheme``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproutematch.html#cfn-appmesh-route-httproutematch-scheme
            """
            return self._values.get('scheme')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpRouteMatchProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.HttpRouteProperty", jsii_struct_bases=[], name_mapping={'action': 'action', 'match': 'match', 'retry_policy': 'retryPolicy'})
    class HttpRouteProperty():
        def __init__(self, *, action: typing.Union["CfnRoute.HttpRouteActionProperty", _IResolvable_9ceae33e], match: typing.Union["CfnRoute.HttpRouteMatchProperty", _IResolvable_9ceae33e], retry_policy: typing.Optional[typing.Union["CfnRoute.HttpRetryPolicyProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param action: ``CfnRoute.HttpRouteProperty.Action``.
            :param match: ``CfnRoute.HttpRouteProperty.Match``.
            :param retry_policy: ``CfnRoute.HttpRouteProperty.RetryPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html
            """
            self._values = {
                'action': action,
                'match': match,
            }
            if retry_policy is not None: self._values["retry_policy"] = retry_policy

        @builtins.property
        def action(self) -> typing.Union["CfnRoute.HttpRouteActionProperty", _IResolvable_9ceae33e]:
            """``CfnRoute.HttpRouteProperty.Action``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-action
            """
            return self._values.get('action')

        @builtins.property
        def match(self) -> typing.Union["CfnRoute.HttpRouteMatchProperty", _IResolvable_9ceae33e]:
            """``CfnRoute.HttpRouteProperty.Match``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-match
            """
            return self._values.get('match')

        @builtins.property
        def retry_policy(self) -> typing.Optional[typing.Union["CfnRoute.HttpRetryPolicyProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.HttpRouteProperty.RetryPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-httproute.html#cfn-appmesh-route-httproute-retrypolicy
            """
            return self._values.get('retry_policy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HttpRouteProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.MatchRangeProperty", jsii_struct_bases=[], name_mapping={'end': 'end', 'start': 'start'})
    class MatchRangeProperty():
        def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
            """
            :param end: ``CfnRoute.MatchRangeProperty.End``.
            :param start: ``CfnRoute.MatchRangeProperty.Start``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html
            """
            self._values = {
                'end': end,
                'start': start,
            }

        @builtins.property
        def end(self) -> jsii.Number:
            """``CfnRoute.MatchRangeProperty.End``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html#cfn-appmesh-route-matchrange-end
            """
            return self._values.get('end')

        @builtins.property
        def start(self) -> jsii.Number:
            """``CfnRoute.MatchRangeProperty.Start``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-matchrange.html#cfn-appmesh-route-matchrange-start
            """
            return self._values.get('start')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MatchRangeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.RouteSpecProperty", jsii_struct_bases=[], name_mapping={'grpc_route': 'grpcRoute', 'http2_route': 'http2Route', 'http_route': 'httpRoute', 'priority': 'priority', 'tcp_route': 'tcpRoute'})
    class RouteSpecProperty():
        def __init__(self, *, grpc_route: typing.Optional[typing.Union["CfnRoute.GrpcRouteProperty", _IResolvable_9ceae33e]]=None, http2_route: typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", _IResolvable_9ceae33e]]=None, http_route: typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", _IResolvable_9ceae33e]]=None, priority: typing.Optional[jsii.Number]=None, tcp_route: typing.Optional[typing.Union["CfnRoute.TcpRouteProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param grpc_route: ``CfnRoute.RouteSpecProperty.GrpcRoute``.
            :param http2_route: ``CfnRoute.RouteSpecProperty.Http2Route``.
            :param http_route: ``CfnRoute.RouteSpecProperty.HttpRoute``.
            :param priority: ``CfnRoute.RouteSpecProperty.Priority``.
            :param tcp_route: ``CfnRoute.RouteSpecProperty.TcpRoute``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html
            """
            self._values = {
            }
            if grpc_route is not None: self._values["grpc_route"] = grpc_route
            if http2_route is not None: self._values["http2_route"] = http2_route
            if http_route is not None: self._values["http_route"] = http_route
            if priority is not None: self._values["priority"] = priority
            if tcp_route is not None: self._values["tcp_route"] = tcp_route

        @builtins.property
        def grpc_route(self) -> typing.Optional[typing.Union["CfnRoute.GrpcRouteProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.RouteSpecProperty.GrpcRoute``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-grpcroute
            """
            return self._values.get('grpc_route')

        @builtins.property
        def http2_route(self) -> typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.RouteSpecProperty.Http2Route``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-http2route
            """
            return self._values.get('http2_route')

        @builtins.property
        def http_route(self) -> typing.Optional[typing.Union["CfnRoute.HttpRouteProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.RouteSpecProperty.HttpRoute``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-httproute
            """
            return self._values.get('http_route')

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            """``CfnRoute.RouteSpecProperty.Priority``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-priority
            """
            return self._values.get('priority')

        @builtins.property
        def tcp_route(self) -> typing.Optional[typing.Union["CfnRoute.TcpRouteProperty", _IResolvable_9ceae33e]]:
            """``CfnRoute.RouteSpecProperty.TcpRoute``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-routespec.html#cfn-appmesh-route-routespec-tcproute
            """
            return self._values.get('tcp_route')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RouteSpecProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.TcpRouteActionProperty", jsii_struct_bases=[], name_mapping={'weighted_targets': 'weightedTargets'})
    class TcpRouteActionProperty():
        def __init__(self, *, weighted_targets: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.WeightedTargetProperty", _IResolvable_9ceae33e]]]) -> None:
            """
            :param weighted_targets: ``CfnRoute.TcpRouteActionProperty.WeightedTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcprouteaction.html
            """
            self._values = {
                'weighted_targets': weighted_targets,
            }

        @builtins.property
        def weighted_targets(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnRoute.WeightedTargetProperty", _IResolvable_9ceae33e]]]:
            """``CfnRoute.TcpRouteActionProperty.WeightedTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcprouteaction.html#cfn-appmesh-route-tcprouteaction-weightedtargets
            """
            return self._values.get('weighted_targets')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TcpRouteActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.TcpRouteProperty", jsii_struct_bases=[], name_mapping={'action': 'action'})
    class TcpRouteProperty():
        def __init__(self, *, action: typing.Union["CfnRoute.TcpRouteActionProperty", _IResolvable_9ceae33e]) -> None:
            """
            :param action: ``CfnRoute.TcpRouteProperty.Action``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html
            """
            self._values = {
                'action': action,
            }

        @builtins.property
        def action(self) -> typing.Union["CfnRoute.TcpRouteActionProperty", _IResolvable_9ceae33e]:
            """``CfnRoute.TcpRouteProperty.Action``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-tcproute.html#cfn-appmesh-route-tcproute-action
            """
            return self._values.get('action')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TcpRouteProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRoute.WeightedTargetProperty", jsii_struct_bases=[], name_mapping={'virtual_node': 'virtualNode', 'weight': 'weight'})
    class WeightedTargetProperty():
        def __init__(self, *, virtual_node: str, weight: jsii.Number) -> None:
            """
            :param virtual_node: ``CfnRoute.WeightedTargetProperty.VirtualNode``.
            :param weight: ``CfnRoute.WeightedTargetProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html
            """
            self._values = {
                'virtual_node': virtual_node,
                'weight': weight,
            }

        @builtins.property
        def virtual_node(self) -> str:
            """``CfnRoute.WeightedTargetProperty.VirtualNode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-virtualnode
            """
            return self._values.get('virtual_node')

        @builtins.property
        def weight(self) -> jsii.Number:
            """``CfnRoute.WeightedTargetProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-route-weightedtarget.html#cfn-appmesh-route-weightedtarget-weight
            """
            return self._values.get('weight')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'WeightedTargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnRouteProps", jsii_struct_bases=[], name_mapping={'mesh_name': 'meshName', 'route_name': 'routeName', 'spec': 'spec', 'virtual_router_name': 'virtualRouterName', 'mesh_owner': 'meshOwner', 'tags': 'tags'})
class CfnRouteProps():
    def __init__(self, *, mesh_name: str, route_name: str, spec: typing.Union["CfnRoute.RouteSpecProperty", _IResolvable_9ceae33e], virtual_router_name: str, mesh_owner: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::AppMesh::Route``.

        :param mesh_name: ``AWS::AppMesh::Route.MeshName``.
        :param route_name: ``AWS::AppMesh::Route.RouteName``.
        :param spec: ``AWS::AppMesh::Route.Spec``.
        :param virtual_router_name: ``AWS::AppMesh::Route.VirtualRouterName``.
        :param mesh_owner: ``AWS::AppMesh::Route.MeshOwner``.
        :param tags: ``AWS::AppMesh::Route.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html
        """
        self._values = {
            'mesh_name': mesh_name,
            'route_name': route_name,
            'spec': spec,
            'virtual_router_name': virtual_router_name,
        }
        if mesh_owner is not None: self._values["mesh_owner"] = mesh_owner
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> str:
        """``AWS::AppMesh::Route.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshname
        """
        return self._values.get('mesh_name')

    @builtins.property
    def route_name(self) -> str:
        """``AWS::AppMesh::Route.RouteName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-routename
        """
        return self._values.get('route_name')

    @builtins.property
    def spec(self) -> typing.Union["CfnRoute.RouteSpecProperty", _IResolvable_9ceae33e]:
        """``AWS::AppMesh::Route.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-spec
        """
        return self._values.get('spec')

    @builtins.property
    def virtual_router_name(self) -> str:
        """``AWS::AppMesh::Route.VirtualRouterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-virtualroutername
        """
        return self._values.get('virtual_router_name')

    @builtins.property
    def mesh_owner(self) -> typing.Optional[str]:
        """``AWS::AppMesh::Route.MeshOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-meshowner
        """
        return self._values.get('mesh_owner')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::AppMesh::Route.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html#cfn-appmesh-route-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRouteProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnVirtualNode(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode"):
    """A CloudFormation ``AWS::AppMesh::VirtualNode``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppMesh::VirtualNode
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh_name: str, spec: typing.Union["VirtualNodeSpecProperty", _IResolvable_9ceae33e], virtual_node_name: str, mesh_owner: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::AppMesh::VirtualNode``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::VirtualNode.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualNode.Spec``.
        :param virtual_node_name: ``AWS::AppMesh::VirtualNode.VirtualNodeName``.
        :param mesh_owner: ``AWS::AppMesh::VirtualNode.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualNode.Tags``.
        """
        props = CfnVirtualNodeProps(mesh_name=mesh_name, spec=spec, virtual_node_name=virtual_node_name, mesh_owner=mesh_owner, tags=tags)

        jsii.create(CfnVirtualNode, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnVirtualNode":
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
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshName
        """
        return jsii.get(self, "attrMeshName")

    @builtins.property
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshOwner
        """
        return jsii.get(self, "attrMeshOwner")

    @builtins.property
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ResourceOwner
        """
        return jsii.get(self, "attrResourceOwner")

    @builtins.property
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Uid
        """
        return jsii.get(self, "attrUid")

    @builtins.property
    @jsii.member(jsii_name="attrVirtualNodeName")
    def attr_virtual_node_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: VirtualNodeName
        """
        return jsii.get(self, "attrVirtualNodeName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::AppMesh::VirtualNode.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """``AWS::AppMesh::VirtualNode.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshname
        """
        return jsii.get(self, "meshName")

    @mesh_name.setter
    def mesh_name(self, value: str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> typing.Union["VirtualNodeSpecProperty", _IResolvable_9ceae33e]:
        """``AWS::AppMesh::VirtualNode.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-spec
        """
        return jsii.get(self, "spec")

    @spec.setter
    def spec(self, value: typing.Union["VirtualNodeSpecProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "spec", value)

    @builtins.property
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> str:
        """``AWS::AppMesh::VirtualNode.VirtualNodeName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-virtualnodename
        """
        return jsii.get(self, "virtualNodeName")

    @virtual_node_name.setter
    def virtual_node_name(self, value: str) -> None:
        jsii.set(self, "virtualNodeName", value)

    @builtins.property
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[str]:
        """``AWS::AppMesh::VirtualNode.MeshOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshowner
        """
        return jsii.get(self, "meshOwner")

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "meshOwner", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.AccessLogProperty", jsii_struct_bases=[], name_mapping={'file': 'file'})
    class AccessLogProperty():
        def __init__(self, *, file: typing.Optional[typing.Union["CfnVirtualNode.FileAccessLogProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param file: ``CfnVirtualNode.AccessLogProperty.File``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-accesslog.html
            """
            self._values = {
            }
            if file is not None: self._values["file"] = file

        @builtins.property
        def file(self) -> typing.Optional[typing.Union["CfnVirtualNode.FileAccessLogProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.AccessLogProperty.File``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-accesslog.html#cfn-appmesh-virtualnode-accesslog-file
            """
            return self._values.get('file')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccessLogProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.AwsCloudMapInstanceAttributeProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class AwsCloudMapInstanceAttributeProperty():
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnVirtualNode.AwsCloudMapInstanceAttributeProperty.Key``.
            :param value: ``CfnVirtualNode.AwsCloudMapInstanceAttributeProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnVirtualNode.AwsCloudMapInstanceAttributeProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html#cfn-appmesh-virtualnode-awscloudmapinstanceattribute-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnVirtualNode.AwsCloudMapInstanceAttributeProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapinstanceattribute.html#cfn-appmesh-virtualnode-awscloudmapinstanceattribute-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AwsCloudMapInstanceAttributeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty", jsii_struct_bases=[], name_mapping={'namespace_name': 'namespaceName', 'service_name': 'serviceName', 'attributes': 'attributes'})
    class AwsCloudMapServiceDiscoveryProperty():
        def __init__(self, *, namespace_name: str, service_name: str, attributes: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnVirtualNode.AwsCloudMapInstanceAttributeProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param namespace_name: ``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.NamespaceName``.
            :param service_name: ``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.ServiceName``.
            :param attributes: ``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html
            """
            self._values = {
                'namespace_name': namespace_name,
                'service_name': service_name,
            }
            if attributes is not None: self._values["attributes"] = attributes

        @builtins.property
        def namespace_name(self) -> str:
            """``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.NamespaceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-namespacename
            """
            return self._values.get('namespace_name')

        @builtins.property
        def service_name(self) -> str:
            """``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.ServiceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-servicename
            """
            return self._values.get('service_name')

        @builtins.property
        def attributes(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnVirtualNode.AwsCloudMapInstanceAttributeProperty", _IResolvable_9ceae33e]]]]:
            """``CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty.Attributes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-awscloudmapservicediscovery.html#cfn-appmesh-virtualnode-awscloudmapservicediscovery-attributes
            """
            return self._values.get('attributes')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AwsCloudMapServiceDiscoveryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.BackendDefaultsProperty", jsii_struct_bases=[], name_mapping={'client_policy': 'clientPolicy'})
    class BackendDefaultsProperty():
        def __init__(self, *, client_policy: typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param client_policy: ``CfnVirtualNode.BackendDefaultsProperty.ClientPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backenddefaults.html
            """
            self._values = {
            }
            if client_policy is not None: self._values["client_policy"] = client_policy

        @builtins.property
        def client_policy(self) -> typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.BackendDefaultsProperty.ClientPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backenddefaults.html#cfn-appmesh-virtualnode-backenddefaults-clientpolicy
            """
            return self._values.get('client_policy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BackendDefaultsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.BackendProperty", jsii_struct_bases=[], name_mapping={'virtual_service': 'virtualService'})
    class BackendProperty():
        def __init__(self, *, virtual_service: typing.Optional[typing.Union["CfnVirtualNode.VirtualServiceBackendProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param virtual_service: ``CfnVirtualNode.BackendProperty.VirtualService``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backend.html
            """
            self._values = {
            }
            if virtual_service is not None: self._values["virtual_service"] = virtual_service

        @builtins.property
        def virtual_service(self) -> typing.Optional[typing.Union["CfnVirtualNode.VirtualServiceBackendProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.BackendProperty.VirtualService``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-backend.html#cfn-appmesh-virtualnode-backend-virtualservice
            """
            return self._values.get('virtual_service')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BackendProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.ClientPolicyProperty", jsii_struct_bases=[], name_mapping={'tls': 'tls'})
    class ClientPolicyProperty():
        def __init__(self, *, tls: typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyTlsProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param tls: ``CfnVirtualNode.ClientPolicyProperty.TLS``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicy.html
            """
            self._values = {
            }
            if tls is not None: self._values["tls"] = tls

        @builtins.property
        def tls(self) -> typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyTlsProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.ClientPolicyProperty.TLS``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicy.html#cfn-appmesh-virtualnode-clientpolicy-tls
            """
            return self._values.get('tls')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ClientPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.ClientPolicyTlsProperty", jsii_struct_bases=[], name_mapping={'validation': 'validation', 'enforce': 'enforce', 'ports': 'ports'})
    class ClientPolicyTlsProperty():
        def __init__(self, *, validation: typing.Union["CfnVirtualNode.TlsValidationContextProperty", _IResolvable_9ceae33e], enforce: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, ports: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[jsii.Number]]]=None) -> None:
            """
            :param validation: ``CfnVirtualNode.ClientPolicyTlsProperty.Validation``.
            :param enforce: ``CfnVirtualNode.ClientPolicyTlsProperty.Enforce``.
            :param ports: ``CfnVirtualNode.ClientPolicyTlsProperty.Ports``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html
            """
            self._values = {
                'validation': validation,
            }
            if enforce is not None: self._values["enforce"] = enforce
            if ports is not None: self._values["ports"] = ports

        @builtins.property
        def validation(self) -> typing.Union["CfnVirtualNode.TlsValidationContextProperty", _IResolvable_9ceae33e]:
            """``CfnVirtualNode.ClientPolicyTlsProperty.Validation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-validation
            """
            return self._values.get('validation')

        @builtins.property
        def enforce(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.ClientPolicyTlsProperty.Enforce``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-enforce
            """
            return self._values.get('enforce')

        @builtins.property
        def ports(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[jsii.Number]]]:
            """``CfnVirtualNode.ClientPolicyTlsProperty.Ports``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-clientpolicytls.html#cfn-appmesh-virtualnode-clientpolicytls-ports
            """
            return self._values.get('ports')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ClientPolicyTlsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.DnsServiceDiscoveryProperty", jsii_struct_bases=[], name_mapping={'hostname': 'hostname'})
    class DnsServiceDiscoveryProperty():
        def __init__(self, *, hostname: str) -> None:
            """
            :param hostname: ``CfnVirtualNode.DnsServiceDiscoveryProperty.Hostname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html
            """
            self._values = {
                'hostname': hostname,
            }

        @builtins.property
        def hostname(self) -> str:
            """``CfnVirtualNode.DnsServiceDiscoveryProperty.Hostname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-dnsservicediscovery.html#cfn-appmesh-virtualnode-dnsservicediscovery-hostname
            """
            return self._values.get('hostname')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DnsServiceDiscoveryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.FileAccessLogProperty", jsii_struct_bases=[], name_mapping={'path': 'path'})
    class FileAccessLogProperty():
        def __init__(self, *, path: str) -> None:
            """
            :param path: ``CfnVirtualNode.FileAccessLogProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html
            """
            self._values = {
                'path': path,
            }

        @builtins.property
        def path(self) -> str:
            """``CfnVirtualNode.FileAccessLogProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-fileaccesslog.html#cfn-appmesh-virtualnode-fileaccesslog-path
            """
            return self._values.get('path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FileAccessLogProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.HealthCheckProperty", jsii_struct_bases=[], name_mapping={'healthy_threshold': 'healthyThreshold', 'interval_millis': 'intervalMillis', 'protocol': 'protocol', 'timeout_millis': 'timeoutMillis', 'unhealthy_threshold': 'unhealthyThreshold', 'path': 'path', 'port': 'port'})
    class HealthCheckProperty():
        def __init__(self, *, healthy_threshold: jsii.Number, interval_millis: jsii.Number, protocol: str, timeout_millis: jsii.Number, unhealthy_threshold: jsii.Number, path: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None) -> None:
            """
            :param healthy_threshold: ``CfnVirtualNode.HealthCheckProperty.HealthyThreshold``.
            :param interval_millis: ``CfnVirtualNode.HealthCheckProperty.IntervalMillis``.
            :param protocol: ``CfnVirtualNode.HealthCheckProperty.Protocol``.
            :param timeout_millis: ``CfnVirtualNode.HealthCheckProperty.TimeoutMillis``.
            :param unhealthy_threshold: ``CfnVirtualNode.HealthCheckProperty.UnhealthyThreshold``.
            :param path: ``CfnVirtualNode.HealthCheckProperty.Path``.
            :param port: ``CfnVirtualNode.HealthCheckProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html
            """
            self._values = {
                'healthy_threshold': healthy_threshold,
                'interval_millis': interval_millis,
                'protocol': protocol,
                'timeout_millis': timeout_millis,
                'unhealthy_threshold': unhealthy_threshold,
            }
            if path is not None: self._values["path"] = path
            if port is not None: self._values["port"] = port

        @builtins.property
        def healthy_threshold(self) -> jsii.Number:
            """``CfnVirtualNode.HealthCheckProperty.HealthyThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-healthythreshold
            """
            return self._values.get('healthy_threshold')

        @builtins.property
        def interval_millis(self) -> jsii.Number:
            """``CfnVirtualNode.HealthCheckProperty.IntervalMillis``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-intervalmillis
            """
            return self._values.get('interval_millis')

        @builtins.property
        def protocol(self) -> str:
            """``CfnVirtualNode.HealthCheckProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-protocol
            """
            return self._values.get('protocol')

        @builtins.property
        def timeout_millis(self) -> jsii.Number:
            """``CfnVirtualNode.HealthCheckProperty.TimeoutMillis``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-timeoutmillis
            """
            return self._values.get('timeout_millis')

        @builtins.property
        def unhealthy_threshold(self) -> jsii.Number:
            """``CfnVirtualNode.HealthCheckProperty.UnhealthyThreshold``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-unhealthythreshold
            """
            return self._values.get('unhealthy_threshold')

        @builtins.property
        def path(self) -> typing.Optional[str]:
            """``CfnVirtualNode.HealthCheckProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-path
            """
            return self._values.get('path')

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnVirtualNode.HealthCheckProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-healthcheck.html#cfn-appmesh-virtualnode-healthcheck-port
            """
            return self._values.get('port')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HealthCheckProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.ListenerProperty", jsii_struct_bases=[], name_mapping={'port_mapping': 'portMapping', 'health_check': 'healthCheck', 'tls': 'tls'})
    class ListenerProperty():
        def __init__(self, *, port_mapping: typing.Union["CfnVirtualNode.PortMappingProperty", _IResolvable_9ceae33e], health_check: typing.Optional[typing.Union["CfnVirtualNode.HealthCheckProperty", _IResolvable_9ceae33e]]=None, tls: typing.Optional[typing.Union["CfnVirtualNode.ListenerTlsProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param port_mapping: ``CfnVirtualNode.ListenerProperty.PortMapping``.
            :param health_check: ``CfnVirtualNode.ListenerProperty.HealthCheck``.
            :param tls: ``CfnVirtualNode.ListenerProperty.TLS``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html
            """
            self._values = {
                'port_mapping': port_mapping,
            }
            if health_check is not None: self._values["health_check"] = health_check
            if tls is not None: self._values["tls"] = tls

        @builtins.property
        def port_mapping(self) -> typing.Union["CfnVirtualNode.PortMappingProperty", _IResolvable_9ceae33e]:
            """``CfnVirtualNode.ListenerProperty.PortMapping``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-portmapping
            """
            return self._values.get('port_mapping')

        @builtins.property
        def health_check(self) -> typing.Optional[typing.Union["CfnVirtualNode.HealthCheckProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.ListenerProperty.HealthCheck``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-healthcheck
            """
            return self._values.get('health_check')

        @builtins.property
        def tls(self) -> typing.Optional[typing.Union["CfnVirtualNode.ListenerTlsProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.ListenerProperty.TLS``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listener.html#cfn-appmesh-virtualnode-listener-tls
            """
            return self._values.get('tls')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ListenerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.ListenerTlsAcmCertificateProperty", jsii_struct_bases=[], name_mapping={'certificate_arn': 'certificateArn'})
    class ListenerTlsAcmCertificateProperty():
        def __init__(self, *, certificate_arn: str) -> None:
            """
            :param certificate_arn: ``CfnVirtualNode.ListenerTlsAcmCertificateProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsacmcertificate.html
            """
            self._values = {
                'certificate_arn': certificate_arn,
            }

        @builtins.property
        def certificate_arn(self) -> str:
            """``CfnVirtualNode.ListenerTlsAcmCertificateProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsacmcertificate.html#cfn-appmesh-virtualnode-listenertlsacmcertificate-certificatearn
            """
            return self._values.get('certificate_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ListenerTlsAcmCertificateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.ListenerTlsCertificateProperty", jsii_struct_bases=[], name_mapping={'acm': 'acm', 'file': 'file'})
    class ListenerTlsCertificateProperty():
        def __init__(self, *, acm: typing.Optional[typing.Union["CfnVirtualNode.ListenerTlsAcmCertificateProperty", _IResolvable_9ceae33e]]=None, file: typing.Optional[typing.Union["CfnVirtualNode.ListenerTlsFileCertificateProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param acm: ``CfnVirtualNode.ListenerTlsCertificateProperty.ACM``.
            :param file: ``CfnVirtualNode.ListenerTlsCertificateProperty.File``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html
            """
            self._values = {
            }
            if acm is not None: self._values["acm"] = acm
            if file is not None: self._values["file"] = file

        @builtins.property
        def acm(self) -> typing.Optional[typing.Union["CfnVirtualNode.ListenerTlsAcmCertificateProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.ListenerTlsCertificateProperty.ACM``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html#cfn-appmesh-virtualnode-listenertlscertificate-acm
            """
            return self._values.get('acm')

        @builtins.property
        def file(self) -> typing.Optional[typing.Union["CfnVirtualNode.ListenerTlsFileCertificateProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.ListenerTlsCertificateProperty.File``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlscertificate.html#cfn-appmesh-virtualnode-listenertlscertificate-file
            """
            return self._values.get('file')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ListenerTlsCertificateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.ListenerTlsFileCertificateProperty", jsii_struct_bases=[], name_mapping={'certificate_chain': 'certificateChain', 'private_key': 'privateKey'})
    class ListenerTlsFileCertificateProperty():
        def __init__(self, *, certificate_chain: str, private_key: str) -> None:
            """
            :param certificate_chain: ``CfnVirtualNode.ListenerTlsFileCertificateProperty.CertificateChain``.
            :param private_key: ``CfnVirtualNode.ListenerTlsFileCertificateProperty.PrivateKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html
            """
            self._values = {
                'certificate_chain': certificate_chain,
                'private_key': private_key,
            }

        @builtins.property
        def certificate_chain(self) -> str:
            """``CfnVirtualNode.ListenerTlsFileCertificateProperty.CertificateChain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html#cfn-appmesh-virtualnode-listenertlsfilecertificate-certificatechain
            """
            return self._values.get('certificate_chain')

        @builtins.property
        def private_key(self) -> str:
            """``CfnVirtualNode.ListenerTlsFileCertificateProperty.PrivateKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertlsfilecertificate.html#cfn-appmesh-virtualnode-listenertlsfilecertificate-privatekey
            """
            return self._values.get('private_key')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ListenerTlsFileCertificateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.ListenerTlsProperty", jsii_struct_bases=[], name_mapping={'certificate': 'certificate', 'mode': 'mode'})
    class ListenerTlsProperty():
        def __init__(self, *, certificate: typing.Union["CfnVirtualNode.ListenerTlsCertificateProperty", _IResolvable_9ceae33e], mode: str) -> None:
            """
            :param certificate: ``CfnVirtualNode.ListenerTlsProperty.Certificate``.
            :param mode: ``CfnVirtualNode.ListenerTlsProperty.Mode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html
            """
            self._values = {
                'certificate': certificate,
                'mode': mode,
            }

        @builtins.property
        def certificate(self) -> typing.Union["CfnVirtualNode.ListenerTlsCertificateProperty", _IResolvable_9ceae33e]:
            """``CfnVirtualNode.ListenerTlsProperty.Certificate``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html#cfn-appmesh-virtualnode-listenertls-certificate
            """
            return self._values.get('certificate')

        @builtins.property
        def mode(self) -> str:
            """``CfnVirtualNode.ListenerTlsProperty.Mode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-listenertls.html#cfn-appmesh-virtualnode-listenertls-mode
            """
            return self._values.get('mode')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ListenerTlsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.LoggingProperty", jsii_struct_bases=[], name_mapping={'access_log': 'accessLog'})
    class LoggingProperty():
        def __init__(self, *, access_log: typing.Optional[typing.Union["CfnVirtualNode.AccessLogProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param access_log: ``CfnVirtualNode.LoggingProperty.AccessLog``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-logging.html
            """
            self._values = {
            }
            if access_log is not None: self._values["access_log"] = access_log

        @builtins.property
        def access_log(self) -> typing.Optional[typing.Union["CfnVirtualNode.AccessLogProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.LoggingProperty.AccessLog``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-logging.html#cfn-appmesh-virtualnode-logging-accesslog
            """
            return self._values.get('access_log')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoggingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.PortMappingProperty", jsii_struct_bases=[], name_mapping={'port': 'port', 'protocol': 'protocol'})
    class PortMappingProperty():
        def __init__(self, *, port: jsii.Number, protocol: str) -> None:
            """
            :param port: ``CfnVirtualNode.PortMappingProperty.Port``.
            :param protocol: ``CfnVirtualNode.PortMappingProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html
            """
            self._values = {
                'port': port,
                'protocol': protocol,
            }

        @builtins.property
        def port(self) -> jsii.Number:
            """``CfnVirtualNode.PortMappingProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html#cfn-appmesh-virtualnode-portmapping-port
            """
            return self._values.get('port')

        @builtins.property
        def protocol(self) -> str:
            """``CfnVirtualNode.PortMappingProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-portmapping.html#cfn-appmesh-virtualnode-portmapping-protocol
            """
            return self._values.get('protocol')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PortMappingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.ServiceDiscoveryProperty", jsii_struct_bases=[], name_mapping={'aws_cloud_map': 'awsCloudMap', 'dns': 'dns'})
    class ServiceDiscoveryProperty():
        def __init__(self, *, aws_cloud_map: typing.Optional[typing.Union["CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty", _IResolvable_9ceae33e]]=None, dns: typing.Optional[typing.Union["CfnVirtualNode.DnsServiceDiscoveryProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param aws_cloud_map: ``CfnVirtualNode.ServiceDiscoveryProperty.AWSCloudMap``.
            :param dns: ``CfnVirtualNode.ServiceDiscoveryProperty.DNS``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html
            """
            self._values = {
            }
            if aws_cloud_map is not None: self._values["aws_cloud_map"] = aws_cloud_map
            if dns is not None: self._values["dns"] = dns

        @builtins.property
        def aws_cloud_map(self) -> typing.Optional[typing.Union["CfnVirtualNode.AwsCloudMapServiceDiscoveryProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.ServiceDiscoveryProperty.AWSCloudMap``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html#cfn-appmesh-virtualnode-servicediscovery-awscloudmap
            """
            return self._values.get('aws_cloud_map')

        @builtins.property
        def dns(self) -> typing.Optional[typing.Union["CfnVirtualNode.DnsServiceDiscoveryProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.ServiceDiscoveryProperty.DNS``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-servicediscovery.html#cfn-appmesh-virtualnode-servicediscovery-dns
            """
            return self._values.get('dns')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ServiceDiscoveryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.TlsValidationContextAcmTrustProperty", jsii_struct_bases=[], name_mapping={'certificate_authority_arns': 'certificateAuthorityArns'})
    class TlsValidationContextAcmTrustProperty():
        def __init__(self, *, certificate_authority_arns: typing.List[str]) -> None:
            """
            :param certificate_authority_arns: ``CfnVirtualNode.TlsValidationContextAcmTrustProperty.CertificateAuthorityArns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextacmtrust.html
            """
            self._values = {
                'certificate_authority_arns': certificate_authority_arns,
            }

        @builtins.property
        def certificate_authority_arns(self) -> typing.List[str]:
            """``CfnVirtualNode.TlsValidationContextAcmTrustProperty.CertificateAuthorityArns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextacmtrust.html#cfn-appmesh-virtualnode-tlsvalidationcontextacmtrust-certificateauthorityarns
            """
            return self._values.get('certificate_authority_arns')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TlsValidationContextAcmTrustProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.TlsValidationContextFileTrustProperty", jsii_struct_bases=[], name_mapping={'certificate_chain': 'certificateChain'})
    class TlsValidationContextFileTrustProperty():
        def __init__(self, *, certificate_chain: str) -> None:
            """
            :param certificate_chain: ``CfnVirtualNode.TlsValidationContextFileTrustProperty.CertificateChain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextfiletrust.html
            """
            self._values = {
                'certificate_chain': certificate_chain,
            }

        @builtins.property
        def certificate_chain(self) -> str:
            """``CfnVirtualNode.TlsValidationContextFileTrustProperty.CertificateChain``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontextfiletrust.html#cfn-appmesh-virtualnode-tlsvalidationcontextfiletrust-certificatechain
            """
            return self._values.get('certificate_chain')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TlsValidationContextFileTrustProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.TlsValidationContextProperty", jsii_struct_bases=[], name_mapping={'trust': 'trust'})
    class TlsValidationContextProperty():
        def __init__(self, *, trust: typing.Union["CfnVirtualNode.TlsValidationContextTrustProperty", _IResolvable_9ceae33e]) -> None:
            """
            :param trust: ``CfnVirtualNode.TlsValidationContextProperty.Trust``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontext.html
            """
            self._values = {
                'trust': trust,
            }

        @builtins.property
        def trust(self) -> typing.Union["CfnVirtualNode.TlsValidationContextTrustProperty", _IResolvable_9ceae33e]:
            """``CfnVirtualNode.TlsValidationContextProperty.Trust``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontext.html#cfn-appmesh-virtualnode-tlsvalidationcontext-trust
            """
            return self._values.get('trust')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TlsValidationContextProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.TlsValidationContextTrustProperty", jsii_struct_bases=[], name_mapping={'acm': 'acm', 'file': 'file'})
    class TlsValidationContextTrustProperty():
        def __init__(self, *, acm: typing.Optional[typing.Union["CfnVirtualNode.TlsValidationContextAcmTrustProperty", _IResolvable_9ceae33e]]=None, file: typing.Optional[typing.Union["CfnVirtualNode.TlsValidationContextFileTrustProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param acm: ``CfnVirtualNode.TlsValidationContextTrustProperty.ACM``.
            :param file: ``CfnVirtualNode.TlsValidationContextTrustProperty.File``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html
            """
            self._values = {
            }
            if acm is not None: self._values["acm"] = acm
            if file is not None: self._values["file"] = file

        @builtins.property
        def acm(self) -> typing.Optional[typing.Union["CfnVirtualNode.TlsValidationContextAcmTrustProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.TlsValidationContextTrustProperty.ACM``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-tlsvalidationcontexttrust-acm
            """
            return self._values.get('acm')

        @builtins.property
        def file(self) -> typing.Optional[typing.Union["CfnVirtualNode.TlsValidationContextFileTrustProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.TlsValidationContextTrustProperty.File``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-tlsvalidationcontexttrust.html#cfn-appmesh-virtualnode-tlsvalidationcontexttrust-file
            """
            return self._values.get('file')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TlsValidationContextTrustProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.VirtualNodeSpecProperty", jsii_struct_bases=[], name_mapping={'backend_defaults': 'backendDefaults', 'backends': 'backends', 'listeners': 'listeners', 'logging': 'logging', 'service_discovery': 'serviceDiscovery'})
    class VirtualNodeSpecProperty():
        def __init__(self, *, backend_defaults: typing.Optional[typing.Union["CfnVirtualNode.BackendDefaultsProperty", _IResolvable_9ceae33e]]=None, backends: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnVirtualNode.BackendProperty", _IResolvable_9ceae33e]]]]=None, listeners: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnVirtualNode.ListenerProperty", _IResolvable_9ceae33e]]]]=None, logging: typing.Optional[typing.Union["CfnVirtualNode.LoggingProperty", _IResolvable_9ceae33e]]=None, service_discovery: typing.Optional[typing.Union["CfnVirtualNode.ServiceDiscoveryProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param backend_defaults: ``CfnVirtualNode.VirtualNodeSpecProperty.BackendDefaults``.
            :param backends: ``CfnVirtualNode.VirtualNodeSpecProperty.Backends``.
            :param listeners: ``CfnVirtualNode.VirtualNodeSpecProperty.Listeners``.
            :param logging: ``CfnVirtualNode.VirtualNodeSpecProperty.Logging``.
            :param service_discovery: ``CfnVirtualNode.VirtualNodeSpecProperty.ServiceDiscovery``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html
            """
            self._values = {
            }
            if backend_defaults is not None: self._values["backend_defaults"] = backend_defaults
            if backends is not None: self._values["backends"] = backends
            if listeners is not None: self._values["listeners"] = listeners
            if logging is not None: self._values["logging"] = logging
            if service_discovery is not None: self._values["service_discovery"] = service_discovery

        @builtins.property
        def backend_defaults(self) -> typing.Optional[typing.Union["CfnVirtualNode.BackendDefaultsProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.VirtualNodeSpecProperty.BackendDefaults``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-backenddefaults
            """
            return self._values.get('backend_defaults')

        @builtins.property
        def backends(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnVirtualNode.BackendProperty", _IResolvable_9ceae33e]]]]:
            """``CfnVirtualNode.VirtualNodeSpecProperty.Backends``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-backends
            """
            return self._values.get('backends')

        @builtins.property
        def listeners(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnVirtualNode.ListenerProperty", _IResolvable_9ceae33e]]]]:
            """``CfnVirtualNode.VirtualNodeSpecProperty.Listeners``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-listeners
            """
            return self._values.get('listeners')

        @builtins.property
        def logging(self) -> typing.Optional[typing.Union["CfnVirtualNode.LoggingProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.VirtualNodeSpecProperty.Logging``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-logging
            """
            return self._values.get('logging')

        @builtins.property
        def service_discovery(self) -> typing.Optional[typing.Union["CfnVirtualNode.ServiceDiscoveryProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.VirtualNodeSpecProperty.ServiceDiscovery``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualnodespec.html#cfn-appmesh-virtualnode-virtualnodespec-servicediscovery
            """
            return self._values.get('service_discovery')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VirtualNodeSpecProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNode.VirtualServiceBackendProperty", jsii_struct_bases=[], name_mapping={'virtual_service_name': 'virtualServiceName', 'client_policy': 'clientPolicy'})
    class VirtualServiceBackendProperty():
        def __init__(self, *, virtual_service_name: str, client_policy: typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param virtual_service_name: ``CfnVirtualNode.VirtualServiceBackendProperty.VirtualServiceName``.
            :param client_policy: ``CfnVirtualNode.VirtualServiceBackendProperty.ClientPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html
            """
            self._values = {
                'virtual_service_name': virtual_service_name,
            }
            if client_policy is not None: self._values["client_policy"] = client_policy

        @builtins.property
        def virtual_service_name(self) -> str:
            """``CfnVirtualNode.VirtualServiceBackendProperty.VirtualServiceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html#cfn-appmesh-virtualnode-virtualservicebackend-virtualservicename
            """
            return self._values.get('virtual_service_name')

        @builtins.property
        def client_policy(self) -> typing.Optional[typing.Union["CfnVirtualNode.ClientPolicyProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualNode.VirtualServiceBackendProperty.ClientPolicy``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualnode-virtualservicebackend.html#cfn-appmesh-virtualnode-virtualservicebackend-clientpolicy
            """
            return self._values.get('client_policy')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VirtualServiceBackendProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualNodeProps", jsii_struct_bases=[], name_mapping={'mesh_name': 'meshName', 'spec': 'spec', 'virtual_node_name': 'virtualNodeName', 'mesh_owner': 'meshOwner', 'tags': 'tags'})
class CfnVirtualNodeProps():
    def __init__(self, *, mesh_name: str, spec: typing.Union["CfnVirtualNode.VirtualNodeSpecProperty", _IResolvable_9ceae33e], virtual_node_name: str, mesh_owner: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::AppMesh::VirtualNode``.

        :param mesh_name: ``AWS::AppMesh::VirtualNode.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualNode.Spec``.
        :param virtual_node_name: ``AWS::AppMesh::VirtualNode.VirtualNodeName``.
        :param mesh_owner: ``AWS::AppMesh::VirtualNode.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualNode.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html
        """
        self._values = {
            'mesh_name': mesh_name,
            'spec': spec,
            'virtual_node_name': virtual_node_name,
        }
        if mesh_owner is not None: self._values["mesh_owner"] = mesh_owner
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> str:
        """``AWS::AppMesh::VirtualNode.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshname
        """
        return self._values.get('mesh_name')

    @builtins.property
    def spec(self) -> typing.Union["CfnVirtualNode.VirtualNodeSpecProperty", _IResolvable_9ceae33e]:
        """``AWS::AppMesh::VirtualNode.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-spec
        """
        return self._values.get('spec')

    @builtins.property
    def virtual_node_name(self) -> str:
        """``AWS::AppMesh::VirtualNode.VirtualNodeName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-virtualnodename
        """
        return self._values.get('virtual_node_name')

    @builtins.property
    def mesh_owner(self) -> typing.Optional[str]:
        """``AWS::AppMesh::VirtualNode.MeshOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-meshowner
        """
        return self._values.get('mesh_owner')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::AppMesh::VirtualNode.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html#cfn-appmesh-virtualnode-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnVirtualNodeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnVirtualRouter(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualRouter"):
    """A CloudFormation ``AWS::AppMesh::VirtualRouter``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppMesh::VirtualRouter
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh_name: str, spec: typing.Union["VirtualRouterSpecProperty", _IResolvable_9ceae33e], virtual_router_name: str, mesh_owner: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::AppMesh::VirtualRouter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::VirtualRouter.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualRouter.Spec``.
        :param virtual_router_name: ``AWS::AppMesh::VirtualRouter.VirtualRouterName``.
        :param mesh_owner: ``AWS::AppMesh::VirtualRouter.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualRouter.Tags``.
        """
        props = CfnVirtualRouterProps(mesh_name=mesh_name, spec=spec, virtual_router_name=virtual_router_name, mesh_owner=mesh_owner, tags=tags)

        jsii.create(CfnVirtualRouter, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnVirtualRouter":
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
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshName
        """
        return jsii.get(self, "attrMeshName")

    @builtins.property
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshOwner
        """
        return jsii.get(self, "attrMeshOwner")

    @builtins.property
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ResourceOwner
        """
        return jsii.get(self, "attrResourceOwner")

    @builtins.property
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Uid
        """
        return jsii.get(self, "attrUid")

    @builtins.property
    @jsii.member(jsii_name="attrVirtualRouterName")
    def attr_virtual_router_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: VirtualRouterName
        """
        return jsii.get(self, "attrVirtualRouterName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::AppMesh::VirtualRouter.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """``AWS::AppMesh::VirtualRouter.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshname
        """
        return jsii.get(self, "meshName")

    @mesh_name.setter
    def mesh_name(self, value: str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> typing.Union["VirtualRouterSpecProperty", _IResolvable_9ceae33e]:
        """``AWS::AppMesh::VirtualRouter.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-spec
        """
        return jsii.get(self, "spec")

    @spec.setter
    def spec(self, value: typing.Union["VirtualRouterSpecProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "spec", value)

    @builtins.property
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> str:
        """``AWS::AppMesh::VirtualRouter.VirtualRouterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-virtualroutername
        """
        return jsii.get(self, "virtualRouterName")

    @virtual_router_name.setter
    def virtual_router_name(self, value: str) -> None:
        jsii.set(self, "virtualRouterName", value)

    @builtins.property
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[str]:
        """``AWS::AppMesh::VirtualRouter.MeshOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshowner
        """
        return jsii.get(self, "meshOwner")

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "meshOwner", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualRouter.PortMappingProperty", jsii_struct_bases=[], name_mapping={'port': 'port', 'protocol': 'protocol'})
    class PortMappingProperty():
        def __init__(self, *, port: jsii.Number, protocol: str) -> None:
            """
            :param port: ``CfnVirtualRouter.PortMappingProperty.Port``.
            :param protocol: ``CfnVirtualRouter.PortMappingProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html
            """
            self._values = {
                'port': port,
                'protocol': protocol,
            }

        @builtins.property
        def port(self) -> jsii.Number:
            """``CfnVirtualRouter.PortMappingProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html#cfn-appmesh-virtualrouter-portmapping-port
            """
            return self._values.get('port')

        @builtins.property
        def protocol(self) -> str:
            """``CfnVirtualRouter.PortMappingProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-portmapping.html#cfn-appmesh-virtualrouter-portmapping-protocol
            """
            return self._values.get('protocol')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PortMappingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualRouter.VirtualRouterListenerProperty", jsii_struct_bases=[], name_mapping={'port_mapping': 'portMapping'})
    class VirtualRouterListenerProperty():
        def __init__(self, *, port_mapping: typing.Union["CfnVirtualRouter.PortMappingProperty", _IResolvable_9ceae33e]) -> None:
            """
            :param port_mapping: ``CfnVirtualRouter.VirtualRouterListenerProperty.PortMapping``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterlistener.html
            """
            self._values = {
                'port_mapping': port_mapping,
            }

        @builtins.property
        def port_mapping(self) -> typing.Union["CfnVirtualRouter.PortMappingProperty", _IResolvable_9ceae33e]:
            """``CfnVirtualRouter.VirtualRouterListenerProperty.PortMapping``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterlistener.html#cfn-appmesh-virtualrouter-virtualrouterlistener-portmapping
            """
            return self._values.get('port_mapping')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VirtualRouterListenerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualRouter.VirtualRouterSpecProperty", jsii_struct_bases=[], name_mapping={'listeners': 'listeners'})
    class VirtualRouterSpecProperty():
        def __init__(self, *, listeners: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnVirtualRouter.VirtualRouterListenerProperty", _IResolvable_9ceae33e]]]) -> None:
            """
            :param listeners: ``CfnVirtualRouter.VirtualRouterSpecProperty.Listeners``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterspec.html
            """
            self._values = {
                'listeners': listeners,
            }

        @builtins.property
        def listeners(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnVirtualRouter.VirtualRouterListenerProperty", _IResolvable_9ceae33e]]]:
            """``CfnVirtualRouter.VirtualRouterSpecProperty.Listeners``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualrouter-virtualrouterspec.html#cfn-appmesh-virtualrouter-virtualrouterspec-listeners
            """
            return self._values.get('listeners')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VirtualRouterSpecProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualRouterProps", jsii_struct_bases=[], name_mapping={'mesh_name': 'meshName', 'spec': 'spec', 'virtual_router_name': 'virtualRouterName', 'mesh_owner': 'meshOwner', 'tags': 'tags'})
class CfnVirtualRouterProps():
    def __init__(self, *, mesh_name: str, spec: typing.Union["CfnVirtualRouter.VirtualRouterSpecProperty", _IResolvable_9ceae33e], virtual_router_name: str, mesh_owner: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::AppMesh::VirtualRouter``.

        :param mesh_name: ``AWS::AppMesh::VirtualRouter.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualRouter.Spec``.
        :param virtual_router_name: ``AWS::AppMesh::VirtualRouter.VirtualRouterName``.
        :param mesh_owner: ``AWS::AppMesh::VirtualRouter.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualRouter.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html
        """
        self._values = {
            'mesh_name': mesh_name,
            'spec': spec,
            'virtual_router_name': virtual_router_name,
        }
        if mesh_owner is not None: self._values["mesh_owner"] = mesh_owner
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> str:
        """``AWS::AppMesh::VirtualRouter.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshname
        """
        return self._values.get('mesh_name')

    @builtins.property
    def spec(self) -> typing.Union["CfnVirtualRouter.VirtualRouterSpecProperty", _IResolvable_9ceae33e]:
        """``AWS::AppMesh::VirtualRouter.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-spec
        """
        return self._values.get('spec')

    @builtins.property
    def virtual_router_name(self) -> str:
        """``AWS::AppMesh::VirtualRouter.VirtualRouterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-virtualroutername
        """
        return self._values.get('virtual_router_name')

    @builtins.property
    def mesh_owner(self) -> typing.Optional[str]:
        """``AWS::AppMesh::VirtualRouter.MeshOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-meshowner
        """
        return self._values.get('mesh_owner')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::AppMesh::VirtualRouter.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html#cfn-appmesh-virtualrouter-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnVirtualRouterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnVirtualService(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualService"):
    """A CloudFormation ``AWS::AppMesh::VirtualService``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppMesh::VirtualService
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh_name: str, spec: typing.Union["VirtualServiceSpecProperty", _IResolvable_9ceae33e], virtual_service_name: str, mesh_owner: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::AppMesh::VirtualService``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param mesh_name: ``AWS::AppMesh::VirtualService.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualService.Spec``.
        :param virtual_service_name: ``AWS::AppMesh::VirtualService.VirtualServiceName``.
        :param mesh_owner: ``AWS::AppMesh::VirtualService.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualService.Tags``.
        """
        props = CfnVirtualServiceProps(mesh_name=mesh_name, spec=spec, virtual_service_name=virtual_service_name, mesh_owner=mesh_owner, tags=tags)

        jsii.create(CfnVirtualService, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnVirtualService":
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
    @jsii.member(jsii_name="attrMeshName")
    def attr_mesh_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshName
        """
        return jsii.get(self, "attrMeshName")

    @builtins.property
    @jsii.member(jsii_name="attrMeshOwner")
    def attr_mesh_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: MeshOwner
        """
        return jsii.get(self, "attrMeshOwner")

    @builtins.property
    @jsii.member(jsii_name="attrResourceOwner")
    def attr_resource_owner(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ResourceOwner
        """
        return jsii.get(self, "attrResourceOwner")

    @builtins.property
    @jsii.member(jsii_name="attrUid")
    def attr_uid(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Uid
        """
        return jsii.get(self, "attrUid")

    @builtins.property
    @jsii.member(jsii_name="attrVirtualServiceName")
    def attr_virtual_service_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: VirtualServiceName
        """
        return jsii.get(self, "attrVirtualServiceName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::AppMesh::VirtualService.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """``AWS::AppMesh::VirtualService.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshname
        """
        return jsii.get(self, "meshName")

    @mesh_name.setter
    def mesh_name(self, value: str) -> None:
        jsii.set(self, "meshName", value)

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> typing.Union["VirtualServiceSpecProperty", _IResolvable_9ceae33e]:
        """``AWS::AppMesh::VirtualService.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-spec
        """
        return jsii.get(self, "spec")

    @spec.setter
    def spec(self, value: typing.Union["VirtualServiceSpecProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "spec", value)

    @builtins.property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> str:
        """``AWS::AppMesh::VirtualService.VirtualServiceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-virtualservicename
        """
        return jsii.get(self, "virtualServiceName")

    @virtual_service_name.setter
    def virtual_service_name(self, value: str) -> None:
        jsii.set(self, "virtualServiceName", value)

    @builtins.property
    @jsii.member(jsii_name="meshOwner")
    def mesh_owner(self) -> typing.Optional[str]:
        """``AWS::AppMesh::VirtualService.MeshOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshowner
        """
        return jsii.get(self, "meshOwner")

    @mesh_owner.setter
    def mesh_owner(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "meshOwner", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualService.VirtualNodeServiceProviderProperty", jsii_struct_bases=[], name_mapping={'virtual_node_name': 'virtualNodeName'})
    class VirtualNodeServiceProviderProperty():
        def __init__(self, *, virtual_node_name: str) -> None:
            """
            :param virtual_node_name: ``CfnVirtualService.VirtualNodeServiceProviderProperty.VirtualNodeName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualnodeserviceprovider.html
            """
            self._values = {
                'virtual_node_name': virtual_node_name,
            }

        @builtins.property
        def virtual_node_name(self) -> str:
            """``CfnVirtualService.VirtualNodeServiceProviderProperty.VirtualNodeName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualnodeserviceprovider.html#cfn-appmesh-virtualservice-virtualnodeserviceprovider-virtualnodename
            """
            return self._values.get('virtual_node_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VirtualNodeServiceProviderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualService.VirtualRouterServiceProviderProperty", jsii_struct_bases=[], name_mapping={'virtual_router_name': 'virtualRouterName'})
    class VirtualRouterServiceProviderProperty():
        def __init__(self, *, virtual_router_name: str) -> None:
            """
            :param virtual_router_name: ``CfnVirtualService.VirtualRouterServiceProviderProperty.VirtualRouterName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualrouterserviceprovider.html
            """
            self._values = {
                'virtual_router_name': virtual_router_name,
            }

        @builtins.property
        def virtual_router_name(self) -> str:
            """``CfnVirtualService.VirtualRouterServiceProviderProperty.VirtualRouterName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualrouterserviceprovider.html#cfn-appmesh-virtualservice-virtualrouterserviceprovider-virtualroutername
            """
            return self._values.get('virtual_router_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VirtualRouterServiceProviderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualService.VirtualServiceProviderProperty", jsii_struct_bases=[], name_mapping={'virtual_node': 'virtualNode', 'virtual_router': 'virtualRouter'})
    class VirtualServiceProviderProperty():
        def __init__(self, *, virtual_node: typing.Optional[typing.Union["CfnVirtualService.VirtualNodeServiceProviderProperty", _IResolvable_9ceae33e]]=None, virtual_router: typing.Optional[typing.Union["CfnVirtualService.VirtualRouterServiceProviderProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param virtual_node: ``CfnVirtualService.VirtualServiceProviderProperty.VirtualNode``.
            :param virtual_router: ``CfnVirtualService.VirtualServiceProviderProperty.VirtualRouter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html
            """
            self._values = {
            }
            if virtual_node is not None: self._values["virtual_node"] = virtual_node
            if virtual_router is not None: self._values["virtual_router"] = virtual_router

        @builtins.property
        def virtual_node(self) -> typing.Optional[typing.Union["CfnVirtualService.VirtualNodeServiceProviderProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualService.VirtualServiceProviderProperty.VirtualNode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html#cfn-appmesh-virtualservice-virtualserviceprovider-virtualnode
            """
            return self._values.get('virtual_node')

        @builtins.property
        def virtual_router(self) -> typing.Optional[typing.Union["CfnVirtualService.VirtualRouterServiceProviderProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualService.VirtualServiceProviderProperty.VirtualRouter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualserviceprovider.html#cfn-appmesh-virtualservice-virtualserviceprovider-virtualrouter
            """
            return self._values.get('virtual_router')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VirtualServiceProviderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualService.VirtualServiceSpecProperty", jsii_struct_bases=[], name_mapping={'provider': 'provider'})
    class VirtualServiceSpecProperty():
        def __init__(self, *, provider: typing.Optional[typing.Union["CfnVirtualService.VirtualServiceProviderProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param provider: ``CfnVirtualService.VirtualServiceSpecProperty.Provider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualservicespec.html
            """
            self._values = {
            }
            if provider is not None: self._values["provider"] = provider

        @builtins.property
        def provider(self) -> typing.Optional[typing.Union["CfnVirtualService.VirtualServiceProviderProperty", _IResolvable_9ceae33e]]:
            """``CfnVirtualService.VirtualServiceSpecProperty.Provider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-virtualservice-virtualservicespec.html#cfn-appmesh-virtualservice-virtualservicespec-provider
            """
            return self._values.get('provider')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VirtualServiceSpecProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.CfnVirtualServiceProps", jsii_struct_bases=[], name_mapping={'mesh_name': 'meshName', 'spec': 'spec', 'virtual_service_name': 'virtualServiceName', 'mesh_owner': 'meshOwner', 'tags': 'tags'})
class CfnVirtualServiceProps():
    def __init__(self, *, mesh_name: str, spec: typing.Union["CfnVirtualService.VirtualServiceSpecProperty", _IResolvable_9ceae33e], virtual_service_name: str, mesh_owner: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::AppMesh::VirtualService``.

        :param mesh_name: ``AWS::AppMesh::VirtualService.MeshName``.
        :param spec: ``AWS::AppMesh::VirtualService.Spec``.
        :param virtual_service_name: ``AWS::AppMesh::VirtualService.VirtualServiceName``.
        :param mesh_owner: ``AWS::AppMesh::VirtualService.MeshOwner``.
        :param tags: ``AWS::AppMesh::VirtualService.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html
        """
        self._values = {
            'mesh_name': mesh_name,
            'spec': spec,
            'virtual_service_name': virtual_service_name,
        }
        if mesh_owner is not None: self._values["mesh_owner"] = mesh_owner
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def mesh_name(self) -> str:
        """``AWS::AppMesh::VirtualService.MeshName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshname
        """
        return self._values.get('mesh_name')

    @builtins.property
    def spec(self) -> typing.Union["CfnVirtualService.VirtualServiceSpecProperty", _IResolvable_9ceae33e]:
        """``AWS::AppMesh::VirtualService.Spec``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-spec
        """
        return self._values.get('spec')

    @builtins.property
    def virtual_service_name(self) -> str:
        """``AWS::AppMesh::VirtualService.VirtualServiceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-virtualservicename
        """
        return self._values.get('virtual_service_name')

    @builtins.property
    def mesh_owner(self) -> typing.Optional[str]:
        """``AWS::AppMesh::VirtualService.MeshOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-meshowner
        """
        return self._values.get('mesh_owner')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::AppMesh::VirtualService.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html#cfn-appmesh-virtualservice-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnVirtualServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.HealthCheck", jsii_struct_bases=[], name_mapping={'healthy_threshold': 'healthyThreshold', 'interval': 'interval', 'path': 'path', 'port': 'port', 'protocol': 'protocol', 'timeout': 'timeout', 'unhealthy_threshold': 'unhealthyThreshold'})
class HealthCheck():
    def __init__(self, *, healthy_threshold: typing.Optional[jsii.Number]=None, interval: typing.Optional[_Duration_5170c158]=None, path: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None, timeout: typing.Optional[_Duration_5170c158]=None, unhealthy_threshold: typing.Optional[jsii.Number]=None) -> None:
        """Properties used to define healthchecks when creating virtual nodes.

        All values have a default if only specified as {} when creating.
        If property not set, then no healthchecks will be defined.

        :param healthy_threshold: Number of successful attempts before considering the node UP. Default: 2
        :param interval: Interval in milliseconds to re-check. Default: 5 seconds
        :param path: The path where the application expects any health-checks, this can also be the application path. Default: /
        :param port: The TCP port number for the healthcheck. Default: - same as corresponding port mapping
        :param protocol: The protocol to use for the healthcheck, for convinience a const enum has been defined. Protocol.HTTP or Protocol.TCP Default: - same as corresponding port mapping
        :param timeout: Timeout in milli-seconds for the healthcheck to be considered a fail. Default: 2 seconds
        :param unhealthy_threshold: Number of failed attempts before considering the node DOWN. Default: 2

        stability
        :stability: experimental
        """
        self._values = {
        }
        if healthy_threshold is not None: self._values["healthy_threshold"] = healthy_threshold
        if interval is not None: self._values["interval"] = interval
        if path is not None: self._values["path"] = path
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol
        if timeout is not None: self._values["timeout"] = timeout
        if unhealthy_threshold is not None: self._values["unhealthy_threshold"] = unhealthy_threshold

    @builtins.property
    def healthy_threshold(self) -> typing.Optional[jsii.Number]:
        """Number of successful attempts before considering the node UP.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('healthy_threshold')

    @builtins.property
    def interval(self) -> typing.Optional[_Duration_5170c158]:
        """Interval in milliseconds to re-check.

        default
        :default: 5 seconds

        stability
        :stability: experimental
        """
        return self._values.get('interval')

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """The path where the application expects any health-checks, this can also be the application path.

        default
        :default: /

        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The TCP port number for the healthcheck.

        default
        :default: - same as corresponding port mapping

        stability
        :stability: experimental
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol to use for the healthcheck, for convinience a const enum has been defined.

        Protocol.HTTP or Protocol.TCP

        default
        :default: - same as corresponding port mapping

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Timeout in milli-seconds for the healthcheck to be considered a fail.

        default
        :default: 2 seconds

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
        """Number of failed attempts before considering the node DOWN.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('unhealthy_threshold')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HealthCheck(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_appmesh.IMesh")
class IMesh(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Interface wich all Mesh based classes MUST implement.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IMeshProxy

    @builtins.property
    @jsii.member(jsii_name="meshArn")
    def mesh_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the AppMesh mesh.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """The name of the AppMesh mesh.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addVirtualNode")
    def add_virtual_node(self, id: str, *, backends: typing.Optional[typing.List["IVirtualService"]]=None, cloud_map_service: typing.Optional[_IService_f28ba3c9]=None, cloud_map_service_instance_attributes: typing.Optional[typing.Mapping[str, str]]=None, dns_host_name: typing.Optional[str]=None, listener: typing.Optional["VirtualNodeListener"]=None, virtual_node_name: typing.Optional[str]=None) -> "VirtualNode":
        """Adds a VirtualNode to the Mesh.

        :param id: -
        :param backends: Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param cloud_map_service: CloudMap service where Virtual Node members register themselves. Instances registering themselves into this CloudMap will be considered part of the Virtual Node. Default: - Don't use CloudMap-based service discovery
        :param cloud_map_service_instance_attributes: Filter down the list of CloudMap service instance. Default: - No CloudMap instance filter
        :param dns_host_name: Host name of DNS record used to discover Virtual Node members. The IP addresses returned by querying this DNS record will be considered part of the Virtual Node. Default: - Don't use DNS-based service discovery
        :param listener: Initial listener for the virtual node. Default: - No listeners
        :param virtual_node_name: The name of the VirtualNode. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addVirtualRouter")
    def add_virtual_router(self, id: str, *, listener: typing.Optional["Listener"]=None, virtual_router_name: typing.Optional[str]=None) -> "VirtualRouter":
        """Adds a VirtualRouter to the Mesh with the given id and props.

        :param id: -
        :param listener: Listener specification for the virtual router. Default: - A listener on HTTP port 8080
        :param virtual_router_name: The name of the VirtualRouter. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addVirtualService")
    def add_virtual_service(self, id: str, *, virtual_node: typing.Optional["IVirtualNode"]=None, virtual_router: typing.Optional["IVirtualRouter"]=None, virtual_service_name: typing.Optional[str]=None) -> "VirtualService":
        """Adds a VirtualService with the given id.

        :param id: -
        :param virtual_node: The VirtualNode attached to the virtual service. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_router: The VirtualRouter which the VirtualService uses as provider. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_service_name: The name of the VirtualService. It is recommended this follows the fully-qualified domain name format, such as "my-service.default.svc.cluster.local". Default: - A name is automatically generated

        stability
        :stability: experimental
        """
        ...


class _IMeshProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Interface wich all Mesh based classes MUST implement.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_appmesh.IMesh"
    @builtins.property
    @jsii.member(jsii_name="meshArn")
    def mesh_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the AppMesh mesh.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "meshArn")

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """The name of the AppMesh mesh.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "meshName")

    @jsii.member(jsii_name="addVirtualNode")
    def add_virtual_node(self, id: str, *, backends: typing.Optional[typing.List["IVirtualService"]]=None, cloud_map_service: typing.Optional[_IService_f28ba3c9]=None, cloud_map_service_instance_attributes: typing.Optional[typing.Mapping[str, str]]=None, dns_host_name: typing.Optional[str]=None, listener: typing.Optional["VirtualNodeListener"]=None, virtual_node_name: typing.Optional[str]=None) -> "VirtualNode":
        """Adds a VirtualNode to the Mesh.

        :param id: -
        :param backends: Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param cloud_map_service: CloudMap service where Virtual Node members register themselves. Instances registering themselves into this CloudMap will be considered part of the Virtual Node. Default: - Don't use CloudMap-based service discovery
        :param cloud_map_service_instance_attributes: Filter down the list of CloudMap service instance. Default: - No CloudMap instance filter
        :param dns_host_name: Host name of DNS record used to discover Virtual Node members. The IP addresses returned by querying this DNS record will be considered part of the Virtual Node. Default: - Don't use DNS-based service discovery
        :param listener: Initial listener for the virtual node. Default: - No listeners
        :param virtual_node_name: The name of the VirtualNode. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        props = VirtualNodeBaseProps(backends=backends, cloud_map_service=cloud_map_service, cloud_map_service_instance_attributes=cloud_map_service_instance_attributes, dns_host_name=dns_host_name, listener=listener, virtual_node_name=virtual_node_name)

        return jsii.invoke(self, "addVirtualNode", [id, props])

    @jsii.member(jsii_name="addVirtualRouter")
    def add_virtual_router(self, id: str, *, listener: typing.Optional["Listener"]=None, virtual_router_name: typing.Optional[str]=None) -> "VirtualRouter":
        """Adds a VirtualRouter to the Mesh with the given id and props.

        :param id: -
        :param listener: Listener specification for the virtual router. Default: - A listener on HTTP port 8080
        :param virtual_router_name: The name of the VirtualRouter. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        props = VirtualRouterBaseProps(listener=listener, virtual_router_name=virtual_router_name)

        return jsii.invoke(self, "addVirtualRouter", [id, props])

    @jsii.member(jsii_name="addVirtualService")
    def add_virtual_service(self, id: str, *, virtual_node: typing.Optional["IVirtualNode"]=None, virtual_router: typing.Optional["IVirtualRouter"]=None, virtual_service_name: typing.Optional[str]=None) -> "VirtualService":
        """Adds a VirtualService with the given id.

        :param id: -
        :param virtual_node: The VirtualNode attached to the virtual service. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_router: The VirtualRouter which the VirtualService uses as provider. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_service_name: The name of the VirtualService. It is recommended this follows the fully-qualified domain name format, such as "my-service.default.svc.cluster.local". Default: - A name is automatically generated

        stability
        :stability: experimental
        """
        props = VirtualServiceBaseProps(virtual_node=virtual_node, virtual_router=virtual_router, virtual_service_name=virtual_service_name)

        return jsii.invoke(self, "addVirtualService", [id, props])


@jsii.interface(jsii_type="monocdk-experiment.aws_appmesh.IRoute")
class IRoute(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Interface for which all Route based classes MUST implement.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRouteProxy

    @builtins.property
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the route.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> str:
        """The name of the route.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IRouteProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Interface for which all Route based classes MUST implement.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_appmesh.IRoute"
    @builtins.property
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the route.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "routeArn")

    @builtins.property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> str:
        """The name of the route.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "routeName")


@jsii.interface(jsii_type="monocdk-experiment.aws_appmesh.IVirtualNode")
class IVirtualNode(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Interface which all VirtualNode based classes must implement.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IVirtualNodeProxy

    @builtins.property
    @jsii.member(jsii_name="virtualNodeArn")
    def virtual_node_arn(self) -> str:
        """The Amazon Resource Name belonging to the VirtualNdoe.

        Set this value as the APPMESH_VIRTUAL_NODE_NAME environment variable for
        your task group's Envoy proxy container in your task definition or pod
        spec.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> str:
        """The name of the VirtualNode.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addBackends")
    def add_backends(self, *props: "IVirtualService") -> None:
        """Utility method to add backends for existing or new VirtualNodes.

        :param props: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addListeners")
    def add_listeners(self, *listeners: "VirtualNodeListener") -> None:
        """Utility method to add Node Listeners for new or existing VirtualNodes.

        :param listeners: -

        stability
        :stability: experimental
        """
        ...


class _IVirtualNodeProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Interface which all VirtualNode based classes must implement.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_appmesh.IVirtualNode"
    @builtins.property
    @jsii.member(jsii_name="virtualNodeArn")
    def virtual_node_arn(self) -> str:
        """The Amazon Resource Name belonging to the VirtualNdoe.

        Set this value as the APPMESH_VIRTUAL_NODE_NAME environment variable for
        your task group's Envoy proxy container in your task definition or pod
        spec.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "virtualNodeArn")

    @builtins.property
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> str:
        """The name of the VirtualNode.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "virtualNodeName")

    @jsii.member(jsii_name="addBackends")
    def add_backends(self, *props: "IVirtualService") -> None:
        """Utility method to add backends for existing or new VirtualNodes.

        :param props: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addBackends", [*props])

    @jsii.member(jsii_name="addListeners")
    def add_listeners(self, *listeners: "VirtualNodeListener") -> None:
        """Utility method to add Node Listeners for new or existing VirtualNodes.

        :param listeners: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addListeners", [*listeners])


@jsii.interface(jsii_type="monocdk-experiment.aws_appmesh.IVirtualRouter")
class IVirtualRouter(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Interface which all VirtualRouter based classes MUST implement.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IVirtualRouterProxy

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> "IMesh":
        """The  service mesh that the virtual router resides in.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="virtualRouterArn")
    def virtual_router_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the VirtualRouter.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> str:
        """The name of the VirtualRouter.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addRoute")
    def add_route(self, id: str, *, route_targets: typing.List["WeightedTargetProps"], prefix: typing.Optional[str]=None, route_name: typing.Optional[str]=None, route_type: typing.Optional["RouteType"]=None) -> "Route":
        """Add a single route to the router.

        :param id: -
        :param route_targets: Array of weighted route targets.
        :param prefix: The path prefix to match for the route. Default: "/" if http otherwise none
        :param route_name: The name of the route. Default: - An automatically generated name
        :param route_type: Weather the route is HTTP based. Default: - HTTP if ``prefix`` is given, TCP otherwise

        stability
        :stability: experimental
        """
        ...


class _IVirtualRouterProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Interface which all VirtualRouter based classes MUST implement.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_appmesh.IVirtualRouter"
    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> "IMesh":
        """The  service mesh that the virtual router resides in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "mesh")

    @builtins.property
    @jsii.member(jsii_name="virtualRouterArn")
    def virtual_router_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the VirtualRouter.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "virtualRouterArn")

    @builtins.property
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> str:
        """The name of the VirtualRouter.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "virtualRouterName")

    @jsii.member(jsii_name="addRoute")
    def add_route(self, id: str, *, route_targets: typing.List["WeightedTargetProps"], prefix: typing.Optional[str]=None, route_name: typing.Optional[str]=None, route_type: typing.Optional["RouteType"]=None) -> "Route":
        """Add a single route to the router.

        :param id: -
        :param route_targets: Array of weighted route targets.
        :param prefix: The path prefix to match for the route. Default: "/" if http otherwise none
        :param route_name: The name of the route. Default: - An automatically generated name
        :param route_type: Weather the route is HTTP based. Default: - HTTP if ``prefix`` is given, TCP otherwise

        stability
        :stability: experimental
        """
        props = RouteBaseProps(route_targets=route_targets, prefix=prefix, route_name=route_name, route_type=route_type)

        return jsii.invoke(self, "addRoute", [id, props])


@jsii.interface(jsii_type="monocdk-experiment.aws_appmesh.IVirtualService")
class IVirtualService(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Represents the interface which all VirtualService based classes MUST implement.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IVirtualServiceProxy

    @builtins.property
    @jsii.member(jsii_name="virtualServiceArn")
    def virtual_service_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the virtual service.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> str:
        """The name of the VirtualService.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IVirtualServiceProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Represents the interface which all VirtualService based classes MUST implement.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_appmesh.IVirtualService"
    @builtins.property
    @jsii.member(jsii_name="virtualServiceArn")
    def virtual_service_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the virtual service.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "virtualServiceArn")

    @builtins.property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> str:
        """The name of the VirtualService.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "virtualServiceName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.Listener", jsii_struct_bases=[], name_mapping={'port_mapping': 'portMapping'})
class Listener():
    def __init__(self, *, port_mapping: "PortMapping") -> None:
        """A single listener for.

        :param port_mapping: Listener port for the virtual router.

        stability
        :stability: experimental
        """
        if isinstance(port_mapping, dict): port_mapping = PortMapping(**port_mapping)
        self._values = {
            'port_mapping': port_mapping,
        }

    @builtins.property
    def port_mapping(self) -> "PortMapping":
        """Listener port for the virtual router.

        stability
        :stability: experimental
        """
        return self._values.get('port_mapping')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Listener(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IMesh)
class Mesh(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.Mesh"):
    """Define a new AppMesh mesh.

    see
    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/meshes.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, egress_filter: typing.Optional["MeshFilterType"]=None, mesh_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param egress_filter: Egress filter to be applied to the Mesh. Default: DROP_ALL
        :param mesh_name: The name of the Mesh being defined. Default: - A name is autmoatically generated

        stability
        :stability: experimental
        """
        props = MeshProps(egress_filter=egress_filter, mesh_name=mesh_name)

        jsii.create(Mesh, self, [scope, id, props])

    @jsii.member(jsii_name="fromMeshArn")
    @builtins.classmethod
    def from_mesh_arn(cls, scope: _Construct_f50a3f53, id: str, mesh_arn: str) -> "IMesh":
        """Import an existing mesh by arn.

        :param scope: -
        :param id: -
        :param mesh_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromMeshArn", [scope, id, mesh_arn])

    @jsii.member(jsii_name="fromMeshName")
    @builtins.classmethod
    def from_mesh_name(cls, scope: _Construct_f50a3f53, id: str, mesh_name: str) -> "IMesh":
        """Import an existing mesh by name.

        :param scope: -
        :param id: -
        :param mesh_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromMeshName", [scope, id, mesh_name])

    @jsii.member(jsii_name="addVirtualNode")
    def add_virtual_node(self, id: str, *, backends: typing.Optional[typing.List["IVirtualService"]]=None, cloud_map_service: typing.Optional[_IService_f28ba3c9]=None, cloud_map_service_instance_attributes: typing.Optional[typing.Mapping[str, str]]=None, dns_host_name: typing.Optional[str]=None, listener: typing.Optional["VirtualNodeListener"]=None, virtual_node_name: typing.Optional[str]=None) -> "VirtualNode":
        """Adds a VirtualNode to the Mesh.

        :param id: -
        :param backends: Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param cloud_map_service: CloudMap service where Virtual Node members register themselves. Instances registering themselves into this CloudMap will be considered part of the Virtual Node. Default: - Don't use CloudMap-based service discovery
        :param cloud_map_service_instance_attributes: Filter down the list of CloudMap service instance. Default: - No CloudMap instance filter
        :param dns_host_name: Host name of DNS record used to discover Virtual Node members. The IP addresses returned by querying this DNS record will be considered part of the Virtual Node. Default: - Don't use DNS-based service discovery
        :param listener: Initial listener for the virtual node. Default: - No listeners
        :param virtual_node_name: The name of the VirtualNode. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        props = VirtualNodeBaseProps(backends=backends, cloud_map_service=cloud_map_service, cloud_map_service_instance_attributes=cloud_map_service_instance_attributes, dns_host_name=dns_host_name, listener=listener, virtual_node_name=virtual_node_name)

        return jsii.invoke(self, "addVirtualNode", [id, props])

    @jsii.member(jsii_name="addVirtualRouter")
    def add_virtual_router(self, id: str, *, listener: typing.Optional["Listener"]=None, virtual_router_name: typing.Optional[str]=None) -> "VirtualRouter":
        """Adds a VirtualRouter to the Mesh with the given id and props.

        :param id: -
        :param listener: Listener specification for the virtual router. Default: - A listener on HTTP port 8080
        :param virtual_router_name: The name of the VirtualRouter. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        props = VirtualRouterBaseProps(listener=listener, virtual_router_name=virtual_router_name)

        return jsii.invoke(self, "addVirtualRouter", [id, props])

    @jsii.member(jsii_name="addVirtualService")
    def add_virtual_service(self, id: str, *, virtual_node: typing.Optional["IVirtualNode"]=None, virtual_router: typing.Optional["IVirtualRouter"]=None, virtual_service_name: typing.Optional[str]=None) -> "VirtualService":
        """Adds a VirtualService with the given id.

        :param id: -
        :param virtual_node: The VirtualNode attached to the virtual service. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_router: The VirtualRouter which the VirtualService uses as provider. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_service_name: The name of the VirtualService. It is recommended this follows the fully-qualified domain name format, such as "my-service.default.svc.cluster.local". Default: - A name is automatically generated

        stability
        :stability: experimental
        """
        props = VirtualServiceBaseProps(virtual_node=virtual_node, virtual_router=virtual_router, virtual_service_name=virtual_service_name)

        return jsii.invoke(self, "addVirtualService", [id, props])

    @builtins.property
    @jsii.member(jsii_name="meshArn")
    def mesh_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the AppMesh mesh.

        stability
        :stability: experimental
        """
        return jsii.get(self, "meshArn")

    @builtins.property
    @jsii.member(jsii_name="meshName")
    def mesh_name(self) -> str:
        """The name of the AppMesh mesh.

        stability
        :stability: experimental
        """
        return jsii.get(self, "meshName")


@jsii.enum(jsii_type="monocdk-experiment.aws_appmesh.MeshFilterType")
class MeshFilterType(enum.Enum):
    """A utility enum defined for the egressFilter type property, the default of DROP_ALL, allows traffic only to other resources inside the mesh, or API calls to amazon resources.

    default
    :default: DROP_ALL

    stability
    :stability: experimental
    """
    ALLOW_ALL = "ALLOW_ALL"
    """Allows all outbound traffic.

    stability
    :stability: experimental
    """
    DROP_ALL = "DROP_ALL"
    """Allows traffic only to other resources inside the mesh, or API calls to amazon resources.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.MeshProps", jsii_struct_bases=[], name_mapping={'egress_filter': 'egressFilter', 'mesh_name': 'meshName'})
class MeshProps():
    def __init__(self, *, egress_filter: typing.Optional["MeshFilterType"]=None, mesh_name: typing.Optional[str]=None) -> None:
        """The set of properties used when creating a Mesh.

        :param egress_filter: Egress filter to be applied to the Mesh. Default: DROP_ALL
        :param mesh_name: The name of the Mesh being defined. Default: - A name is autmoatically generated

        stability
        :stability: experimental
        """
        self._values = {
        }
        if egress_filter is not None: self._values["egress_filter"] = egress_filter
        if mesh_name is not None: self._values["mesh_name"] = mesh_name

    @builtins.property
    def egress_filter(self) -> typing.Optional["MeshFilterType"]:
        """Egress filter to be applied to the Mesh.

        default
        :default: DROP_ALL

        stability
        :stability: experimental
        """
        return self._values.get('egress_filter')

    @builtins.property
    def mesh_name(self) -> typing.Optional[str]:
        """The name of the Mesh being defined.

        default
        :default: - A name is autmoatically generated

        stability
        :stability: experimental
        """
        return self._values.get('mesh_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MeshProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.PortMapping", jsii_struct_bases=[], name_mapping={'port': 'port', 'protocol': 'protocol'})
class PortMapping():
    def __init__(self, *, port: jsii.Number, protocol: "Protocol") -> None:
        """Port mappings for resources that require these attributes, such as VirtualNodes and Routes.

        :param port: Port mapped to the VirtualNode / Route. Default: 8080
        :param protocol: Protocol for the VirtualNode / Route, only TCP or HTTP supported. Default: HTTP

        stability
        :stability: experimental
        """
        self._values = {
            'port': port,
            'protocol': protocol,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        """Port mapped to the VirtualNode / Route.

        default
        :default: 8080

        stability
        :stability: experimental
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> "Protocol":
        """Protocol for the VirtualNode / Route, only TCP or HTTP supported.

        default
        :default: HTTP

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PortMapping(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_appmesh.Protocol")
class Protocol(enum.Enum):
    """Enum of supported AppMesh protocols.

    stability
    :stability: experimental
    """
    HTTP = "HTTP"
    """
    stability
    :stability: experimental
    """
    TCP = "TCP"
    """
    stability
    :stability: experimental
    """

@jsii.implements(IRoute)
class Route(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.Route"):
    """Route represents a new or existing route attached to a VirtualRouter and Mesh.

    see
    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/routes.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh: "IMesh", virtual_router: "IVirtualRouter", route_targets: typing.List["WeightedTargetProps"], prefix: typing.Optional[str]=None, route_name: typing.Optional[str]=None, route_type: typing.Optional["RouteType"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param mesh: The service mesh to define the route in.
        :param virtual_router: The virtual router in which to define the route.
        :param route_targets: Array of weighted route targets.
        :param prefix: The path prefix to match for the route. Default: "/" if http otherwise none
        :param route_name: The name of the route. Default: - An automatically generated name
        :param route_type: Weather the route is HTTP based. Default: - HTTP if ``prefix`` is given, TCP otherwise

        stability
        :stability: experimental
        """
        props = RouteProps(mesh=mesh, virtual_router=virtual_router, route_targets=route_targets, prefix=prefix, route_name=route_name, route_type=route_type)

        jsii.create(Route, self, [scope, id, props])

    @jsii.member(jsii_name="fromRouteArn")
    @builtins.classmethod
    def from_route_arn(cls, scope: _Construct_f50a3f53, id: str, route_arn: str) -> "IRoute":
        """Import an existing route given an ARN.

        :param scope: -
        :param id: -
        :param route_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRouteArn", [scope, id, route_arn])

    @jsii.member(jsii_name="fromRouteName")
    @builtins.classmethod
    def from_route_name(cls, scope: _Construct_f50a3f53, id: str, mesh_name: str, virtual_router_name: str, route_name: str) -> "IRoute":
        """Import an existing route given its name.

        :param scope: -
        :param id: -
        :param mesh_name: -
        :param virtual_router_name: -
        :param route_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRouteName", [scope, id, mesh_name, virtual_router_name, route_name])

    @builtins.property
    @jsii.member(jsii_name="routeArn")
    def route_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the route.

        stability
        :stability: experimental
        """
        return jsii.get(self, "routeArn")

    @builtins.property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> str:
        """The name of the route.

        stability
        :stability: experimental
        """
        return jsii.get(self, "routeName")

    @builtins.property
    @jsii.member(jsii_name="virtualRouter")
    def virtual_router(self) -> "IVirtualRouter":
        """The virtual router this route is a part of.

        stability
        :stability: experimental
        """
        return jsii.get(self, "virtualRouter")


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.RouteBaseProps", jsii_struct_bases=[], name_mapping={'route_targets': 'routeTargets', 'prefix': 'prefix', 'route_name': 'routeName', 'route_type': 'routeType'})
class RouteBaseProps():
    def __init__(self, *, route_targets: typing.List["WeightedTargetProps"], prefix: typing.Optional[str]=None, route_name: typing.Optional[str]=None, route_type: typing.Optional["RouteType"]=None) -> None:
        """Base interface properties for all Routes.

        :param route_targets: Array of weighted route targets.
        :param prefix: The path prefix to match for the route. Default: "/" if http otherwise none
        :param route_name: The name of the route. Default: - An automatically generated name
        :param route_type: Weather the route is HTTP based. Default: - HTTP if ``prefix`` is given, TCP otherwise

        stability
        :stability: experimental
        """
        self._values = {
            'route_targets': route_targets,
        }
        if prefix is not None: self._values["prefix"] = prefix
        if route_name is not None: self._values["route_name"] = route_name
        if route_type is not None: self._values["route_type"] = route_type

    @builtins.property
    def route_targets(self) -> typing.List["WeightedTargetProps"]:
        """Array of weighted route targets.

        stability
        :stability: experimental
        requires:
        :requires:: minimum of 1
        """
        return self._values.get('route_targets')

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """The path prefix to match for the route.

        default
        :default: "/" if http otherwise none

        stability
        :stability: experimental
        """
        return self._values.get('prefix')

    @builtins.property
    def route_name(self) -> typing.Optional[str]:
        """The name of the route.

        default
        :default: - An automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get('route_name')

    @builtins.property
    def route_type(self) -> typing.Optional["RouteType"]:
        """Weather the route is HTTP based.

        default
        :default: - HTTP if ``prefix`` is given, TCP otherwise

        stability
        :stability: experimental
        """
        return self._values.get('route_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RouteBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.RouteProps", jsii_struct_bases=[RouteBaseProps], name_mapping={'route_targets': 'routeTargets', 'prefix': 'prefix', 'route_name': 'routeName', 'route_type': 'routeType', 'mesh': 'mesh', 'virtual_router': 'virtualRouter'})
class RouteProps(RouteBaseProps):
    def __init__(self, *, route_targets: typing.List["WeightedTargetProps"], prefix: typing.Optional[str]=None, route_name: typing.Optional[str]=None, route_type: typing.Optional["RouteType"]=None, mesh: "IMesh", virtual_router: "IVirtualRouter") -> None:
        """Properties to define new Routes.

        :param route_targets: Array of weighted route targets.
        :param prefix: The path prefix to match for the route. Default: "/" if http otherwise none
        :param route_name: The name of the route. Default: - An automatically generated name
        :param route_type: Weather the route is HTTP based. Default: - HTTP if ``prefix`` is given, TCP otherwise
        :param mesh: The service mesh to define the route in.
        :param virtual_router: The virtual router in which to define the route.

        stability
        :stability: experimental
        """
        self._values = {
            'route_targets': route_targets,
            'mesh': mesh,
            'virtual_router': virtual_router,
        }
        if prefix is not None: self._values["prefix"] = prefix
        if route_name is not None: self._values["route_name"] = route_name
        if route_type is not None: self._values["route_type"] = route_type

    @builtins.property
    def route_targets(self) -> typing.List["WeightedTargetProps"]:
        """Array of weighted route targets.

        stability
        :stability: experimental
        requires:
        :requires:: minimum of 1
        """
        return self._values.get('route_targets')

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """The path prefix to match for the route.

        default
        :default: "/" if http otherwise none

        stability
        :stability: experimental
        """
        return self._values.get('prefix')

    @builtins.property
    def route_name(self) -> typing.Optional[str]:
        """The name of the route.

        default
        :default: - An automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get('route_name')

    @builtins.property
    def route_type(self) -> typing.Optional["RouteType"]:
        """Weather the route is HTTP based.

        default
        :default: - HTTP if ``prefix`` is given, TCP otherwise

        stability
        :stability: experimental
        """
        return self._values.get('route_type')

    @builtins.property
    def mesh(self) -> "IMesh":
        """The service mesh to define the route in.

        stability
        :stability: experimental
        """
        return self._values.get('mesh')

    @builtins.property
    def virtual_router(self) -> "IVirtualRouter":
        """The virtual router in which to define the route.

        stability
        :stability: experimental
        """
        return self._values.get('virtual_router')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RouteProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_appmesh.RouteType")
class RouteType(enum.Enum):
    """Type of route.

    stability
    :stability: experimental
    """
    HTTP = "HTTP"
    """HTTP route.

    stability
    :stability: experimental
    """
    TCP = "TCP"
    """TCP route.

    stability
    :stability: experimental
    """

@jsii.implements(IVirtualNode)
class VirtualNode(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.VirtualNode"):
    """VirtualNode represents a newly defined AppMesh VirtualNode.

    Any inbound traffic that your virtual node expects should be specified as a
    listener. Any outbound traffic that your virtual node expects to reach
    should be specified as a backend.

    see
    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_nodes.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh: "IMesh", backends: typing.Optional[typing.List["IVirtualService"]]=None, cloud_map_service: typing.Optional[_IService_f28ba3c9]=None, cloud_map_service_instance_attributes: typing.Optional[typing.Mapping[str, str]]=None, dns_host_name: typing.Optional[str]=None, listener: typing.Optional["VirtualNodeListener"]=None, virtual_node_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param mesh: The name of the AppMesh which the virtual node belongs to.
        :param backends: Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param cloud_map_service: CloudMap service where Virtual Node members register themselves. Instances registering themselves into this CloudMap will be considered part of the Virtual Node. Default: - Don't use CloudMap-based service discovery
        :param cloud_map_service_instance_attributes: Filter down the list of CloudMap service instance. Default: - No CloudMap instance filter
        :param dns_host_name: Host name of DNS record used to discover Virtual Node members. The IP addresses returned by querying this DNS record will be considered part of the Virtual Node. Default: - Don't use DNS-based service discovery
        :param listener: Initial listener for the virtual node. Default: - No listeners
        :param virtual_node_name: The name of the VirtualNode. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        props = VirtualNodeProps(mesh=mesh, backends=backends, cloud_map_service=cloud_map_service, cloud_map_service_instance_attributes=cloud_map_service_instance_attributes, dns_host_name=dns_host_name, listener=listener, virtual_node_name=virtual_node_name)

        jsii.create(VirtualNode, self, [scope, id, props])

    @jsii.member(jsii_name="fromVirtualNodeArn")
    @builtins.classmethod
    def from_virtual_node_arn(cls, scope: _Construct_f50a3f53, id: str, virtual_node_arn: str) -> "IVirtualNode":
        """Import an existing VirtualNode given an ARN.

        :param scope: -
        :param id: -
        :param virtual_node_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromVirtualNodeArn", [scope, id, virtual_node_arn])

    @jsii.member(jsii_name="fromVirtualNodeName")
    @builtins.classmethod
    def from_virtual_node_name(cls, scope: _Construct_f50a3f53, id: str, mesh_name: str, virtual_node_name: str) -> "IVirtualNode":
        """Import an existing VirtualNode given its name.

        :param scope: -
        :param id: -
        :param mesh_name: -
        :param virtual_node_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromVirtualNodeName", [scope, id, mesh_name, virtual_node_name])

    @jsii.member(jsii_name="addBackends")
    def add_backends(self, *props: "IVirtualService") -> None:
        """Add a Virtual Services that this node is expected to send outbound traffic to.

        :param props: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addBackends", [*props])

    @jsii.member(jsii_name="addListeners")
    def add_listeners(self, *listeners: "VirtualNodeListener") -> None:
        """Utility method to add an inbound listener for this virtual node.

        :param listeners: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addListeners", [*listeners])

    @builtins.property
    @jsii.member(jsii_name="backends")
    def _backends(self) -> typing.List["CfnVirtualNode.BackendProperty"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "backends")

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def _listeners(self) -> typing.List["CfnVirtualNode.ListenerProperty"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "listeners")

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> "IMesh":
        """The service mesh that the virtual node resides in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "mesh")

    @builtins.property
    @jsii.member(jsii_name="virtualNodeArn")
    def virtual_node_arn(self) -> str:
        """The Amazon Resource Name belonging to the VirtualNdoe.

        stability
        :stability: experimental
        """
        return jsii.get(self, "virtualNodeArn")

    @builtins.property
    @jsii.member(jsii_name="virtualNodeName")
    def virtual_node_name(self) -> str:
        """The name of the VirtualNode.

        stability
        :stability: experimental
        """
        return jsii.get(self, "virtualNodeName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.VirtualNodeBaseProps", jsii_struct_bases=[], name_mapping={'backends': 'backends', 'cloud_map_service': 'cloudMapService', 'cloud_map_service_instance_attributes': 'cloudMapServiceInstanceAttributes', 'dns_host_name': 'dnsHostName', 'listener': 'listener', 'virtual_node_name': 'virtualNodeName'})
class VirtualNodeBaseProps():
    def __init__(self, *, backends: typing.Optional[typing.List["IVirtualService"]]=None, cloud_map_service: typing.Optional[_IService_f28ba3c9]=None, cloud_map_service_instance_attributes: typing.Optional[typing.Mapping[str, str]]=None, dns_host_name: typing.Optional[str]=None, listener: typing.Optional["VirtualNodeListener"]=None, virtual_node_name: typing.Optional[str]=None) -> None:
        """Basic configuration properties for a VirtualNode.

        :param backends: Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param cloud_map_service: CloudMap service where Virtual Node members register themselves. Instances registering themselves into this CloudMap will be considered part of the Virtual Node. Default: - Don't use CloudMap-based service discovery
        :param cloud_map_service_instance_attributes: Filter down the list of CloudMap service instance. Default: - No CloudMap instance filter
        :param dns_host_name: Host name of DNS record used to discover Virtual Node members. The IP addresses returned by querying this DNS record will be considered part of the Virtual Node. Default: - Don't use DNS-based service discovery
        :param listener: Initial listener for the virtual node. Default: - No listeners
        :param virtual_node_name: The name of the VirtualNode. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        if isinstance(listener, dict): listener = VirtualNodeListener(**listener)
        self._values = {
        }
        if backends is not None: self._values["backends"] = backends
        if cloud_map_service is not None: self._values["cloud_map_service"] = cloud_map_service
        if cloud_map_service_instance_attributes is not None: self._values["cloud_map_service_instance_attributes"] = cloud_map_service_instance_attributes
        if dns_host_name is not None: self._values["dns_host_name"] = dns_host_name
        if listener is not None: self._values["listener"] = listener
        if virtual_node_name is not None: self._values["virtual_node_name"] = virtual_node_name

    @builtins.property
    def backends(self) -> typing.Optional[typing.List["IVirtualService"]]:
        """Virtual Services that this is node expected to send outbound traffic to.

        default
        :default: - No backends

        stability
        :stability: experimental
        """
        return self._values.get('backends')

    @builtins.property
    def cloud_map_service(self) -> typing.Optional[_IService_f28ba3c9]:
        """CloudMap service where Virtual Node members register themselves.

        Instances registering themselves into this CloudMap will
        be considered part of the Virtual Node.

        default
        :default: - Don't use CloudMap-based service discovery

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_service')

    @builtins.property
    def cloud_map_service_instance_attributes(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Filter down the list of CloudMap service instance.

        default
        :default: - No CloudMap instance filter

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_service_instance_attributes')

    @builtins.property
    def dns_host_name(self) -> typing.Optional[str]:
        """Host name of DNS record used to discover Virtual Node members.

        The IP addresses returned by querying this DNS record will be considered
        part of the Virtual Node.

        default
        :default: - Don't use DNS-based service discovery

        stability
        :stability: experimental
        """
        return self._values.get('dns_host_name')

    @builtins.property
    def listener(self) -> typing.Optional["VirtualNodeListener"]:
        """Initial listener for the virtual node.

        default
        :default: - No listeners

        stability
        :stability: experimental
        """
        return self._values.get('listener')

    @builtins.property
    def virtual_node_name(self) -> typing.Optional[str]:
        """The name of the VirtualNode.

        default
        :default: - A name is automatically determined

        stability
        :stability: experimental
        """
        return self._values.get('virtual_node_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VirtualNodeBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.VirtualNodeListener", jsii_struct_bases=[], name_mapping={'health_check': 'healthCheck', 'port_mapping': 'portMapping'})
class VirtualNodeListener():
    def __init__(self, *, health_check: typing.Optional["HealthCheck"]=None, port_mapping: typing.Optional["PortMapping"]=None) -> None:
        """Represents the properties needed to define healthy and active listeners for nodes.

        :param health_check: Array fo HealthCheckProps for the node(s). Default: - no healthcheck
        :param port_mapping: Array of PortMappingProps for the listener. Default: - HTTP port 8080

        stability
        :stability: experimental
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        if isinstance(port_mapping, dict): port_mapping = PortMapping(**port_mapping)
        self._values = {
        }
        if health_check is not None: self._values["health_check"] = health_check
        if port_mapping is not None: self._values["port_mapping"] = port_mapping

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """Array fo HealthCheckProps for the node(s).

        default
        :default: - no healthcheck

        stability
        :stability: experimental
        """
        return self._values.get('health_check')

    @builtins.property
    def port_mapping(self) -> typing.Optional["PortMapping"]:
        """Array of PortMappingProps for the listener.

        default
        :default: - HTTP port 8080

        stability
        :stability: experimental
        """
        return self._values.get('port_mapping')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VirtualNodeListener(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.VirtualNodeProps", jsii_struct_bases=[VirtualNodeBaseProps], name_mapping={'backends': 'backends', 'cloud_map_service': 'cloudMapService', 'cloud_map_service_instance_attributes': 'cloudMapServiceInstanceAttributes', 'dns_host_name': 'dnsHostName', 'listener': 'listener', 'virtual_node_name': 'virtualNodeName', 'mesh': 'mesh'})
class VirtualNodeProps(VirtualNodeBaseProps):
    def __init__(self, *, backends: typing.Optional[typing.List["IVirtualService"]]=None, cloud_map_service: typing.Optional[_IService_f28ba3c9]=None, cloud_map_service_instance_attributes: typing.Optional[typing.Mapping[str, str]]=None, dns_host_name: typing.Optional[str]=None, listener: typing.Optional["VirtualNodeListener"]=None, virtual_node_name: typing.Optional[str]=None, mesh: "IMesh") -> None:
        """The properties used when creating a new VirtualNode.

        :param backends: Virtual Services that this is node expected to send outbound traffic to. Default: - No backends
        :param cloud_map_service: CloudMap service where Virtual Node members register themselves. Instances registering themselves into this CloudMap will be considered part of the Virtual Node. Default: - Don't use CloudMap-based service discovery
        :param cloud_map_service_instance_attributes: Filter down the list of CloudMap service instance. Default: - No CloudMap instance filter
        :param dns_host_name: Host name of DNS record used to discover Virtual Node members. The IP addresses returned by querying this DNS record will be considered part of the Virtual Node. Default: - Don't use DNS-based service discovery
        :param listener: Initial listener for the virtual node. Default: - No listeners
        :param virtual_node_name: The name of the VirtualNode. Default: - A name is automatically determined
        :param mesh: The name of the AppMesh which the virtual node belongs to.

        stability
        :stability: experimental
        """
        if isinstance(listener, dict): listener = VirtualNodeListener(**listener)
        self._values = {
            'mesh': mesh,
        }
        if backends is not None: self._values["backends"] = backends
        if cloud_map_service is not None: self._values["cloud_map_service"] = cloud_map_service
        if cloud_map_service_instance_attributes is not None: self._values["cloud_map_service_instance_attributes"] = cloud_map_service_instance_attributes
        if dns_host_name is not None: self._values["dns_host_name"] = dns_host_name
        if listener is not None: self._values["listener"] = listener
        if virtual_node_name is not None: self._values["virtual_node_name"] = virtual_node_name

    @builtins.property
    def backends(self) -> typing.Optional[typing.List["IVirtualService"]]:
        """Virtual Services that this is node expected to send outbound traffic to.

        default
        :default: - No backends

        stability
        :stability: experimental
        """
        return self._values.get('backends')

    @builtins.property
    def cloud_map_service(self) -> typing.Optional[_IService_f28ba3c9]:
        """CloudMap service where Virtual Node members register themselves.

        Instances registering themselves into this CloudMap will
        be considered part of the Virtual Node.

        default
        :default: - Don't use CloudMap-based service discovery

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_service')

    @builtins.property
    def cloud_map_service_instance_attributes(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Filter down the list of CloudMap service instance.

        default
        :default: - No CloudMap instance filter

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_service_instance_attributes')

    @builtins.property
    def dns_host_name(self) -> typing.Optional[str]:
        """Host name of DNS record used to discover Virtual Node members.

        The IP addresses returned by querying this DNS record will be considered
        part of the Virtual Node.

        default
        :default: - Don't use DNS-based service discovery

        stability
        :stability: experimental
        """
        return self._values.get('dns_host_name')

    @builtins.property
    def listener(self) -> typing.Optional["VirtualNodeListener"]:
        """Initial listener for the virtual node.

        default
        :default: - No listeners

        stability
        :stability: experimental
        """
        return self._values.get('listener')

    @builtins.property
    def virtual_node_name(self) -> typing.Optional[str]:
        """The name of the VirtualNode.

        default
        :default: - A name is automatically determined

        stability
        :stability: experimental
        """
        return self._values.get('virtual_node_name')

    @builtins.property
    def mesh(self) -> "IMesh":
        """The name of the AppMesh which the virtual node belongs to.

        stability
        :stability: experimental
        """
        return self._values.get('mesh')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VirtualNodeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IVirtualRouter)
class VirtualRouter(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.VirtualRouter"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh: "IMesh", listener: typing.Optional["Listener"]=None, virtual_router_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param mesh: The AppMesh mesh the VirtualRouter belongs to.
        :param listener: Listener specification for the virtual router. Default: - A listener on HTTP port 8080
        :param virtual_router_name: The name of the VirtualRouter. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        props = VirtualRouterProps(mesh=mesh, listener=listener, virtual_router_name=virtual_router_name)

        jsii.create(VirtualRouter, self, [scope, id, props])

    @jsii.member(jsii_name="fromVirtualRouterArn")
    @builtins.classmethod
    def from_virtual_router_arn(cls, scope: _Construct_f50a3f53, id: str, virtual_router_arn: str) -> "IVirtualRouter":
        """Import an existing VirtualRouter given an ARN.

        :param scope: -
        :param id: -
        :param virtual_router_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromVirtualRouterArn", [scope, id, virtual_router_arn])

    @jsii.member(jsii_name="fromVirtualRouterAttributes")
    @builtins.classmethod
    def from_virtual_router_attributes(cls, scope: _Construct_f50a3f53, id: str, *, mesh: typing.Optional["IMesh"]=None, mesh_name: typing.Optional[str]=None, virtual_router_arn: typing.Optional[str]=None, virtual_router_name: typing.Optional[str]=None) -> "IVirtualRouter":
        """Import an existing virtual router given attributes.

        :param scope: -
        :param id: -
        :param mesh: The AppMesh mesh the VirtualRouter belongs to.
        :param mesh_name: The name of the AppMesh mesh the VirtualRouter belongs to.
        :param virtual_router_arn: The Amazon Resource Name (ARN) for the VirtualRouter.
        :param virtual_router_name: The name of the VirtualRouter.

        stability
        :stability: experimental
        """
        attrs = VirtualRouterAttributes(mesh=mesh, mesh_name=mesh_name, virtual_router_arn=virtual_router_arn, virtual_router_name=virtual_router_name)

        return jsii.sinvoke(cls, "fromVirtualRouterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromVirtualRouterName")
    @builtins.classmethod
    def from_virtual_router_name(cls, scope: _Construct_f50a3f53, id: str, mesh_name: str, virtual_router_name: str) -> "IVirtualRouter":
        """Import an existing VirtualRouter given names.

        :param scope: -
        :param id: -
        :param mesh_name: -
        :param virtual_router_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromVirtualRouterName", [scope, id, mesh_name, virtual_router_name])

    @jsii.member(jsii_name="addRoute")
    def add_route(self, id: str, *, route_targets: typing.List["WeightedTargetProps"], prefix: typing.Optional[str]=None, route_name: typing.Optional[str]=None, route_type: typing.Optional["RouteType"]=None) -> "Route":
        """Add a single route to the router.

        :param id: -
        :param route_targets: Array of weighted route targets.
        :param prefix: The path prefix to match for the route. Default: "/" if http otherwise none
        :param route_name: The name of the route. Default: - An automatically generated name
        :param route_type: Weather the route is HTTP based. Default: - HTTP if ``prefix`` is given, TCP otherwise

        stability
        :stability: experimental
        """
        props = RouteBaseProps(route_targets=route_targets, prefix=prefix, route_name=route_name, route_type=route_type)

        return jsii.invoke(self, "addRoute", [id, props])

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> "IMesh":
        """The AppMesh mesh the VirtualRouter belongs to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "mesh")

    @builtins.property
    @jsii.member(jsii_name="virtualRouterArn")
    def virtual_router_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the VirtualRouter.

        stability
        :stability: experimental
        """
        return jsii.get(self, "virtualRouterArn")

    @builtins.property
    @jsii.member(jsii_name="virtualRouterName")
    def virtual_router_name(self) -> str:
        """The name of the VirtualRouter.

        stability
        :stability: experimental
        """
        return jsii.get(self, "virtualRouterName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.VirtualRouterAttributes", jsii_struct_bases=[], name_mapping={'mesh': 'mesh', 'mesh_name': 'meshName', 'virtual_router_arn': 'virtualRouterArn', 'virtual_router_name': 'virtualRouterName'})
class VirtualRouterAttributes():
    def __init__(self, *, mesh: typing.Optional["IMesh"]=None, mesh_name: typing.Optional[str]=None, virtual_router_arn: typing.Optional[str]=None, virtual_router_name: typing.Optional[str]=None) -> None:
        """Interface with properties ncecessary to import a reusable VirtualRouter.

        :param mesh: The AppMesh mesh the VirtualRouter belongs to.
        :param mesh_name: The name of the AppMesh mesh the VirtualRouter belongs to.
        :param virtual_router_arn: The Amazon Resource Name (ARN) for the VirtualRouter.
        :param virtual_router_name: The name of the VirtualRouter.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if mesh is not None: self._values["mesh"] = mesh
        if mesh_name is not None: self._values["mesh_name"] = mesh_name
        if virtual_router_arn is not None: self._values["virtual_router_arn"] = virtual_router_arn
        if virtual_router_name is not None: self._values["virtual_router_name"] = virtual_router_name

    @builtins.property
    def mesh(self) -> typing.Optional["IMesh"]:
        """The AppMesh mesh the VirtualRouter belongs to.

        stability
        :stability: experimental
        """
        return self._values.get('mesh')

    @builtins.property
    def mesh_name(self) -> typing.Optional[str]:
        """The name of the AppMesh mesh the VirtualRouter belongs to.

        stability
        :stability: experimental
        """
        return self._values.get('mesh_name')

    @builtins.property
    def virtual_router_arn(self) -> typing.Optional[str]:
        """The Amazon Resource Name (ARN) for the VirtualRouter.

        stability
        :stability: experimental
        """
        return self._values.get('virtual_router_arn')

    @builtins.property
    def virtual_router_name(self) -> typing.Optional[str]:
        """The name of the VirtualRouter.

        stability
        :stability: experimental
        """
        return self._values.get('virtual_router_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VirtualRouterAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.VirtualRouterBaseProps", jsii_struct_bases=[], name_mapping={'listener': 'listener', 'virtual_router_name': 'virtualRouterName'})
class VirtualRouterBaseProps():
    def __init__(self, *, listener: typing.Optional["Listener"]=None, virtual_router_name: typing.Optional[str]=None) -> None:
        """Interface with base properties all routers willl inherit.

        :param listener: Listener specification for the virtual router. Default: - A listener on HTTP port 8080
        :param virtual_router_name: The name of the VirtualRouter. Default: - A name is automatically determined

        stability
        :stability: experimental
        """
        if isinstance(listener, dict): listener = Listener(**listener)
        self._values = {
        }
        if listener is not None: self._values["listener"] = listener
        if virtual_router_name is not None: self._values["virtual_router_name"] = virtual_router_name

    @builtins.property
    def listener(self) -> typing.Optional["Listener"]:
        """Listener specification for the virtual router.

        default
        :default: - A listener on HTTP port 8080

        stability
        :stability: experimental
        """
        return self._values.get('listener')

    @builtins.property
    def virtual_router_name(self) -> typing.Optional[str]:
        """The name of the VirtualRouter.

        default
        :default: - A name is automatically determined

        stability
        :stability: experimental
        """
        return self._values.get('virtual_router_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VirtualRouterBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.VirtualRouterProps", jsii_struct_bases=[VirtualRouterBaseProps], name_mapping={'listener': 'listener', 'virtual_router_name': 'virtualRouterName', 'mesh': 'mesh'})
class VirtualRouterProps(VirtualRouterBaseProps):
    def __init__(self, *, listener: typing.Optional["Listener"]=None, virtual_router_name: typing.Optional[str]=None, mesh: "IMesh") -> None:
        """The properties used when creating a new VritualRouter.

        :param listener: Listener specification for the virtual router. Default: - A listener on HTTP port 8080
        :param virtual_router_name: The name of the VirtualRouter. Default: - A name is automatically determined
        :param mesh: The AppMesh mesh the VirtualRouter belongs to.

        stability
        :stability: experimental
        """
        if isinstance(listener, dict): listener = Listener(**listener)
        self._values = {
            'mesh': mesh,
        }
        if listener is not None: self._values["listener"] = listener
        if virtual_router_name is not None: self._values["virtual_router_name"] = virtual_router_name

    @builtins.property
    def listener(self) -> typing.Optional["Listener"]:
        """Listener specification for the virtual router.

        default
        :default: - A listener on HTTP port 8080

        stability
        :stability: experimental
        """
        return self._values.get('listener')

    @builtins.property
    def virtual_router_name(self) -> typing.Optional[str]:
        """The name of the VirtualRouter.

        default
        :default: - A name is automatically determined

        stability
        :stability: experimental
        """
        return self._values.get('virtual_router_name')

    @builtins.property
    def mesh(self) -> "IMesh":
        """The AppMesh mesh the VirtualRouter belongs to.

        stability
        :stability: experimental
        """
        return self._values.get('mesh')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VirtualRouterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IVirtualService)
class VirtualService(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appmesh.VirtualService"):
    """VirtualService represents a service inside an AppMesh.

    It routes traffic either to a Virtual Node or to a Virtual Router.

    see
    :see: https://docs.aws.amazon.com/app-mesh/latest/userguide/virtual_services.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, mesh: "IMesh", virtual_node: typing.Optional["IVirtualNode"]=None, virtual_router: typing.Optional["IVirtualRouter"]=None, virtual_service_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param mesh: The AppMesh mesh name for which the VirtualService belongs to.
        :param virtual_node: The VirtualNode attached to the virtual service. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_router: The VirtualRouter which the VirtualService uses as provider. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_service_name: The name of the VirtualService. It is recommended this follows the fully-qualified domain name format, such as "my-service.default.svc.cluster.local". Default: - A name is automatically generated

        stability
        :stability: experimental
        """
        props = VirtualServiceProps(mesh=mesh, virtual_node=virtual_node, virtual_router=virtual_router, virtual_service_name=virtual_service_name)

        jsii.create(VirtualService, self, [scope, id, props])

    @jsii.member(jsii_name="fromVirtualServiceArn")
    @builtins.classmethod
    def from_virtual_service_arn(cls, scope: _Construct_f50a3f53, id: str, virtual_service_arn: str) -> "IVirtualService":
        """Import an existing VirtualService given an ARN.

        :param scope: -
        :param id: -
        :param virtual_service_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromVirtualServiceArn", [scope, id, virtual_service_arn])

    @jsii.member(jsii_name="fromVirtualServiceName")
    @builtins.classmethod
    def from_virtual_service_name(cls, scope: _Construct_f50a3f53, id: str, mesh_name: str, virtual_service_name: str) -> "IVirtualService":
        """Import an existing VirtualService given mesh and service names.

        :param scope: -
        :param id: -
        :param mesh_name: -
        :param virtual_service_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromVirtualServiceName", [scope, id, mesh_name, virtual_service_name])

    @builtins.property
    @jsii.member(jsii_name="virtualServiceArn")
    def virtual_service_arn(self) -> str:
        """The Amazon Resource Name (ARN) for the virtual service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "virtualServiceArn")

    @builtins.property
    @jsii.member(jsii_name="virtualServiceName")
    def virtual_service_name(self) -> str:
        """The name of the VirtualService, it is recommended this follows the fully-qualified domain name format.

        stability
        :stability: experimental
        """
        return jsii.get(self, "virtualServiceName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.VirtualServiceBaseProps", jsii_struct_bases=[], name_mapping={'virtual_node': 'virtualNode', 'virtual_router': 'virtualRouter', 'virtual_service_name': 'virtualServiceName'})
class VirtualServiceBaseProps():
    def __init__(self, *, virtual_node: typing.Optional["IVirtualNode"]=None, virtual_router: typing.Optional["IVirtualRouter"]=None, virtual_service_name: typing.Optional[str]=None) -> None:
        """The base properties which all classes in VirtualService will inherit from.

        :param virtual_node: The VirtualNode attached to the virtual service. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_router: The VirtualRouter which the VirtualService uses as provider. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_service_name: The name of the VirtualService. It is recommended this follows the fully-qualified domain name format, such as "my-service.default.svc.cluster.local". Default: - A name is automatically generated

        stability
        :stability: experimental
        """
        self._values = {
        }
        if virtual_node is not None: self._values["virtual_node"] = virtual_node
        if virtual_router is not None: self._values["virtual_router"] = virtual_router
        if virtual_service_name is not None: self._values["virtual_service_name"] = virtual_service_name

    @builtins.property
    def virtual_node(self) -> typing.Optional["IVirtualNode"]:
        """The VirtualNode attached to the virtual service.

        default
        :default: - At most one of virtualRouter and virtualNode is allowed.

        stability
        :stability: experimental
        """
        return self._values.get('virtual_node')

    @builtins.property
    def virtual_router(self) -> typing.Optional["IVirtualRouter"]:
        """The VirtualRouter which the VirtualService uses as provider.

        default
        :default: - At most one of virtualRouter and virtualNode is allowed.

        stability
        :stability: experimental
        """
        return self._values.get('virtual_router')

    @builtins.property
    def virtual_service_name(self) -> typing.Optional[str]:
        """The name of the VirtualService.

        It is recommended this follows the fully-qualified domain name format,
        such as "my-service.default.svc.cluster.local".

        default
        :default: - A name is automatically generated

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            service.domain.local
        """
        return self._values.get('virtual_service_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VirtualServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.VirtualServiceProps", jsii_struct_bases=[VirtualServiceBaseProps], name_mapping={'virtual_node': 'virtualNode', 'virtual_router': 'virtualRouter', 'virtual_service_name': 'virtualServiceName', 'mesh': 'mesh'})
class VirtualServiceProps(VirtualServiceBaseProps):
    def __init__(self, *, virtual_node: typing.Optional["IVirtualNode"]=None, virtual_router: typing.Optional["IVirtualRouter"]=None, virtual_service_name: typing.Optional[str]=None, mesh: "IMesh") -> None:
        """The properties applied to the VirtualService being define.

        :param virtual_node: The VirtualNode attached to the virtual service. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_router: The VirtualRouter which the VirtualService uses as provider. Default: - At most one of virtualRouter and virtualNode is allowed.
        :param virtual_service_name: The name of the VirtualService. It is recommended this follows the fully-qualified domain name format, such as "my-service.default.svc.cluster.local". Default: - A name is automatically generated
        :param mesh: The AppMesh mesh name for which the VirtualService belongs to.

        stability
        :stability: experimental
        """
        self._values = {
            'mesh': mesh,
        }
        if virtual_node is not None: self._values["virtual_node"] = virtual_node
        if virtual_router is not None: self._values["virtual_router"] = virtual_router
        if virtual_service_name is not None: self._values["virtual_service_name"] = virtual_service_name

    @builtins.property
    def virtual_node(self) -> typing.Optional["IVirtualNode"]:
        """The VirtualNode attached to the virtual service.

        default
        :default: - At most one of virtualRouter and virtualNode is allowed.

        stability
        :stability: experimental
        """
        return self._values.get('virtual_node')

    @builtins.property
    def virtual_router(self) -> typing.Optional["IVirtualRouter"]:
        """The VirtualRouter which the VirtualService uses as provider.

        default
        :default: - At most one of virtualRouter and virtualNode is allowed.

        stability
        :stability: experimental
        """
        return self._values.get('virtual_router')

    @builtins.property
    def virtual_service_name(self) -> typing.Optional[str]:
        """The name of the VirtualService.

        It is recommended this follows the fully-qualified domain name format,
        such as "my-service.default.svc.cluster.local".

        default
        :default: - A name is automatically generated

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            service.domain.local
        """
        return self._values.get('virtual_service_name')

    @builtins.property
    def mesh(self) -> "IMesh":
        """The AppMesh mesh name for which the VirtualService belongs to.

        stability
        :stability: experimental
        """
        return self._values.get('mesh')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VirtualServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_appmesh.WeightedTargetProps", jsii_struct_bases=[], name_mapping={'virtual_node': 'virtualNode', 'weight': 'weight'})
class WeightedTargetProps():
    def __init__(self, *, virtual_node: "IVirtualNode", weight: typing.Optional[jsii.Number]=None) -> None:
        """Properties for the Weighted Targets in the route.

        :param virtual_node: The VirtualNode the route points to.
        :param weight: The weight for the target. Default: 1

        stability
        :stability: experimental
        """
        self._values = {
            'virtual_node': virtual_node,
        }
        if weight is not None: self._values["weight"] = weight

    @builtins.property
    def virtual_node(self) -> "IVirtualNode":
        """The VirtualNode the route points to.

        stability
        :stability: experimental
        """
        return self._values.get('virtual_node')

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        """The weight for the target.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('weight')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'WeightedTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnMesh",
    "CfnMeshProps",
    "CfnRoute",
    "CfnRouteProps",
    "CfnVirtualNode",
    "CfnVirtualNodeProps",
    "CfnVirtualRouter",
    "CfnVirtualRouterProps",
    "CfnVirtualService",
    "CfnVirtualServiceProps",
    "HealthCheck",
    "IMesh",
    "IRoute",
    "IVirtualNode",
    "IVirtualRouter",
    "IVirtualService",
    "Listener",
    "Mesh",
    "MeshFilterType",
    "MeshProps",
    "PortMapping",
    "Protocol",
    "Route",
    "RouteBaseProps",
    "RouteProps",
    "RouteType",
    "VirtualNode",
    "VirtualNodeBaseProps",
    "VirtualNodeListener",
    "VirtualNodeProps",
    "VirtualRouter",
    "VirtualRouterAttributes",
    "VirtualRouterBaseProps",
    "VirtualRouterProps",
    "VirtualService",
    "VirtualServiceBaseProps",
    "VirtualServiceProps",
    "WeightedTargetProps",
]

publication.publish()
