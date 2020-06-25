# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ps2_analysis',
 'ps2_analysis.fire_groups',
 'ps2_analysis.visualizations',
 'ps2_analysis.weapons',
 'ps2_analysis.weapons.infantry',
 'ps2_analysis.weapons.vehicle']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.1,<5.0',
 'ndjson>=0.3,<0.4',
 'ps2-census>=0.12,<0.13',
 'python-slugify>=4.0,<5.0',
 'toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'ps2-analysis',
    'version': '0.12.0',
    'description': "Daybreak Game's Planetside 2 data analysis (UNOFFICIAL)",
    'long_description': '# ps2-analysis [WORK IN PROGRESS]\n\n*ps2-analysis* is a library written in Python >= 3.8 that fetches data from the\nDaybreak Planetside 2 Census API and eases advanced analysis.\n\nIt uses its sister project, the [ps2-census](https://github.com/spascou/ps2-census) client\nwhose objective is simply to handle data retrieval from the Census API. Further parsing\nand exploitation is performed here in *ps2-analysis*.\n\n   * [ps2-analysis](#ps2-analysis)\n      * [Examples](#examples)\n      * [Development](#development)\n        * [Environment](#environment)\n\n*Features*:\n- Currently supports infantry and vehicle weapons data\n- Downloads datasets from the API and stores them locally as *ndjson* files\n- Parses data and generates class objects suitable for further processing\n- Generates *vega-lite* charts using [Altair](https://altair-viz.github.io/)\n\n## Installation\n```sh\npip install ps2-analysis\n```\n\n## Examples\n\nExamples are available in the `examples` folder:\n- `discover_infantry_weapons.py`: updates the infantry weapons datafile and outputs all different (nested) key paths as well as associated set of values encountered within the whole dataset; example output in `discover_infantry_weapons.json`\n- `discover_vehicle_weapons.py`: updates the vehicle weapons datafile and outputs all different (nested) key paths as well as associated set of values encountered within the whole dataset; example output in `discover_vehicle_weapons.json`\n- `generate_infantry_weapons.py`: no output; simply an example of `InfantryWeapon` objects generation\n- `generate_vehicle_weapons.py`: no output; simply an example of `VehicleWeapon` objects generation\n- `fire_simulation_plot.py`: generates a fire simulation plot for the TRAC-5 TR carbine, 100 runs of 10 shots\n- `ttk_to_mhd_plot.py`: generates a plot of time to kill at 15meters to mean horizontal deviation for all SMGs\n\n## Development\n\n### Environment\n\nIn order to develop *ps2-analysis*:\n- Setup a virtual environment with python 3.8\n- Install [poetry](https://github.com/python-poetry/poetry)\n- Install dependencies with `poetry install`\n- Run tests with `pytest`\n- Update dependencies with `poetry update`\n\nTo run the examples in the `examples` folder:\n- Add your Census API service ID to the `CENSUS_SERVICE_ID` environment variable\n- Create two folders inside the `examples` folder of the cloned repository: `datafiles` and `plots`\n- Run the scripts and check the outputs\n',
    'author': 'Sylvain Pascou',
    'author_email': 'sylvain@pascou.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spascou/ps2-analysis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
