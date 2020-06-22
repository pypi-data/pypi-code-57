# import grequests 
from requests import Session
import itertools

def taxonomyAPI(names):
    capNames = list(map(lambda x: x.capitalize(),names))
    reqs = packageReqs(capNames)
    urls = list(map(prepUrl,reqs))
    session = Session()
    results = list(map(lambda x: session.get(x),urls))
    succeeded,excepted = groupToSuccessesAndFailures(results,reqs)
    newSucceeded, newExcepted = individuallyMakeRequests(excepted.split("|"))
    succeeded.extend(newSucceeded)
    speciesResponses = list(map(processSingleResponse,succeeded))
    speciesResponses.extend(list(map(lambda x:(x,False,('','')),newExcepted)))
    return speciesResponses,newExcepted

def groupToSuccessesAndFailures(results,reqs):
    succeeded = []
    excepted = []
    for i in range(len(results)):
        try: 
            packagedResults = results[i].json()['data']
            if len(packagedResults) != (reqs[i].count("|")+1): raise ValueError()
            succeeded.extend(packagedResults)
        except: excepted.append(reqs[i])
    excepted = "|".join(excepted)
    return succeeded,excepted

def packageReqs(names):
    bulked = []
    politeness = 50
    for i in range(0,len(names),politeness):
        bulked.append("|".join(names[i:i+politeness]))
    return bulked

def prepUrl(req):
    return f'http://resolver.globalnames.org/name_resolvers.json?names={req}'

def processSingleResponse(response):
    try:
        if response['is_known_name']: return (response['supplied_name_string'].lower(), True, parseSingleTaxonomyFromAPI(response))
        elif 'results' in response: return (response['supplied_name_string'].lower(),False, parseSingleTaxonomyFromAPI(response))
        return (response['supplied_name_string'].lower(), False, ('',''))
    except:
        return('hello',False,('',''))

def parseSingleTaxonomyFromAPI(taxonomicAPIres):
    dataFromMultipleSources = taxonomicAPIres['results']
    dataFromMultipleSources = list(map(extractTaxaData,dataFromMultipleSources))
    for item in ['species','genus','subfamily','family']:
        for taxaMap in dataFromMultipleSources:
            if 'kingdom' in taxaMap and taxaMap['kingdom'].strip().lower() == 'orthornavirae': return ('','')
            if (item in taxaMap) and (taxaMap[item].strip() != ''): 
                return (item,taxaMap[item].strip())
    return ('','')
    
def extractTaxaData(singleTaxaSource):
    mappingDict = {}
    try: mappingDict = dict(zip(singleTaxaSource['classification_path_ranks'].lower().split("|"),\
                                singleTaxaSource['classification_path'].lower().split("|")))
    except: pass
    return mappingDict

def callTaxaAPI(rawNames):
    excepted = []
    preparedAPILoad = prepareTaxaAPIinput(rawNames) #try a bulk-call
    success,result = makeCall(preparedAPILoad) 
    if (not success) or (len(result) != len(rawNames)):
        namesSucceeded = list(filter(lambda resp: 'supplied_string_name' in resp, result))
        namesSucceeded = list(map(lambda resp: resp['supplied_string_name'], namesSucceeded))
        failedNames = list(set(rawNames) - set(namesSucceeded))
        succeededResults, failedNames = individuallyMakeRequests(failedNames)
        result.extend(succeededResults)
        excepted.extend(failedNames)
    
    return result, excepted

def prepareTaxaAPIinput(names):
    namesToSend = "|".join(names)
    return namesToSend
    
def individuallyMakeRequests(names):
    succeededResults = []
    failedNames = []
    for name in names:
        success,result = makeCall(name)
        if success: succeededResults.extend(result)
        else: failedNames.extend(name)
    
    return succeededResults, failedNames

def makeCall(preparedAPILoad):
    try:
        reqs = (grequests.get(url) for url in [f'http://resolver.globalnames.org/name_resolvers.json?names={preparedAPILoad}'])
        results = grequests.map(reqs,size=1)
        res = ([r.json()['data'] for r in results][0])
        return (True,res)
    except Exception as e: 
        return (False,[])
