

class BatchPrediction():
    '''

    '''

    def __init__(self, client, batchPredictionId=None, name=None, status=None, deploymentId=None, inputLocation=None, outputLocation=None, predictionsStartedAt=None, predictionsCompletedAt=None):
        self.client = client
        self.id = batchPredictionId
        self.batch_prediction_id = batchPredictionId
        self.name = name
        self.status = status
        self.deployment_id = deploymentId
        self.input_location = inputLocation
        self.output_location = outputLocation
        self.predictions_started_at = predictionsStartedAt
        self.predictions_completed_at = predictionsCompletedAt

    def __repr__(self):
        return f"BatchPrediction(batch_prediction_id={repr(self.batch_prediction_id)}, name={repr(self.name)}, status={repr(self.status)}, deployment_id={repr(self.deployment_id)}, input_location={repr(self.input_location)}, output_location={repr(self.output_location)}, predictions_started_at={repr(self.predictions_started_at)}, predictions_completed_at={repr(self.predictions_completed_at)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'batch_prediction_id': self.batch_prediction_id, 'name': self.name, 'status': self.status, 'deployment_id': self.deployment_id, 'input_location': self.input_location, 'output_location': self.output_location, 'predictions_started_at': self.predictions_started_at, 'predictions_completed_at': self.predictions_completed_at}

    def refresh(self):
        self = self.describe()
        return self

    def describe(self):
        return self.client.describe_batch_prediction(self.batch_prediction_id)

    def wait_for_predictions(self, timeout=1200):
        return self.client._poll(self, {'PENDING', 'PREDICTING'}, timeout=timeout)

    def get_status(self):
        return self.describe().status
