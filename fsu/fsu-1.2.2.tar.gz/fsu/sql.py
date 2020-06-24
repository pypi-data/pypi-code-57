from collections import namedtuple
from functools import reduce
from inspect import signature, isclass

from sqlalchemy import join, select, func
from sqlalchemy.sql import and_, or_
from pydantic import BaseModel

from fsu.internal.error import ObjectNotExist, FieldNotExist, UnsupportedOperator

_LOGICAL_OPERATORS = {
    "AND" : and_,
    "OR"  : or_,
}
_COMPARISON_OPERATORS = {
    "EQ"          : lambda v : ("=", v),
    "LIKE"        : lambda v : ("like", f"%{v}%"),
    "STARTS_WITH" : lambda v : ("like", f"{v}%"),
    "IN"          : lambda v : ("in", v),
    "GT"          : lambda v : (">", v),
    "GE"          : lambda v : (">=", v),
    "LT"          : lambda v : ("<", v),
    "LE"          : lambda v : ("<=", v),
}

def _schema_names(schema):
    ret = []

    for n, p in signature(schema).parameters.items():
        if issubclass(p.annotation, BaseModel):
            ret.append((n, _schema_names(p.annotation)))
        else:
            ret.append(n)

    return ret


def _get_fields_and_tables(table_name, models, schema_names):
    if table_name not in models:
        raise ObjectNotExist(table_name)

    model = models[table_name]

    tables = [model]
    fields = []

    for n in schema_names:
        if isinstance(n, tuple):
            n, s = n
            sub_tables, sub_fields = _get_fields_and_tables(n, models, s)

            tables.extend(sub_tables)
            fields.extend(sub_fields)
        else:
            if n not in model.c:
                raise FieldNotExist(table_name, n)

            fields.append(model.c[n])

    return tables, fields


def _row_to_dict(row, table_name, models, schema_names):
    model = models[table_name]

    ret = {}

    for n in schema_names:
        if isinstance(n, tuple):
            n, s = n
            ret[n] = _row_to_dict(row, n, models, s)
        else:
            ret[n] = row[model.c[n]]

    return ret


def _get_field_from_path(path, tables):
    table_name, field_name = path[-2:]

    if table_name not in tables:
        raise ObjectNotExist(table_name)

    table = tables[table_name]

    if field_name not in table.c:
        raise FieldNotExist(table_name, field_name)

    return table, table.c[field_name]


Mapper = namedtuple("Mapper", ["select", "count", "dict", "where", "order_by"])

def make_mapper(table_name, metadata, schema_def):
    models = metadata.tables

    if isclass(schema_def) and issubclass(schema_def, BaseModel):
        schema_names = _schema_names(schema_def)
    else:
        schema_names = schema_def

    tables, fields = _get_fields_and_tables(table_name, models, schema_names)

    where_clause  = None
    order_clauses = None

    def select_():
        sql = select(fields).select_from(reduce(join, tables))

        if where_clause is not None:
            sql = sql.where(where_clause)

        if order_clauses is not None:
            sql = sql.order_by(*order_clauses)

        return sql

    def count():
        sql = select([func.count("*")]).select_from(reduce(join, tables))

        if where_clause is not None:
            sql = sql.where(where_clause)

        return sql

    def dict_(row):
        return _row_to_dict(row, table_name, models, schema_names)

    # I used a trick to assign the where_clause, there DO have some intermediate assignments
    # but will be overrided with the outermost value which is the final where clause
    def where(filter_expr):
        nonlocal where_clause

        op_name = filter_expr[0]

        if op_name in _LOGICAL_OPERATORS:
            op       = _LOGICAL_OPERATORS[op_name]
            operands = map(where, filter_expr[1])

            where_clause = op(*operands)
        elif op_name in _COMPARISON_OPERATORS:
            op_fn = _COMPARISON_OPERATORS[op_name]

            path         = [table_name, *filter_expr[1]]
            table, field = _get_field_from_path(path, models)

            if table not in tables:
                tables.append(table)

            op, value = op_fn(filter_expr[2])

            where_clause = field.op(op)(value)
        else:
            raise UnsupportedOperator(op_name)

    def order_by(order_expr):
        nonlocal order_clauses

        os = []
        for ordering, path in order_expr:
            path         = [table_name, *path]
            table, field = _get_field_from_path(path, models)

            if table not in tables:
                tables.append(table)

            if ordering == "ASC":
                os.append(field.asc())
            elif ordering == "DESC":
                os.append(field.desc())

        order_clauses = os

    mapper = Mapper(
        select   = select_,
        dict     = dict_,
        where    = where,
        order_by = order_by,
        count    = count,
    )

    return mapper


def verbose_where(table_name, metadata, filter_expr):
    tables  = metadata.tables
    op_name = filter_expr[0]

    if op_name in _LOGICAL_OPERATORS:
        op       = _LOGICAL_OPERATORS[op_name]
        operands = map(verbose_where, filter_expr[1])

        return op(*operands)
    elif op_name in _COMPARISON_OPERATORS:
        op_fn = _COMPARISON_OPERATORS[op_name]

        where_clauses = []
        path = [table_name, *filter_expr[1]]

        if len(path) > 2:
            for i in range(0, len(path) - 2):
                t0_name = path[i]
                t1_name = path[i + 1]

                if t0_name not in tables:
                    raise ObjectNotExist(t0_name)

                if t1_name not in tables:
                    raise ObjectNotExist(t1_name)

                fkey = f"{t1_name}_id"
                t0   = tables[t0_name]
                t1   = tables[t1_name]

                if fkey not in t0.c:
                    raise FieldNotExist(t0_name, fkey)

                where_clauses.append(t0.c[fkey] == t1.c.id)

        table, field = _get_field_from_path(path, tables)

        op, value = op_fn(filter_expr[2])
        where_clauses.append(field.op(op)(value))

        return and_(*where_clauses)
    else:
        raise UnsupportedOperator(op_name)
