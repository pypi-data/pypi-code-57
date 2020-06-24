from gooey import Gooey, GooeyParser
import ruamel.yaml
from models import *
import pyaware.devices
import ibm_watson


def load_config(config):
    with open(config) as f:
        return ruamel.yaml.safe_load(f)


def get_one(model, **kwargs):
    try:
        doc = model.objects(**kwargs).get()
    except DoesNotExist:
        doc = model(**kwargs)
        doc.save()
    return doc


def get_aware_device_type(device_type: str):
    return getattr(pyaware.devices, device_type)


def update_organisation(name: str):
    """
    Updates organisations by the unique name
    :param name:
    :return:
    """
    return get_one(Organisation, name=name)


def update_entities(entity_map: dict, organisation: Organisation, parent=None, entities=None) -> dict:
    """
    Recursive function to set up all the entities from top to bottom
    :param entity_map: Heirarchy dictionary of entities from the configuration. Each tier must have
    type: ...,
    kind: ...,
    <child_key_1>:
        type: ...,
        kind: ...,
        <child_key_2>.....
    :param organisation:
    :return:
    """
    if entities is None:
        entities = {}
    for current, attributes in entity_map.items():
        if current in ["type", "name"]:
            continue
        entity = get_one(Entity, name=current, organisation=organisation,
                         entityType=get_one(EntityType, kind=attributes["name"]))
        # entity.entityType.displayName = entity.entityType.name
        # entity.entityType.name = entity.entityType.kind
        # entity.entityType.save()
        if parent is not None:
            entity.parentEntity = parent
        entity.save()
        entities[current] = entity
        entities.update(update_entities(attributes, organisation=organisation, parent=entity, entities=entities))
    return entities


def update_location(name: str):
    return get_one(Location, name=name)


def update_parameter_types(device_types):
    device_params = {}
    param_types = []
    for dev_type in device_types:
        device = getattr(pyaware.devices, dev_type)
        for k, v in device.data_info.items():
            device_params["{} {}".format(v.description, v.parameter_type)] = {"type": v.status_or_command,
                                                                              "valueType": v.parameter_type,
                                                                              "deviceWrite": v.device_write}
    for name, values in device_params.items():
        parameter_type = get_one(ParameterType, name=name, **values)
        param_types.append(parameter_type)
    return param_types


def update_parameters(devices):
    parameters = []
    for device in devices:
        aware_device = get_aware_device_type(device.deviceType.name)
        for name, data_type in aware_device.data_info.items():
            parameter = get_one(Parameter, name=name, device=device,
                                parameterType=get_one(ParameterType, name="{} {}".format(data_type.description,
                                                                                         data_type.parameter_type)))
            parameters.append(parameter)
    return parameters


def update_device_types(devices: list):
    device_types = {dev["device_type"]: None for dev in devices}
    for name in device_types:
        device_type = get_one(DeviceType, name=name)
        device_types[name] = device_type
    return device_types


def update_devices(devices: list, device_types: dict, entities: dict):
    device_docs = []
    for device in devices:
        dev = get_one(Device,
                      name=device["device_params"]["dev_id"],
                      deviceType=device_types[device["device_type"]],
                      entity=entities[device["parent"]])
        try:
            dev.location = device["location"]
        except KeyError:
            pass
        dev.save()
        device_docs.append(dev)
    return device_docs


def update_privileges(entities):
    pass




def rehome_orphans(devices):
    for device in devices:
        orphans = OrphanTelemetry.objects(device=device.name)
        for orphan in orphans:
            try:
                parameter = Parameter.objects(device=device, name=orphan.parameter)[0]
            except IndexError:
                continue
            new_value = ParameterValue(parameter=parameter, value=orphan.value, date=orphan.date)
            new_value.save()
            orphan.delete()


def update_mongodb_from_config(config):
    """
    Update mongodb database from a device configuration dictionary.
    The device configuration dictionary should live with the deployment configuration as device_config.yaml and should
    eventually be used to both update the database and instantiate the client
    :param config:
    :return:
    """
    org = update_organisation(config["meta_data"]["organisation"])
    entities = update_entities(config["meta_data"]["entity_map"], org)
    dev_types = update_device_types(config["devices"])
    param_types = update_parameter_types(dev_types)
    devices = update_devices(config["devices"], dev_types, entities)  # TODO fix assets
    parameters = update_parameters(devices)
    # Pull in orphaned data
    rehome_orphans(devices)


def update_ibm_cloud_from_config(config):
    ibm_watson.update_device_types(config)


def main():
    parser = GooeyParser(description="Update server configuration from deployment config")
    parser.add_argument('-c', '--config', widget="FileChooser",
                        help="Configuration file to load device data from")
    parser.add_argument('-p', '--prod', action="store_true",
                        help="Deploy to production database. Only do after confirming dry run without this mode")
    parser.add_argument('-s', '--staging', action="store_true",
                        help="Deploy to cloud dev database. Only do after confirming dry run without this mode")
    args = parser.parse_args()
    config_data = load_config(args.config)
    if args.staging:
        connect('aware-iot', alias='aware-iot',
                host="mongodb://aware_dev:8k6l6b6csF1qbm4q@cluster-1-shard-00-00-i80r2.gcp.mongodb.net:27017,cluster-1-shard-00-01-i80r2.gcp.mongodb.net:27017,cluster-1-shard-00-02-i80r2.gcp.mongodb.net:27017/aware-iot?ssl=true&replicaSet=Cluster-1-shard-0&authSource=admin&retryWrites=true")
    elif args.prod:
        raise NotImplementedError("Production deployment not set up yet")
    else:
        connect('aware-iot', alias='aware-iot', host='localhost', port=27017)
    update_mongodb_from_config(config_data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        main()
    else:
        Gooey(main())
