# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotcp']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'numpy>=1.18.4,<2.0.0']

setup_kwargs = {
    'name': 'plotcp',
    'version': '0.3.1',
    'description': 'Python package for drawing transformations of functions of a complex variable of the whole grid or a given area',
    'long_description': '# PlotComplexPlane\n\nPython library for plotting complex functions transformations\n\n## It can...\n\n- *plot complex planes (both transformed and original)*\n- *plot transformations of specific areas (both transformed and original)*\n- *plot lines parallel to real or imaginary axis (both transformed and original)*\n\n## Usage\n### plotcp\nTo plot f(z) = (z+1)/z with x bound from -4 to 4 and y bound from -4 to 4\n\n```python3\nfrom plotcp import plotcp\n\n\ndef f(z: complex) -> complex: # Define function to plot\n    return (z+1)/z\n\n\n# Call plotcp\n# Second and third arguments define limits of a plot\nax = plotcp(f, (-4, 4), (-4, 4))\n```\nFor full parameters list check ```help(plotcp.plotcp)```\n### plot_complex_points\n```python3\nfrom cmath import sin\n\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom plotcp import plot_complex_points\n\ndef f(z: compex) -> complex: # Define function to plot\n    return sin(z)\n\n\n# Define area to be plotted\ntop = [x + 2 * 1j for x in np.linspace(1, 2, 5)]\nbottom = [x + 1 * 1j for x in np.linspace(1, 2, 5)]\nleft = [1 + y * 1j for y in np.linspace(1, 2, 5)]\nright = [2 + y * 1j for y in np.linspace(1, 2, 5)]\n\n# Plot original area\nax = plot_complex_points(top)\nax = plot_complex_points(bottom, ax=ax)\nax = plot_complex_points(left, ax=ax)\nax = plot_complex_points(right, ax=ax)\n\n\n# Apply function to area and plot it on a new plot\nax2 = plot_complex_points([f(z) for z in top])\nax2 = plot_complex_points([f(z) for z in bottom], ax=ax2)\nax2 = plot_complex_points([f(z) for z in left], ax=ax2)\nax2 = plot_complex_points([f(z) for z in right], ax=ax2)\n\nplt.show()\n```\nFor full parameters list check ```help(plotcp.plot_complex_points)```',
    'author': 'ZetZet',
    'author_email': 'dmesser@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZettZet/plotcp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
