#  © Copyright IBM Corporation 2020.

from ai_lifecycle_cli.lib.clients.rest_client import RESTClient
from ai_lifecycle_cli.lib.actions import manage_wml_deployment_jobs


def do_deployment_job(args):

    client = RESTClient(args.cpd_url, (args.cpd_user, args.cpd_pass))

    # 'deployment-job create' command
    if args.deployment_job == "create":

        space_id = args.space_id
        job_spec_json = args.job_spec_json

        manage_wml_deployment_jobs.create_deployment_job(
            client=client,
            space_id=space_id,
            deployment_job_spec=job_spec_json
        )

    # 'deployment-job cancel' command
    if args.deployment_job == "cancel":

        space_id = args.space_id
        job_id = args.job_id

        manage_wml_deployment_jobs.delete_deployment_job(
            client=client,
            space_id=space_id,
            job_id=job_id
        )

    # 'deployment-job list' command
    if args.deployment_job == "list":

        space_id = args.space_id

        manage_wml_deployment_jobs.list_deployment_jobs(
            client=client,
            space_id=space_id,
        )
