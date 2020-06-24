from mongoengine import *
from datetime import datetime


class Location(Document):
    name = StringField(uniquer=True, required=True)
    address = StringField()
    lat = FloatField()
    long = FloatField()
    isActive = BooleanField(default=True)

    meta = {'db_alias': 'aware-iot', 'collection': 'locations'}


class Organisation(Document):
    name = StringField(required=True, unique=True)
    isActive = BooleanField(default=True)
    createdAt = DateTimeField(default=datetime.now(), required=True)
    updatedAt = DateTimeField(default=datetime.now(), required=True)
    location = ReferenceField(Location)
    description = StringField()
    website = StringField()
    image = BinaryField()
    imageType = StringField()
    imageId = StringField()
    mongooseVersion = IntField(db_field="__v")

    meta = {'db_alias': 'aware-iot', 'collection': "organisations"}


class EntityType(Document):
    name = StringField(required=True)
    kind = StringField()
    allowedAttributes = ListField()
    allowedStatuses = ListField()
    displayName = StringField(required=True)
    description = StringField()
    isActive = BooleanField(default=True)
    updatedAt = DateTimeField()
    createdAt = DateTimeField()
    mongooseVersion = IntField(db_field="__v")

    meta = {'db_alias': 'aware-iot', 'collection': "entityTypes"}


class Entity(Document):
    name = StringField(required=True)
    description = StringField()
    organisation = ReferenceField(Organisation, required=True)
    entityType = ReferenceField(EntityType, required=True)
    isActive = BooleanField(default=True)
    attributes = ListField()
    parentEntity = ReferenceField('self', required=False)
    mongooseVersion = IntField(db_field="__v")
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    files = ListField()
    meta = {'db_alias': 'aware-iot', 'collection': "entities"}


class DeviceType(Document):
    name = StringField(required=True)
    displayName = StringField()
    description = StringField()
    isActive = BooleanField(default=True)
    updatedAt = DateTimeField()
    createdAt = DateTimeField()
    mongooseVersion = IntField(db_field="__v")

    meta = {'db_alias': 'aware-iot', 'collection': "deviceTypes"}


class Device(Document):
    name = StringField(required=True, unique_with="entity")
    displayName = StringField()
    description = StringField()
    deviceType = ReferenceField(DeviceType)
    entity = ReferenceField(Entity)
    location = ReferenceField(Location)
    isActive = BooleanField(default=True)
    isEnabled = BooleanField(default=True)

    meta = {'db_alias': 'aware-iot', 'collection': "devices"}


class ParameterType(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    valueType = StringField(required=True)
    type = StringField(required=True)
    deviceWrite = BooleanField(required=True)
    isActive = BooleanField(default=True)
    range = DictField()

    meta = {'db_alias': 'aware-iot', 'collection': "parameterTypes"}


class Parameter(Document):
    name = StringField(required=True, unique_with="device")
    description = StringField()
    parameterType = ReferenceField(ParameterType, required=True)
    device = ReferenceField(Device, required=True)
    statusLink = ReferenceField('self')
    isActive = BooleanField(default=True)

    meta = {'db_alias': 'aware-iot', 'collection': "parameters"}


class ParameterValue(Document):
    parameter = ReferenceField(Parameter, required=True)
    date = DateTimeField(required=True)
    value = DictField(required=True)

    meta = {'db_alias': 'aware-iot', 'collection': "parameterValues"}


class Privilege(Document):
    name = StringField(required=True)
    description = StringField()
    organisations = ListField(ReferenceField(Organisation))
    entities = ListField(ReferenceField(Entity))
    devices = ListField(ReferenceField(Device))
    parameters = ListField(ReferenceField(Parameter))
    isActive = BooleanField(default=True)
    createdBy = DateTimeField()
    updatedBy = DateTimeField()
    updatedAt = DateTimeField(default=datetime.now)
    createdAt = DateTimeField(default=datetime.now)
    mongooseVersion = IntField(db_field="__v")
    meta = {'db_alias': 'aware-iot', 'collection': "privileges"}


class OrphanTelemetry(Document):
    date = DateTimeField()
    device = StringField()
    parameter = StringField()
    value = DictField()
    updatedAt = DateTimeField()
    createdAt = DateTimeField()
    mongooseVersion = IntField(db_field="__v")
    meta = {'db_alias': 'aware-iot', 'collection': "orphanTelemetry"}
