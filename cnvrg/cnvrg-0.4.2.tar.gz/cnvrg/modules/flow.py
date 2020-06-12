import json
import yaml

from cnvrg.modules.project import Project
from cnvrg.modules.flow_version import FlowVersion
from cnvrg.helpers.url_builder_helper import url_join
from cnvrg.modules.errors import CnvrgError

import cnvrg.helpers.param_build_helper as param_build_helper
import cnvrg.helpers.apis_helper as apis_helper
import cnvrg.modules.errors as errors


class Flow():
    def __init__(self, slug, project=None, version=None):
        owner, project_slug, slug = param_build_helper.parse_params(slug, param_build_helper.FLOW)

        p = Project.factory(owner, project)

        if p is None:
            p = Project(url_join(owner, project_slug))

        self.slug = slug
        self.version = version or "latest"
        self.owner = owner
        self.project = p

    def run(self):
        project = self.project
        resp = apis_helper.post(url_join(project.get_base_url(), 'flows', 'run_flow'), data={"flow_slug": self.slug})
        status = resp["status"]
        if status == 200:
            fv_title = resp["flow_version"]["title"]
            return FlowVersion(self, fv_title, project)
        else:
            raise CnvrgError("Could not create flow")

    @staticmethod
    def create(file=None, yaml_content=None, project=None):
        if not file and not yaml_content:
            raise errors.CnvrgError("File or yaml is missing")

        project = project or Project()

        if yaml_content:
            try:
                data = yaml.safe_load(yaml_content)
            except Exception:
                raise errors.CnvrgError("Please check that your yaml valid")
        else:
            try:
                with open(file, 'r') as f:
                    data = yaml.safe_load(f)
            except Exception:
                raise errors.CnvrgError("Please check that your yaml exists")

        if not data:
            raise errors.CnvrgError("Yaml can't be empty")

        resp = apis_helper.post(url_join(project.get_base_url(), 'flows'), data={"flow_version": json.dumps(data)})

        status = resp["status"]
        if status == 200:
            flow_title = resp["flow"]["title"]
            print("Flow {} created successfully".format(flow_title))
            flow_slug = resp["flow"]["slug"]
            return Flow(flow_slug, project)
        else:
            raise CnvrgError("Could not create flow")
