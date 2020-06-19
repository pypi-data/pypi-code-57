from .DataObject import DataObject
from .SchemaEntry import SchemaEntry
from .Entity import EntityCollection
from .Entity import Entity
from .LocalEntity import LocalEntity
from .Annotation import AnnotationCollection
from .Relationship import RelationshipCollection
from .SingleKeyRelationship import SingleKeyRelationship
from .Reference import ReferenceCollection
from .Attribute import Attribute
from .Annotation import Annotation
from .AttributeReference import AttributeReference
from .Partition import Partition
from .Partition import PartitionCollection
from .CsvFormatSettings import CsvFormatSettings
from .CdmDataType import DataType
from .utils import String
from .utils import dtype_converter
from datetime import datetime
from .utils import String
from .utils import dtype_converter
from .utils import to_utc_timestamp
from .utils import from_utc_timestamp
from retry.api import retry_call
import time
import random
import pandas as pd
import pytz
import numpy as np
import json
# import p#print
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config.ini'))


class Model(DataObject):
    
    def __init__(self, from_json=False, json_data=None, 
                        application=config['DEFAULT']['application'], 
                        name=config['DEFAULT']['name'], 
                        description=config['DEFAULT']['description'], 
                        version=config['DEFAULT']['version'],
                        culture=None,
                        modified_time=None):

        self.schema = [
            SchemaEntry("application", String),
            SchemaEntry("name", String),
            SchemaEntry("description", String),
            SchemaEntry("version", String),
            SchemaEntry("culture", String),
            SchemaEntry("modifiedTime", String),
            SchemaEntry("isHidden", bool),
            SchemaEntry("entities", EntityCollection),
            SchemaEntry("annotations", AnnotationCollection),
            SchemaEntry("relationships", RelationshipCollection),
            SchemaEntry("referenceModels", ReferenceCollection)
        ]
        super().__init__(self.schema)
        
        if from_json:
            self.application = json_data.get("application", None)
            self.name = json_data["name"]
            self.description = json_data.get("description", None)
            self.version = json_data["application"]
            self.culture = json_data.get("culture", None)
            self.modifiedTime = json_data.get("modifiedTime", None)
            self.isHidden = json_data.get("isHidden", None)

            self.entities = EntityCollection.fromJson(json_data["entities"])

            annotations = json_data.get("annotations", None)
            if annotations is not None:
                self.annotations = AnnotationCollection.fromJson(annotations)

            relationships = json_data.get("relationships", None)
            if relationships is not None:
                self.relationships = RelationshipCollection.fromJson(relationships)

            referenceModels = json_data.get("referenceModels", None)
            if referenceModels is not None:
                self.referenceModels = ReferenceCollection.fromJson(referenceModels)

        else:
            self.application = application
            self.name = name
            self.description = description
            self.version = version
            self.culture = culture
            self.modifiedTime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')


    def add_entity(self, entity):
        for entity_index in range(len(self.entities)):
            if self.entities[entity_index].name.lower() == entity.name.lower():
                self.entities[entity_index] = entity
                break
        else:
            self.entities.append(entity)

    def add_relationship(self, from_attribute_entity_name, from_attribute_attribute_name,
                               to_attribute_entity_name, to_attribute_attribute_name):
        from_attribute = AttributeReference()
        from_attribute.entityName = from_attribute_entity_name
        from_attribute.attributeName = from_attribute_attribute_name

        to_attribute = AttributeReference()
        to_attribute.entityName = to_attribute_entity_name
        to_attribute.attributeName = to_attribute_attribute_name

        relationship = SingleKeyRelationship()
        relationship.fromAttribute = from_attribute
        relationship.toAttribute = to_attribute
        
        self.relationships.append(relationship)
  
    @staticmethod
    def generate_entity(dataframe, name, description=None, _dtype_converter=None):
        entity = LocalEntity()
        entity.name = name
        entity.description = description
        if _dtype_converter is None:
            _dtype_converter = dtype_converter
        if isinstance(dataframe, pd.DataFrame):
            for column_name, column_datatype in (dataframe.dtypes).items():
                attribute = Attribute()
                attribute.name = column_name
                attribute.dataType = _dtype_converter.get(column_datatype, 'string')
                entity.attributes.append(attribute)
        else:
            for column_name, column_datatype in dataframe.dtypes:
                attribute = Attribute()
                attribute.name = column_name
                attribute.dataType = _dtype_converter.get(column_datatype, 'string')
                entity.attributes.append(attribute)
        return entity

    @staticmethod
    def add_annotation(name, value, obj):
        """
        Annotations can be added at root level (model.json),
        entity level or attribute level.
        obj is an object in which if "annotations" is present
        then new annotation will be added.
        """    
        annotation = Annotation()
        annotation.name = name
        annotation.value = value
        added = False
        for _annotation in obj.annotations:
            if _annotation.name.lower() == annotation.name.lower():
                _annotation.value = annotation.value
                added = True
                break
        
        if not added:
            obj.annotations.append(annotation)
        return True

    @staticmethod
    def __add_attribute_with_date(col_name, column_datatype, _dtype_converter, date_metadata=None):
        attribute = Attribute()
        attribute.name = col_name
        if date_metadata is None:
            column_datatype = str(column_datatype)
            datatype_obj = DataType(_dtype_converter.get(column_datatype, 'string'))
            attribute.dataType = datatype_obj
        else:
            attribute.dataType = DataType("dateTime")  # Hard coded datetime
            for key, value in date_metadata.items():
                if not value == col_name:
                    Model.add_annotation(key, value, attribute)
        return attribute
  
    @staticmethod
    def __preprocess_dataframe_totimestamp(entity, dataframe, fn=None, lit=None):
        attributes = entity.attributes
        for attribute in attributes:
            if attribute.dataType.value == "dateTime":
                col_name = attribute.name
                timeformat = None
                timezone = None
                for annotation in attribute.annotations:
                    if annotation.name == "format":
                        timeformat = annotation.value
                    if annotation.name == "timezone":
                        timezone = annotation.value
                if timezone:
                    if isinstance(dataframe, pd.DataFrame):
                        dataframe[col_name] = dataframe.apply(lambda x: to_utc_timestamp(x[col_name], timeformat, timezone), axis=1)
                    elif fn is not None:
                        dataframe = dataframe.withColumn(col_name, fn(dataframe[col_name], lit(timeformat), lit(timezone)))
                    else:
                        raise AssertionError("For Spark Passed fn argument should not be null")
                elif timeformat:
                    if isinstance(dataframe, pd.DataFrame):
                        dataframe[col_name] = dataframe.apply(lambda x: to_utc_timestamp(x[col_name], timeformat), axis=1)
                    elif fn is not None:
                        dataframe = dataframe.withColumn(col_name, fn(dataframe[col_name], lit(timeformat)))
                    else:
                        raise AssertionError("For Spark Passed fn argument should not be null")
                else:
                    pass
                
        return dataframe

    @staticmethod
    def __preprocess_dataframe_fromtimestamp(entity, dataframe, fn=None, lit=None):
        attributes = entity.attributes
        for attribute in attributes:
            if attribute.dataType.value == "dateTime":
                col_name = attribute.name
                timeformat = None
                timezone = None
                offset_hours = None
                for annotation in attribute.annotations:
                    if annotation.name == "format":
                        timeformat = annotation.value
                    elif annotation.name == "timezone":
                        timezone = annotation.value
                    elif annotation.name == "offset_hour":
                        offset_hour = annotation.value

                if timezone:
                    if isinstance(dataframe, pd.DataFrame):
                        dataframe[col_name] = dataframe.apply(lambda x: from_utc_timestamp(x[col_name], timeformat, timezone), axis=1)
                    elif fn is not None:
                        dataframe = dataframe.withColumn(col_name, fn(dataframe[col_name], lit(timeformat), lit(timezone), lit(False)))
                    else:
                        raise AssertionError("For Spark Passed fn argument should not be null")
                elif timeformat:
                    if isinstance(dataframe, pd.DataFrame):
                        dataframe[col_name] = dataframe.apply(lambda x: from_utc_timestamp(x[col_name], timeformat, tz=offset_hour, offset_hour=True), axis=1)
                    elif fn is not None:
                        dataframe = dataframe.withColumn(col_name, fn(dataframe[col_name], lit(timeformat), lit(offset_hour), lit(True)))
                    else:
                        raise AssertionError("For Spark Passed fn argument should not be null")
                else:
                    pass
        return dataframe

    @staticmethod
    def generate_entity(dataframe, name, description=None, _dtype_converter=None, date_metadata=None):
        entity = LocalEntity()
        entity.name = name
        entity.description = description
        if _dtype_converter is None:
            _dtype_converter = dtype_converter

        date_columns = []
        if date_metadata is not None:
            for date_metaobject in date_metadata:
                date_columns.append(date_metaobject['col_name'])
        
        if isinstance(dataframe, pd.DataFrame):
            for column_name, column_datatype in (dataframe.dtypes).items():
                date_metaobject = None
                if column_name in date_columns:
                    date_metaobject = date_metadata[date_columns.index(column_name)]

                attribute = Model.__add_attribute_with_date(column_name, column_datatype, _dtype_converter, date_metaobject)
                entity.attributes.append(attribute)
        else:
            for column_name, column_datatype in dataframe.dtypes:
                date_metaobject = None
                if column_name in date_columns:
                    date_metaobject = date_metadata[date_columns.index(column_name)]

                attribute = Model.__add_attribute_with_date(column_name, column_datatype, _dtype_converter, date_metaobject)
                entity.attributes.append(attribute)
        return entity



    def toJson(self):
        result = dict()
        result["application"] = self.application
        result["name"] = self.name
        result["description"] = self.description
        result["version"] = self.version
        result["culture"] = self.culture
        result["modifiedTime"] = self.modifiedTime
        result["isHidden"] = self.isHidden
        result["entities"] = self.entities.toJson()
        result["annotations"] = self.annotations.toJson()
        result["relationships"] = self.relationships.toJson()
        result["referenceModels"] = self.referenceModels.toJson()
        return result

    def write_to_storage(self, entity_name, dataframe, writer, number_of_partition=None, fn=None, lit=None, model_json_name="model.json", csv_delimiter=",", column_headers=False, csv_quote_style="QuoteStyle.Csv", csv_style="CsvStyle.QuoteAlways"):
        entity = None
        entity_index = -1
        for _entity_index, _entity in enumerate(self.entities):
            if _entity.name.lower() == entity_name.lower():
                entity = _entity
                entity_index = _entity_index
                break
        else:
            return AssertionError("Passed entity is not a part of current model.json")

        if number_of_partition is None:
            number_of_partition = 1
        
        entity = self.entities[entity_index]
        partitions = PartitionCollection()
        run_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        location  = '{entity_name}/{entity_name}.csv.snapshots-{run_time}'.format(entity_name=entity_name, run_time=run_time)

        dataframe = Model.__preprocess_dataframe_totimestamp(entity, dataframe, fn=fn, lit=lit)
        names_and_urls = writer.write_df(location, dataframe, number_of_partition)

        for name, url in names_and_urls:
            partition = Partition()
            partition.name = name
            partition.location = url
            partition.refreshTime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            
            csvFormatSettings = CsvFormatSettings()
            csvFormatSettings.delimiter = csv_delimiter
            csvFormatSettings.columnHeaders = column_headers
            csvFormatSettings.quoteStyle = csv_quote_style
            csvFormatSettings.csvStyle = csv_style
            
            partition.fileFormatSettings = csvFormatSettings
            partitions.append(partition)
        entity.partitions = partitions
        random_sleep_time = random.randint(1, 5)
        time.sleep(random_sleep_time)
        #print("Starting snapshot")
        #print("Writer object:", writer.get_existing)
        existing, content = retry_call(writer.get_existing, fargs=[model_json_name, model_json_name + ".snapshots"], delay=1, jitter=0.5)
        #print("Snapshot done")
        # If JSON already exists
        if existing:
            json_data, lease_id = content[0], content[1]

            # Append entities    
            for entity in EntityCollection.fromJson(json_data["entities"]):
                for old_entity in self.entities:
                    if old_entity.name.lower() == entity.name.lower():
                        break
                else:
                    self.entities.append(entity)

            # Append Annotations
            annotations = json_data.get("annotations", None)
            if annotations is not None:
                for annotation in AnnotationCollection.fromJson(annotations):
                    self.annotations.append(annotation)

            # Append relationships
            relationships = json_data.get("relationships", None)
            if relationships is not None:
                for relationship in RelationshipCollection.fromJson(relationships):
                    same = False
                    for current_relationship in self.relationships:
                        if Model.is_same_relationship(relationship, current_relationship):
                            same = True
                            break
                    if not same:
                        self.relationships.append(relationship)

            # Append Reference Models
            referenceModels = json_data.get("referenceModels", None)
            if referenceModels is not None:
                for referenceModel in ReferenceCollection.fromJson(referenceModels):
                    self.referenceModels.append(referenceModel)

            model_json = self.toJson()
            #print("Writing model.json after lock")
            writer.write_json(model_json_name, model_json, lease_id=lease_id)
        else:
            model_json = self.toJson()
            #print("Writing model.json without lock")
            writer.write_json(model_json_name, model_json, lease_id=None)
        return
    
    @staticmethod
    def is_same_relationship(first_relationship, second_relationship):
        first_from_attribute = first_relationship.fromAttribute
        second_from_attribute = second_relationship.fromAttribute
        first_to_attribute = first_relationship.toAttribute
        second_to_attribute = second_relationship.toAttribute
        same_from = False
        same_to = False
        if first_from_attribute.entityName.lower() == second_from_attribute.entityName.lower() and first_from_attribute.attributeName.lower() == second_from_attribute.attributeName.lower():
            same_from = True

        if first_to_attribute.entityName.lower() == second_to_attribute.entityName.lower() and first_to_attribute.attributeName.lower() == second_to_attribute.attributeName.lower():
            same_to = True
        
        if same_from and same_to:
            return True
        return False

    def read_from_storage(self, entity_name, reader, fn=None, lit=None):
        entity = None
        entity_index = -1
        for _entity_index, _entity in enumerate(self.entities):
            if _entity.name.lower() == entity_name.lower():
                entity = _entity
                entity_index = _entity_index
                break
        else:
            return AssertionError("Passed entity is not a part of current model.json")

        entity = self.entities[entity_index]
        
        locations = []
        for partition in entity.partitions:
            locations.append(partition.location)

        headers = []
        dtypes = []
        attributes = entity.attributes
        for attribute in attributes:
            headers.append(attribute.name)
            dtypes.append({attribute.name: attribute.dataType})

        dataframe = reader.read_df(locations, headers, dtypes)
        dataframe = Model.__preprocess_dataframe_fromtimestamp(entity, dataframe, fn=fn, lit=lit)
        return dataframe
