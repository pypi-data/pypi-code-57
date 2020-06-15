"""RML Serializer"""
from __future__ import print_function

import sys

# TODO: add parameter to specify banks to be used as variables instead of literals, or auto-generate

#
# BANKS
#
def generateBanks(workspace,root=None,file=sys.stdout,options=[]):
    # TODO: generate create bank statements
    pass
#
# CLASSIFICATIONS
#
def generateClassifications(workspace, file=sys.stdout, options=[]):
    for resource in workspace.getResources(type="classification"):
        generateClassification(resource, workspace, file=file, options=options)

def generateClassification(resource, workspace, file=sys.stdout, options=[]):
    # Init
    bank = resource.getBank()
    id = resource.getId()

    # Validate
    validated = True
    if bank is None:
        print(resource.source, "Missing bank")
        validated = False
    if id is None:
        print(resource.source, "Missing bank id")
        validated = False

    # Generate
    if validated:
        print("RML: Generating classification "+bank+"."+id)
        print(file=file)
        print("// ", bank, ".", id, sep='', file=file)
        print("create classification", id, "in", bank, ";", file=file)

        # set local properties
        keys = resource.getLocalPropertiesKeys() - set({"bank", "id"})
        props = []
        for key in sorted(keys):
            entry = resource.getPropertyEntry(key)
            map = entry.get("map")
            # check if this is an "rml" property
            rml_map = map.get("rml")
            if rml_map:
                value = entry.get("value")
                if not isinstance(value, str):
                    value = str(value)
                if rml_map != "*":
                    key = rml_map
                props.append(key+"=\""+escape(value)+"\"")
        if props:
            print("let", id, ','.join(props), ";", file=file)

        # Process matching code entries
        count = 0
        for code in workspace.getResources(type="code", bank=bank+"."+id):
            count += 1
            # Init
            value = code.getPropertyValue("value")
            label = str(code.getName())

            #print(value,label)
            # Validate
            validated = True

            # Generate
            if validated:
                print("create code ", value, ",\"", escape(label), "\"", ";", sep='', file=file)
            else:
                print("CODE VALIDATION ERROR")
                print(code.properties)
        print("--> "+str(count)+" code(s)")
#
# RECORD LAYOUTS
#
def generateRecordLayouts(workspace, file=sys.stdout, options=[]):
    for resource in workspace.getResources(type="record"):
        generateRecordLayout(resource, workspace, file=file, options=options)

def generateRecordLayout(record, workspace, file=sys.stdout, options=[]):
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
        print("RML: Generating Record "+record.getReference())
        print(file=file)

        print("//",record.getReference(),  file=file)
        print("create recordlayout", id, "in", bank, ";", file=file)

        # Primary key
        if record.hasProperty("pk"):
            key = record.getPropertyValue("pk")
            vars = key.split("+")
            rml_key = ",".join(vars)
            print("RML: primary key "+rml_key)
            print("create recordlayoutKey PRIMARY", id, rml_key, file=file)

        # Foreign keys
        if record.hasProperty("fk"):
            fk = record.getPropertyValue("fk")
            keys = fk.split(";")
            for key in keys:
                vars = key.split("+")
                rml_key = ",".join(vars)
                print("RML: foreign key "+rml_key)
                print("create recordlayoutKey FOREIGN", id, rml_key, file=file)

        # set local properties
        keys = record.getLocalPropertiesKeys() - set({"bank", "id"})
        props = []
        for key in sorted(keys):
            entry = record.getPropertyEntry(key)
            map = entry.get("map")
            # check if this is an "rml" property
            rml_map = map.get("rml")
            if rml_map:
                value = entry.get("value")
                if not isinstance(value, str):
                    value = str(value)
                if rml_map != "*":
                    key = rml_map
                props.append(key+"=\""+escape(value)+"\"")
        if props:
            print("let", id, ','.join(props), ";", file=file)

        # Process matching layout entries
        for layout in workspace.getResources(type="layout", bank=bank+"."+id):
            # Init

            #rlbank = layout.getPropertyValue("rlbank")
            #lbank = layout.getPropertyValue("bank")
            #recRef = layout.getPropertyValue("bank")
            #if rlbank:
            #    recRef = rlbank+"."+recRef
            #else:
            #    recRef = bank+"."+recRef

            varbank = layout.getPropertyValue("varbank")
            variable = layout.getPropertyValue("id")
            varRef = variable
            if varbank:
                varRef = varbank+"."+varRef

            # Validate
            validated = True

            # Generate
            if validated:
                # Variable can be either a simple reference or locally defined
                # Check if there are local properties beyond simple references
                referenceProps = {"id", "rlbank", "bank", "varbank", "basis"}
                propDiff = set(layout.getLocalPropertiesKeys()) - referenceProps
                if len(propDiff):
                    # create the variable locally
                    print("create variable", variable, "in", record.getReference(), ";", file=file)
                    # set local properties
                    keys = layout.getLocalPropertiesKeys() - (referenceProps-{"basis"}) # bring basis back in 
                    props = []
                    for key in sorted(keys):
                        entry = layout.getPropertyEntry(key)
                        map = entry.get("map")
                        # check if this is an "rml" property
                        rml_map = map.get("rml")
                        if rml_map:
                            value = entry.get("value")
                            if not isinstance(value, str):
                                value = str(value)
                            if rml_map != "*":
                                key = rml_map
                            props.append(key+"=\""+escape(value)+"\"")
                    if props:
                        print("let", variable, ','.join(props), ";", file=file)

                else:
                    # add the variable basis as a reference
                    print("add variable", layout.getPropertyValue("basis"), "to", record.getReference(), ";", file=file)
            else:
                print("LAYOUT VALIDATION ERROR")
                print(layout.properties)

    else:
        print("RECORD VALIDATION ERROR")
        print(record.properties)


