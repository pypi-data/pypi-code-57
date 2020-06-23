import opisense_client as oc
import datetime
import random
import json
from time import sleep

""" Inputs """

# set test inputs
opisense_site = {
    "clientData": {},
    "typeId": 15,
    "street": "Street test site",
    "postalCode": "0000",
    "city": "Test City",
    "country": "Test Country",
    "timeZoneId": "UTC",
    "name": "Test Site"
}

opisense_source = {
    "siteId": 0,
    "serialNumber": "Source_test_SN",
    "clientData": {},
    "energyTypeId": 1,
    "name": "Source_test",
    "sourceTypeId": 72,
    "timeZoneId": "UTC"
}

opisense_variable = {
    "name": "Variable Test",
    "sourceId": 0,
    "isDefault": True,
    "unitId": 8,
    "granularity": 1,
    "granularityTimeBase": "Second",
    "quantityType": "Instantaneous",
    "mappingConfig": "mapping_config"
}

# get Opisense credentials from file
credentials_file_path = 'opisense_client/tests/test_credentails.JSON'

with open(credentials_file_path, encoding='utf-8') as file:
    credentials = json.load(file)
user_credentials = credentials['user']
api_credentials = credentials['api']

""" TESTS """


def test_OpisenseObject():
    site = oc.OpisenseObject(type='site', opisense_object=opisense_site)
    assert site.type == 'site'
    assert site.id == None
    assert site.content == {'clientData': {},
                            'typeId': 15,
                            'street': 'Street test site',
                            'postalCode': '0000',
                            'city': 'Test City',
                            'country': 'Test Country',
                            'timeZoneId': 'UTC',
                            'name': 'Test Site'}

    assert site.json() == '{"clientData": {}, "typeId": 15, "street": "Street test site", "postalCode": "0000", "city": "Test City", "country": "Test Country", "timeZoneId": "UTC", "name": "Test Site"}'

    assert site.api_path == 'sites'


def test_ApiFilter():
    filter = oc.ApiFilter('data', granularity='Hour',
                          date_from='2019-01-01T23:00:00',
                          date_to='2019-01-02T23:00:00')

    assert filter.filters['from'] == '2019-01-01T23:00:00'
    assert filter.filters['to'] == '2019-01-02T23:00:00'
    assert filter.filters == {'granularity': 'Hour', 'from': '2019-01-01T23:00:00', 'to': '2019-01-02T23:00:00'}
    assert filter.path == 'data'


def test_authorize():
    opisense_token = oc.authorize(user_credentials, api_credentials, feedback=True)
    assert type(opisense_token) == str


# If Authorize is tested and OK, get one uniaue token for the remaining tests
opisense_token = oc.authorize(user_credentials, api_credentials, feedback=True)


def test_GET():
    assert oc.GET(opisense_token, oc.ApiFilter('units')).status_code == 200


def test_OpisenseObject_Calls():
    # POST
    site = oc.OpisenseObject(type='site', opisense_object=opisense_site)
    result = site.POST(opisense_token)
    assert result.status_code == 200
    site.id = result.json()
    assert type(result.json()) == int

    source = oc.OpisenseObject(type='source', opisense_object=opisense_source)
    source.content['siteId'] = site.id
    result = source.POST(opisense_token)
    source.id = result.json()['id']
    assert result.status_code == 200
    assert type(result.json()) == dict

    variable = oc.OpisenseObject(type='variable', opisense_object=opisense_variable)
    variable.content['sourceId'] = source.id
    result = variable.POST(opisense_token, parent_id=source.id)
    variable.id = result.json()['id']
    assert result.status_code == 200
    assert type(result.json()) == dict

    # PUT
    source.content['name'] = 'Source New Name'
    result = source.PUT(opisense_token)
    assert result.status_code == 204
    assert oc.GET(opisense_token, oc.ApiFilter('sources', id=source.id), json_output=True)[0][
               'name'] == 'Source New Name'

    variable.content['name'] = 'Variable New Name'
    result = variable.PUT(opisense_token, parent_id=source.id)
    assert result.status_code == 204
    assert oc.GET(opisense_token, oc.ApiFilter('variables', id=variable.id), json_output=True)[0][
               'name'] == 'Variable New Name'

    # DELETE
    result = variable.DELETE(opisense_token,
                             force_path='/sources/{}/variables/'.format(variable.content["sourceId"]))
    assert result.status_code == 204

    result = source.DELETE(opisense_token)
    assert result.status_code == 204

    result = site.DELETE(opisense_token)
    assert result.status_code == 204


def test_StandardData_POST():
    variableId = 991929

    now = datetime.datetime.now()
    start = now
    datapoints = oc.DataPoints(now, random.randint(5, 25))
    for _ in range(5):
        now += datetime.timedelta(minutes=5)
        datapoints.__add__(now, random.randint(5, 25))

    data = oc.StandardData(datapoints,
                           variableId=variableId)

    result = data.POST(opisense_token)
    assert result.status_code == 204

    sleep(5)

    result = oc.GET(opisense_token, oc.ApiFilter('data', variableId=991929,
                                                 date_from=start.strftime('%Y-%m-%dT%H:%M:%S%z')))
    assert result.status_code == 200
    assert result.json().__len__() == 6
