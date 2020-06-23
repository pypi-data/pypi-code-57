import os
import unittest

from kaistack.components.component_store import create_from_template

ARGO_SPEC_FILENAME = os.path.join(os.path.dirname(__file__), 'argo_component.yaml')
ARGO_SPEC_FILENAME_2 = os.path.join(os.path.dirname(__file__), 'argo_component_2.yaml')


class ComponentStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create_from_component(self):
        with open(ARGO_SPEC_FILENAME, 'r') as f:
            spec = f.read()
            component = create_from_template(spec)
            self.assertEqual("Git clone", component.name)
            self.assertEqual("Creates a shallow clone of the specified repo branch", component.description)
            self.assertEqual("alpine/git", component.image)

    def test_create_from_component_2(self):
        with open(ARGO_SPEC_FILENAME_2, 'r') as f:
            spec = f.read()
            component = create_from_template(spec)
            self.assertEqual("preprocess", component.name)
