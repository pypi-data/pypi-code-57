import jsonref
from jsonschema import validate
from os import path
from os import name as os_name


class Validator:
    def __init__(self):
        self.schema_path = path.join(path.dirname(__file__), f'static/schemas/{self.schema_name}')

        base_path = path.dirname(self.schema_path)
        base_uri = f'file://{base_path}/'

        if os_name == 'nt':
            base_uri = 'file:///{}/'.format(base_path)

        with open(self.schema_path) as schema:
            self.schema = jsonref.loads(schema.read(), base_uri=base_uri, jsonschema=True)

    def validate(self, instance):
        validate(instance=instance, schema=self.schema)
        return True


class ExecutionCompletionValidator(Validator):
    def __init__(self):
        self.schema_name = 'execution_completion.json'
        super().__init__()


class ExecutionFailureValidator(Validator):
    def __init__(self):
        self.schema_name = 'execution_failure.json'
        super().__init__()


class ExecutionRequestValidator(Validator):
    def __init__(self):
        self.schema_name = 'execution_request.json'
        super().__init__()


class OfferExecutionRequestValidator(Validator):
    def __init__(self):
        self.schema_name = 'offer_execution_request.json'
        super().__init__()


class ExecutionRequestAcceptValidator(Validator):
    def __init__(self):
        self.schema_name = 'execution_request_accept.json'
        super().__init__()


class ExecutionRequestCancelValidator(Validator):
    def __init__(self):
        self.schema_name = 'execution_request_cancel.json'
        super().__init__()


class ExecutionRequestDeclineValidator(Validator):
    def __init__(self):
        self.schema_name = 'execution_request_decline.json'
        super().__init__()


class ExecutionStatusUpdateValidator(Validator):
    def __init__(self):
        self.schema_name = 'execution_status_update.json'
        super().__init__()


class ServiceDiscoveryValidator(Validator):
    def __init__(self):
        self.schema_name = 'service_discovery.json'
        super().__init__()


class ServiceDiscoveryResponseValidator(Validator):
    def __init__(self):
        self.schema_name = 'service_discovery_response.json'
        super().__init__()


class ServiceOfferingValidator(Validator):
    def __init__(self):
        self.schema_name = 'service_offering.json'
        super().__init__()


class ServiceRequestValidator(Validator):
    def __init__(self):
        self.schema_name = 'service_request.json'
        super().__init__()
