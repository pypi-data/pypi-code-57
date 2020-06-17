'''
stub_target_generator

Created on 11 May 2020
Author: Joachim Kestner <joachim.kestner@khoch3.de>
'''

def generate_target_stub(functionDefinitionDict, targetFile=None):
    
    lines = []
    
    
    for funcName, funcDict in functionDefinitionDict.items():
        inPmrs = []
        outPrms = []
        prmList = funcDict["parameters"]
        for prmNm, inOut, typeString in prmList:
            if inOut == "in":
                inPmrs.append((prmNm, typeString))
            elif inOut == "out":
                outPrms.append((prmNm, typeString))
            else:
                raise RuntimeError(f"Unexpected inOut value '{inOut}'")
            
        lines.append("# Input prms: "+", ".join([f"{nm} {t}" for nm, t in inPmrs]))
        lines.append("# Return: {}".format(funcDict["return"]))
        lines.append(f"def {funcName}({', '.join([nm for nm, t in inPmrs])}):")
        lines.append("    # Output prms: "+", ".join([f"{nm} {t}" for nm, t in outPrms]))
        lines.append("    return {{{}}}, 0".format(", ".join([f'"{nm}" : None' for nm, t in outPrms])))
        lines.append("")
        
    if targetFile:
        with open(targetFile, 'w') as fh:
            for l in lines:
                fh.write(l+"\n")
    else:
        for l in lines:
            print(l)
    