"""
   SDC Base model module
"""
# coding=utf-8
# pylint: disable=invalid-name
import json
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
models_namespace = 'sdc_helpers.models'
json_date_format = '%Y-%m-%d %H:%M:%S'

class Model(Base):
    """
       SDC base model class
    """
    # pylint: disable=too-few-public-methods, no-member
    __abstract__ = True
    read_only = False

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def __init__(self, **kwargs):
        """
            Creation of abstract model
        """
        model_id = kwargs.get('id')
        if model_id is not None:
            self.id = model_id
        read_only = kwargs.get('read_only')
        if read_only is not None:
            self.read_only = read_only
        self.created_at = self.convert_json_datetime(kwargs.get('created_at'))
        self.updated_at = self.convert_json_datetime(kwargs.get('updated_at'))
        properties = kwargs.get('properties')
        if properties is not None:
            if isinstance(properties, str):
                properties = json.loads(properties)
            self.properties = properties

    def to_dict(self) -> dict:
        """
            Convert model object to dictionary
        """
        return {
            column.name: getattr(self, column.name, None)
            for column in self.__table__.columns
        }

    @staticmethod
    def convert_json_datetime(date_string):
        """
            Convert JSON string date to datetime object

            args:
                date_string(str): JSON date string
        """
        if date_string is None:
            return None

        return datetime.strptime(date_string, json_date_format)
