import itertools
from .dataCleaning import *
from requests import Session
from itertools import accumulate

def reverseNameAPI(bestEffortsOnSpecies):
    noWorkResults = []
    toProcess = []
    noWorkResults = list(filter(lambda x: len(x[1])==0,bestEffortsOnSpecies))
    bestEffortsOnSpecies = list(filter(lambda x: len(x[1])>0,bestEffortsOnSpecies))
    lenKeeper = list(map(lambda x: len(x[1]),bestEffortsOnSpecies))
    toProcess = list(itertools.chain(*list(map(lambda x: x[1],bestEffortsOnSpecies))))
    urls = list(map(constructUrls,toProcess))
    session = Session()
    results = list(map(lambda x: session.get(x),urls))
    results = safeMapResToJson(results)
    results = reMapResultsWithBaseNames(bestEffortsOnSpecies,lenKeeper,results)
    results = list(map(processIndividualGroup,results))
    noWorkResults = list(map(lambda x: (x[0],False,[]),noWorkResults))
    return [*noWorkResults,*results]

def reMapResultsWithBaseNames(bestEffortsOnSpecies,lenKeeper,results):
    resultTuples = []
    bestEffortsOnSpecies = list(map(lambda x: x[0], bestEffortsOnSpecies))
    indexMapper = r = [0,*list(accumulate(lenKeeper, lambda x, y: x+y))]
    splitResults = [results[indexMapper[i]:indexMapper[i+1]] for i in range(len(indexMapper)-1)]
    return list(zip(bestEffortsOnSpecies,splitResults))

def safeMapResToJson(results):
    res = []
    for r in results:
        try: res.append(r.json())
        except: res.append({})
    return res
        
def constructUrls(name):
    return "https://www.itis.gov/ITISWebService/jsonservice/getITISTermsFromScientificName?srchKey="+name

def processIndividualGroup(nameAndResTuple):
    name,res = nameAndResTuple
    return (name,True,list(set( \
                            itertools.chain(*list( \
                                filter( \
                                    lambda x: len(x) > 0, \
                                    map(processIndividualResult,res) \
                                ) \
                            )) \
                        )) \
            )

def processIndividualResult(res):
    if 'itisTerms' not in res: return []
    if res['itisTerms'] is None: return []
    if res['itisTerms'][0] is None: return []
    nameTranslation = res['itisTerms']
    resultsToReturn = []
    for item in nameTranslation:
        if 'commonNames' not in item: continue 
        if item['commonNames'] is None: continue 
        cleanResults = list(filter(lambda x: x is not None,item['commonNames']))
        cleanResults = list(map(lambda x: " ".join(list(map(lambda y: y.capitalize(),x.split(" ")))),cleanResults))
        resultsToReturn.append(cleanResults)
    
    return list(itertools.chain(*resultsToReturn))