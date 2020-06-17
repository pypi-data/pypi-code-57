import sys
import os
sys.path.append('..')

from waapi import WaapiClient
from pprint import pprint
from csg_helpers import soundbank_helper
import operator

client = None

def connect(port=8095):
    """ Connect to Wwise authoring api , on default port 8095 or an alternative port.
    This sets up the client used for all future calls in the same session, so should be called before any other functions

    :param port: The waapi port to use (default 8095)
    :return: wwise connection info structure OR False

    """
    global client
    try:
        client = WaapiClient(url="ws://127.0.0.1:{0}/waapi".format(port))
    except Exception as ex:
        print("Connection error: {}".format(ex))
        print("Error connecting to Wwise. Please check your Waapi settings in User Preferences (wamp port expecting 8095) .....exiting")
        #input('Press <ENTER> to continue')
        return False
        #sys.exit()
    else:
        result = client.call("ak.wwise.core.getInfo")
        return result

def exit():
    """Exiting the connection

    """
    automationMode(False)
    try:
        client.disconnect()
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def getClient():
    """Getter for the waapi client connection

    """
    return client

def call(procedure,arguments):
    """Support manually calling a procedure with args

    """
    try:
        res = client.call(procedure,arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

############# Function definitions #########################################

### Project undo and save ######

def beginUndoGroup():
    """Begin an undo group

    """
    try:
        client.call("ak.wwise.core.undo.beginGroup")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def cancelUndoGroup():
    """Cancel an undo group

        """
    try:
        client.call("ak.wwise.core.undo.cancelGroup")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def endUndoGroup(undogroup):
    """Name and end an undo group
    args:
    undogroup -- Name to give the undo group that is ending

    """
    undoArgs = {"displayName": undogroup}
    try:
        client.call("ak.wwise.core.undo.endGroup", undoArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def saveWwiseProject():
    """Save the wwise project

    """
    try:
        client.call("ak.wwise.core.project.save")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def setupSubscription(subscription, target, returnArgs = ["id", "name", "path"]):
    """Subscribe to an event. Do target when triggered, get retunArgs in

    """
    try:
        client.subscribe(subscription, target, {"return": returnArgs})
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def getProjectInfo():
    """Get the wwise project info
    e.g. filePath, @DefaultLanguage

    """
    arguments = {
        "from": {"ofType": ["Project"]},
        "options": {
            "return": ["type","id", "name", "filePath","@DefaultLanguage"]
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get",arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res["return"][0]

def getLanguages():
    """Get the list of languages from the wwise project

    """
    langlist=[]
    arguments = {
        "from": {"ofType": ["Language"]},
        "options": {
            "return": ["name"]
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        for lang in res.kwresults["return"]:
            if lang['name'] != 'SFX' and lang['name'] != 'External' and lang['name'] != 'Mixed':
                langlist.append(lang['name'])
        return langlist

def getPathToWwiseProjectFolder():
    """Gets a path to the root folder of wwise project, cleans any nonsense from Mac paths.

    """
    projectInfo = getProjectInfo()
    WwiseProjectPath = projectInfo["filePath"]
    WwiseProjectPath = WwiseProjectPath.replace("Y:", "~").replace('\\', '/')
    pathToWwiseFolder = os.path.expanduser(os.path.dirname(WwiseProjectPath))
    return pathToWwiseFolder

###  Object creation and property setting ######


def createWwiseObject(parentID, otype="BlendContainer", oname="", conflict="merge"):
    """Create a wwise object of type otype, called oname, underneath

    args:
    parentID -- The GUID of the parent object
    otype -- The type of wwise object to create
    oname -- The name to give the new object
    conflict -- Behaviour for conflicting objects (default=merge)

    returns:
    The newly created wwise object structure or False

    """
    createObjArgs = {
        "parent": parentID,
        "type": otype,
        "name": oname,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.create", createObjArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def createWwiseObjectFromArgs(args = {}):
    """Create a wwise object from a custom argument structure.
    Useful if you need to create many complex objects.

    args:
    args{} -- A map of custom arguments for ak.wwise.core.object.create

    returns:
    The newly created wwise object(s) or False

    """
    try:
        res = client.call("ak.wwise.core.object.create", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setProperty(object, property, value):
    """Set a property of a wwise object

    args;
    object -- GUID of the object
    property -- Name of the property to set
    value -- The value to set for given property

    returns:
    The result of the operation

    """
    setPropertyArgs = {
        "object": object,
        "property": property,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setProperty",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setReference(object, reference, value):
    """Set a reference of a wwise object

    args;
    object -- GUID of the object
    reference -- Name of the reference to set
    value -- The value to set for given property

    returns:
    The result of the operation

    """
    setArgs = {
        "object": object,
        "reference": reference,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setReference",setArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setNotes(object, value):
    """Set the notes of object to value

    args:
    object -- GUID of the object
    value -- String to set as notes

    """
    setPropertyArgs = {
        "object": object,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setNotes",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def importAudioFiles(args):
    """Import audio files with custom args
    args:
    args{} -- A map of custom arguments for ak.wwise.core.audio.import

    returns:
    The newly created imported object(s) or False

    """
    try:
        res = client.call("ak.wwise.core.audio.import", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setupImportArgs(parentID, fileList,originalsPath,language="SFX"):
    """Helper function to construct args for import operation

    args:
    parentID -- GUID of the parent object
    fileList -- List of audio files to import
    originalsPath -- Relative location to put new files inside Originals
    language -- Import audio as SFX (default) or a given language

    returns:
    An arguments structure that can be used with importAudioFiles()

    """
    ParentID = str(parentID)
    importFilelist = []
    for audiofile in fileList:
        foo = audiofile.rsplit('.') #remove extension from filename
        audiofilename = foo[0]
        importFilelist.append(
            {
                "audioFile": audiofile,
                "objectPath": "<Sound SFX>"+os.path.basename(audiofilename)
            }
        )

    importArgs = {
        "importOperation": "useExisting",
        "autoAddToSourceControl": True,
        "default": {
            "importLanguage": language,
            "importLocation": ParentID,
            "originalsSubFolder": originalsPath
            },
        "imports": importFilelist
        }
    return importArgs


def deleteWwiseObject(object):
    """Delete a wwise object

    args:
    object -- GUID of object to be deleted

    """
    args = {"object":object}
    try:
        client.call("ak.wwise.core.object.delete",args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

###  Searching the project  ######

def getSelectedObjects(properties=[]):
    """Get the currently selected object(s), returning any extra properties

    args:
    properties[] -- list of additional properties to be returned for the wwise objects.
    by default objects will return ["id","type", "name", "path"] + properties[]

    returns:
    List of currently selected wwise objects or False

    """
    baseProperties = ["id","type", "name", "path"]
    selectedObjectArgs = {
        "options": {
            "return": baseProperties+properties
        }
    }
    try:
        res = client.call("ak.wwise.ui.getSelectedObjects",selectedObjectArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["objects"]
        else:
            return []

def getDescendantObjectsOfType(fromObject,ofType,returnProperties=[],tfrom="id",select="descendants"):
    """Perform a search fromObject to find descendants ofType, return additional properties for each object.
    Optionally change the from and select parts of the query, by default use ID as the object

    args:
    fromObject -- starting point of search. Default is a GUID
    ofType -- Type of wwise objects to search for
    returnProperties -- Additional properties to return for each object
    tfrom -- Key that determines how fromObject is used in the search (default=id)
    select -- Key that determines which objects are searched in relation to the fromObject (default=descendants)

    for more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [fromObject]},
        "transform": [
            {"select": [select]},
            {"where":["type:isIn",[ofType]]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getDescendantObjects(fromObject,returnProperties=[],tfrom="id",select="descendants"):
    """Perform a search fromObject to find all descendants, return additional properties for each object.
    Optionally change the from and select parts of the query, by default use ID as the object

    args:
    fromObject -- starting point of search. Default is a GUID
    returnProperties -- Additional properties to return for each object
    tfrom -- Key that determines how fromObject is used in the search (default=id)
    select -- Key that determines which objects are searched in relation to the fromObject (default=descendants)

    for more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [fromObject]},
        "transform": [
            {"select": [select]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []


def getObjectsByName(name,type,returnProperties=[],tfrom="ofType"):
    """Perform a search by name, return additional properties for each object.
    Named search must also include a type filter

    args:
    name -- String to match with object names
    type -- Type of wwise objects to search for
    returnProperties -- Additional properties to return for each object
    tfrom -- Key that determines how fromObject is used in the search (default=ofType)

    for more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [type]},
        "transform": [
            #{"where": ["name:matches",[name]]}
            {"where": ['name:matches', '^'+name+'$']}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getObjectProperties(fromObject,returnProperties=[],tfrom="id"):
    """Get some additional properties from a wwise Object, by default use ID as the object

    args:
    fromObject --  Wwise object to get properties from. Default is a GUID
    returnProperties -- Additional properties to return for each object
    tfrom -- Key that determines how fromObject is used in the search (default=id)

    for more info on options see Wwise SDK for ak.wwise.core.object.get
    https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_get.html

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [fromObject]},
        "transform": [],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None and len(res["return"])>0:
            if len(res["return"]) > 1:
                return res["return"]
            else:
                return res["return"][0]
        else:
            return []

def getAllObjectsOfType(ofType,returnProperties=[]):
    """Get all objects of a certain type, and return any extra properties

    args:
    ofType -- Type of wwise objects to search for
    returnProperties -- Additional return properties to get for each object

    """
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {"ofType": [ofType]},
        "transform": [
            #{"select": "parent"}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getReferencesToObject(objectID,returnProperties=[],tfrom="id"):
    """ get the references to a given object, by default use ID as the object"""
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [objectID]},
        "transform": [
            {"select": ["referencesTo"]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getListOfTypes():
    """return the list of valid object types, can help debugging"""
    try:
        res = client.call("ak.wwise.core.object.getTypes")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def filterWwiseObjects(objects,property,operation, value, NOT=0):
    """helper function to filter a list of objects by a specific property, value and comparison operation"""
    # e.g. return only objects with "@Volume" , "<" , "-48"
    results = []
    op = getOperator(operation)
    for obj in objects:
        if not property in obj:## this object doesnt have the property, so skip it
            continue
        if NOT ==0:
            if op(obj[property],value):
                results.append(obj)
        else:
            if not op(obj[property],value):
                results.append(obj)
    return results

def getOperator(string):
    if string == "==":
        return operator.eq
    elif string == "<":
        return operator.lt
    elif string == "<=":
        return operator.le
    elif string == ">":
        return operator.gt
    elif string == ">=":
        return operator.ge
    elif string == "!=":
        return operator.ne
    elif string == "contains":
        return operator.contains
    else:
        print("WARNING!!! Did not recognise operator argument..defaulting to EQUALS")
        return operator.eq


#####  Soundbanks #####
def generateSoundbanks(banklist = []):
    args = {
        "command": "GenerateSelectedSoundbanksAllPlatforms",
        "objects": [
            banklist
        ]
    }
    try:
        client.call("ak.wwise.ui.commands.execute", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def getSoundbanks(fromType,fromValue):
    """ Return all Soundbanks referencing any object of the Work Unit directly"""
    BankList =[]
    for transform in bankhelper.bankTransforms:
        arguments = {
            "from": {fromType: [fromValue]},
            "transform": transform,
            "options": {
                "return": ['id', 'name', 'type']
            }
        }
        try:
            res = client.call("ak.wwise.core.object.get", arguments)
        except Exception as ex:
            print("call error: {}".format(ex))
            return False
        else:
            # print (res.kwresults["return"])
            for bank in res["return"]:
                if bank["name"] not in BankList:
                    BankList.append((bank["name"]))
    return BankList


def executeCommand(command,objects = []):
    """wrapper to execute UI commands"""
    args = {
        "command": command,
        "objects": [
            objects
        ]
    }
    try:
        res = client.call("ak.wwise.ui.commands.execute", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def automationMode(enabled):
    """set automation mode on/off

    :param enabled: True or False

    :return: Result

    """
    args = {
        "enable": enabled
    }
    try:
        res = client.call("ak.wwise.debug.enableAutomationMode", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def checkoutWorkUnit(workunitID):
    """Source control operation to check out work unit"""
    return executeCommand("WorkgroupCheckoutWWU",workunitID)

def cleanfilePathFromWwise(path):
    """Cleans the nonsense from Mac paths that Wwise gives you"""
    cleanMacpath = path.replace("Y:","~").replace('\\', '/')
    return os.path.abspath(os.path.expanduser(cleanMacpath))

def setSwitchContainerAssignment(switch,child):
    """Assign a given child object to a given switch (switch container)"""
    args = {
        "stateOrSwitch": switch,
        "child":child
    }
    try:
        res = client.call("ak.wwise.core.switchContainer.addAssignment", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def removeSwitchContainerAssignment(switch,child):
    """Remove a given child object from a given switch (switch container)"""
    args = {
        "stateOrSwitch": switch,
        "child":child
    }
    try:
        res = client.call("ak.wwise.core.switchContainer.removeAssignment", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def moveWwiseObject(object,parent, conflict="replace"):
    """move object to new location under parent"""
    args = {

        "object": object,
        "parent": parent,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.move", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def copyWwiseObject(object, parent, conflict="replace"):
    """copy object to new location under parent"""
    args = {

        "object": object,
        "parent": parent,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.copy", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

############## End of Function definitions ##############################################

#If pywaapi is run as the main script, connect and print result
if __name__ == "__main__":
    result = connect()
    pprint(result)
    exit()

