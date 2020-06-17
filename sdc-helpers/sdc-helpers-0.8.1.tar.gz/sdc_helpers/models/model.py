"""
   SDC Base model module
"""
# coding=utf-8
# pylint: disable=invalid-name
import json
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
models_namespace = 'sdc_helpers.models'

class Model(Base):
    """
       SDC base model class
    """
    # pylint: disable=too-few-public-methods, no-member
    __abstract__ = True

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def __init__(self, **kwargs):
        """
            Creation of abstract model
        """
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        properties = kwargs.get('properties')
        if properties is not None:
            if isinstance(properties, dict):
                properties = json.dumps(properties)
            self.properties = properties

    def to_dict(self) -> dict:
        """
            Convert model object to dictionary
        """
        return {
            column.name: getattr(self, column.name, None)
            for column in self.__table__.columns
        }
