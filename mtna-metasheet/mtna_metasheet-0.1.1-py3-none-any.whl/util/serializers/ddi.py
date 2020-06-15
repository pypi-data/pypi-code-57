from __future__ import print_function

import re
import sys

import xml.etree.ElementTree as ET
import xml.sax.saxutils as saxutils

#
# DDI
#

def generateRecordLayout(record,workspace,
                         name=None, # the schema name. Will use record layout id as default.
                         version="2.5",
                         file=sys.stdout,
                         instance=None,
                         useClassificationBank=False):
    """Generates DDI-XML."""
    record.dump()
    # Init
    id = record.getId()
    
    # Generate
    print("DDI: Generating Record "+record.getReference())

    # SCHEMA
    if not name: name = record.getReference()

    if float(version) < 3:
        # codeBook
        codeBook = ET.Element('codeBook',{"version":version})
        tree = ET.ElementTree(codeBook) 
        if float(version) < 2.5:
            codeBook.set("xmlns","")
        else:
            codeBook.set("xmlns","ddi:codebook:2_5")

        # stdyDscr
        stdyDscr = ET.SubElement(codeBook,"stdyDscr")
        citation = ET.SubElement(stdyDscr,"citation")
        titlStmt = ET.SubElement(citation,"titlStmt")
        titl = ET.SubElement(titlStmt,"titl")
        titl.text = id

        # fileDscr
        fileDscr = ET.SubElement(codeBook,"fileDscr")
        fileDscr.set("ID",id)
        fileTxt = ET.SubElement(fileDscr,"fileTxt") 
        labl = ET.SubElement(fileTxt,"fileName")
        labl.text=record.getId()

        # dataDscr
        dataDscr = ET.SubElement(codeBook,"dataDscr")

        # variable groups
        varGroups = {}
        for layout in workspace.getResources(type="layout", bank=record.getReference()):
            # detect all groups names for this layout variable (facets)
            groupIds = layout.getFacetedPropertyFacets("group")
            for groupId in groupIds:
                if groupId not in varGroups:
                    # create new variable group
                    varGroups[groupId] = {"id":groupId,"groups":{}}
                varGroup = varGroups[groupId]
                # subgroup
                varSubgroupId = layout.getFacetedPropertyValue("group["+groupId+"]",fallback=False)
                if varSubgroupId not in varGroup["groups"]:
                    # create new variable subgroup
                    varGroup["groups"][varSubgroupId]={"id":varSubgroupId,"variables":{}}
                varSubgroup = varGroup["groups"][varSubgroupId]
                # add this variable to the subgroup
                varSubgroup["variables"][layout.getId()] = layout

        for varGroupId,varGroup in varGroups.items():
            # generate each group
            print("GROUP:"+varGroupId)
            varGroupElem = ET.SubElement(dataDscr,"vargrp")
            varGroupElem.set("ID",varGroupId)
            varGroupElem.set("vargrp",",".join(varGroup["groups"].keys()))
            varGroupLabl = ET.SubElement(varGroupElem,"labl")
            varGroupLabl.text=saxutils.escape(varGroupId)
            for varSubgroupId, varSubgroup in varGroup["groups"].items():
                print("   SUBGROUP: "+varSubgroupId)
                varSubgroupElem = ET.SubElement(dataDscr,"vargrp")
                varSubgroupElem.set("ID",varGroupId+"-"+varSubgroupId)
                varSubgroupElem.set("var",",".join(varSubgroup["variables"].keys()))
                varSubgroupLabl = ET.SubElement(varSubgroupElem,"labl")
                varSubgroupLabl.text=saxutils.escape(varGroupId+" "+varSubgroupId)
                for variableId, variable in varSubgroup["variables"].items():
                    print("      VARIABLE: "+variableId)


        # variables
        for layout in workspace.getResources(type="layout", bank=record.getReference()):
            # var
            var = ET.SubElement(dataDscr,"var")
            # @ID
            var.set("ID",layout.getName())
            # @name
            var.set("name",layout.getName())
            # @files
            var.set("files",id)
            # @dcml
            if layout.hasProperty("decimals"):
                var.set("dcml",str(layout.getPropertyValue("decimals")))

            # isGeospatial
            if getFlagValue(layout.getPropertyValue("isGeospatial")):
                var.set("geog","Y")
            # isTemporal
            if getFlagValue(layout.getPropertyValue("isTemporal")):
                var.set("temporal","Y")
                
            # isWeight
            if getFlagValue(layout.getPropertyValue("isWeight")):
                var.set("wgt","wgt")

            # location
            if layout.getPropertyValue("end") or layout.getPropertyValue("start") or layout.getPropertyValue("width"):
                location = ET.SubElement(var,"location")
                start = layout.getPropertyValue("start")
                end = layout.getPropertyValue("end")
                width = layout.getPropertyValue("width")
                if width: location.attrib["width"] = str(width)

            # labl
            if layout.getLabel():
                labl = ET.SubElement(var,"labl")
                labl.text=saxutils.escape(str(layout.getLabel()))
            # description
            if layout.getDescription():
                txt = ET.SubElement(var,"txt")
                txt.text=saxutils.escape(str(layout.getDescription()))

            # question
            if layout.getPropertyValue("description[question]"):
                qstn = ET.SubElement(var,"qstn")
                qstnLit = ET.SubElement(qstn,"qstnLit")
                qstnLit.text=saxutils.escape(str(layout.getPropertyValue("description[question]")))

            # catgry
            if layout.getPropertyValue("classification"):
                classification = workspace.resolve(
                    layout.getPropertyValue("classification"), "classification")
                if classification:
                    for code in workspace.getResources(
                            bank=classification.getBank()+"."+classification.getId(),
                            type="code"):
                        catgry = ET.SubElement(var, "catgry")
                        value = ET.SubElement(catgry, "catValu")
                        value.text = saxutils.escape(str(code.getPropertyValue("value")))
                        labl = ET.SubElement(catgry, "labl")
                        labl.text = saxutils.escape(str(code.getName()))
                else:
                    print("WARNING: classifcation "+layout.getPropertyValue("classification")+" not found for "+layout.getId())


            # varFormat
            varFormat = ET.SubElement(var,"varFormat")

            # varFormat: type
            type="character"
            datatype=None

            if layout.hasProperty("datatype[ddi-c]"):
                type=layout.getPropertyValue("datatype[ddi-c]")
            elif layout.hasProperty("datatype"):
                datatype=layout.getPropertyValue("datatype")
            elif layout.hasProperty("datatype[generic]"):
                datatype = layout.getPropertyValue("datatype[generic]")
            
            if datatype and re.match("^NUM.*",datatype,re.IGNORECASE):
                type="numeric"
            if datatype and re.match("^INT.*",datatype,re.IGNORECASE):
                type="numeric"
                var.set("dcml","0")
            
            varFormat.set("type",type)

            # varFormat: date/time
            if datatype and re.match("^datetime",datatype,re.IGNORECASE):
                varFormat.set("category","time")
            elif datatype and re.match("^date",datatype,re.IGNORECASE):
                varFormat.set("category","date")
            elif datatype and re.match("^time",datatype,re.IGNORECASE):
                varFormat.set("category","time")

            # varFormat: content
            if layout.hasProperty("format"):
                varFormat.text = saxutils.escape(str(layout.getPropertyValue("format")))
            
    else:
        # DDI 3
        raise RuntimeError("Unsupported DDI version "+version)    

    # write file
    tree.write(file,encoding='unicode')

def getFlagValue(value):
    flagValue = True
    if value is None or not value or value.lower() in ["false","n","no","-"]:
        flagValue = False
    return flagValue

def escape(str):
    """RML string escaping"""
    return str.replace('"','\\\"')
    
