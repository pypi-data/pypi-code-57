# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from sfsdk import log
from sfsdk import exrsettings
from sfsdk import authsettings
from urllib.parse import urlparse
import boto3
import requests
import re
import time
import tempfile
import json

r = requests.Session()
#r.proxies.update({'https': 'http://127.0.0.1:8090'})
#r.verify = False

remote_archive_format = '%s-%s-%d.zip'

ctoken = None
url = None

hub_url = None
hub_token = None

def login_to_deployment(username, password, management_url):

    global r, ctoken, url

    url = management_url
    source = authsettings.current_source

    r.headers.update(
            authsettings.settings['sources'][source].get('headers', {})
        )

    r.post(
            url + '/handler', 
            json={
                "action":"doLogin",
                "username": username,
                "password": password
                }
            )
 
    res = r.post(
            url + '/management/sfadmin/handler', 
            json={"action":"getUserCToken"},
            allow_redirects=False
    )

    if res.status_code == 200:
        ctoken = res.json() ['ctoken']
        log.header("Logged in %s deployment as user %s" % (source, username))
    else:
        raise log.FatalMsg("Failed authentication on %s deployment as user %s, check credentials" % (source, username))

def get_s3_creds_via_deployment():

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":"getS3Credentials"} )

    return res.json()

def get_ecr_creds_via_deployment():

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":"getECRCredentials"} )

    return res.json()

def login_to_hub(username, password, management_hub_url):

    global hub_token, hub_url

    hub_url = management_hub_url
    
    source = authsettings.current_source
    r.headers.update(
            authsettings.settings['sources'][source].get('headers', {})
        )

    res = r.post(
            hub_url + '/rest/api/login-developer',
            json = {
                "username": username,
                "password": password
                } 
            )

    hub_repr = 'SecureFlag' if management_hub_url == authsettings.default_hub_url else source

    if res.status_code != 200:
        raise log.FatalMsg("Failed authentication to the %s hub as user '%s', check credentials in %s" % (hub_repr, username, authsettings.settings_path))
    else:
        log.header("Logged in the %s hub  as user '%s'" % (hub_repr, username))
        hub_token = res.json()

def get_s3_creds_via_hub():

    res = r.get(
            hub_url + '/rest/user/uploads/credentials',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    return res.json()

def get_arn_via_hub():

    res = r.get(
            hub_url + '/rest/user/uploads/bucket',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    return res.json()['arn']

def get_arn_via_deployment():

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":"getUploadBucket"} )

    return res.json()['arn']

def get_frameworks_via_hub():

    res = r.get(
            hub_url + '/rest/user/frameworks',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            })
    
    if res.status_code == 204:
        return []

    return res.json()

def get_frameworks_via_deployment():

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":"getFrameworks", "ctoken": ctoken} )

    return res.json()

def get_technologies_via_hub():

    res = r.get(
            hub_url + '/rest/user/technologies',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )
    
    if res.status_code == 204:
        return []

    return res.json()

def get_technologies_via_deployment():

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":"getHubTechnologyKBList", "ctoken": ctoken} )

    return res.json()

def get_technology_via_deployment_by_uuid(uuid):

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":" getHubTechnologyItem", "ctoken": ctoken, "uuid": uuid} )

    return res.json()

def get_technology_via_hub_by_uuid(uuid):

    res = r.get(
            hub_url + '/rest/user/technologies/%s' % uuid,
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    if res.status_code == 204:
        return {}

    return res.json()

def get_vulnerabilities_via_hub():

    res = r.get(
            hub_url + '/rest/user/vulnerabilities',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    if res.status_code == 204:
        return []

    return res.json()

def get_vulnerabilities_via_deployment():

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":"getHubVulnerabilityKBList", "ctoken": ctoken} )
    
    return res.json()

def get_vulnerability_via_hub_by_uuid(uuid):

    res = r.get(
            hub_url + '/rest/user/vulnerabilities/%s' % uuid,
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    if res.status_code == 204:
        return {}

    return res.json()

def get_vulnerability_via_deployment_by_uuid(uuid):

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":"getHubKBItem", "ctoken": ctoken, "uuid": uuid } )

    return res.json()

def get_exercises_via_deployment():

    res = r.post(
            url + '/management/sfadmin/handler',
            json = {"action":"getExercises","ctoken": ctoken} )

    exercises_raw = res.json()

    exercises_raw = exercises_raw.get('exercises', [])

    return exercises_raw

def get_exercises_via_hub():

    res = r.get(
            hub_url + '/rest/user/exercises',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    if res.status_code == 204:
        return {}

    return res.json()

def get_exercise_by_uuid(uuid):

    res = r.post(
        url + '/management/sfadmin/handler',
        json = {"action":"getExerciseDetails", "uuid": uuid, "ctoken": ctoken} )

    return res.json()

def push_exercise(exercise_json, exercises_uuids):

    if exercise_json['uuid'] in exercises_uuids:
        log.debug('Updating exercise with uuid %s' % exercise_json['uuid'])
        exercise_json['action'] = "updateExercise"
    else:
        log.debug('Adding exercise as new')
        exercise_json['action'] = "addExercise"

    exrsettings.fix_outgoing_exercise_data(exercise_json)

    exercise_json['ctoken'] = ctoken

    if log.verbose:
        with tempfile.NamedTemporaryFile(
                mode='w+',
                suffix='-push-exercise-last-pushed.json',
                delete=False
                ) as exercise_debug_file:
            log.debug('Saving JSON debug to %s' % (exercise_debug_file.name))
            json.dump(exercise_json, exercise_debug_file, indent=4)

    res = r.post(
            url + '/management/sfadmin/handler',
            json = exercise_json )

    return res.json()

def push_exercise_and_get_new_json(exercise_json, exercises_uuids):

    push_res = push_exercise(exercise_json, exercises_uuids)
    if push_res.get('result') != 'success':
        log.debug(str(push_res))
        raise log.FatalMsg("Exercise has not been pushed, its metadata might be corrupted of the exercise could be read-only")

    new_uuid = push_res['uuid']

    return get_exercise_by_uuid(new_uuid)

def push_to_s3(archive_path, aws_creds, username, aws_arn):

    stsclient = boto3.client(
        'sts',
        aws_access_key_id=aws_creds['accessKeyId'],
        aws_secret_access_key=aws_creds['secretAccessKey'],
        aws_session_token=aws_creds['sessionToken'],
    )
    account_identity = stsclient.get_caller_identity()

    s3client = boto3.client(
        's3',
        aws_access_key_id=aws_creds['accessKeyId'],
        aws_secret_access_key=aws_creds['secretAccessKey'],
        aws_session_token=aws_creds['sessionToken'],
    )

    remote_archive_name = remote_archive_format % (
        account_identity['Account'],
        username,
        int(time.time())
    )

    bucket = aws_arn.split(":")[5]

    try:
        res = s3client.upload_file(
            archive_path + '.zip', 
            bucket, 
            remote_archive_name
        )
    except boto3.exceptions.S3UploadFailedError as e:
        raise log.FatalMsg(str(e))

    log.header('Exercise has been published as %s' % (remote_archive_name))

def create_repo_and_get_image_url_via_deployment(image_name):

    res = r.post(
        url + '/management/sfadmin/handler',
        json = {"action":"createECRRepo", "ctoken": ctoken, "name": image_name} 
    )

    return res.json().get('url')