import pathlib

from dask_kubernetes import KubeCluster
from distributed import Client
from moksh_orchestrator.framework.apis.execution_context import ExecutionContext
from moksh_orchestrator.framework.apis.step import Step
from moksh_orchestrator.framework.apis.dataset import Dataset
from moksh_orchestrator.framework.utils.file_utils import find_file
from moksh_orchestrator.logging.moksh_logger import MokshLogger


class ParallelExecutor:

    def __init__(self, step, execution_context, unit_of_work):
        self.step: Step = step
        self.execution_context: ExecutionContext = execution_context
        self.unit_of_work: Dataset = unit_of_work

    def submit(self):
        path_to_k8s_config = find_file('dask-workers.yaml', pathlib.Path(__file__).parent.absolute())

        cluster = KubeCluster.from_yaml(path_to_k8s_config)
        cluster.scale(10)  # specify number of workers explicitly

        cluster.adapt(minimum=1, maximum=100)  # or dynamically scale based on current workload

        # client = Client(processes=False)
        client = Client(cluster)
        client.get_versions(check=True)
        futures = []
        for i in range(0, self.step.get_threads(), 1):
            MokshLogger.moksh_log_debug('Launching thread {}'.format(str(i)))
            self.execution_context.addParam('parallel_exec_cnt', str(i))
            futures.append(client.submit(self.do_submit))

        print('Future results size {}'.format(len(futures)))
        tuples = client.gather(futures)
        # merge the contexts
        for _ in tuples:
            print(_[0].getAllParam())
            self.execution_context.merge(_[0])

        cluster.close()

    def do_submit(self) -> (ExecutionContext, Dataset):
        self.unit_of_work.execute(self.execution_context)
        return self.step.execute(self.execution_context, self.unit_of_work)
