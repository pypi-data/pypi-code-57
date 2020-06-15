from __future__ import print_function

from collections import OrderedDict
import json
import re
import sys

#
# GOOGLE BIG QUERY
#

def generateRecordLayout(resource,workspace,
                         name=None, # the schema name. Will use record layout id as default.
                         format="json",
                         file=sys.stdout,
                         instance=None,
                         useClassificationBank=False):
    """Generates BigQuery code for creating and importing file. @format can be json|text"""
    # Init
    bank = resource.getBank()
    id = resource.getId()
    
    # Generate
    print("BQ: Generating Record "+id)

    # SCHEMA
    bq = OrderedDict()
    if not name: name = id 
    bq["name"]=name
    bq["type"]="RECORD"

    # FIELDS
    fields=[]
    bq["fields"]=fields
    for layout in workspace.getResources(type="layout",bank=id):
        # FIELD
        field = OrderedDict()
        # NAME
        field["name"]=layout.getName()
        # TYPE
        type="STRING"
        datatype=None

        if layout.hasProperty("datatype[bq]"):
            type=layout.getPropertyValue("datatype[bq]")
        elif layout.hasProperty("datatype"):
            datatype=layout.getPropertyValue("datatype")
        elif layout.hasProperty("datatype[generic]"):
            datatype = layout.getPropertyValue("datatype[generic]")
            
        if datatype and re.match("^N.*",datatype,re.IGNORECASE):
            type="FLOAT64"
            if layout.hasProperty("decimals") and int(layout.getPropertyValue("decimals"))==0:
                type="INTEGER"
        elif datatype and re.match("^DATETIME.*", datatype, re.IGNORECASE):
            type = "DATETIME"
        elif datatype and re.match("^DATE.*",datatype,re.IGNORECASE):
            type = "DATE"
        elif datatype and re.match("^TIME.*",datatype,re.IGNORECASE):
            type = "TIME"

        field["type"]=type
        # DESCRIPTION
        if layout.getLabel():
            field["description"]=layout.getLabel()
        # ADD
        fields.append(field)

    # write file
    print(json.dumps(bq,indent=4),file=file)

def escape(str):
    """RML string escaping"""
    return str.replace('"','\\\"')
    
