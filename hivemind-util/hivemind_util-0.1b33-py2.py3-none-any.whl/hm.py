import pkg_resources
import requests
import json
import os
import re
import pandas as pd
import re
try:  # Python 2/3 compatibility
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest


def help(searchterm=''):
    '''
    Displays the help file text.
    searchterm: search for hivemindutil method names containing the given string
    
    returns: print to stdout the help text or help text for methods with names 
        containing the searchterm.
    '''
    helpFile = pkg_resources.resource_string(__name__, 'help.txt')
    hf = helpFile.decode('utf8')

    m = re.split(r'(- \w*\([^\)]*\))', hf)
    if searchterm:
        for idx in range(1,len(m),2):
            if searchterm in m[idx].lower().split('(')[0]:
                print(''.join(m[idx:idx+2]))
    else:
        print(hf)


def info(searchterm=''):
    '''
    Wrapper function for the hepp function.
    searchterm: search for hivemindutil method names containing the given string
    
    returns: print to stdout the help text or help text for methods with names 
        containing the searchterm.
    '''
    help(searchterm) 


def makeAuthHeader(apiKey):
    return {'Authorization': 'ApiKey {0}'.format(apiKey)}


def removeMetadata(x):
    x.pop('_metadata', None)
    return x


def cleanBaseUrl(url):
    url = url.rstrip('/')
    if(url[:4].lower()!='http'):
        url = 'https://' + url
    return url


def checkHttpResponse(r):
    if(r.status_code>=300):
        print('API request error')
        print('Url: ' + r.url)
        print('Status: ' + str(r.status_code))
        print('Reason: ' + r.reason) 
        print('Text: ' + r.text)
        print('Request body:')
        print(r.request.body)
    return r


def getResults(taskId, baseUrl, apiKey, incIncompleteInstances=False, incIterations=True): 
    if(incIncompleteInstances==True):
        incIncompleteInstances='true'
    if(incIncompleteInstances==False):
        incIncompleteInstances='false'
    if(incIterations==True):
        incIterations='true'
    if(incIterations==False):
        incIterations='false'
        
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        
        paginatedUrl = '{0}/api/tasks/{1}/results?perPage=1000&incIncompleteInstances={2}&incIterations={3}'.format(baseUrl, taskId, incIncompleteInstances, incIterations)
        results = []

        while paginatedUrl is not None:            
            response = checkHttpResponse(s.get(paginatedUrl))         
            results += response.json()
            n = response.links["next"] if "next" in response.links else None
            if n is not None:
                paginatedUrl = baseUrl + n["url"]
            else:
                paginatedUrl = None
    return results    


def getInstanceResult(taskId, baseUrl, apiKey, instanceId):
    target = '{0}/api/tasks/{1}/instances/{2}/results'.format(baseUrl, taskId, instanceId)
    r = requests.get(target, headers=makeAuthHeader(apiKey))
    r.raise_for_status()
    return r.json()


def getTableExtractionResults(taskId, baseUrl, apiKey, instanceId, outputDir=None, outputFormat='csv'):
    def getFormatted(fFormat, data, outDir, outFile):
        if fFormat == 'csv':
            ret = os.path.join(outDir, outFile)
            data.to_csv(ret,
                        header=False,
                        index=False,
                        encoding='utf-8-sig')
        elif fFormat == 'dataframe':
            ret = data.copy()
        else:
            raise Exception('Unknown return format requested')

        return ret

    if outputDir is None:
        outputDir = ''

    counter = {}
    outputName = '{filename}_{tabletype}_page{tablePage:03}_{tableNum:02}.csv'
    instanceResult = getInstanceResult(taskId, baseUrl, apiKey, instanceId)

    tables = instanceResult[0].get('data').get('Tables', [])
    dataSet = []
    for table in tables:
        tablepg = table.get('relativePageNumber')
        file = table.get('file')
        td = table.get('tableData')
        tt = table.get('metadata').get('tableType')
        tablenum = counter.get((file, tablepg), 0) + 1
        counter[(file, tablepg)] = tablenum
        outputFile = outputName.format(filename=file, tabletype=tt, tablePage=tablepg, tableNum=tablenum)
        df = pd.read_json(json.dumps(td), orient='columns')
        dataSet.append(getFormatted(outputFormat, df, outputDir, outputFile))
    return dataSet


