"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

PyChipBuilder sfabric CLI Script

Description:
    Script for exposing the SmartFabric class as a CLI,
    built with the PyChipBuilder python library.

"""

import os
import re
import sys
import pip
import time
import json
import inspect

import chipbuilder
from chipbuilder.smartfabric.util import IS_CLI_CMD, OPEN_HOST_ATTR


PKG_DIR_PATH   = os.path.dirname(chipbuilder.smartfabric.__file__)
API_DICT_FNAME = os.path.join(PKG_DIR_PATH, "data", "sf_api_cmds.json")
API_NAME       = os.path.basename(__file__).split(".")[0]
API_METHODS    = {}
API_DICT       = {}

CLI_CONF_FNAME   = os.path.join(PKG_DIR_PATH, "data", "cli_config.json")
CLI_CONF_FI    = open(CLI_CONF_FNAME, "r")
CLI_CONF       = json.load(CLI_CONF_FI)
MPSSE_NUM_DEVS   = 0

CMD_PATH  = []
CMD_DELIM = '_'


def run_sf_func(inst, func, args):
    
    global MPSSE_NUM_DEVS, CLI_CONF
    # print(func.__name__, func)
    
    ret = None
    fname = func.__name__
    safeToOpen = (MPSSE_NUM_DEVS != 0)
    needToOpen = hasattr(func, OPEN_HOST_ATTR)

    if not safeToOpen and needToOpen:
        cmd = " ".join(fname.split("_"))
        print("No FTDI devices connected")
        print("Aborting command: %s" % cmd)
        exit()

    if needToOpen:
        ftSN = CLI_CONF["devSN"]

        if ftSN != "":
            inst.select_device(ftSN)

        inst.open()

    try:
        if len(args):
            ret = func(*args)
        else:
            ret = func()
    except Exception as e:
        print(e)

    # if len(args):
    #     ret = func(*args)
    # else:
    #     ret = func()

    if needToOpen:
        inst.close()

    # print(ret)
    
    return ret


def parse_cmd(args, apiDict):

    global CMD_PATH, CMD_DELIM, API_NAME

    curDict = apiDict
    dictType = apiDict["type"]
    # print(dictType)

    if dictType == "cmd":

        try:
            curArg = args.pop(0)
        
        except IndexError:
            partialCmd = " ".join(CMD_PATH)
            dictKeys = list(apiDict.keys())
            dictKeys.remove("type")
            print("Missing argumens for {0} command: {1}".format(API_NAME, partialCmd))
            print("available options:\n{0}".format(dictKeys))
            exit()

        try:
            curDict = apiDict[curArg]
            CMD_PATH.append(curArg)
        
        except KeyError:
            dictKeys = list(apiDict.keys())
            dictKeys.remove("type")
            print("Invalid {0} command: {1}".format(API_NAME, curArg))
            print("available options:\n{0}".format(dictKeys))
            exit()

        # print(args)
        # print(curDict)
        curArg, curDict = parse_cmd(args, curDict)

    return args, curDict


def format_args(argDict):

    adict = {}
    argKeys = list(argDict.keys())
    argKeys.remove("type")

    for argName in argKeys:
        adict[argName] = type(argDict[argName]["val"][0])

    return adict


def print_func_help(func, msg, quit=True):

    helpMsg = msg + "\n"
    cmd = " ".join(func.__name__.split("_"))
    kwds = str(inspect.signature(func))
    kwds = re.sub(r"[\(|\)|,]", "", kwds)
    kwds = re.sub(r"\s=\s", "=", kwds)
    kwds = re.sub(r":\s", ":", kwds)
    helpMsg += "usage> %s %s\n" % (cmd, kwds )
    # argTypes = re.findall(r"\w+:\w+", kwds)
    # kwds = re.split(r":\w+=?\w+\s?", kwds)
    # fmtDocStr = func.__doc__
    # print(kwds, argTypes)

    # for kwid, kwd in enumerate(argTypes):
    #     fmtDocStr = fmtDocStr.replace(kwds[kwid], kwd)

    # helpMsg += fmtDocStr + "\n"
    try:
        helpMsg += func.__doc__ + "\n"
    except:
        helpMsg = ""

    if quit:
        print(helpMsg)
        exit()
    else:
        return helpMsg


def validate_args(apiFunc, argList, argDict):

    global CMD_PATH

    dictKeys = list(argDict.keys())
    dictKeys.remove("type")
    # print(len(argList), len(dictKeys))

    if not len(argList) and not len(dictKeys):

        return

    if "help" in argList:
        print_func_help(apiFunc, "Command Help Message")
        # print("arg %s doesn't have a default parameter" % argName)
        # print("usage: %s%s" % (srcFunc.__name__, inspect.signature(srcFunc) ) )
        # print(srcFunc.__doc__)

    if len(argList) > len(dictKeys):

        cmd = " ".join(CMD_PATH)
        dictArg = format_args(argDict)
        print_func_help(apiFunc, "Too many arguments for fast command: %s" % cmd)
        # print("Too many arguments for fast command: %s" % cmd)
        # print("usage:\n%s %s" % (cmd, inspect.signature(apiFunc)) )
        # print(apiFunc.__doc__)

    elif len(argList) < len(dictKeys):

        cmd = " ".join(CMD_PATH)
        dictArg = format_args(argDict)
        print_func_help(apiFunc, "Too few arguments for fast command: %s" % cmd)
        # print("Too few arguments for fast command: %s" % cmd)
        # print("usage:\n%s %s" % (cmd, inspect.signature(apiFunc)) )
        # print(apiFunc.__doc__)

    for argId, argName in enumerate(dictKeys):
        expArgType = type(argDict[argName]["val"][0])
        # print(argList[argId], type(argList[argId]))

        try:

            if argList[argId] in ["-", "None"]:
                if "default" in argDict[argName]:
                    argList[argId] = argDict[argName]["default"]
                
                else:
                    print_func_help(apiFunc, "arg %s doesn't have a default parameter" % argName)
                    # print("arg %s doesn't have a default parameter" % argName)
                    # print("usage: %s%s" % (apidFunc.__name__, inspect.signature(apidFunc) ) )
                    # print(apidFunc.__doc__)

                continue

            if expArgType == type(int()):
                if "0x" in argList[argId]:
                    argList[argId] = int(argList[argId], 16)
                
                else:
                    argList[argId] = int(argList[argId])

            elif expArgType == type(float()):
                argList[argId] = float(argList[argId])

            elif expArgType == type(str()):

                pass
                # fiType = argList[argId].split(".")[-1]

                # if fiType not in ["txt", "log", "csv"]:
                #     print("File '%s' not supported" % argList[argId])
                #     raise ValueError()

            elif expArgType == type(None):
                argList[argId] = None
            
        except ValueError:
            print("Wrong type for %s" % argName)
            print("Expected type: %s" % expArgType)
            exit()


def create_api_fi(func):

    def check_api_fi(*args, **kwargs):

        global API_DICT, API_DICT_FNAME, PKG_DIR_PATH

        isUpToDate = False
        installTime = os.path.getmtime(PKG_DIR_PATH)

        if os.path.exists(API_DICT_FNAME):
            datFiTime = os.path.getmtime(API_DICT_FNAME)

            if datFiTime > installTime: 
                # print("SF cmd json file up to date.")
                isUpToDate = True

        if isUpToDate: return

        # Only build API dict if needed
        # print("Creating SF cmd json file.")
        API_DICT.update(func(*args, **kwargs) )
        sfApiDictFi = open(API_DICT_FNAME, "w")
        json.dump(API_DICT, sfApiDictFi)
        sfApiDictFi.close()

    return check_api_fi


def build_arg_dict(method):

    argDict = {"type":"args"}
    srcFunc = inspect.unwrap(method)
    argSpecs = inspect.getfullargspec(srcFunc)
    argTypes = argSpecs.annotations
    defaults = argSpecs.defaults
    args = argSpecs.args

    if "self" in args:
        args.remove("self")

    try:
        argLen = len(args)
    except TypeError:
        argLen = 0

    try:
        defLen = len(defaults)
    except TypeError:
        defLen = 0

    diffLen = argLen - defLen
    # print(args)
    # print(argTypes)


    for argId, curArg in enumerate(args):
        # Get type class
        argType = argTypes[curArg]
        val = [argType()]
        # print(val)
        # TODO: add argument ranges for validation
        # print(argType)

        if argId >= diffLen:
            argDict[curArg] = { 
                "val": val, 
                "default": defaults[argId - diffLen]
            }

        else:
            argDict[curArg] = { 
                "val": val
            }
    
    # print(argDict)

    return argDict


@create_api_fi
def build_api_dict(methods):

    apiDict = {"type":"cmd"}

    for methodName in methods.keys():
        method = methods[methodName]
        cmdPath = methodName.split("_")
        cmdDict = apiDict
        # print(cmdPath, method)
        # print("api", apiDict)

        for cmd in cmdPath:
            # print(cmd)

            try:
               cmdDict = cmdDict[cmd]

            except KeyError:
                # Create dict path
                if cmd == cmdPath[-1]:
                    # moving to arguments
                    cmdDict[cmd] = build_arg_dict(method)
                else:
                    cmdDict[cmd] = {"type":"cmd"}
                    cmdDict = cmdDict[cmd]

            # print(cmdDict)

    apiDict = {
        "type":"cmd",
        API_NAME:apiDict
    }

    return apiDict


def get_api_methods(inst):

    global API_METHODS

    ### Config Methods ###
    for name, func in inspect.getmembers(sys.modules[__name__], predicate=inspect.isroutine):
        if callable(func) and hasattr(func, IS_CLI_CMD):
            API_METHODS[name] = func

    ### Smart Fabric Methods ###
    for name, func in inspect.getmembers(inst, predicate=inspect.isroutine):
        # Add SmartFabric API methods
        if callable(func) and hasattr(func, IS_CLI_CMD):
            API_METHODS[name] = func


def help():
    """
    Get this help message.
    """

    global API_METHODS

    print("SmartFabric CLI Commands:\n")
    helpMsg = ""

    for funcName in API_METHODS.keys():
        func = API_METHODS[funcName]
        helpMsg += print_func_help(func, "### API Command ###", quit=False)

    return helpMsg


def set_devsn(sn:str):
    """
    Store FTDI device serial number to json data file.
    
    Args:
        sn - FTDI device serial number (str). Use get devs for list of devices
    """
        
    global CLI_CONF, CLI_CONF_FI, MPSSE_NUM_DEVS

    if sn == "-":
        CLI_CONF["devSN"] = ""

    else:
        CLI_CONF["devSN"] = sn

    CLI_CONF_FI.close()
    CLI_CONF_FI = open(CLI_CONF_FNAME, "w")
    json.dump(CLI_CONF, CLI_CONF_FI)
    ret = get_devsn()

    return ret


def set_ftdevid(idx:int):
    """
    Store FTDI device ID to json data file.
    
    Args:
        idx - FTDI device ID (int). Use get devs for list of devices
    """
        
    global CLI_CONF, CLI_CONF_FI, MPSSE_NUM_DEVS

    if idx == 0:
        pass

    elif idx > (MPSSE_NUM_DEVS - 1):
        print("Invalid FTDI id: %d\nAvailable options:" % idx)
        print([str(ftid) for ftid in range(0, MPSSE_NUM_DEVS)])
        exit()

    CLI_CONF["ftDevId"] = idx
    CLI_CONF_FI.close()
    CLI_CONF_FI = open(CLI_CONF_FNAME, "w")
    json.dump(CLI_CONF, CLI_CONF_FI)
    ret = get_ftdevid()

    return ret


def set_latency(lat:int):
    """
    Store MPSSE Rx HW buffer latency to json data file.
    
    Args:
        lat - HW latency in ms (2ms - 255ms)
    """

    global CLI_CONF, CLI_CONF_FI

    CLI_CONF["latency"] = lat
    CLI_CONF_FI.close()
    CLI_CONF_FI = open(CLI_CONF_FNAME, "w")
    json.dump(CLI_CONF, CLI_CONF_FI)
    ret = get_latency()

    return ret


def set_freq(freq:float):
    """
    Store MPSSE JTAG clock frequency to json data file.
    
    Args:
        freq - JTAG clock frequency in Hz (float)
    """
    
    global CLI_CONF, CLI_CONF_FI

    CLI_CONF["freq"] = freq
    CLI_CONF_FI.close()
    CLI_CONF_FI = open(CLI_CONF_FNAME, "w")
    json.dump(CLI_CONF, CLI_CONF_FI)
    ret = get_freq()

    return ret


def set_stallcycles(stCyc:int):
    """
    Store stall cycles for OTP programming and realignment to json data file.
    
    Args:
        stCyc - number of stall cycles (int)
    """
    
    global CLI_CONF, CLI_CONF_FI

    CLI_CONF["stallCycles"] = stCyc
    CLI_CONF_FI.close()
    CLI_CONF_FI = open(CLI_CONF_FNAME, "w")
    json.dump(CLI_CONF, CLI_CONF_FI)
    ret = get_stallcycles()

    return ret


def get_devsn():
    """
    Get FTDI device serial number from json data file.
    """

    global CLI_CONF
    print("FTDI Serial Number: %s" % CLI_CONF["devSN"])

    return CLI_CONF["devSN"]


def get_ftdevid():
    """
    Get FTDI device ID from json data file.
    """

    global CLI_CONF
    print("FTDI Device ID: %s" % CLI_CONF["ftDevId"])

    return CLI_CONF["ftDevId"]


def get_latency():
    """
    Get MPSSE Rx HW buffer latency from json data file.
    """

    global CLI_CONF
    print("Read Latency: %s" % CLI_CONF["latency"])

    return CLI_CONF["latency"]


def get_freq():
    """
    Get stall cycles for OTP programming and realignment from json data file.
    """

    global CLI_CONF
    print("JTAG frequency: %s Hz" % CLI_CONF["freq"])

    return CLI_CONF["freq"]


def get_stallcycles():
    """
    Get stall cycles for OTP programming and realignment from json data file.
    """

    global CLI_CONF
    print("OTP Stall Cycles: %s Cycles" % CLI_CONF["stallCycles"])

    return CLI_CONF["stallCycles"]


setattr(help, IS_CLI_CMD, True)
setattr(set_devsn, IS_CLI_CMD, True)
setattr(set_ftdevid, IS_CLI_CMD, True)
setattr(set_latency, IS_CLI_CMD, True)
setattr(set_freq, IS_CLI_CMD, True)
setattr(set_stallcycles, IS_CLI_CMD, True)
setattr(get_devsn, IS_CLI_CMD, True)
setattr(get_ftdevid, IS_CLI_CMD, True)
setattr(get_latency, IS_CLI_CMD, True)
setattr(get_freq, IS_CLI_CMD, True)
setattr(get_stallcycles, IS_CLI_CMD, True)


def main():

    global CLI_CONF, MPSSE_NUM_DEVS, API_METHODS

    sf = chipbuilder.smartfabric.SmartFabric(
        devid = CLI_CONF["ftDevId"], 
        latency = CLI_CONF["latency"],
        freq = CLI_CONF["freq"],
        scycles = CLI_CONF["stallCycles"]
    )

    MPSSE_NUM_DEVS = sf._get_num_devices()

    # TODO: create dict from API_METHODS
    # this removes need to maintain sf_api_cmds.json
    get_api_methods(sf)
    # print(API_METHODS)
    build_api_dict(API_METHODS)
    sfDictFi = open(API_DICT_FNAME,"r")
    sfDict = json.load(sfDictFi)
    sfArgs = sys.argv[1:]
    sfArgs, sfDict = parse_cmd(sfArgs, sfDict[API_NAME])
    # print(sfArgs, sfDict)
    sfFuncKey = CMD_DELIM.join(CMD_PATH)

    try:
        sfFunc = API_METHODS[sfFuncKey]
    except KeyError:
        print("%s function not supported" % sfFuncKey)
        exit()

    validate_args(sfFunc, sfArgs, sfDict)
    rc = run_sf_func(sf, sfFunc, sfArgs)

    return rc


if __name__ == '__main__':
    main()
