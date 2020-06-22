# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aksdp',
 'aksdp.data',
 'aksdp.dataset',
 'aksdp.graph',
 'aksdp.repository',
 'aksdp.task',
 'aksdp.util']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aksdp',
    'version': '0.0.1.post4',
    'description': 'Simple DataPipeline Library',
    'long_description': '# aksdp\n\n## Overview\n\nA simple framework for writing data pipelines in Python\n\n## INSTALL\n\n```bash\n$ pip install aksdp\n```\n\n## QuickStart\n\n```python\n\nclass TaskA(Task):\n   def main(self, ds):\n      return ds\n\nclass TaskB(Task):\n   ...\n\nclass TaskC(Task):\n   ...\n\nclass TaskD(Task):\n   ...\n\ngraph = Graph()\ntask_a = graph.append(TaskA())\ntask_b = graph.append(TaskB(), [task_a])\ntask_c = graph.append(TaskC(), [task_b])\ntask_d = graph.append(TaskD(), [task_b, task_c])\ngraph.run()\n\n```\n\nEach task runs after each dependent task completes.  \nAlso, the data output upstream can be received as input data and processed.',
    'author': 'Y.Arimitsu',
    'author_email': 'yoshikazu_arimitsu@albert2005.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/YoshikazuArimitsu/aksdp',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
