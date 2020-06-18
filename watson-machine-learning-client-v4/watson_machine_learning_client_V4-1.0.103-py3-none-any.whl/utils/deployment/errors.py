from watson_machine_learning_client.utils import WMLClientError


__all__ = [
    "WrongDeploymnetType",
    "ModelTypeNotSupported",
    "NotAutoAIExperiment",
    "EnvironmentNotSupported"
]


class WrongDeploymnetType(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"This deployment is not of type: {value_name} ", reason)


class ModelTypeNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"This model type is not supported yet: {value_name} ", reason)


class NotAutoAIExperiment(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"This experiment_run_id is not from an AutoAI experiment: {value_name} ", reason)


class EnvironmentNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"This environment is not supported: {value_name}", reason)
