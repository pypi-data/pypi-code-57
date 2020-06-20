import math
import os
import pickle
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from littleutils import retry
from sqlalchemy import Column, DateTime, Integer, LargeBinary, Text, create_engine, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import (
    InterfaceError,
    InternalError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

from fn_station.utils import rows_to_dicts

from .queries import QueryStore


class FilePickleBlobStoreMixin(QueryStore):
    def __init__(self, root):
        self.root = Path(root)

    def store(self, query_id, path, obj):
        storage_path = self.root / str(query_id) / path
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(storage_path, "wb") as f:
            pickle.dump(obj, f)

    def get(self, query_id, path):
        storage_path = self.root / str(query_id) / path
        with open(storage_path, "rb") as f:
            return pickle.load(f)

    def store_parameters(self, query_id, parameters):
        return self.store(query_id, "parameters.pkl", parameters)

    def get_parameters(self, query_id):
        return self.get(query_id, "parameters.pkl")

    def store_signatures(self, query_id, signatures):
        return self.store(query_id, "signatures.pkl", signatures)

    def get_signatures(self, query_id):
        return self.get(query_id, "signatures.pkl")

    def store_result(self, query_id, result_name, result):
        return self.store(query_id, f"results/{result_name}.pkl", result)

    def get_result(self, query_id, result_name):
        return self.get(query_id, f"results/{result_name}.pkl")

    def store_definitions(self, query_id, definitions):
        return self.store(query_id, "definitions.pkl", definitions)

    def get_definitions(self, query_id):
        return self.get(query_id, "definitions.pkl")


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__dict__.get("__name__", cls.__name__).lower()


Base = declarative_base(cls=Base)


class ComposerQuery(Base):
    id = Column("id", Integer, primary_key=True)
    client_id = Column(Text)
    composer_name = Column(Text)
    user = Column(Text)
    timestamp = Column(DateTime)


# Based on https://docs.sqlalchemy.org/en/latest/errors.html#error-dbapi
retry_db = retry(3, (InterfaceError, OperationalError, InternalError, ProgrammingError))


class SQLAlchemyEntryStoreMixin:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)

        def session_scope():
            """Provide a transactional scope around a series of operations."""
            session = self.Session()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

        self.session_scope = contextmanager(session_scope)

    def setup(self):
        super().setup()
        Base.metadata.create_all(self.engine)

    def store_query_entry(self, composer_name, client_id):
        with self.session_scope() as session:
            query = ComposerQuery(
                client_id=client_id,
                composer_name=composer_name,
                timestamp=datetime.now(),
            )
            session.add(query)
            session.commit()
            return query.id

    def list_query_entries(
        self, page, id=None, composer_name=None, client_id=None, user=None, date=None
    ):
        cq = ComposerQuery
        with self.session_scope() as session:
            query = session.query(ComposerQuery)
            if id:
                query = query.filter(cq.id == id)
            if composer_name:
                query = query.filter(cq.composer_name.ilike(f"%{composer_name}%"))
            if client_id:
                query = query.filter(cq.client_id.ilike(f"%{client_id}%"))
            if user:
                query = query.filter(cq.client_id.ilike(f"%{user}%"))
            if date:
                query = query.filter(func.date(cq.timestamp) == date)

            PAGE_SIZE = 30
            num_pages = math.ceil(query.count() / PAGE_SIZE)
            page = min(page, num_pages)
            return (
                rows_to_dicts(
                    query.order_by(-cq.id)
                    .limit(PAGE_SIZE)
                    .offset((page - 1) * PAGE_SIZE)
                ),
                num_pages,
            )
