# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yapapi',
 'yapapi._cli',
 'yapapi.props',
 'yapapi.rest',
 'yapapi.runner',
 'yapapi.storage']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0',
 'async_exit_stack>=1.0.1,<2.0.0',
 'jsonrpc-base>=1.0.3,<2.0.0',
 'typing_extensions>=3.7.4,<4.0.0',
 'urllib3>=1.25.9,<2.0.0',
 'ya-client-activity>=0.1.0,<0.2.0',
 'ya-client-payment>=0.1.0,<0.2.0',
 'ya-market>=0.1.0,<0.2.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'cli': ['fire>=0.3.1,<0.4.0', 'rich>=2.2.5,<3.0.0']}

setup_kwargs = {
    'name': 'yapapi',
    'version': '0.1.1',
    'description': 'Hi-Level API for Golem The Next Milestone',
    'long_description': '# Golem Python API\n\n[![GitHub license](https://img.shields.io/github/license/prekucki/yapapi)](https://github.com/prekucki/yapapi/blob/master/LICENSE)\n[![PyPI version](https://badge.fury.io/py/yapapi.svg)](https://badge.fury.io/py/yapapi)\n[![GitHub issues](https://img.shields.io/github/issues/prekucki/yapapi)](https://github.com/prekucki/yapapi/issues)\n![Continuous integration](https://github.com/prekucki/yapapi/workflows/Continuous%20integration/badge.svg)\n\n## How to use\n\nRendering\n\n```python\nfrom yapapi.runner import Engine, Task, vm\nfrom datetime import timedelta\n\n\nasync def main():\n    package = await vm.repo(\n        image_hash="ef007138617985ebb871e4305bc86fc97073f1ea9ab0ade9ad492ea995c4bc8b",\n        min_mem_gib=0.5,\n        min_storage_gib=2.0,\n    )\n\n    async def worker(ctx, tasks):\n        ctx.send_file("./scene.blend", "/golem/resource/scene.blend")\n        async for task in tasks:\n            frame = task.data\n            ctx.begin()\n            crops = [\n                {\n                    "outfilebasename": "out",\n                    "borders_x": [0.0, 1.0],\n                    "borders_y": [0.0, 1.0],\n                }\n            ]\n            ctx.send_json(\n                "/golem/work/params.json",\n                {\n                    "scene_file": "/golem/resource/scene.blend",\n                    "resolution": (800, 600),\n                    "use_compositing": False,\n                    "crops": crops,\n                    "samples": 100,\n                    "frames": [frame],\n                    "output_format": "PNG",\n                    "RESOURCES_DIR": "/golem/resources",\n                    "WORK_DIR": "/golem/work",\n                    "OUTPUT_DIR": "/golem/output",\n                },\n            )\n            ctx.run("/golem/entrypoints/render_entrypoint.py")\n            ctx.download_file("/golem/output/out.png", f"output_{frame}.png")\n            yield ctx.commit()\n            # TODO: Check if job is valid\n            # and reject by: task.reject_task(msg = \'invalid file\')\n            task.accept_task()\n\n        ctx.log("no more frame to render")\n\n    async with Engine(\n        package=package, max_worker=10, budget=10.0, timeout=timedelta(minutes=5)\n    ) as engine:\n        async for progress in engine.map(\n            worker, [Task(data=frame) for frame in range(1, 101)]\n        ):\n            print("progress=", progress)\n```\n',
    'author': 'Przemysław K. Rekucki',
    'author_email': 'przemyslaw.rekucki@golem.network',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/prekucki/yapapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
