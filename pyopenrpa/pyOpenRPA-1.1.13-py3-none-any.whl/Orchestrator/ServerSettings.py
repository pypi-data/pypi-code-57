import json
from inspect import signature # For detect count of def args
#ControlPanelDict
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)

# /Orchestrator/RobotRDPActive/ControlPanelDictGet
def RobotRDPActive_ControlPanelDictGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    lResultDict = {
        "DataList":[
            # {"SessionKeyStr":"", "SessionHexStr": "", "IsFullScreenBool": False, "IsIgnoredBool": False}
        ]
    }
    # Iterate throught the RDP List
    for lRDPSessionKeyStrItem in inGlobalDict["RobotRDPActive"]["RDPList"]:
        lRDPConfiguration = inGlobalDict["RobotRDPActive"]["RDPList"][lRDPSessionKeyStrItem] # Get the configuration dict
        lDataItemDict = {"SessionKeyStr":"", "SessionHexStr": "", "IsFullScreenBool": False, "IsIgnoredBool": False} # Template
        lDataItemDict["SessionKeyStr"] = lRDPSessionKeyStrItem # Session key str
        lDataItemDict["SessionHexStr"] = lRDPConfiguration["SessionHex"] # Session Hex
        lDataItemDict["IsFullScreenBool"] = True if lRDPSessionKeyStrItem == inGlobalDict["RobotRDPActive"]["FullScreenRDPSessionKeyStr"] else False # Check  the full screen for rdp window
        lDataItemDict["IsIgnoredBool"] = lRDPConfiguration["SessionIsIgnoredBool"] # Is ignored
        lResultDict["DataList"].append(lDataItemDict)
    # Send message back to client
    message = json.dumps(lResultDict)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")

def Monitor_ControlPanelDictGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    # Create result JSON
    lResultJSON = {"RenderRobotList": []}
    lRenderFunctionsRobotList = inGlobalDict["ControlPanelDict"]["RobotList"]
    for lItem in lRenderFunctionsRobotList:
        lUACBool = True # Check if render function is applicable User Access Rights (UAC)
        if inGlobalDict["Server"]["AccessUsers"]["FlagCredentialsAsk"] is True:
            lUserRights = inGlobalDict["Server"]["AccessUsers"]["RuleDomainUserDict"][(inRequest.OpenRPA["Domain"].upper(),inRequest.OpenRPA["User"].upper())]
            if len(lUserRights["ControlPanelKeyAllowedList"]) > 0 and lItem["KeyStr"] not in lUserRights["ControlPanelKeyAllowedList"]:
                lUACBool = False # UAC Check is not passed - False for user
        if lUACBool: # Run function if UAC is TRUE
            # Выполнить вызов и записать результат
            # Call def (inRequest, inGSettings) or def (inGSettings)
            lItemResultDict = None
            lDEFSignature = signature(lItem["RenderFunction"]) # Get signature of the def
            lDEFARGLen = len(lDEFSignature.parameters.keys()) # get count of the def args
            if lDEFARGLen == 1: # def (inGSettings)
                lItemResultDict = lItem["RenderFunction"](inGlobalDict)
            elif lDEFARGLen == 2: # def (inRequest, inGSettings)
                lItemResultDict = lItem["RenderFunction"](inRequest, inGlobalDict)
            elif lDEFARGLen == 0: # def ()
                lItemResultDict = lItem["RenderFunction"]()
            # RunFunction
            lResultJSON["RenderRobotList"].append(lItemResultDict)
    # Send message back to client
    message = json.dumps(lResultJSON)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")

# UserAccess get rights hierarchy dict in json
def UserRoleHierarchyGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    # Create result JSON
    lResultDict = inRequest.OpenRPA["DefUserRoleHierarchyGet"]() # Get the User Role Hierarchy list
    # Send message back to client
    message = json.dumps(lResultDict)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")

def GetScreenshot(inRequest,inGlobalDict):
    # Get Screenshot
    def SaveScreenshot(inFilePath):
        # grab fullscreen
        # Save the entire virtual screen as a PNG
        lScreenshot = getScreenAsImage()
        lScreenshot.save('screenshot.png', format='png')
        # lScreenshot = ScreenshotSecondScreen.grab_screen()
        # save image file
        # lScreenshot.save('screenshot.png')
    # Сохранить файл на диск
    SaveScreenshot("Screenshot.png")
    lFileObject = open("Screenshot.png", "rb")
    # Write content as utf-8 data
    inRequest.OpenRPAResponseDict["Body"] = lFileObject.read()
    # Закрыть файловый объект
    lFileObject.close()
def SettingsUpdate(inGlobalConfiguration):
    import os
    import pyOpenRPA.Orchestrator
    lOrchestratorFolder = "\\".join(pyOpenRPA.Orchestrator.__file__.split("\\")[:-1])
    lURLList = \
        [ #List of available URLs with the orchestrator server
            #{
            #    "Method":"GET|POST",
            #    "URL": "/index", #URL of the request
            #    "MatchType": "", #"BeginWith|Contains|Equal|EqualCase",
            #    "ResponseFilePath": "", #Absolute or relative path
            #    "ResponseFolderPath": "", #Absolute or relative path
            #    "ResponseContentType": "", #HTTP Content-type
            #    "ResponseDefRequestGlobal": None #Function with str result
            #}
            #Orchestrator basic dependencies
            {"Method":"GET", "URL": "/", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\Index.xhtml"), "ResponseContentType": "text/html"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.css"), "ResponseContentType": "text/css"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.js"), "ResponseContentType": "application/javascript"},
            {"Method":"GET", "URL": "/3rdParty/jQuery/jquery-3.1.1.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\jQuery\\jquery-3.1.1.min.js"), "ResponseContentType": "application/javascript"},
            {"Method":"GET", "URL": "/3rdParty/Google/LatoItalic.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Google\\LatoItalic.css"), "ResponseContentType": "font/css"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/themes/default/assets/fonts/icons.woff2", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default\\assets\\fonts\\icons.woff2"), "ResponseContentType": "font/woff2"},
            {"Method":"GET", "URL": "/favicon.ico", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\favicon.ico"), "ResponseContentType": "image/x-icon"},
            {"Method":"GET", "URL": "/3rdParty/Handlebars/handlebars-v4.1.2.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Handlebars\\handlebars-v4.1.2.js"), "ResponseContentType": "application/javascript"},
            {"Method": "GET", "URL": "/Monitor/ControlPanelDictGet", "MatchType": "Equal", "ResponseDefRequestGlobal": Monitor_ControlPanelDictGet, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/GetScreenshot", "MatchType": "BeginWith", "ResponseDefRequestGlobal": GetScreenshot, "ResponseContentType": "image/png"},
            {"Method": "GET", "URL": "/Orchestrator/RobotRDPActive/ControlPanelDictGet", "MatchType": "Equal","ResponseDefRequestGlobal": RobotRDPActive_ControlPanelDictGet, "ResponseContentType": "application/json"},
            {"Method": "POST", "URL": "/Orchestrator/UserRoleHierarchyGet", "MatchType": "Equal","ResponseDefRequestGlobal": UserRoleHierarchyGet, "ResponseContentType": "application/json"}
    ]
    inGlobalConfiguration["Server"]["URLList"]=inGlobalConfiguration["Server"]["URLList"]+lURLList
    return inGlobalConfiguration