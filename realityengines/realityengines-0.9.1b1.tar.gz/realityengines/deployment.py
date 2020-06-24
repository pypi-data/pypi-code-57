

class Deployment():
    '''

    '''

    def __init__(self, client, deploymentId=None, name=None, status=None, description=None, deploymentConfig=None, deployedAt=None, createdAt=None, projectId=None, modelId=None, modelVersion=None):
        self.client = client
        self.id = deploymentId
        self.deployment_id = deploymentId
        self.name = name
        self.status = status
        self.description = description
        self.deployment_config = deploymentConfig
        self.deployed_at = deployedAt
        self.created_at = createdAt
        self.project_id = projectId
        self.model_id = modelId
        self.model_version = modelVersion

    def __repr__(self):
        return f"Deployment(deployment_id={repr(self.deployment_id)}, name={repr(self.name)}, status={repr(self.status)}, description={repr(self.description)}, deployment_config={repr(self.deployment_config)}, deployed_at={repr(self.deployed_at)}, created_at={repr(self.created_at)}, project_id={repr(self.project_id)}, model_id={repr(self.model_id)}, model_version={repr(self.model_version)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'deployment_id': self.deployment_id, 'name': self.name, 'status': self.status, 'description': self.description, 'deployment_config': self.deployment_config, 'deployed_at': self.deployed_at, 'created_at': self.created_at, 'project_id': self.project_id, 'model_id': self.model_id, 'model_version': self.model_version}

    def refresh(self):
        self = self.describe()
        return self

    def describe(self):
        return self.client.describe_deployment(self.deployment_id)

    def update(self, name=None, description=None):
        return self.client.update_deployment(self.deployment_id, name, description)

    def start(self):
        return self.client.start_deployment(self.deployment_id)

    def stop(self):
        return self.client.stop_deployment(self.deployment_id)

    def delete(self):
        return self.client.delete_deployment(self.deployment_id)

    def batch_predict(self, input_location=None, output_location=None, name=None):
        return self.client.batch_predict(self.deployment_id, input_location, output_location, name)

    def list_batch_predictions(self):
        return self.client.list_batch_predictions(self.deployment_id)

    def wait_for_deployment(self, timeout=480):
        return self.client._poll(self, {'PENDING', 'DEPLOYING'}, timeout=timeout)

    def get_status(self):
        return self.describe().status
