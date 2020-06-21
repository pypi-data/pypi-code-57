import os

from dagger.logger import logger
from dagger.integrations.base import Integration
from dagger.Task import Task

class AWSLambdaIntegration(Integration):
    def isInIntegration(self):
        return os.getenv('_HANDLER', None) is not None

    def getStaticTask(self, lambda_context=None, task_name=None, task_run_id=None, **kwargs):
        if lambda_context is None:
            logger.error('Lambda getStaticTask called without lambda_context')
            return Task(
                task_name,
                task_run_id,
                **kwargs
            )

        if task_name is None:
            task_name = lambda_context.function_name
        if task_run_id is None:
            task_run_id = lambda_context.aws_request_id

        return Task(
            task_name,
            task_run_id
        ).update(
            task_metadata=dict(
                region=os.getenv('AWS_REGION', None)
            ),
            task_logs=dict(
                type='aws_cloudwatch',
                data=dict(
                    log_group_name=lambda_context.log_group_name,
                    log_stream_name=lambda_context.log_stream_name,
                    time_filter=True
                )
            ),
            task_system='aws_lambda'
        )

    def autoloadIntegration(self, dagger_api, wrap):
        try:
            import bootstrap # pylint: disable=import-error
        except ImportError:
            logger.critical('Attempted to autoload lambda integration, but bootstrap script failed to import. This is likely because we are being called outside of a lambda environment')
            return

        old_handle_request = bootstrap.handle_event_request
        def _newHandleRequest(lambda_runtime_client, request_handler, *args):
            def _newRequestHandler(event, context):
                wrap(
                    dagger_api,
                    request_handler,
                    integration=self,
                    lambda_context=context
                )(event, context)
            old_handle_request(lambda_runtime_client, _newRequestHandler, *args)
        bootstrap.handle_event_request = _newHandleRequest
