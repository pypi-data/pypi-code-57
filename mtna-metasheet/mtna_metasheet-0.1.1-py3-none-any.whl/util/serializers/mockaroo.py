#
# MOCKAROO GENERATOR
# runtime options (-mockopts):
# - id=<nnn>: a existing schema numeric identifier (for update instead of create)
#
# metasheet columns:
# - mock[type]: Column data type (see https://api.mockaroo.com/api/types?key={{apiKey}})
# - mock[fx]: Column formula (see https://mockaroo.com/help/formulas)
# - mock[min]: min value for Number (default 1)
# - mock[max]: maxn value for Number (default 100)
#

from __future__ import print_function
import re
import json
import os.path
import sys

import xml.etree.ElementTree as ET
import xml.sax.saxutils as saxutils

mockaroo_types = None

def generateRecordLayout(record,workspace,
                         name=None, # the schema name. Will use record layout id as default.
                         file=sys.stdout,
                         options=[]):
    """Generates Mockaroo JSON schema."""
    # Generate
    print("Mockaroo: Generating Record "+record.getReference())
    record.dump()

    # Init
    id = record.getId()
    if not name: name = record.getReference()

    # parse options
    mock_options={}
    for option in options:
        tokens = option.split("=")
        mock_options[tokens[0]] = tokens[1] if len(tokens)>1 else None
    #print(mock_options)

    # setup
    mock = {}
    if("id" in mock_options):
        mock["id"] = int(mock_options["id"]);
    mock["num_rows"] = 1000
    mock["file_format"]="csv"
    mock["name"]=name
    mock["include_header"]=True
    mock_cols = []
    mock["columns"]=mock_cols

    # variables
    for layout in workspace.getResources(type="layout", bank=record.getReference()):
        mock_col = {}
        mock["columns"].append(mock_col)
        mock_col["name"]=layout.getName()
        mock_col["null_pct"] = layout.getFacetedPropertyValue("mock[blank]",fallback=False) or 0
        mock_col["null_pct"] = int(mock_col["null_pct"])
        mock_col["type"] = layout.getFacetedPropertyValue("mock[type]",fallback=False) or "Blank"

        if layout.getPropertyValue("classification"):
            # Custom List
            mock_col["type"]="Custom List"
            mock_col["values"]=[]
            classification = workspace.resolve(
                layout.getPropertyValue("classification"), "classification")
            if classification:
                for code in workspace.getResources(
                        bank=classification.getBank()+"."+classification.getId(),
                        type="code"):
                    mock_col["values"].append(str(code.getPropertyValue("value")))
            else:
                print("WARNING: classifcation "+layout.getPropertyValue("classification")+" not found for "+layout.getId())
        else:
            # read data type
            datatype = None
            if layout.hasProperty("datatype"):
                datatype=layout.getPropertyValue("datatype")
            elif layout.hasProperty("datatype[generic]"):
                datatype = layout.getPropertyValue("datatype[generic]")
            # process data type
            if datatype and re.match("^NUM.*",datatype,re.IGNORECASE):
                # Numeric
                mock_col["type"]="Number"
                mock_col["min"] = int(layout.getFacetedPropertyValue("mock[min]") or 1)
                mock_col["max"] = int(layout.getFacetedPropertyValue("mock[min]") or 100)
                mock_col["decimals"] = int(layout.getPropertyValue("decimals") or 0)
            if datatype and re.match("^INT.*",datatype,re.IGNORECASE):
                # Integer
                mock_col["type"]="Number"
                mock_col["min"] = int(layout.getFacetedPropertyValue("mock[min]") or 1)
                mock_col["max"] = int(layout.getFacetedPropertyValue("mock[min]") or 100)
                mock_col["decimals"] = 0
        # FX
        mock_col["fx"] = layout.getFacetedPropertyValue("mock[fx]") or ""

        validateColumn(mock_col)
                
    # write file
    print(json.dumps(mock,indent=4),file=file)


def validateColumn(mock_col):
    is_valid = True
    if mock_col["type"] in getMockTypes():
        pass
    else:
        print("ERROR: Invalid coulmn type",mock_col["type"])
        is_valid = False

def getMockTypes():
    global mockaroo_types
    if not mockaroo_types:
        mockaroo_types = {}
        script_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(script_dir,"mockaroo.types.json")) as json_file:
            json_types = json.load(json_file)
            for json_type in json_types["types"]:
                mockaroo_types[json_type["name"]]=json_type
    return mockaroo_types

