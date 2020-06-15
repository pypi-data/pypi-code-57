from __future__ import print_function

from collections import OrderedDict
import json
import re
import sys

#
# RECORD LAYOUTS
#

def generatePandasRecordLayout(resource,workspace,
                               file=sys.stdout,
                               format="fixed",
                               instance="",
                               useClassificationBank=False,
                               importPd=False
):
    """Generates code snippets for read_fwf, read_csv, read_table"""

    # Init
    bank = resource.getBank()
    id = resource.getId()
    print("Pandas: Generating Record "+id)

    # Collect start/end and variable names
    fwf_colspecs=[]
    fwf_widths=[]
    fwf_names=[]
    fwf_converters=[]

    nextStart=1 # use for running column width in case start/end are not provided
    index=0
    for layout in workspace.getResources(type="layout",bank=id):
        if format=="fixed":
            # FIXED FORMAT
            # Gather basic properties
            start=layout.getPropertyValue("start")
            if start: start = int(start)
            end=layout.getPropertyValue("end")
            if end: end = int(end)
            width=layout.getPropertyValue("width")
            if width: width=int(width)
            
            # compute missing width/start/end properties
            if not start: start = nextStart
            if start and (not end) and width: end = start+width-1
            if not start or not end:
                layout.dump()
                raise RuntimeError("width/start/end not found for "+layout.source+" "+layout.getName())
            if not width: width = start-end+1
            
            # record value
            fwf_colspecs.append((start-1,end)) # for pandas, position is zero based and end is exclusive
            fwf_widths.append(width)

            # keep track of where we are
            nextStart = start + width

            # data type
            converter = "str"
            datatype=None
            if layout.hasProperty("datatype"):
                datatype = layout.getPropertyValue("datatype")
            elif layout.hasProperty("datatype[generic]"):
                datatype = layout.getPropertyValue("datatype[generic]")
            if datatype and re.match("^N.*",datatype,re.IGNORECASE):
                if layout.hasProperty("decimals") and layout.getPropertyValue("decimals")==0:
                    converter="int"
                else:
                    converter="float"
            fwf_converters.append(converter)

        else:
            # DELIMITED
            pass
        index += 1
        # label
        fwf_names.append(layout.getName())
    ### for

    print("import pandas as pd",file=file)
    print(file=file)
    print("data=pd.read_fwf('"+instance+"'",sep='',file=file)
    print(",colspecs=",fwf_colspecs,sep='',file=file)
    #print(",widths=",fwf_widths,sep='',file=file)
    print(",names=",fwf_names,sep='',file=file)
    converters="{"
    for index,value in enumerate(fwf_converters):
        if index>0: converters+=","
        converters+=str(index)+":"+value
    converters+="}"
    print(",converters=",converters,sep='',file=file)
    print(")",file=file)
    print(file=file)
    print("print(data.head())",file=file)
    print("print(data.describe())",file=file)