def getInstances(taskId, baseUrl, apiKey, expandSummary=True): 
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        expandSummaryOption = '&expand=summary' if expandSummary else ''
        paginatedUrl = '{0}/api/tasks/{1}/instances?perPage=1000{2}'.format(baseUrl, taskId, expandSummaryOption)
        instances = []

        while paginatedUrl is not None:
            response = checkHttpResponse(s.get(paginatedUrl))
            instances += response.json()
            n = response.links["next"] if "next" in response.links else None
            if n is not None:
                paginatedUrl = baseUrl + n["url"]
            else:
                paginatedUrl = None
    return instances


def getInstance(taskId, baseUrl, apiKey, instanceId, expandSummary=True): 
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        expandSummaryOption = '?expand=summary' if expandSummary else ''
        paginatedUrl = '{0}/api/tasks/{1}/instances/{2}{3}'.format(baseUrl, taskId, instanceId, expandSummaryOption)
        response = checkHttpResponse(s.get(paginatedUrl))
            
    return response.json()     


def getInstanceIds(taskId, baseUrl, apiKey):
    instances = getInstances(taskId, baseUrl, apiKey)
    instanceIds = []
    for i in instances:
        instanceIds.append(i.get('id'))
    return instanceIds


def transferEntry(source, target, entryFields=["data", "annotations"], sourceIdField="id", targetIdField="instanceId"):
    # source and target are each an array of dictionaries.
    # For each entry in source, extract "entry" and insert it into  
    # the dictionary in target in which sourceId matches targetId.
    # By default transfers "data" from list of instance dictionaries to list of results dictionaries.
    # If entry doesn't exist in source, insert null into target
    
    # Create set of sourceId : entry pairs
    
    for entryField in entryFields:
        sourceIdEntryPairs = {}
        for s in source:
            if(entryField not in s):
                continue
            entry = s.get(entryField)
            sourceId = s.get(sourceIdField)
            sourceIdEntryPairs[sourceId] = entry
        for t in target:
            targetId = t.get(targetIdField)
            t[entryField] = sourceIdEntryPairs.get(targetId)


def getInstancesAndResults(taskId, baseUrl, apiKey, expandSummary=True, incIncompleteInstances=False, incIterations=True):
    # Make API calls for both instances and results, and transfer data from the former to the latter.
    instances = getInstances(taskId, baseUrl, apiKey, expandSummary)
    results = getResults(taskId, baseUrl, apiKey, incIncompleteInstances, incIterations)
    transferEntry(instances, results)
    return results


def listFilesUploaded(taskId, baseUrl, apiKey):
    # Make API call to get list of filenames uploaded to the task.
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        paginatedUrl = '{0}/api/tasks/{1}/files?perPage=1000'.format(baseUrl, taskId)
        result = []

        while paginatedUrl is not None:
            response = checkHttpResponse(s.get(paginatedUrl))
            result += response.json()
            n = response.links["next"] if "next" in response.links else None
            if n is not None:
                paginatedUrl = baseUrl + n["url"]
            else:
                paginatedUrl = None
        lstFilesAlreadyUploaded = map(lambda x: x.get('filename'), result)
    return list(lstFilesAlreadyUploaded)


def uploadFiles(taskId, baseUrl, apiKey, lstFilenames, localRepo, overwrite=False):    
    if(overwrite==False):
        filesUploaded = listFilesUploaded(taskId, baseUrl, apiKey)
        lstFilenames = list(set(lstFilenames) - set(filesUploaded))
        
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        fileUrl = '{0}/api/tasks/{1}/files'.format(baseUrl, taskId)
        files = map(lambda x: os.path.join(localRepo, x), lstFilenames)

        for filename in files:
            with open(filename, 'rb') as f:
                try:
                    response = checkHttpResponse(s.post(fileUrl, files={'file': f}))
                except:
                    continue


def downloadFile(filepath, localRepo, prefix='', overwrite=False):

    pattern = r'/hivemind\.lambda\.task\.\d+/output/\d+/\d+/(.*)\?X-Amz-Expires='
    filename = re.search(pattern, filepath).group(1)

    newFilename = '{0}_{1}'.format(prefix, filename) if prefix!='' else filename

    lstFilesDownloaded = os.listdir(localRepo)
    if overwrite or (newFilename not in lstFilesDownloaded):
        urlrequest.urlretrieve(filepath, os.path.join(localRepo, newFilename))
    return newFilename


