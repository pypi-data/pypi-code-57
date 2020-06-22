#  © Copyright IBM Corporation 2020.

import time
import datetime
import string
import textwrap
import json

from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler
from ai_lifecycle_cli.lib.utils import print_utils
from ai_lifecycle_cli.lib.actions import preparation


logger = LoggingHandler()


def create_deployment_job(client, space_id, deployment_job_spec):

    print("Creating deployment job...\n")

    post_deployment_job_url = "/v4/deployment_jobs"

    # Load deployment_job_spec
    with open(deployment_job_spec, 'r') as f:
        deployment_job_body = json.load(f)

    # Verify space ID in specification
    if deployment_job_body.get('space_id', 'do_not_exist') != space_id:
        print("Deployment job space ID in specification is not consistent with given space.")
        print("Given space ID: {}".format(space_id))
        print("Deployment job spec's space ID: {}".format(deployment_job_body.get('space_id', 'do_not_exist')))
        return

    # Create deployment job
    post_deploy_job_res = client.make_request('post', path=post_deployment_job_url, body=deployment_job_body)
    if not post_deploy_job_res.ok:
        raise Exception("Couldn't create new deployment job - reason: {}".format(post_deploy_job_res.text))

    deploy_guid = post_deploy_job_res.json()['metadata']['guid']
    print("Deployment job created with ID: {}".format(deploy_guid))


def delete_deployment_job(client, space_id, job_id):

    print("Cancelling deployment job...\n")

    # Check if deployment exists in space
    get_deployment_job_url = "/v4/deployment_jobs/{}".format(job_id)

    get_deploy_job_res = client.make_request('get', path=get_deployment_job_url)
    if not get_deploy_job_res.ok:
        raise Exception("Couldn't check if deployment job exists in space - reason: {}".format(get_deploy_job_res.text))

    if 'metadata' not in get_deploy_job_res.json():
        print("Deployment job does not exist.")
        return
    if get_deploy_job_res.json()['metadata']['space_id'] != space_id:
        print("Deployment job does not exists in given space.")
        print("Given space ID: {}".format(space_id))
        print("Deployment's space ID: {}".format(get_deploy_job_res.json()['metadata']['space_id']))
        return

    # Check if deployment job is already in completed or failed state
    try:
        job_status = get_deploy_job_res.json()['entity']['scoring']['status']['state']
        if job_status == 'completed':
            print("Cannot cancel deployment job with ID {} as it is already completed".format(job_id))
            return
        if job_status == 'failed':
            print("Cannot cancel deployment job with ID {} as it is in failed state".format(job_id))
            return
        if job_status == 'canceled':
            print("Cannot cancel deployment job with ID {} as it is already canceled".format(job_id))
            return
    except Exception as e:
        print("Couldn't retrieve current status of the job - trying to cancel it anyway...")

    # Cancelling deployment job
    delete_deployment_job_url = "/v4/deployment_jobs/{}".format(job_id)

    delete_deploy_job_res = client.make_request('delete', path=delete_deployment_job_url)
    if not delete_deploy_job_res.ok:
        raise Exception("Couldn't cancel deployment - reason: {}".format(delete_deploy_job_res.text))

    print("Cancelling deployment job with ID {} has been initiated".format(job_id))


def list_deployment_jobs(client, space_id):

    print("Listing deployment jobs...\n")

    # Listing deployment jobs
    get_deployment_jobs_url = "/v4/deployment_jobs?space_id={}".format(space_id)

    get_deploy_jobs_res = client.make_request('get', path=get_deployment_jobs_url)
    if not get_deploy_jobs_res.ok:
        raise Exception("Couldn't retrieve deployment jobs - reason: {}".format(get_deploy_jobs_res.text))

    resources = {}
    resources['deployment_jobs'] = []
    deployment_jobs = get_deploy_jobs_res.json()['resources']
    for deploy_job in deployment_jobs:
        resources['deployment_jobs'].append(
            dict(
                id=deploy_job['metadata']['id'],
                name=deploy_job['metadata'].get('name', '<no name provided>')
            ))

    print_utils.print_resource_lists(['deployment_jobs'], ["ID", "Name"], resources)