#
# RULES
#
def generateRules(workspace,file=sys.stdout,autogen=True, options=[]):
    # generate explicit rules
    print("RML: Generating explicit rules...")
    for resource in workspace.getResources(type="rule"):
        generateRule(resource,workspace,file=file,options=options)
    # autogen 
    if autogen:
        print("RML: Auto-generating implicit rules...")
        print("#",file=file)
        print("# AUTO GENERATED RULES",file=file)
        print("#",file=file)
        # variables
        for resource in workspace.getResources(type="variable"):
            targetId = resource.getId()
            if resource.getBank(): targetId = resource.getBank()+"."+targetId
            if "classification" in resource.getLocalPropertiesKeys():
                statement = "assert null(?) or validCode(?);"
                statement = statement.replace("?",targetId)
                print(file=file)
                print("#",targetId,"[autogen]",file=file)
                print(statement,file=file)
                
def generateRule(resource,workspace,file=sys.stdout, options=[]):
    # Init
    bank = resource.getBank()
    id = resource.getId()
    
    # Validate
    validated=True
    if not resource.hasProperty("assert"):
        print(resource.source,"Missing assert statement")
        validated=False

    if validated:
        #print("RML: Generating Rule "+resource.source)

        targetId = resource.getPropertyValue("resource")
        if bank:
            targetId = bank+"."+targetId
        
        assertion = resource.getPropertyValue("assert")
        if "?" in assertion:
            assertion = assertion.replace("?",targetId)

        condition = resource.getPropertyValue("condition")
        if condition and "?" in condition:
            condition = condition.replace("?",targetId)

        onFail = resource.getPropertyValue("onFail")
        if onFail and "?" in onFail:
            onFail = onFail.replace("?",targetId)

        onPass = resource.getPropertyValue("onPass")
        if onPass and "?" in onPass:
            onPass = onPass.replace("?",targetId)
        
        contextVariables = resource.getPropertyValue("contextVariables")
        if contextVariables and "?" in contextVariables:
            contextVariables = contextVariables.replace("?",targetId)
        
        statement = "assert "+assertion
        if condition: statement += " if "+condition
        if onFail: statement += " onFail "+onFail
        if onPass: statement += " onPass "+onPass
        if contextVariables: statement += " contextVariables "+contextVariables
        statement += ";"

        print(file=file)
        print("//",targetId,file=file)
        print(statement,file=file)

    else:
        print("RML: RULE VALIDATION ERROR!")
        resource.dump()


#
# VARIABLES
#
def generateVariables(workspace, file=sys.stdout, options=[]):
    print("RML: Generating variables...")
    for resource in workspace.getResources(type="variable"):
        generateVariable(resource,workspace,file,options)

def generateVariable(resource,workspace, file=sys.stdout, options=[]):
    # Init
    bank = resource.getBank()
    id = resource.getId()
    if id is None:
        id = resource.getName()
    # Validate
    validated=True
    if id is None:
        print(resource.source,"Missing id")
        validated=False
    if bank is None:
        print(resource.source,"Missing bank")
        validated=False
    if resource.hasProperty("classification"):
        classification = workspace.resolve(resource.getPropertyValue("classification"),"classification")
        if not classification: 
            print("WARNING: classifcation "+resource.getPropertyValue("classification")+" not found for "+resource.getId())
    # Generate
    if validated:
        #print("RML: Generating variable "+bank+"."+id)
        print(file=file)
        print("// ",bank,".",id,sep='',file=file)

        # create the variable
        if 'update_mode' not in options:
            print("create variable",id,"in",bank,";",file=file)
        if 'update_mode' in options:
            print("remove",id,"classification;",file=file)

        # set local properties
        keys=resource.getLocalPropertiesKeys() - set({"bank","id"})
        props=[]
        for key in sorted(keys):
            entry = resource.getPropertyEntry(key)
            map = entry.get("map")
            # check if this is an "rml" property
            rml_map = map.get("rml")
            if rml_map:
                value = entry.get("value")
                if not isinstance(value,str):
                    value = str(value)
                if rml_map != "*":
                    key = rml_map
                props.append(key+"=\""+escape(value)+"\"")
        if props:
            print("let",id,','.join(props),";",file=file) 

def escape(str):
    """RML string escaping"""
    str = str.replace('"','\\\"')
    #str = str.replace('\n','\\n')
    return str
    
