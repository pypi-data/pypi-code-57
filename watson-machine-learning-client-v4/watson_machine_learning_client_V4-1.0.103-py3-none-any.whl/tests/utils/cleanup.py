from watson_machine_learning_client.wml_client_error import WMLClientError


def delete_model_deployment(wml_client, deployment_name: 'str'):
    '''
    Delete deployment (and model) with name `deployment_name`

    '''
    deployments_details = wml_client.deployments.get_details()
    for deployment in deployments_details['resources']:
        if deployment['entity']['name'] == deployment_name:
            deployment_id = deployment['metadata']['id']
            print('Deleting deployment id', deployment_id)
            wml_client.deployments.delete(deployment_id)
            model_href_split = deployment['entity']['asset']['href'].split('/')
            model_id = model_href_split[model_href_split.index('models') + 1].split('?')[0]
            try:
                print('Deleting model id', model_id)
                wml_client.repository.delete(model_id)
            except WMLClientError as client_error:
                print("Could not delete model. Error message:")
                print(client_error)
        else:
            pass


def bucket_cleanup(cos_resource, prefix='bucket-tests'):
    import datetime
    """
    Delete all buckets started with `prefix`.
    """
    for bucket in cos_resource.buckets.all():
        if bucket.name.startswith(prefix):
            if bucket.creation_date < datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(weeks=1):
                print(f"Delete bucket older than a week: {bucket.name}")
                bucket.objects.delete()# Emptying bucket
                bucket.delete() # delete empty bucket
