from sqlalchemy import inspect
from sqlalchemy.orm import joinedload
import datetime


op_mapping = {
    "eq": lambda attr, value: attr == value,
    "neq": lambda attr, value: attr != value,
    "gt": lambda attr, value: attr > value,
    "gte": lambda attr, value: attr >= value,
    "lt": lambda attr, value: attr < value,
    "lte": lambda attr, value: attr <= value,
}


def generate_query(session, model, raw_query):
    return _generate_query(model, session.query(model), raw_query)


def _generate_query(model, query, raw_query, parent=None):
    inst = inspect(model)
    for c_attr in inst.mapper.column_attrs:
        prop = c_attr.key
        if prop in raw_query:
            simple_query = raw_query[prop]
            operation = op_mapping[simple_query["op"]]
            value = simple_query["value"]
            if c_attr.columns[0].type.python_type == datetime.datetime and isinstance(
                simple_query["value"], str
            ):
                value = datetime.datetime.fromisoformat(value)
            query = query.filter(operation(getattr(model, prop), simple_query["value"]))
    for r_attr in inst.mapper.relationships:
        prop = r_attr.key
        if prop in raw_query:
            query = query.join(getattr(model, prop))
            if parent is None:
                parent = joinedload(getattr(model, prop))
            else:
                parent = parent.joinedload(getattr(model, prop))
            query = query.options(parent)
            query = _generate_query(
                r_attr.entity.class_, query, raw_query[prop], parent=parent,
            )

    return query
