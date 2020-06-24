from spell.api import base_client
from spell.api.models import ModelFileSpec
from spell.api.utils import url_path_join

MODEL_URL = "model"


class ModelClient(base_client.BaseClient):
    def new_model(self, owner, name, resource, version, files):
        payload = {
            "name": name,
            "version": version,
            "resource": resource,
            "files": [ModelFileSpec.from_string(f).to_payload() for f in files],
        }
        r = self.request("post", url_path_join(MODEL_URL, owner), payload=payload)
        self.check_and_raise(r)
        return self.get_json(r)["model_version"]

    def list_models(self, owner):
        r = self.request("get", url_path_join(MODEL_URL, owner))
        self.check_and_raise(r)
        return self.get_json(r)["models"]

    def rm_model(self, owner, name):
        r = self.request("delete", url_path_join(MODEL_URL, owner, name))
        self.check_and_raise(r)

    def rm_model_version(self, owner, name, version):
        r = self.request("delete", url_path_join(MODEL_URL, owner, name, "version", version))
        self.check_and_raise(r)
