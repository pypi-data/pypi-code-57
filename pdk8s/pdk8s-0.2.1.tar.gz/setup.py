# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdk8s',
 'pdk8s.cookiecutter.{{cookiecutter.slug}}',
 'pdk8s.gen',
 'pdk8s.gen.io',
 'pdk8s.gen.io.k8s',
 'pdk8s.gen.io.k8s.api',
 'pdk8s.gen.io.k8s.api.admissionregistration',
 'pdk8s.gen.io.k8s.api.apps',
 'pdk8s.gen.io.k8s.api.auditregistration',
 'pdk8s.gen.io.k8s.api.authentication',
 'pdk8s.gen.io.k8s.api.authorization',
 'pdk8s.gen.io.k8s.api.autoscaling',
 'pdk8s.gen.io.k8s.api.batch',
 'pdk8s.gen.io.k8s.api.certificates',
 'pdk8s.gen.io.k8s.api.coordination',
 'pdk8s.gen.io.k8s.api.core',
 'pdk8s.gen.io.k8s.api.discovery',
 'pdk8s.gen.io.k8s.api.events',
 'pdk8s.gen.io.k8s.api.extensions',
 'pdk8s.gen.io.k8s.api.networking',
 'pdk8s.gen.io.k8s.api.node',
 'pdk8s.gen.io.k8s.api.policy',
 'pdk8s.gen.io.k8s.api.rbac',
 'pdk8s.gen.io.k8s.api.scheduling',
 'pdk8s.gen.io.k8s.api.settings',
 'pdk8s.gen.io.k8s.api.storage',
 'pdk8s.gen.io.k8s.apiextensions_apiserver',
 'pdk8s.gen.io.k8s.apiextensions_apiserver.pkg',
 'pdk8s.gen.io.k8s.apiextensions_apiserver.pkg.apis',
 'pdk8s.gen.io.k8s.apiextensions_apiserver.pkg.apis.apiextensions',
 'pdk8s.gen.io.k8s.apimachinery',
 'pdk8s.gen.io.k8s.apimachinery.pkg',
 'pdk8s.gen.io.k8s.apimachinery.pkg.api',
 'pdk8s.gen.io.k8s.apimachinery.pkg.apis',
 'pdk8s.gen.io.k8s.apimachinery.pkg.apis.meta',
 'pdk8s.gen.io.k8s.apimachinery.pkg.util',
 'pdk8s.gen.io.k8s.kube_aggregator',
 'pdk8s.gen.io.k8s.kube_aggregator.pkg',
 'pdk8s.gen.io.k8s.kube_aggregator.pkg.apis',
 'pdk8s.gen.io.k8s.kube_aggregator.pkg.apis.apiregistration']

package_data = \
{'': ['*'], 'pdk8s': ['cookiecutter/*']}

install_requires = \
['click==7.1.2',
 'cookiecutter==1.7.2',
 'datamodel-code-generator>=0.5.9,<0.6.0',
 'pydantic==1.5.1',
 'pyyaml==5.3.1',
 'setuptools==47.1.1']

entry_points = \
{'console_scripts': ['pdk8s = pdk8s.cli:main']}

