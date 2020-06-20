import plynx.db.node
import plynx.plugins.executors.local as local
import plynx.plugins.executors.dag as dag
import plynx.plugins.resources.common as common


SEQ_OUTPUT = 'seq_o'


def create_seq_operation(num):
    node = local.BashJinja2.get_default_node(is_workflow=False)

    node.outputs.append(
        plynx.db.node.Output.from_dict({
            'name': SEQ_OUTPUT,
            'file_type': common.FILE_KIND,
        })
    )

    cmd_param = node.get_parameter_by_name('_cmd', throw=True)
    cmd_param.value = 'seq {0} > {{{{ output.{1} }}}}\n'.format(num, SEQ_OUTPUT)

    return node

def create_dag_executor(N):
    """
    Create a Dag with the following layout:

                +-- (grep ^0) --+
    (seq 100) --+   ...         +-- (sum)
                +-- (grep ^9) --+

    Args:
        N: int, sequence
    """

    dag_node = dag.DAG.get_default_node(is_workflow=True)
    nodes = dag_node.get_parameter_by_name('_nodes', throw=True).value.value

    seq_operation = create_seq_operation(1)
    nodes.append(seq_operation)

    return dag.DAG(dag_node)


def test_dag():
    N = 1
    executor = create_dag_executor(N)
    executor.run()

    assert False, executor.node.get_parameter_by_name('_nodes').value.value[0].get_output_by_name().value
