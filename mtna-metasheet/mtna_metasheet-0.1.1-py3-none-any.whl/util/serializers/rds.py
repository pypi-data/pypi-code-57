"""RDS Serializer"""
from __future__ import print_function

from collections import OrderedDict
import json
import sys
import re

#
# RECORD LAYOUTS
#
def generateRecordLayout(resource, workspace, file=sys.stdout,
                         extended=True, create=False):
    """Generates Stat/Transfer code for importing file. @format can be fixed|delimted|csv """
    # Init
    bank = resource.getBank()
    id = resource.getId()

    rds = {}
    rds_metadata = OrderedDict()
    rds["metadata"] = rds_metadata

    print("RDS: Generating Record "+id)

    # VARIABLES
    rds_vars = OrderedDict()
    rds_metadata["variables"] = rds_vars
    rds_vars_res = []
    rds_vars["resources"] = rds_vars_res

    classifications = {} # the classification references and resources used by this layout.
    for layout in workspace.getResources(type="layout", bank=id):
        rds_var = OrderedDict() # new variable
        rds_vars_res.append(rds_var) # add to the dictionnary
        props = layout.getProperties().copy() # working copy of the properties for processing

        rds_var["id"] = layout.getPropertyValue("id")
        del props["id"]

        if props.get("name[rds]"):
            rds_var["name"] = layout.getPropertyValue("name[rds]")
            del props["name[rds]"]
        elif props.get("name"):
            rds_var["name"] = layout.getPropertyValue("name")
            del props["name"]

        if create:
            # storage type
            rds_var["storageType"] = "TEXT"
            if props.get("datatype[rds]"):
                rds_var["storageType"] = layout.getPropertyValue("storageType[rds]")
                del props["datatype[rds]"]
            elif props.get("datatype"):
                if re.match("[Nn]", layout.getPropertyValue("datatype")):
                    rds_var["storageType"] = "NUMERIC"
                del props["datatype"]
        else:
            pass
        #decimals
        if props.get("decimals"):
            rds_var["decimals"] = layout.getPropertyValue("decimals")
            del props["decimals"]

        if props.get("name[label]"):
            rds_var["label"] = layout.getPropertyValue("name[label]")
            del props["name[label]"]

        if props.get("width"):
            rds_var["width"] = layout.getPropertyValue("width")
            del props["width"]

        # variable classification
        if props.get("classification"):
            ref = layout.getPropertyValue("classification")
            classification = workspace.resolve(ref, type="classification")
            if classification:
                # generate the reference
                rds_var["classification"] = ref
                # add to set
                if ref not in classifications:
                    classifications[ref] = classification
            else:
                raise RuntimeError("Error resolving classification for "+layout.source)
        else:
            pass

    # CLASSIFICATIONS
    if classifications:
        rds_classifications = OrderedDict()
        rds_metadata["classifications"] = rds_classifications
        rds_classifications_res = []
        rds_classifications["resources"] = rds_classifications_res

        for ref, classification in classifications.items():
            rds_classfn = OrderedDict()
            rds_classifications_res.append(rds_classfn)
            rds_classfn["id"] = classification.getId()

            rds_codes = OrderedDict()
            rds_classfn["codes"] = rds_codes

            rds_rlassfn_res = []
            rds_codes["resources"] = rds_rlassfn_res
            # codes
            for code in workspace.getResources(bank=classification.getId(), type="code"):
                rds_code = OrderedDict()
                rds_rlassfn_res.append(rds_code)
                rds_code["value"] = str(code.getPropertyValue("value"))
                rds_code["label"] = code.getName()
            ###
        ###
    else:
        pass # no classifications


    # write file
    print(json.dumps(rds, indent=4), file=file)


def escape(value):
    """RDS string escaping"""
    return value.replace('"', '\\\"')
