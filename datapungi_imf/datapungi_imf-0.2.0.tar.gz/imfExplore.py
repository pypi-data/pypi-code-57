'''
https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
   https://www.bd-econ.com/imfapi1.html
 
   The IMF's CompactData method, combined with codes for the series, frequency, area, and indicator, 
   returns a JSON structured dataset. The codes and method are explained in more detail as follows:
 
   - Method: **CompactData** retrieves data, **DataStructure** retrieves series information, and **GenericMetadata** returns the metadata;
   - Series: The broad group of indicators, in this case International Financial Statistics IFS;
   - Frequency: For example monthly M, quarterly Q, or annually A;
   - Area: The country, region, or set of countries, for example GB for the U.K., or GB+US for the U.K. and the U.S.;
   - Indicator: The code for the indicator of interest--IFS includes more than 2,500. In the example above, the code of interest is PMP_IX; and
   - Date Range (Optional): Use this to limit the data range returned, for example ?startPeriod=2010&endPeriod=2017 otherwise the full set of data is returned.
   - The order in which codes are combined is referred to as the dimensions of the data, in the IFS case: {Method}/{Series}/{Frequency}.{Area}.{Indicator}.{Date Range}
   - Part 2 covers how to use the DataStructure method to obtain the dimensions and codes for any series in the API. Part 3 discusses metadata and more complex requests, and also includes some links to additional references.
 
'''
 
import requests
import pandas as pd
import numpy as np
 
url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
 
# method: CompactData, Series: IFS, Frequency: M, Area: GB, Indicator: PMP_IX, 
 
#list of dbs:
def getDBs(key = 'DataFlow',url='http://dataservices.imf.org/REST/SDMX_JSON.svc/'):
    
    # Navigate to series in API-returned JSON data
    data = requests.get(f'{url}{key}').json()
    
    #clea output @id is just id with DS- in front of it keyFamily Agnecy ID is always IMF
    df_out = [ { 'id': entry['KeyFamilyRef']['KeyFamilyID'] , 'description':entry['Name']['#text'], 'language':entry['Name']['@xml:lang']} for entry in data['Structure']['Dataflows']['Dataflow'] ]
    df_out = pd.DataFrame(df_out)
    return(df_out)


def getParams(dbname,url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'):
    # get the parameter of a db
    # Navigate to series in API-returned SON data
    data = requests.get(f'{url}DataStructure/{dbname}').json()
    
    #cleaning:
    concepts = data.get('Structure',{}).get('Concepts',{}).get('ConceptScheme',{}).get('Concept',[])
    concepts = pd.DataFrame([ {'id':entry.get('@id',''), 'text' : entry.get('Name',{}).get('#text','')}   for entry in concepts])
    
    annotations = data.get('Structure',{}).get('KeyFamilies',{}).get('KeyFamily',{}).get('Annotations',{}).get('Annotation',[])
    annotations = pd.DataFrame([ {'title':entry.get('AnnotationTitle',''), 'text' : entry.get('AnnotationText',{}).get('#text','')}   for entry in annotations])
    
    codes = data.get('Structure',{}).get('CodeLists',{}).get('CodeList',[])
    codes =  {entry.get('@id',{}) : pd.DataFrame([ {'value': specs.get('@value',''), 'description' : specs.get('Description',{}).get('#text','') }  for specs in entry.get('Code',[])     ])  for entry in codes   }
    
    return(dict(concepts = concepts, annotations = annotations, codes = codes, data = data))

def getData(key,url='http://dataservices.imf.org/REST/SDMX_JSON.svc/'):
    # Navigate to series in API-returned JSON data
    data = (requests.get(f'{url}CompactData/{key}').json()['CompactData']['DataSet']['Series'])
    
    print(data['Obs'][-1]) # Print latest observation
    
    baseyr = data.get(['@BASE_YEAR'],"")  # Save the base year
    
    # Create pandas dataframe from the observations
    df_out = pd.DataFrame.from_dict(data['Obs']) \
        .rename(columns={'@TIME_PERIOD':'date','@OBS_VALUE':'value'}) \
        .set_index('date') \
        .astype({'value':'float'})
    return(df_out)
     
def getMeta(key):
    url='http://dataservices.imf.org/REST/SDMX_JSON.svc/'
    data = (requests.get(f'{url}GenericMetadata/{key}').json())['GenericMetadata']['MetadataSet']['AttributeValueSet']
    
    try:
        data = [entry.get('ReportedAttribute',entry) for entry in data]
        simplify = lambda x: {x['@conceptID']: x.get('Value',{}).get('#text',x) } if (isinstance(x,dict)) else {entry['@conceptID']: entry.get('Value',{}).get('#text','') for entry in x }
        data = [  [ simplify(x['ReportedAttribute']) for x in entry ] for entry in data ] #a list of (two) dicts
        data = [  {k: v for d in entry for k, v in d.items() } for entry in data  ]
    except:
        pass
    
    return(data)


getDBs()
getParams('IFS')
getData('IFS/A.GB.PMP_IX')
getData('IFS/M.GB.PMP_IX')
getMeta('IFS/A.GB.PMP_IX')

#search for all brazilian annual data:
getMeta('IFS/A.BR')
getMeta('IFS/A.BR.MFS') #description of an indicator obtained from the above list

