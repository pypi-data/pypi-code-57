from sqlalchemy import create_engine, inspect, or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

Base = declarative_base()  # The declarative_base object to be used by all classes
engine = create_engine("sqlite:///data/collection.sqlite")  # Creates a SQLAlchemy base of operations
session_maker = sessionmaker(bind=engine)  # Generate reusable session factory


def init_sqlite_db(db_path: str):
    global engine
    global session_maker
    if db_path is not None:
        engine = create_engine("sqlite:///" + db_path)
        session_maker = sessionmaker(bind=engine)
    _create_all()


def _create_all():
    Base.metadata.create_all(engine)


@contextmanager
def get_session():
    session = session_maker()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


def add_all(object_type, objects, batch_size):
    """Because SQLAlchemy cannot handle Upserts without losing its
    mind, this function does it. Otherwise session.add_all would
    be great."""
    table = object_type.__table__
    keys = [key.name for key in inspect(table).primary_key]  # List of all primary keys

    # Loop through objects as batches to avoid overwhelming
    # memory constraints
    for i in range(0, len(objects), batch_size):
        # Each loop should be a separate session to avoid transient
        # or dirty data
        with get_session() as session:
            batch = objects[i:i + batch_size]

            # Collect the value of each object for a given key and store it as a list for that key
            # [{name: obj1.name, id: obj1.id}, {name: obj2.name, id: obj2.id}]
            filter_values = [{key: getattr(obj, key) for key in keys} for obj in batch]

            # Create a SQLAlchemy filter list based on filter_values
            filter_list = [and_(
                *[getattr(getattr(object_type, key), "__eq__")(value)
                  for key, value in val.items()])
                for val in filter_values]

            # Get a list of all matching objects in the database to avoid integrity issues
            exists_query = session.query(object_type).filter(or_(*filter_list))
            new_list = [obj for obj in batch
                        if obj not in exists_query.all()]

            # Now filter insert_list for duplicates
            insert_list = list(_primary_key_deduplicate(keys, new_list))
            session.add_all(insert_list)


def get_all(object_type, filters):
    with get_session() as session:
        q = session.query(object_type).filter_by(**filters).all()
        res = [_refresh_obj(session, item) for item in q]
        session.expunge_all()
        return res


def _refresh_obj(session, obj):
    session.refresh(obj)
    return obj


def _primary_key_deduplicate(keys, dup_list):
    """Generator providing items that are not duplicates"""
    seen = set()
    for item in dup_list:
        compare = tuple(getattr(item, key) for key in keys)
        if compare not in seen:
            seen.add(compare)
            yield item
