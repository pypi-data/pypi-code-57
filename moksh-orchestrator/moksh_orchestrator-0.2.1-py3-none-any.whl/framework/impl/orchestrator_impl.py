import yaml
from zope.interface import implementer

from moksh_orchestrator.framework.apis.execution_context import ExecutionContext
from moksh_orchestrator.framework.apis.orchestrator import Orchestrator

from moksh_orchestrator.framework.apis.step import Step
from moksh_orchestrator.framework.impl.steps import Steps
from moksh_orchestrator.framework.impl.dataset_impl import DatasetImpl

from moksh_orchestrator.framework.parallel.parallel_executor import ParallelExecutor
from moksh_orchestrator.framework.utils.interface_utils import verify_object_graph
from moksh_orchestrator.logging.moksh_logger import MokshLogger


@implementer(Orchestrator)
class OrchestratorImpl(yaml.YAMLObject):
    yaml_tag = '!task'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # def __repr__(self):
    #     return "%s(name=%r, steps=%r)" % (self.name, self.steps,)
    #
    # def __str__(self):
    #     return 'name: {} steps: {}'.format(self.name, self.steps)

    def execute(self, execution_context: ExecutionContext) -> ExecutionContext:
        try:
            dataset = DatasetImpl()
            for step in self.steps:
                verify_object_graph(Step, step)
                if step.is_parallel():
                    MokshLogger.moksh_log_debug('parallel execution using DASK')

                    ParallelExecutor(step, execution_context, dataset).submit()

                step.execute(execution_context, dataset)
        except Exception as e:
            MokshLogger.moksh_log_debug(e)
            raise e

    def get_steps(self) -> Steps:
        return self.steps
