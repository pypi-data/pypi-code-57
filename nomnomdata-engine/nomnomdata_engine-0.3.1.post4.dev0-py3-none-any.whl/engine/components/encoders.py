import re
from json import JSONEncoder
from pathlib import PosixPath

from .base import Connection, Parameter, ParameterGroup, ParameterType
from .engine import Action, Engine


class ModelEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, PosixPath):
            return str(o)
        if isinstance(o, Parameter):
            return self.serialize_parameter(o)
        if isinstance(o, ParameterGroup):
            return self.serialize_parameter_group(o)
        elif isinstance(o, ParameterType):
            return self.serialize_parameter_type(o)
        elif isinstance(o, Connection):
            return {"connection_type_uuid": o.connection_type_uuid}
        elif isinstance(o, Engine):
            return self.serialize_engine(o)
        elif isinstance(o, Action):
            return self.serialize_action(o)
        else:
            return super().default(o)

    def serialize_engine(self, engine: Engine):
        result = {
            "uuid": engine.uuid,
            "alias": engine.alias,
            "description": engine.description,
            "nnd_model_version": engine.nnd_model_version,
            "categories": engine.categories,
            "type": engine.model_type.__str__(),
        }

        if engine.icons:
            result["icons"] = engine.icons
        if engine.help:
            result["help"] = engine.help
        result["actions"] = engine.actions
        return result

    def serialize_action(self, action: Action):
        # add parameters to this dict last so
        # that it's more human readable
        result = {
            "display_name": action.display_name or action.name.capitalize(),
            "description": action.description,
        }
        if action.help:
            result["help"] = action.help
        result["parameters"] = [p for p in action.parameter_groups.values()]
        return result

    def serialize_parameter_group(self, pg: ParameterGroup):
        result = {
            "name": pg.name,
            "display_name": pg.display_name,
            "description": pg.description,
            "type": pg.type,
            "collapsed": pg.collapsed,
            "parameters": [p for p in pg.parameters],
        }
        if pg.shared_parameter_group_uuid:
            result["shared_parameter_group_uuid"] = pg.shared_parameter_group_uuid
        return result

    def serialize_parameter(self, p: Parameter):
        result = {
            "name": p.name,
            "display_name": p.display_name,
            "description": p.description,
            "required": p.required,
        }
        if p.help:
            result["help"] = p.help
        if p.default:
            result["default"] = p.default
        result.update(self.serialize_parameter_type(p.type))
        return result

    def serialize_parameter_type(self, pt: ParameterType):
        result = {k: v for k, v in pt.__dict__.items() if v is not None}
        result["type"] = pt.type
        if pt.shared_object_type_uuid:
            result["shared_object_type_uuid"] = pt.shared_object_type_uuid
        return result
