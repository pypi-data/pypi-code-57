"""MySQL SQL Serializer"""
from __future__ import print_function

from collections import OrderedDict
import json
import sys
import re

#
# RECORD LAYOUTS
#
def generateRecordLayouts(workspace, file=sys.stdout, options=[]):
    for resource in workspace.getResources(type="record"):
        generateRecordLayout(resource, workspace, file=file, options=options)

def generateRecordLayout(record, workspace, file=sys.stdout, options=[]):
    """Generates MySQL SQL."""
    # Init
    id = record.getId()
    
    # Generate
    print("MySQL: Generating Record "+record.getReference())


    # Init
    bank = record.getBank()
    id = record.getId()

    # Validate
    validated = True
    if bank is None:
        print(record.source, "Missing bank")
        validated = False
    if id is None:
        print(record.source, "Missing id")
        validated = False


    # Generate
    if validated:
        print("MySQL: Generating table for "+record.getReference())
        print(file=file)

        print("# ",record.getReference(),  file=file)            
        print("create table if not exists `", id, "`(", file=file, sep='')

        # Process matching layout entries
        layouts = workspace.getResources(type="layout", bank=bank+"."+id)
        layouts_count = len(layouts)
        for index, layout in enumerate(layouts):
            varbank = layout.getPropertyValue("varbank")
            variable = layout.getPropertyValue("id")
            varRef = variable
            if varbank:
                varRef = varbank+"."+varRef
            # Validate
            validated = True
            # Generate
            if validated:
                layout.dump()
                sql_name = layout.getFacetedPropertyValue("name[mysql]")
                if layout.hasProperty("datatype[mysql]"):
                    sql_datatype = layout.getFacetedPropertyValue("datatype[mysql]")
                else:
                    sql_datatype = infer_mysql_datatype(layout)
                sql = "`"+sql_name+"` "+sql_datatype
                if index != layouts_count-1:
                    sql += ","
                print(sql,file=file)
        print(")", file=file) # end create table

def infer_mysql_datatype(layout):
    datatype = layout.getFacetedPropertyValue("datatype").lower()
    width = layout.getFacetedPropertyValue("width")
    sqltype = None
    if datatype == "text":
        sqltype = "text"
    elif datatype == "string":
        if width is None:
            width = 256
        sqltype = "varchar("+str(width)+")"
    elif datatype.startswith("int"):
        sqltype = "int"
    elif datatype.startswith("num") or datatype.startswith("decimal"):
        if width is None:
            sqltype = "double"
        else:
            decimals = layout.getFacetedPropertyValue("decimals")
            if decimals is None:
                decimals = "0"
            sqltype = "decimal("+str(width)+","+str(decimals)+")"
    elif datatype == "date":
        sqltype = "date"
    elif datatype.startswith("bool"):
        sqltype = "boolean"
    return sqltype

def escape(str):
    """SQL string escaping"""
    return str
    