from __future__ import print_function

import sys
import re

#
# RECORD LAYOUTS
#

def generateRecordLayout(resource,workspace,
                         format="delimited",
                         delimiter="tabs",
                         file=sys.stdout,
                         instance=None,
                         useClassificationBank=False):
    """Generates Stat/Transfer code for importing file. @format can be fixed|delimted|csv """
    # Init
    bank = resource.getBank()
    id = resource.getId()
    
    print("STS: Generating Record "+id)

    print(file=file)
    print("// ",bank,".",id,sep='',file=file)

    print(file=file)
    print("ENCODING UTF-8",file=file)

    print(file=file)
    if instance is None:
        print("// TODO: SPECIFY DATA FILE NAME/PATH BELOW",file=file)
    print("FILE ",instance,file=file)

    print(file=file)
    if format=="fixed":
        print("FORMAT fixed",file=file)
    else:
        print("FORMAT delimted",delimiter,file=file)

    # VARIABLES
    print(file=file)
    print("VARIABLES",file=file)
    nextStart=1 # use for running column width in case start/end are not provided
    classifications = {} # the classification references and resources used by this layout. 
    for layout in workspace.getResources(type="layout",bank=id):
        line = "\t"+layout.getName()
        if format=="fixed":
            # FIXED FORMAT
            # Gather basic properties
            start=layout.getPropertyValue("start")
            if start: start = int(start)
            end=layout.getPropertyValue("end")
            if end: end = int(end)
            width=layout.getPropertyValue("width")
            if width:
                width=int(width)

            if not start:
                # carry over if we do not know where to start
                start = nextStart

            # compute end as start+width-1 if necessary
            if start and (not end) and width:
                end = start+width-1

            # sanity check
            if not start or not end:
                # can't figure out the column
                layout.dump()
                raise RuntimeError("width/start/end not found for "+layout.source+" "+layout.getName())

            # write start-end
            line = line+"\t"+str(start)+"-"+str(end)

            # keep track of where we are
            nextStart = start + width
        else:
            # DELIMITED
            pass

        # data type
        ststype="A" # STRING
        datatype=None
        if layout.hasProperty("datatype[sts]"):
            ststype=layout.getPropertyValue("datatype[sts]")
        elif layout.hasProperty("datatype"):
            datatype=layout.getPropertyValue("datatype")
        elif layout.hasProperty("datatype[generic]"):
            datatype=layout.getPropertyValue("datatype[generic]")

        if datatype and re.match("^N.*",datatype,re.IGNORECASE):
            ststype=None
            if layout.hasProperty("decimals") and int(layout.getPropertyValue("decimals"))==0:
                ststype=None

        if datatype and re.match("^D.*",datatype,re.IGNORECASE):
            # TODO: convert out RML dates to STS dates
            pass

        if ststype:
            line += " ("+ststype+")"
        
        # label
        if layout.getLabel():
            line += "\t{"+layout.getLabel()+"}"
        else:
            pass

        # variable classification
        if layout.hasProperty("classification"):
            ref=layout.getPropertyValue("classification")
            classification=workspace.resolve(ref,type="classification")
            if classification:
                # generate the reference
                if useClassificationBank:
                    stsId=classification.getBank()+"_"+classification.getId()
                else:
                    stsId=classification.getId()
                line += " \\"+stsId
                # add to set
                if ref not in classifications:
                    classifications[ref]=classification
            else:
                raise RuntimeError("Error resolving classification for "+layout.source)
            pass
        else:
            pass

        # write line
        print(line,sep='',file=file)
    ### for

    # VALUE LABELS
    print(file=file)

    if classifications:
        print("VALUE LABELS",file=file)
        for ref,classification in classifications.items():
            if useClassificationBank:
                stsId=classification.getBank()+"_"+classification.getId()
            else:
                stsId=classification.getId()
            print("\t\\",stsId,sep='',file=file)
            # codes
            for code in workspace.getResources(type="code",bank=classification.getBank()+"."+classification.getId()):
                value=code.getPropertyValue("value")
                label=code.getName()
                print("\t\t",value," \"",escape(label),"\"",sep='',file=file)
                
def escape(value):
    """RML string escaping"""
    if not isinstance(value,str):
        value = str(value)
    return value.replace('"','\\\"')
    
