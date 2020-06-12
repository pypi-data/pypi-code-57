from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
from db_session import db_engine

# Graph with pydot

graph = create_schema_graph(
    metadata=MetaData(db_engine),
    show_datatypes=True,
    show_indexes=True,
    rankdir='LR',
    concentrate=False)

graph.write_png('collector_schema.png')
