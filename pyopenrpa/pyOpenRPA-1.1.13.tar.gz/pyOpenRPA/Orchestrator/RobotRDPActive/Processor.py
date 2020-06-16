# ATTENTION! HERE IS NO Relative import because it will be imported dynamically
# All function check the flag SessionIsWindowResponsibleBool == True else no cammand is processed
# All functions can return None, Bool or Dict { "IsSuccessful": True }
from . import CMDStr # Create CMD Strings
from . import Connector # RDP API
from . import ConnectorExceptions # Exceptions
import time # sleep function
# ATTENTION
gSettings = None # Gsettings will be initialized after the import module

# Create new RDPSession in RobotRDPActive
def RDPSessionConnect(inRDPSessionKeyStr, inHostStr, inPortStr, inLoginStr, inPasswordStr):
    global gSettings
    # ATTENTION - dont connect if RDP session is exist
    if inRDPSessionKeyStr not in gSettings["RobotRDPActive"]["RDPList"]:
        lRDPConfigurationItem = { # Init the configuration item
            "Host": inHostStr,  # Host address, example "77.77.22.22"
            "Port": inPortStr,  # RDP Port, example "3389"
            "Login": inLoginStr,  # Login, example "test"
            "Password": inPasswordStr,  # Password, example "test"
            "Screen": {
                "Width": 1680,  # Width of the remote desktop in pixels, example 1680
                "Height": 1050,  # Height of the remote desktop in pixels, example 1050
                # "640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen, example
                "FlagUseAllMonitors": False,  # True or False, example False
                "DepthBit": "32"  # "32" or "24" or "16" or "15", example "32"
            },
            "SharedDriveList": ["c"],  # List of the Root sesion hard drives, example ["c"]
            ###### Will updated in program ############
            "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  # Hex is created when robot runs, example ""
            "SessionIsWindowExistBool": False,  # Flag if the RDP window is exist, old name "FlagSessionIsActive". Check every n seconds , example False
            "SessionIsWindowResponsibleBool": False,  # Flag if RDP window is responsible (recieve commands). Check every nn seconds. If window is Responsible - window is Exist too , example False
            "SessionIsIgnoredBool": False  # Flag to ignore RDP window False - dont ignore, True - ignore, example False
        }
        gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] = lRDPConfigurationItem # Add item in RDPList
        Connector.Session(lRDPConfigurationItem) # Create the RDP session
        Connector.SystemRDPWarningClickOk()  # Click all warning messages
    return True

# Disconnect the RDP session
def RDPSessionDisconnect(inRDPSessionKeyStr):
    global gSettings
    lSessionHex = gSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
    if lSessionHex:
        gSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None)
        Connector.SessionClose(inSessionHexStr=lSessionHex)
        Connector.SystemRDPWarningClickOk()  # Click all warning messages
    return True

# RDP Session reconnect
def RDPSessionReconnect(inRDPSessionKeyStr):
    global gSettings
    lRDPConfigurationItem = gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr]
    RDPSessionDisconnect(inRDPSessionKeyStr=inRDPSessionKeyStr) # Disconnect the RDP
    # Add item in RDPList
    gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] = lRDPConfigurationItem
    # Create the RDP session
    Connector.Session(lRDPConfigurationItem)
    return True

# Stop track the RDP session. Current def dont kill RDP session - only stop to track it (it can give )
def RDPSessionMonitorStop(inRDPSessionKeyStr):
    global gSettings
    lResult = True
    gSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None) # Remove item from RDPList
    return lResult

# Logoff the RDP session
def RDPSessionLogoff(inRDPSessionKeyStr):
    global gSettings
    lResult = True
    lCMDStr = "shutdown -L" # CMD logoff command
    # Calculate the session Hex
    lSessionHex = gSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
    if lSessionHex:
        # Run CMD - dont crosscheck because CMD dont return value to the clipboard when logoff
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="RUN", inLogger=gSettings["Logger"], inRDPConfigurationItem=gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
        gSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None) # Remove item from RDPList
    return lResult

