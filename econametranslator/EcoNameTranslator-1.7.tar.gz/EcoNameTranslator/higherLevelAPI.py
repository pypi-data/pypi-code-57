from requests import Session
from .dataCleaning import *

def higherLevelAPI(originalNamesWithTaxa):
    noWorkResults = []
    toProcess = []
    for name,taxaDetails in originalNamesWithTaxa:
        if taxaDetails == '': noWorkResults.append((name, False, []))
        elif taxaDetails[0] == '': noWorkResults.append((name,False,[]))
        elif taxaDetails[0] == 'species': noWorkResults.append((name,True,[cleanSingleSpeciesString(taxaDetails[1])]))
        else: toProcess.append((name,taxaDetails))
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

def constructUrls(nameAndTaxaTuple):
    name, taxaDetails = nameAndTaxaTuple
    taxaRank,taxaName = taxaDetails
    return 'https://api.gbif.org/v1/species/search?q='+taxaName+'&rank=species'

def processIndividualResult(identifiedResponse):
    inTuple, response = identifiedResponse
    name, taxaDetails = inTuple
    rank, value = taxaDetails
    if 'results' in response:
        potentialSpecies = list(map(lambda x: x.get('species',''),response['results']))
        potentialSpecies = list(filter(lambda x: x != '',potentialSpecies))
        potentialSpecies = list(map(cleanSingleSpeciesString,potentialSpecies))
        if rank == "genus": potentialSpecies = list(filter(lambda x: x.split(" ")[0] == value,potentialSpecies))
        return (name,True,potentialSpecies)
    return (name,False,[])
