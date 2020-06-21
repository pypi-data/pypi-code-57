from dagger.logger import logger
from dagger.Task import Task

class DaggerFunctionWrapper():
    def __init__(self, dagger_api, func, integration=None, **static_kwargs):
        self.dagger_api = dagger_api
        self.func = func
        self.integration = integration
        self.static_kwargs = static_kwargs

    def getStaticTask(self):
        if self.integration is not None:
            return self.integration.getStaticTask(**self.static_kwargs)

        return Task(
            **self.static_kwargs
        )

    def __call__(self, *args, **kwargs):
        task = self.getStaticTask()
        self.dagger_api.registerTask(task)

        try:
            logger.info('Called with %s %s', args, kwargs)

            task_input = dict(
                args=args,
                kwargs=kwargs
            )

            task.update(task_status='started', task_input=task_input)
        except Exception as e:
            logger.error('Failed to initialize dagger')
            logger.error(e)
            raise e

        try:
            task_output = self.func(*args, **kwargs)
            task.update(task_status='succeeded', task_output=task_output)
            return task_output
        except Exception as e:
            logger.debug('Task failed')
            logger.debug(e)
            if task is not None:
                task.update(task_status='failed', task_output=str(e))
            raise e
