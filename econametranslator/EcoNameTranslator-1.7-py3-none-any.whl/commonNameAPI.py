from .higherLevelAPI import *
import itertools
from .dataCleaning import *
from .taxonomyAPI import *
from requests import Session

def commonNameAPI(bestEffortsOnSpecies):
    noWorkResults = []
    toProcess = []
    for name,speciesResult in bestEffortsOnSpecies:
        if len(speciesResult) > 0: noWorkResults.append((name,True,speciesResult))
        else: toProcess.append(name)
    urls = list(map(constructUrls,toProcess))
    session = Session()
    results = list(map(lambda x: session.get(x),urls))
    results = safeMapResToJson(results)
    results = list(zip(toProcess,results))
    results = list(map(processIndividualResult,results))
    return [*noWorkResults,*results]

def safeMapResToJson(results):
    res = []
    for r in results:
        try: res.append(r.json())
        except: res.append({})
    return res
        
def constructUrls(name):
    return "https://itis.gov/ITISWebService/jsonservice/getITISTermsFromCommonName?srchKey="+name

def processIndividualResult(nameAndResTuple):
    name,res = nameAndResTuple
    if 'itisTerms' not in res: return (name,False,[])
    if res['itisTerms'] is None: return (name,False,[])
    if res['itisTerms'][0] is None: return (name,False,[])
    nameTranslation = res['itisTerms']
    scientificNames = processTranslationToScientificName(name,nameTranslation)
    scientificNames = list(map(cleanSingleSpeciesString,scientificNames))
    scientificNames = expandIfHigherLevelTaxaName(scientificNames)
    return (name,True,scientificNames)

def expandIfHigherLevelTaxaName(scientificNames):
    return list(filter(lambda x: len(x.strip().split(" ")) > 1 ,scientificNames))

def processTranslationToScientificName(name,nameTranslation):
    sNames = list(filter(containsUsableData,nameTranslation))
    sNames = list(filter(lambda x: containsValidCommonName(name,x['commonNames']), sNames))
    return list(map(lambda x: x['scientificName'],sNames))

def containsUsableData(individualCommonNameResult):
    return \
        'scientificName' in individualCommonNameResult and \
        'commonNames' in individualCommonNameResult and \
        individualCommonNameResult['commonNames'][0] is not None and \
        individualCommonNameResult['scientificName'] is not None

def containsValidCommonName(name,listOfCommonNames):
    if len(name.strip().split(" ")) > 1: return True
    return any(list(map(lambda x: checkIfCommonNameResultIsValid(name,x),listOfCommonNames)))

def checkIfCommonNameResultIsValid(name,result):
    result = result.lower().split(" ")
    stringPotential1 = name 
    stringPotential2 = name+'s' #plurals
    return stringPotential1 in result or stringPotential2 in result
