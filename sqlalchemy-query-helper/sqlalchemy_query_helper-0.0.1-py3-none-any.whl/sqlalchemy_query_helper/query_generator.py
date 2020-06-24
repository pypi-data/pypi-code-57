from sqlalchemy import inspect


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


def _generate_query(model, query, raw_query):
    inst = inspect(model)
    for c_attr in inst.mapper.column_attrs:
        prop = c_attr.key
        if prop in raw_query:
            simple_query = raw_query[prop]
            operation = op_mapping[simple_query["op"]]
            query = query.filter(operation(getattr(model, prop), simple_query["value"]))
    for r_attr in inst.mapper.relationships:
        prop = r_attr.key
        if prop in raw_query:
            query = query.join(getattr(model, prop))
            query = _generate_query(r_attr.entity.class_, query, raw_query[prop])

    return query
