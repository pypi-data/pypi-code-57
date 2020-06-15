"""
Python method wrappers around ngscheck service REST API calls.

The JSON manifest files used have the following simple form:
[
    {
        "jobid": <job_1>,
        "filepath": <input_filepath_1>
    },
    {
        "jobid": <job_2>,
        "filepath": <input_filepath_2>
    },
    ...
]
"""
import json
import logging
import os.path
import uuid

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import requests


APIBASE = "https://f4b45zm2fc.execute-api.ap-southeast-2.amazonaws.com/v1"
APIRESULTS = f"{APIBASE}/pickup"
APISTATUS = f"{APIBASE}/status"
APISUBMIT = f"{APIBASE}/submit"
APIUSERID = f"{APIBASE}/userid"
# ngscheck-service-client
CLIENTID = '7n8nbvr1slgml6nv5221pn1k65'
# use boto anonymously
COGNITO = boto3.client('cognito-idp', region_name='ap-southeast-2',
                       config=Config(signature_version=UNSIGNED))
NGSCHECK_EXTENSIONS = ['.ngcbas.json', '.ngcbas.pdf', '.ngcbas.xml']
LOGGER = logging.getLogger(__name__)


def get_access_token(identifier, password):
    """
    Returns AuthenticationResult.AccessToken from Cognito
    """
    response = COGNITO.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={'USERNAME': identifier, 'PASSWORD': password},
        ClientId=CLIENTID)
    LOGGER.info("auth response OK")
    return response['AuthenticationResult']['AccessToken']


def get_results(manifest_file, userid, token):
    """
    Get results for all SUCCEEDED jobs listed in the manifest.
    """
    try:
        manifest = json.loads(manifest_file.read())
        manifest_file.close()
    # if get_status was called first, manifest_file is closed
    except ValueError:
        with open(manifest_file.name) as reopened:
            manifest = json.loads(reopened.read())

    succeeded = [job for job in manifest if job['status'] == 'SUCCEEDED']
    failed = [job for job in manifest if job['status'].startswith('FAILED')]
    if len(succeeded) + len(failed) != len(manifest):
        LOGGER.warning("There are unfinished jobs. Aborting")
        return
    if failed:
        LOGGER.warning("There are failed jobs")
        LOGGER.warning(json.dumps(failed, indent=2))

    for job in succeeded:
        jobid = job['jobid']
        infilepath = job['filepath']
        key = os.path.basename(infilepath)
        for ext in NGSCHECK_EXTENSIONS:
            response = requests.get(
                f"{APIRESULTS}/{userid}/{jobid}/{key}{ext}",
                headers={'Authorization': token})
            response.raise_for_status()
            outfilepath = infilepath + ext
            with open(outfilepath, 'xb') as outfile:
                outfile.write(response.content)
            LOGGER.info(outfilepath)


def get_status(manifest_file, userid, token):
    """
    Get and update the status of the jobs listed in the manifest.
    """
    manifest = json.loads(manifest_file.read())
    manifest_file.close()
    for job in manifest:
        jobid = job['jobid']
        response = requests.get(
            f"{APISTATUS}/{userid}/{jobid}/STATUS",
            headers={'Authorization': token})
        response.raise_for_status()
        job.update({"status": response.text})
    manifest_str = json.dumps(manifest, indent=2)
    with open(manifest_file.name, 'w') as manifest_update:
        manifest_update.write(manifest_str)
    LOGGER.info(manifest_str)


def get_userid(token):
    """
    Returns userid from the token, in case it isn't known already.
    """
    response = requests.get(
        f"{APIUSERID}",
        headers={'Authorization': token})
    return response.text


def submit(files, manifest_file, userid, token):
    """
    Generate a job manifest and submit some files for processing.
    """
    manifest = [{'jobid': str(uuid.uuid4()), 'filepath': f.name}
                for f in files]
    manifest_str = json.dumps(manifest, indent=2)
    manifest_file.write(manifest_str)
    manifest_file.close()
    for infile, job in zip(files, manifest):
        jobid = job['jobid']
        key = os.path.basename(job['filepath'])
        response = requests.put(
            f"{APISUBMIT}/{userid}/{jobid}/{key}",
            data=infile.read(),
            headers={'Authorization': token})
        response.raise_for_status()
    LOGGER.info(manifest_str)
