import os
import unittest

from kaistack.components.component_store import create_from_template

ARGO_SPEC_FILENAME = os.path.join(os.path.dirname(__file__), 'argo_component.yaml')


class ComponentStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["AUTH_DOMAIN"] = 'dev-kdiij5qn.auth0.com'
        os.environ["AUTH_CLIENT_SECRET"] = 'nx_qxMhX0N4fUs5cBvxCmFuKwU5t7Rop20dDONB_zMeFUs0Oke1u7_Ce-nNqicQK'
        os.environ["AUTH_CLIENT_ID"] = 'gwkHgc6x19rT2CcUzqac7z2NGcyWzxnD'

    def tearDown(self) -> None:
        pass

    def test_create_from_component(self):
        with open(ARGO_SPEC_FILENAME, 'r') as f:
            spec = f.read()
            component = create_from_template(spec)
            self.assertEqual("Git clone", component.name)
            self.assertEqual("Creates a shallow clone of the specified repo branch", component.description)
            self.assertEqual("alpine/git", component.image)
