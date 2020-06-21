import os

from dagger.logger import logger
from dagger.DaggerAPI import DaggerAPI
from dagger.DaggerFunctionWrapper import DaggerFunctionWrapper

from dagger.integrations.aws_ecs import AWSECSIntegration
from dagger.integrations.aws_lambda import AWSLambdaIntegration

AUTO_INTEGRATION = 'auto'
INTEGRATIONS = {
    'aws_ecs': AWSECSIntegration(),
    'aws_lambda': AWSLambdaIntegration()
}

def _getAutoIntegration():
    for inteagration_name, integration in INTEGRATIONS.items():
        if integration.isInIntegration():
            logger.info('Loaded integration: %s', inteagration_name)
            return integration

def wrap(dagger_api, func, integration=AUTO_INTEGRATION, **kwargs):
    if dagger_api is None:
        logger.info('wrap called with dagger_api=None, not doing anything')
        return func

    try:
        if integration == AUTO_INTEGRATION:
            integration = _getAutoIntegration()

        if isinstance(integration, str):
            if integration not in INTEGRATIONS:
                raise RuntimeError('Integration not found in INTEGRATIONS. "%s" not in (%s)' % (integration, ', '.join(INTEGRATIONS.keys())))
            integration = INTEGRATIONS[integration]

        return DaggerFunctionWrapper(
            dagger_api,
            func,
            integration=integration,
            **kwargs
        )
    except Exception as e:
        logger.critical('Dagger failed to initialize with exception:')
        logger.critical(e)
        return func

def initDagger(api_key, autoload_integration=True):
    logger.info('Initializing Dagger')

    api = DaggerAPI(api_key)

    if autoload_integration:
        integration = _getAutoIntegration()
        if integration is not None:
            try:
                integration.autoloadIntegration(api, wrap)
            except NotImplementedError:
                logger.debug('Integration did not have autoload function implemented')
                pass # Not all integrations can be autoloaded

    return api