setup_kwargs = {
    'name': 'pdk8s',
    'version': '0.2.1',
    'description': '',
    'long_description': '![CI](https://github.com/FlorianLudwig/pdk8s/workflows/CI/badge.svg)\n![license](https://img.shields.io/github/license/FlorianLudwig/pdk8s.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# pdk8s\n\nGenerating Kubernetes definitions (yaml) with python, inspired by [cdk8s](https://github.com/awslabs/cdk8s).  The main use case is to use those definitions with helm.  This means cdk8s does replace all the templating that helm does - but helm still takes care of rolling out your changes to your cluster.\n\n\n# Getting started\n\n<!-- add nice video here -->\n\n## Installing pdk8s\n\n### Prerequisites\n\n* Python >= 3.7.\n* Python knowledge\n\n\n### Installation via PyPi\n\npdk8s is available on PyPi, you can install it with your preferred python package manage, `pip`, `pipenv`, etc:\n\n```\npip install pdk8s\n```\n\n## Intro\n\nThe format of `pdk8s` charts is similar to helm charts, just that they are python instead of yaml.  Your “python chart" must define the following variables:\n\n * `name`: Name of your chart\n * `chart_version`: This is the chart version. This version number should be incremented each time you make changes to the chart and its templates, including the app version. Versions are expected to follow [Semantic Versioning](https://semver.org/).\n * `app_version`: This is the version number of the application being deployed. This version number should be incremented each time you make changes to the application. Versions are not expected to follow Semantic Versioning. They should reflect the version the application is using.\n * `chart`: Your chart. A list or `pdk8s.k8s.Chart` (or actually any iterable python object) of k8s resources.\n\nIf you had a déjà vu while reading - that is because the description for `chart_version` and `app_version` are copied straight from Helm ;)\n\n## Getting started\n\n```bash\n$ pdk8s init\nchart_name [awesome chart]: Webserver Example\nslug [webserver_example]: \nchart_version [0.1.0]: \napp_version [0.1.0]: \n```\n\nYou will find a new folder and files named: `webserver_example/chart.py`.  Inside this file you will find a hello world example:\n\n```python\nchart = [\n    k8s.Deployment(name=\'deployment\',\n                    spec=k8s.DeploymentSpec(\n                        replicas=2,\n                        selector=k8s.LabelSelector(match_labels=label),\n                        template=k8s.PodTemplateSpec(\n                        metadata=k8s.ObjectMeta(labels=label),\n                        spec=k8s.PodSpec(containers=[\n                            k8s.Container(\n                            name=\'hello-kubernetes\',\n                            image=\'paulbouwer/hello-kubernetes:1.7\',\n                            ports=[k8s.ContainerPort(container_port=8080)])]))))\n]\n```\n\nWhich you can turn into a running helm chart with:\n\n```bash\n$ pdk8s synth\n```\n\nYou will find your generated chart under `dist`:\n\n<pre>\n├── chart.py\n└── <font color="#0087FF">dist</font>\n    ├── Chart.yaml\n    ├── <font color="#0087FF">templates</font>\n    │\xa0\xa0 └── generated.yaml\n    └── values.yaml\n</pre>\n\n## Creating Ressources\n\nCreating a service:\n\n```python\nfrom pdk8s import k8s\n\nservice = k8s.Service(name="service",\n            spec=k8s.ServiceSpec(\n                type="LoadBalancer",\n                ports=[k8s.ServicePort(port=80, target_port=8080)],\n                selector={"app": "hello-k8s"}))\n\nchart = [service]\n```\n\nAll `pdk8s` classes are [pydantic](https://pydantic-docs.helpmanual.io/) data classes.  Which provides - among other things - automatic conversion for parameters, so you can just as well write:\n\n```python\nfrom pdk8s import k8s\n\nk8s.Service(name="service",\n            spec={\n                "type": "LoadBalancer",\n                "ports": [{"port": 80, "target_port": 8080}],\n                "selector": {"app": "hello-k8s"}})\n```\n\n## Manipulating\n\nAll attributes can be manipulated after creation:\n\n```python\n\ndeployment = k8s.Deployment(name=\'deployment\',\n                    spec=k8s.DeploymentSpec(\n                        replicas=2))\n\ndeployment.spec.replicas = math.randint(0, 666)\n```\n\nNote 1: Automatic casting is only available on creation.  `deployment.spec = {"replicas": 2}` would not work.\n\nNote 2: Currently all required parameters must be provided at creation time.  You cannot create an empty `k8s.Deployment()`.  This might change.\n\n\n## CamelCase names\n\nThe Kubernetes APIs use camelCase for naming attributes, while python usually uses snake_case.  `pdk8s` also follows the snake_case convention, same as `cdk8s`.\n\n`pdk8s` provides aliases for all arguments:\n\n```python\nk8s.ServicePort(port=80, target_port=8080)\nk8s.ServicePort(port=80, targetPort=8080)\n```\n\nBoth work and result in the same result.  This is for compatibility when importing from other sources (and makes `pdk8s.k8s.parse` possible).\n\n## Importing existing charts\n\nYou might already have templates you want to build upon, you can easily import them using `pdk8s.k8s.parse`. Let\'s assume you have the following `chart.yaml`:\n\n```yaml\napiVersion: v1\nkind: Service\nmetadata:\n  name: service\nspec:\n  ports:\n  - port: 80\n    targetPort: 8080\n  selector:\n    app: hello-k8s\n  type: LoadBalancer\n```\n\nWith:\n\n```python\nimport pdk8s\nfrom pdk8s import k8s\n\nmy_chart = k8s.parse("example/chart.yaml")\nmy_chart[0].name = "service_new"\npdk8s.synth(my_chart)\n```\n\nYou get:\n\n```yaml\napiVersion: v1\nkind: Service\nmetadata:\n  name: service_new\nspec:\n  ports:\n  - port: 80\n    targetPort: 8080\n  selector:\n    app: hello-k8s\n  type: LoadBalancer\n```\n\n# Compatibility to cdk8s\n\nThere are a few differences that make code between the `cdk8s` and `pdk8s` incompatible.  A good overview can be archived by comparing the following to examples:\n\n * [cdk8s example](https://github.com/awslabs/cdk8s/blob/master/docs/getting-started/python.md#importing-constructs-for-the-kubernetes-api)\n * [pdk8s example](https://github.com/FlorianLudwig/pdk8s/blob/master/example/hello_world.py)\n\n### Pure python\n\n`cdk8s` is written in TypeScript and with the power of jsii usable from other languages, as python.  `pdk8s` is written in pure python with no bridge to other languages.  This means you are limited to python and cannot reuse charts written in other languages.  Therefore, a `pdk8s` is focused on providing an awesome experience writing charts in python: Readable tracebacks, happy IDE and linters, ... \n\n### Context / Constructs\n\nCurrently, there is no equivalent of "constructs" in `pdk8s`.  In `cdk8s` highlevel objects (e.g. `Service`) are special: They have an extra argument (the first one) which is the context in which they are defined, e.g. `k8s.Service(self, ...)` where `self` is the context.\n\nIn `pdk8s` there is no special treatment of these types.  There might be later on, but they would be added and not replaced.\n\nThis allows for more flexibility on how to construct your chart generator.\n\n\n### Names\n\nIn `cdk8s` names are automatically made unique by adding a hash to it.  `pdk8s` does not observe this behavior.  Also in `pdk8s` names must be provided as keyword argument.\n\n```python\n\n# cdk8s\nk8s.Service(Chart("hello"), "service")\n# kind: Service\n# apiVersion: v1\n# metadata:\n#   name: hello-service-9878228b\n\n\n# pdk8s\nk8s.Service(name=\'service\')\n# kind: Service\n# apiVersion: v1\n# metadata:\n#   name: service\n\n\n```\n<!-- TODO add reasoning -->\n\n### IntOrString\n\n```python\n# cdk8s\nk8s.ServicePort(port=80, target_port=k8s.IntOrString.from_number(8080))\n\n# pdk8s\nk8s.ServicePort(port=80, target_port=8080)\n# k8s.IntOrString might be added for compatibility later on\n```\n\n\n# Why\n\nTODO explain why this exists (NIH syndrom)\n## Design Decisions\n\n### Generate at build time\n\nGenerate everything at build time and not runtime as it makes it easier for linters and other dev tools, like IDEs.\n\n### Attribute case\n\nCamelCase?\n\n### Naming\n\n\n### Versioning\n\n# Development and building\n\nCurrently, generating the code of `pdk8s` depends on a patched version of `datamodel-code-generator`.  I am working on upstreaming changes to not depend on local patches anymore.\n\n## Sources\n\n * https://github.com/kubernetes/kubernetes/tree/master/api/openapi-spec - openapi definition.\n * https://github.com/instrumenta/kubernetes-json-schema - JSON Schema of Kubernetes API, generated from official openapi definitions.  Used by cdk8s.\n',
    'author': 'Florian Ludwig',
    'author_email': 'f.ludwig@greyrook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
