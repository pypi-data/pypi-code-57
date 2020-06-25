import sqlalchemy as sa

from sqlalchemy.engine import reflection
from sqlalchemy.dialects import mssql

from datainventory.core import Access
from datainventory.core import Level
from datainventory.core import Manifest
from datainventory.core import Resource
from datainventory.core import Model
from datainventory.core import Property
from datainventory.core import set_computed_values


TYPES = {
    sa.Integer: 'integer',
    sa.String: 'string',
    sa.Date: 'date',
    sa.DateTime: 'datetime',
    sa.Numeric: 'number',
    sa.LargeBinary: 'binary',

    # MSSQL types
    mssql.IMAGE: 'image',
    mssql.TIMESTAMP: 'datetime',
    mssql.BIT: 'boolean',
    mssql.MONEY: 'number',
    mssql.UNIQUEIDENTIFIER: 'string',  # 16-byte GUID
}


def inspect(manifest: Manifest, resource: Resource, engine, schema=None):
    insp = reflection.Inspector.from_engine(engine)
    for table in insp.get_table_names(schema):
        pkey = insp.get_pk_constraint(table, schema)
        if pkey:
            pkeys = pkey['constrained_columns']
        else:
            pkeys = []
        model = Model()
        model.name = table.lower()
        model.source = table
        model.ref = [pk.lower() for pk in pkeys]
        model.properties = {}
        model.resource = resource
        model.comp.access = Access.protected
        inspect_table(model, insp, table, schema, pkeys)
        set_computed_values(model)
        manifest.models[model.name] = model


def inspect_table(model: Model, insp, table, schema, pkeys):
    refs = {}
    fkeys = insp.get_foreign_keys(table, schema)
    for fkey in fkeys:
        for col, ref in zip(fkey['constrained_columns'], fkey['referred_columns']):
            assert col not in refs, (table, col, refs)
            refschema = fkey['referred_schema']
            reftable = fkey['referred_table'].lower()
            ref = ref.lower()
            if schema and refschema and refschema != schema:
                refs[col] = f'{refschema}.{reftable}[{ref}]'
            else:
                refs[col] = f'{reftable}[{ref}]'

    for column in insp.get_columns(table, schema):
        source = column['name']
        prop = Property(source.lower(), model)
        prop.source = source
        if source in refs:
            prop.type = 'ref'
        else:
            prop.type = detect_type(column['type'])
        prop.ref = refs.get(source)
        if prop.level is None:
            if source in pkeys or source in refs:
                prop.level = Level.identifiable
            else:
                prop.level = Level.open
        prop.comp.level = prop.level
        prop.comp.access = prop.access or Access.protected


def detect_type(ctype):
    for ct in ctype.__class__.__mro__:
        if ct in TYPES:
            return TYPES[ct]
    raise Exception("Can't detect column {column.name} type. Type MRO:\n - " + '\n - '.join(
        ct.__name__
        for ct in ctype.__class__.__mro__
    ))
