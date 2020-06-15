"""Metassheet Core Module"""
import copy
import json
import os
import pickle
import re

from .classes import Workspace
from . import excel

# http://www.python-excel.org/
# https://openpyxl.readthedocs.io/en/default/

# GLOBALS
workspace = Workspace()
config = None


def getConfig():
    """Returns the configuration"""
    global config
    if not config:
        home = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        fileName = "config.json"
        filePath = os.path.join(home, fileName)
        with open(filePath) as f:
            config = json.load(f)
    return config


def getResourceTypeConfig(resourceType):
    return getResourceTypes().get(resourceType)


def getResourceTypes():
    """Returns a dictionnary of configured resource types"""
    return getConfig().get("resourceTypes")


def getResourceTypeSheetRegex(resourceType):
    """ Returns the regular expression matching sheet names for specified resource type"""
    config = getResourceTypeConfig(resourceType)
    if config is not None:
        return config["sheetRegex"]


def getPropertyMaps(resourceType=None):
    """Returns dictionary of global or resource type specific proprety maps"""
    if resourceType:
        return getResourceTypeConfig(resourceType).get("propertyMaps")
    else:
        return getConfig().get("propertyMaps")


def getPropertyMap(property, resourceType=None):
    for map in getPropertyMaps(resourceType):
        if property == map.get("property"):
            return map


def getWorkspace():
    return workspace


def load(file="workspace.p"):
    global workspace
    print("LOADING WORKSPACE...")
    workspace = pickle.load(open(file, "rb"))
    return workspace


def matchMap(map, value):
    # print("matching",map,value)
    m = re.match(map["regex"], value, re.IGNORECASE)
    if m:
        property = map["property"]
        if m.groups() and m.group('facets'):
            # faceted property
            property += "["+m.group('facets')+"]"
        return property


def parseFiles(files):
    for file in files:
        print("PARSING "+file)
        excel.readExcel(workspace, file)
    # POST-LOAD PROCESSING
    print("POST-PROCESSING...")
    postProcess(workspace)
    # Inheritance
    print("INHERITANCE...")
    workspace.inheritProperties()


def postProcess(workspace):
    # POST PROCESSING

    # for variables and codes, an optional clbank can be provided in which case
    # it should prepended to the reference to the bank (for code) or classification (for variables)
    print("Expanding code classification clbank.bank...")
    for import_code in workspace.getResources(type="code"):
        if import_code.hasProperty("clbank"):
            map = getPropertyMap("bank")
            import_code.setProperty("bank", import_code.getPropertyValue(
                "clbank")+"."+import_code.getPropertyValue("bank"), map)
        # the code, the id should be the value, not the name
        map = getPropertyMap("id", resourceType="code")
        import_code.setProperty("id", import_code.getPropertyValue("value"), map)

    print("Expanding variable classification clbank.bank...")
    for variable in workspace.getResources(type="variable"):
        if variable.hasProperty("clbank"):
            map = getPropertyMap("classification", resourceType="variable")
            variable.setProperty("classification", variable.getPropertyValue(
                "clbank")+"."+variable.getPropertyValue("classification"), map)

    # process classification imports
    print("Processing classification imports...")
    for classification in workspace.getResources(type="classification"):
        if classification.hasProperty("import"):
            # exclusion examples:
            # "us_fips64[(?!72).*]"
            # "us_fips64[(?!(55|72)).*]"
            rex = re.compile("(.*)\[(.*)\]")
            import_value = classification.getPropertyValue("import")
            if "[" not in import_value:
                import_value += "[.*]"
            m = rex.match(import_value)
            print("IMPORT: ",classification.getId(), import_value, m.group(1), m.group(2))
            import_classification_id = m.group(1)
            import_code_pattern = m.group(2)
            import_code_rex = None
            if import_code_pattern:
                import_code_rex = re.compile(import_code_pattern)
            # find classification to import from
            import_classification = workspace.resolve(import_classification_id,"classification")
            if import_classification:
                # loop codes
                for import_code in workspace.getResources(
                            bank=import_classification.getBank()+"."+import_classification.getId(),
                            type="code"):
                    # check code value
                    import_code_value = str(import_code.getPropertyValue("value"))
                    if import_code_rex and not import_code_rex.match(import_code_value):
                        # skip this code (does not match)
                        continue
                    # copy the code into this classification
                    import_code_copy = import_code.clone()
                    import_code_copy.setPropertyValue("bank",classification.getId())
                    # register new code
                    workspace.addResource(import_code_copy)
            else:
                print("WARNING: Import classification not found:",import_classification_id)

    # for record layout, an optional rlbank can be provided in which case
    # it should prepended to the reference to the bank
    print("Expanding record layout rlbank.bank...")
    for layout in workspace.getResources(type="layout"):    
        if layout.hasProperty("rlbank"):
            map = getPropertyMap("bank", resourceType="layout")
            layout.setProperty("bank", layout.getPropertyValue(
                "rlbank")+"."+layout.getPropertyValue("bank"), map)

    # For Layout, we need to derive the basis property for the variable and optional varbank
    # Note that the default variable bank may be set locally on the layout or on the record (default)
    for layout in workspace.getResources(type="layout"):
        # Disable basis if the varbank is set to a special character
        # This is to allow local variable definitions when there is a
        # default varbank set on the record (2020-04)
        if layout.hasProperty("varbank") and layout.getPropertyValue("varbank").startswith('-'):
            continue

        # Resolve record for this layout
        record = workspace.resolve(layout.getPropertyValue("bank"), "record")

        # Get default variable bank set on record (if any)
        defaultVarBank = None
        if record and record.hasProperty("varbank"):
            defaultVarBank = record.getPropertyValue("varbank")

        if not layout.hasProperty("basis"):
            # no basis specified
            # derive the variable basis
            basis = None
            if layout.hasProperty("name"):
                #
                if layout.hasProperty("varbank"):
                    # if there is a varbank, but no basis, set basis to the name (2020-04)
                    if not basis:
                        basis = layout.getPropertyValue("name")
                    # prefix with variable bank specified in the layout
                    basis = layout.getPropertyValue(
                        "varbank") + "." + layout.getPropertyValue("name")
                elif defaultVarBank:
                    # prefix with variable bank specified in the record
                    basis = defaultVarBank + "." + \
                        layout.getPropertyValue("name")
                else:
                    # variable has no basis
                    pass
                if basis:
                    # add basis to layout
                    layout.addProperty("basis", basis, getPropertyMap("basis"))
                else:
                    pass
            else:
                pass
        else:
            basis = layout.getPropertyValue("basis")
            if '.' not in basis:
                if layout.hasProperty("varbank"):
                    # 2018-09-18
                    # an explicit variable bank is specified for the basis
                    # --> is as a prefix for the basis
                    layout.addProperty("basis", layout.getPropertyValue(
                        "varbank")+"."+basis, getPropertyMap("basis"))
                elif defaultVarBank:
                    # If a default variable bank is set for the record
                    # add prefix to basis if not set
                    layout.addProperty(
                        "basis", defaultVarBank+"."+basis, getPropertyMap("basis"))
                pass
            pass


def save(file="workspace.p"):
    print("SAVING WORKSPACE...")
    pickle.dump(workspace, open(file, "wb"))
    return workspace
