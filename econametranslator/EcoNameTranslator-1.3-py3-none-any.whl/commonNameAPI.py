from .higherLevelAPI import *
import itertools
from .dataCleaning import *
from .taxonomyAPI import *
import grequests

def commonNameAPI(bestEffortsOnSpecies):
    noWorkResults = []
    toProcess = []
    for name,speciesResult in bestEffortsOnSpecies:
        if len(speciesResult) > 0: noWorkResults.append((name,True,speciesResult))
        else: toProcess.append(name)
    urls = list(map(constructUrls,toProcess))
    reqs = (grequests.get(url) for url in urls)
    results = grequests.map(reqs,size=10)
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
    return "https://www.itis.gov/ITISWebService/jsonservice/searchByCommonName?srchKey="+name

def processIndividualResult(nameAndResTuple):
    name,res = nameAndResTuple
    if 'commonNames' not in res: return (name,False,[])
    commonNames = res['commonNames']
    if noResults(commonNames): return (name,False,[]) 
    if len(name.split(" ")) == 1: 
        commonNames = list(filter(lambda x: checkIfCommonNameResultIsValid(name,x['commonName']),commonNames))
    commonNamesWithId = list(map(lambda x: (x['commonName'],x['tsn']) , commonNames))
    scientificNames = mapTSNsToScientificNames(commonNamesWithId)
    return (name,True,list(itertools.chain(*scientificNames)))

def mapTSNsToScientificNames(commonNamesWithId):
    urls = list(map(prepareTSNUrl,commonNamesWithId))
    reqs = (grequests.get(url) for url in urls)
    results = grequests.map(reqs,size=10)
    scientificNames = ([r.json() for r in results])
    scientificNames = list(map(handleHigherTaxaAPIOutput,scientificNames))
    return scientificNames

def noResults(commonNames):
    return commonNames is None or len(commonNames) == 0 or (len(commonNames) == 1 and commonNames[0] is None)

def prepareTSNUrl(commonNameTup):
    name,tsnId = commonNameTup
    baseUrl = "https://www.itis.gov/ITISWebService/jsonservice/getFullRecordFromTSN?tsn="
    return baseUrl+str(tsnId)

def handleHigherTaxaAPIOutput(response):
    if 'scientificName' not in response: return []
    response = response['scientificName']
    if 'combinedName' not in response: return []
    response = response['combinedName']

    response = cleanSingleSpeciesString(response)
    if len(response.strip().split(" ")) < 2: 
        return higherLevelAPI([("hello",('family',response))])[0][2]
    else:
        return [response]

def checkIfCommonNameResultIsValid(name,result):
    result = result.lower().split(" ")
    stringPotential1 = name 
    stringPotential2 = name+'s' #plurals
    return stringPotential1 in result or stringPotential2 in result