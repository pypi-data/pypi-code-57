# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nomnomdata',
 'nomnomdata.tools.engine',
 'nomnomdata.tools.engine.template.engine.pkg',
 'nomnomdata.tools.engine.template.engine.pkg.tests',
 'nomnomdata.tools.engine.tests']

package_data = \
{'': ['*'], 'nomnomdata.tools.engine': ['template/engine/*']}

install_requires = \
['cerberus>=1.3.2,<2.0.0',
 'docker-compose>=1.25.5,<2.0.0',
 'docker[ssh]>=4.2.0,<5.0.0',
 'dunamai>=1.1.0,<2.0.0',
 'fsspec>=0.7.3,<0.8.0',
 'jinja2>=2.11.2,<3.0.0',
 'nomnomdata-auth>=2.2.0,<3.0.0',
 'nomnomdata-cli>=0.1.0,<0.2.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 's3fs>=0.4.2,<0.5.0']

entry_points = \
{'nomnomdata.cli_plugins': ['engine-tools = nomnomdata.tools.engine.cli:cli']}

setup_kwargs = {
    'name': 'nomnomdata-tools-engine',
    'version': '0.11.0.post10.dev0',
    'description': 'Package containing tooling for developing nominode engines',
    'long_description': '# Installation\n\n`pip install nomnomdata-engine-tools nomnomdata-engine`\n\n# Creating a new engine\n\nThis will walk through all the information required to create, build and deploy a new engine.\n\nDirectory Structure\n\nInitialize a new engine with\n\n`nnd engine-tools create-new <ENGINE_NAME>`\n\nThis will create a new directory with the layout\n\n``` directory\n.\n├── .dockerignore\n├── .gitignore\n├── .ex_pyproject.toml\n└── engine\n    ├── build.dockerfile\n    ├── model.yaml\n    ├── requirements.txt\n    └── pkg\n        ├── __init__.py\n        ├── executable.py\n        └── tests\n            ├── __init__.py\n            └── test_executable.py\n```\n\n## build.dockerfile\n\nEngines are deployed as docker images, so for every engine you must have a build.dockerfile located next to a model.yaml file. You will want to place your python files the \'pkg\' directory if you want nnd engine-tools build -rt to work properly.\n\nLook at the template build.dockerfile for an example and more information. You must include\n\n`CMD nnd engine run pkg/executable.py`\n\n Or your engine will not start correctly.\n\n## requirements.txt\n\nSimple pip requirements file. Requirements should be set to a specific version (ie requests==2.18.4) . Only requirements specific to your engine should be included in here. The template requirements.txt shows how to include the packages nomnomdata-cli & nomnomdata-engine which are the easiest way to run your executable.\n\n## executable.py\n\nThis is where the code that actually gets run lives.\n\n``` python\nfrom nomnomdata.engine.api import NominodeClient\nfrom nomnomdata.engine.core import Executable\n\nclass TemplateExecutable(Executable):\n    def __init__(self):\n        # Very important to call the inherited __init__ before anything else\n        super().__init__("nomigen.{{engine_name}}")\n\n    def do_thing(self):\n        self.logger.info("I did a thing!")\n        self.logger.info(f"My parameters are {self.params}")\n        self.nominode.update_progress(message="I did it!")\n\n```\n\n## test_executable.py\n\nTests! Our run tests command uses pytest to run these inside your docker image, so you can use anything pytest supports. The most important thing is to wrap your test code with a NominodeMock , this essentially sets up a \'fake\' nomnominode catching http requests to it.\n\n```python\nfrom nomnomdata.engine.test import NominodeMock\nfrom nomnomdata.engine.test_creds import credentials\nfrom ..executable import TemplateExecutable\n\nconfig = {\n\n    1: credentials["aws_connection"],\n\n}\n\nparams = {\n    "config": config,\n    \'action_name\': \'test\',\n    "aws_connection": {\n        "connection_uuid": \'2\'\n    },\n    \'other_param\': \'some variable\'\n\n}\n\n# the most basic test possible..\ndef test_init(self):\n    with NominodeMock(params):\n        t = TemplateExecutable()\n        t.do_thing()\n\n```\n\n## model.yaml\n\nThis is the description of your engine that will reside in the nomitall database, used by the nominode_ui to dynamically create configuration pages.\n\n```yaml\n# the unique identifier for this engine, must be unique across all engines\nuuid: NOMNOM_EXAMPLE_DOWNLOADER\nalias: "EXAMPLE: Downloader"\ndescription: An Example\n# repo information, most of the information is static apart from image\nlocation:\n  repo: 445607516549.dkr.ecr.us-east-1.amazonaws.com\n  # the :testing tag at the end indicates which ECS tag to use, for staging this should be testing, prod should use alpha\n  image: example/api/downloader:testing\n  region: us-east-1\n  repo_type: aws\n# categories this engine fits into, there are no fixed categories at this time\ncategories:\n\n  + name: example\n  + name: s3\n  + name: nomnomdata\n\n# this is a list of actions this engine can perform, these map directly to\n# functions of your Executable class in executable.py\nparameters:\n\n  + action_name: example_function\n\n    description: An example\n    display_name: Example Function\n    # this is where you can add what connections the engine requires\n    # also what adhoc parameters the engine uses.\n    # these will be presented to the user to fill in\n    parameters:\n    # this include parameter is a special directive that allows you include parameters from other files\n    # includes that are specific to the engine should be stored in your_engine/models\n\n    - include:\n      - \'common/meta_types/user_range.yaml\'\n    - connection_type_uuid: APP1E-T0NXM\n\n      parameter_name: app_annie_token\n      display_name: App Annie Token\n      description:  Credential token used to access the App Annie api.\n      required: true\n      type: connection\n\n    - parameter_name: s3_info\n\n      display_name: S3 Info\n      type: group\n\n    - connection_type_uuid: AWS5D-TO99M\n\n      description: AWS Credentials with access to the s3 bucket where the data table lives.\n      display_name: AWS Token Credentials\n      parameter_name: aws_connection\n      parameter_group: s3_info\n      required: false\n      type: connection\n\n    - connection_type_uuid: AWSS3-BUCKT\n\n      description: S3 Bucket where you want to unload the data to.\n      display_name: S3 Bucket\n      parameter_name: s3_bucket\n      parameter_group: s3_info\n      required: false\n      type: connection\n\n    - description: Path to a location where data files will be exported\n\n      display_name: S3 Path\n      parameter_name: s3_path\n      parameter_group: s3_info\n      required: True\n      type: string\n      max: 2048\n\n    - parameter_name: format_options\n\n      display_name: File/Formatting Options\n      type: group\n\n    - description: If specified will insert the date into the folder structure.  Example... y=1998/m=12/d=25/file_name.json.gz.\n\n      display_name: Date Folders\n      parameter_name: append_date\n      parameter_group: format_options\n      required: True\n      type: enum\n      default: True\n      choices:\n\n        - True\n        - False\n\n```\n\n## nomigen_test_credentials.json\n\nThis file exists outside the engine folders, and should be placed in your copy of the engines-config repo, you can find an example of it there. This is where you can store your credentials required by tests. If you set the environment variable NOMIGEN_TEST_CREDENTIALS to the location of your copy of engines-config, these creds will be made accessible via the nomnomdata.engine.test_credentials module at runtime.\n\n``` JSON\n{\n    "app_annie_token": {\n        "token": "your_app_annie_token"\n    },\n    "aws_connection": {\n        "aws_access_key_id": "your_aws_access_key",\n        "aws_secret_access_key": "your_aws_secret_access_key"\n    },\n    "s3_bucket": {\n        "bucket": "shughes-test-bucket"\n    }\n}\n```\n',
    'author': 'Nom Nom Data Inc',
    'author_email': 'info@nomnomdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nomnomdata/tools/nomnomdata-tools-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
