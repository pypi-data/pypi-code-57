from kong_config_builder.base import BaseYamlObject


def remove_none(obj):
    if isinstance(obj, BaseYamlObject):
        return remove_none(obj.__dict__)
    elif isinstance(obj, (list, tuple, set)):
        return list(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return dict((remove_none(k), remove_none(v))
                    for k, v in obj.items()
                    if k is not None and v is not None)
    else:
        return obj


def no_empty(dumper, data):
    values = remove_none(data)
    data.__dict__ = values
    return dumper.represent_yaml_object(
        BaseYamlObject.yaml_tag, data, BaseYamlObject,
        flow_style=BaseYamlObject.yaml_flow_style
    )


def noop(self, *args, **kw):
    pass