# Check RDP Session responsibility TODO NEED DEV + TEST
def RDPSessionResponsibilityCheck(inRDPSessionKeyStr):
    global gSettings
    inGlobalDict = gSettings
    lRDPConfigurationItem = inGlobalDict["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] # Get the alias
    # set the fullscreen
    # ATTENTION!!! Session hex can be updated!!!
    Connector.SessionScreenFull(inSessionHex=lRDPConfigurationItem["SessionHex"], inLogger=gSettings["Logger"], inRDPConfigurationItem=gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    time.sleep(1)
    # Check RDP responsibility
    lDoCheckResponsibilityBool = True
    lDoCheckResponsibilityCountMax = 20
    lDoCheckResponsibilityCountCurrent = 0
    while lDoCheckResponsibilityBool:
        # Check if counter is exceed - raise exception
        if lDoCheckResponsibilityCountCurrent >= lDoCheckResponsibilityCountMax:
            pass
            #raise ConnectorExceptions.SessionWindowNotResponsibleError("Error when initialize the RDP session - RDP window is not responding!")
        # Check responding
        lDoCheckResponsibilityBool = not Connector.SystemRDPIsResponsible(inSessionHexStr = lRDPConfigurationItem["SessionHex"])
        # Wait if is not responding
        if lDoCheckResponsibilityBool:
            time.sleep(3)
        # increase the couter
        lDoCheckResponsibilityCountCurrent+=1
    return True

# Start process if it is not running
def RDPSessionProcessStartIfNotRunning(inRDPSessionKeyStr, inProcessNameWEXEStr, inFilePathStr, inFlagGetAbsPathBool=True):
    global gSettings
    inGlobalDict = gSettings
    lResult = True
    lCMDStr = CMDStr.ProcessStartIfNotRunning(inProcessNameWEXEStr, inFilePathStr, inFlagGetAbsPath= inFlagGetAbsPathBool)
    # Calculate the session Hex
    lSessionHex = inGlobalDict["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
    # Run CMD
    if lSessionHex:
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="CROSSCHECK", inLogger=gSettings["Logger"], inRDPConfigurationItem=gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult
# Create CMD str to stop process
def RDPSessionProcessStop(inRDPSessionKeyStr, inProcessNameWEXEStr, inFlagForceCloseBool):
    global gSettings
    inGlobalDict = gSettings
    lResult = True
    lCMDStr = f'taskkill /im "{inProcessNameWEXEStr}" /fi "username eq %USERNAME%"'
    if inFlagForceCloseBool:
        lCMDStr+= " /F"
    # Calculate the session Hex
    lSessionHex = inGlobalDict["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
    # Run CMD
    if lSessionHex:
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="CROSSCHECK", inLogger=gSettings["Logger"], inRDPConfigurationItem=gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult
# Send file from Host to Session RDP using shared drive in RDP
def RDPSessionFileStoredSend(inRDPSessionKeyStr, inHostFilePathStr, inRDPFilePathStr):
    global gSettings
    inGlobalDict = gSettings
    lResult = True
    lCMDStr = CMDStr.FileStoredSend(inHostFilePath = inHostFilePathStr, inRDPFilePath = inRDPFilePathStr)
    # Calculate the session Hex
    lSessionHex = inGlobalDict["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr, {}).get("SessionHex", None)
    #lSessionHex = inGlobalDict["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr]["SessionHex"]
    # Run CMD
    if lSessionHex:
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120, inLogger=gSettings["Logger"], inRDPConfigurationItem=gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult
# Recieve file from Session RDP to Host using shared drive in RDP
def RDPSessionFileStoredRecieve(inRDPSessionKeyStr, inRDPFilePathStr, inHostFilePathStr):
    global gSettings
    inGlobalDict = gSettings
    lResult = True
    lCMDStr = CMDStr.FileStoredRecieve(inRDPFilePath = inRDPFilePathStr, inHostFilePath = inHostFilePathStr)
    # Calculate the session Hex
    lSessionHex = inGlobalDict["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
    # Run CMD
    if lSessionHex:
        Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120, inLogger=gSettings["Logger"], inRDPConfigurationItem=gSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult