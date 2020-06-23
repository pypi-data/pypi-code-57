import os
import unittest

from kfp import dsl

from kaistack.components.kubeflow_converter import component_to_template, containerOp_to_template
from kfp.dsl._pipeline_param import PipelineParam
COMPONENT_SPEC_FILENAME = os.path.join(os.path.dirname(__file__), 'kfp_component.yaml')


class KubeflowConverterTest(unittest.TestCase):
    def test_component_to_workflow_template(self):
        template = component_to_template(COMPONENT_SPEC_FILENAME)
        self.assertEqual('irxxo3tmn5qwiidgojxw2ichinjq', template['name'])  # Name has a space. It is encoded
        self.assertEqual(1, len(template['inputs']['parameters']))
        self.assertEqual('GCS-path', template['inputs']['parameters'][0]['name'])
        self.assertEqual(1, len(template['outputs']['artifacts']))
        self.assertFalse('parameters' in template['outputs'])

    def test_container_op_to_workflow_template(self):
        echo_task = dsl.ContainerOp(
            name='echo',
            image='library/bash:4.4.23',
            command=['sh', '-c'],
            arguments=['echo "hello world"', '%s' % PipelineParam(name="arg1")],
        )

        template = containerOp_to_template(echo_task)
        self.assertEqual('echo', template['name'])
        self.assertEqual('library/bash:4.4.23', template['container']['image'])
        self.assertEqual(['sh', '-c'], template['container']['command'])
        self.assertEqual(['echo "hello world"','{{inputs.parameters.arg1}}'], template['container']['args'])
