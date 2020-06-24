from marshmallow import Schema, fields, post_load, EXCLUDE
from swap.common.models import (
    ServiceDiscoveryData,
    ServiceDiscoveryDataset,
    ServiceDiscoveryIcon,
    ServiceDiscoveryParameters,
    ServiceDiscoveryProperty,
    ServiceDiscoveryResponse,
    ServiceDiscoveryService,
    ServiceDiscoveryVendor
)


class ServiceDiscoveryVendorSchema(Schema):
    service_provider_name = fields.Str()
    service_provider_uuid = fields.Str()
    service_provider_signature = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceDiscoveryVendor(**other)


class ServiceDiscoveryPropertySchema(Schema):
    title = fields.Str()
    type = fields.Str()
    options = fields.List(fields.Str())

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceDiscoveryProperty(**other)


class ServiceDiscoveryParametersSchema(Schema):
    properties = fields.Dict(
        keys=fields.Str(), values=fields.Nested(ServiceDiscoveryPropertySchema)
    )

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceDiscoveryParameters(**other)


class ServiceDiscoveryServiceSchema(Schema):
    name = fields.Str()
    catalogue_uuid = fields.Str()
    service_description = fields.Str()
    parameters = fields.Nested(ServiceDiscoveryParametersSchema)

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceDiscoveryService(**other)


class ServiceDiscoveryDatasetSchema(Schema):
    input = fields.Str()
    output = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceDiscoveryDataset(**other)


class ServiceDiscoveryIconSchema(Schema):
    base64 = fields.Str()
    url = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceDiscoveryIcon(**other)


class ServiceDiscoveryDataSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    vendor = fields.Nested(ServiceDiscoveryVendorSchema)
    service = fields.Nested(ServiceDiscoveryServiceSchema)
    dataset = fields.Nested(ServiceDiscoveryDatasetSchema)
    icon = fields.Nested(ServiceDiscoveryIconSchema)

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceDiscoveryData(**other)


class ServiceDiscoveryResponseSchema(Schema):
    data = fields.List(fields.Nested(ServiceDiscoveryDataSchema))

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceDiscoveryResponse(**other)


class ServiceDiscoverySchema(Schema):
    pass
