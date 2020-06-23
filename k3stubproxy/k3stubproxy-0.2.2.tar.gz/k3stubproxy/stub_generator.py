'''
k3stubproxy.stub_generator

Created on 7 May 2020
Author: Joachim Kestner <joachim.kestner@khoch3.de>
'''

import re
import logging
import os
import json

logger = logging.getLogger(__name__)

FUNCTION_BODY = """
{{
    return convert_python_object_to_{returnType}(forwardThroughStubConnector("{functionName}"{args}));
}}

"""


def find_in_out_in_comment(paramterNm, commentText):
    pattern = r"\@param\s+\[ ?(\w+)\]\s+"+ paramterNm
    m = re.search(pattern, commentText)
    if not m:
        return None
    inOutStr = m.group(1)
    if inOutStr not in ["in", "out"]:
        return None
    return inOutStr

def parse_param(paramStr, funcComment):
    
    #const uint16_t ErrorCodeList_p[HAL_NVM_ParamSize10]
    m = re.match("^const\s+(\w+)\s+(\w+)(\[\w+\])$", paramStr)
    if m:
        paramName = m.group(2)
        paramType = m.group(1)+m.group(3)
        paramInOut = find_in_out_in_comment(paramName, funcComment)
        return paramName, paramType, paramInOut
    
    #uint16_t HistorySeconds_p[HAL_NVM_ParamSize60]
    m = re.match("^(\w+)\s+(\w+)(\[\w+\])$", paramStr)
    if m:
        paramName = m.group(2)
        paramType = m.group(1)+m.group(3)
        paramInOut = find_in_out_in_comment(paramName, funcComment)
        return paramName, paramType, paramInOut
    
    #const en_HAL_InputChannels_t fb_channel_p
    m = re.match("^const\s+(\w+)\s+(\w+)$", paramStr)
    if m:
        paramType = m.group(1)
        paramName = m.group(2)
        paramInOut = find_in_out_in_comment(paramName, funcComment)
        return paramName, paramType, paramInOut
    
    #uint16_t *pGain_p
    m = re.match("^(\w+)\s*\*\s*(\w+)$", paramStr)
    if m:
        paramType = m.group(1)+"*"
        paramName = m.group(2)
        paramInOut = find_in_out_in_comment(paramName, funcComment)
        return paramName, paramType, paramInOut
    
    #bool_t enable_p
    m = re.match("^(\w+)\s+(\w+)$", paramStr)
    if m:
        paramType = m.group(1)
        paramName = m.group(2)
        paramInOut = find_in_out_in_comment(paramName, funcComment)
        return paramName, paramType, paramInOut
    
    return None, None, None


def generate_stubs(fileList, outputDirPath, headerLines=[], funcPrefixes=None, fileNmSuffix=None, configOutFile=None):
    
    filesToText = {}
    funcConfig = {}
    
    for filePath in fileList:
        with open(filePath) as fh:
            filesToText[filePath] = fh.read()
    
    logger.info("Finished reading files")
    
    if funcPrefixes is not None:
        logger.info("Restricting found functions to functions with one of the following prefix {}".format(funcPrefixes))
    
    totalFunctionsFound = 0
    
    for filePath in filesToText:
        numMatch = 0
        txtStr = filesToText[filePath]
        logger.info(f"Processing file {filePath}, size {len(txtStr)}")
#         for m in re.finditer("\/\*([^*]|[\r\n]|(\*+([^*\/]|[\r\n])))*\*+\/", txtStr, re.MULTILINE|re.DOTALL):
#         #for m in re.finditer("\/\*.+?(?=\*\/)\*\/", txtStr, re.MULTILINE|re.DOTALL):
#             
#             numMatch += 1
#             print(m.group(0))
#             print("=================================================================")
        #for m in re.finditer("\s*extern\s+(\w+) +(\w+) *\(([^\)]+)\)\s*{", txtStr):
        
        fileNm = os.path.basename(filePath);
        pname, ext = os.path.splitext(fileNm);
        targetFileNm = fileNm if fileNmSuffix == None else pname + fileNmSuffix + ext
        ouputFilePath = os.path.join(outputDirPath, targetFileNm)
        
        with open(ouputFilePath, "w") as fh:
            logging.info(f"Writing file to {ouputFilePath}")
            

            
            for line in headerLines:
                fh.write(line)
                
            fh.write(f'#include "{pname}.h"\n')
            fh.write(f'#include "Stub_Connector_Interface.h"\n')
            fh.write('\n')
        
            for m in re.finditer("(\/\*.+?(?=\*\/)\*\/)\s*extern\s+(\w+) +(\w+) *\(([^\)]+)\)\s*{", txtStr,  re.MULTILINE|re.DOTALL):
                wholeMatch = m.group(0)
                comment = m.group(1)
                returnType = m.group(2)
                functionName = m.group(3)
                args = m.group(4)
                
                if funcPrefixes:
                    preNotFound = True
                    for fPre in funcPrefixes:
                        if functionName.startswith(fPre):
                            preNotFound = False
                    if preNotFound:
                        continue
                logger.debug("Found function "+ str(functionName));
                
                argNames = []
                parsedArgList = []
                
                for arg in args.split(","):
                    arg = arg.strip()
                    if arg == "void":
                        continue
                    
                    
                    paramName, paramType, paramInOut = parse_param(arg, comment)
                    if None in [paramName, paramType, paramInOut]:
                        logger.warning(f"Unknown parameter format for paramter '{arg}' in function {functionName} in file {filePath}")
                        raise Exception(f"Could not parse argument {arg}")
                    
                    logger.debug(f"  Argument: '{arg}', ({paramName}, {paramInOut}, {paramType})")
                    argNames.append(paramName)
                    parsedArgList.append((paramName, paramInOut, paramType))
                
                fh.write(f"extern {returnType} {functionName}({args})")
                argString = "" if len(argNames) == 0 else ", "
                argString += ", ".join(argNames)
                fh.write(FUNCTION_BODY.format(functionName=functionName, args=argString, returnType=returnType))

                if functionName in funcConfig:
                    raise KeyError(f"{functionName} already in dict")
                funcConfig[functionName] = {"parameters" : parsedArgList, "return" : returnType}
                numMatch += 1
    
        logger.info(f"Num matches found {numMatch}")
        
        totalFunctionsFound += numMatch
    
    logger.info(f"Total number of functions found accross all input files: {totalFunctionsFound}")
    
    if configOutFile:
        with open(configOutFile, "w") as fh:
            json.dump(funcConfig, fh, indent=2)
        logger.info(f"Function paramter configuration written to {configOutFile}")

    