def getIterations(taskId, baseUrl, apiKey, instanceId): 
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)        
        iterationResults = checkHttpResponse(s.get('{0}/api/tasks/{1}/instances/{2}/results'.format(baseUrl, taskId, instanceId))).json()
    return iterationResults       


def getIterationIds(taskId, baseUrl, apiKey, instanceId):
    iterationResults = getIterations(taskId, baseUrl, apiKey, instanceId)
    iterationIds = []
    for i in iterationResults:
        iterationIds.append(i.get('iterationId'))
    return iterationIds


def deleteIteration(taskId, baseUrl, apiKey, instanceId, iterationId):    
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        response = checkHttpResponse(s.delete('{0}/api/tasks/{1}/instances/{2}/iterations/{3}'.format(baseUrl, taskId, instanceId, iterationId))) 
    return response


def deleteInstance(taskId, baseUrl, apiKey, instanceId):
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    iterationIds = getIterationIds(taskId, baseUrl, apiKey, instanceId)
    
    for iterationId in iterationIds:
        deleteIteration(taskId, baseUrl, apiKey, instanceId, iterationId)
    
    with requests.Session() as s:
        s.headers.update(authHeader)
        response = checkHttpResponse(s.delete('{0}/api/tasks/{1}/instances/{2}'.format(baseUrl, taskId, instanceId)))
    return response
   
    
def setAnnotation(taskId, baseUrl, apiKey, instanceId, key, value):
    authHeader = makeAuthHeader(apiKey)
    with requests.Session() as s:
        s.headers.update(authHeader)
        baseUrl = cleanBaseUrl(baseUrl)               
        data = {
            'key': key,
            'value': value
        }        
        response = checkHttpResponse(s.post('{0}/api/tasks/{1}/instances/{2}/annotations'.format(baseUrl, taskId, instanceId), json = data))

    return response
    
def addAnnotation(taskId, baseUrl, apiKey, instanceId, key, value):
    return setAnnotation(taskId, baseUrl, apiKey, instanceId, key, value)


def createInstance(taskId, baseUrl, apiKey, name, instructions='', data={}, overrideSchema=None, tags=[], priority=0, annotations = {}):
    # overrideSchema must either have a value or be null; cannot be {}
    if overrideSchema=={}:
        overrideSchema = None
    authHeader = makeAuthHeader(apiKey)
    with requests.Session() as s:
        s.headers.update(authHeader)
        baseUrl = cleanBaseUrl(baseUrl)               
        instance = {
            'name' : name,
            'instruction' : instructions,
            'data' : data,
            'overrideSchema' : overrideSchema,
            'tags' : tags,
            'priority' : priority
        }        
        response = checkHttpResponse(s.post('{0}/api/tasks/{1}/instances'.format(baseUrl, taskId), json = instance))
        instanceId = response.json()['id']
        for x in annotations:
            setAnnotation(taskId, baseUrl, apiKey, instanceId, x, annotations[x])

    return response

def reiterateInstance(taskId, baseUrl, apiKey, instanceId):
    authHeader = makeAuthHeader(apiKey)
    with requests.Session() as s:
        s.headers.update(authHeader)
        baseUrl = cleanBaseUrl(baseUrl)               
        response = checkHttpResponse(s.post('{0}/api/tasks/{1}/instances/{2}/reiterate'.format(baseUrl, taskId,instanceId)))
    return response
        

def deleteAnnotation(taskId, baseUrl, apiKey, instanceId, key):
    authHeader = makeAuthHeader(apiKey)
    with requests.Session() as s:
        s.headers.update(authHeader)
        baseUrl = cleanBaseUrl(baseUrl)           
        response = checkHttpResponse(s.delete('{0}/api/tasks/{1}/instances/{2}/annotations/{3}'.format(baseUrl, taskId, instanceId, key)))

    return response
    
def wipe(taskId, baseUrl, apiKey):
    instanceIds = getInstanceIds(taskId, baseUrl, apiKey)
    for id in instanceIds:
        deleteInstance(taskId, baseUrl, apiKey, id)
