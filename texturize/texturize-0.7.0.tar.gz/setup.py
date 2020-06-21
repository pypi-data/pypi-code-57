# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['texturize']

package_data = \
{'': ['*']}

install_requires = \
['creativeai>=0.1.1,<0.2.0',
 'docopt>=0.6.2,<0.7.0',
 'progressbar2>=3.51.3,<4.0.0',
 'schema>=0.7.2,<0.8.0']

entry_points = \
{'console_scripts': ['texturize = texturize.__main__:main']}

setup_kwargs = {
    'name': 'texturize',
    'version': '0.7.0',
    'description': '🤖🖌️ Automatically generate new textures similar to a source photograph.',
    'long_description': 'neural-texturize\n================\n\n.. image:: docs/dirt-x4.webp\n\nAutomatically generate new textures similar to your source image.  Useful if you\nwant to make variations on a theme or expand the size of an existing texture.\n\n1. Examples & Usage\n===================\n\nThe main script takes a source image as a texture, and generates a new output that\ncaptures the style of the original.  Here are some examples:\n\n.. code-block:: bash\n\n    texturize samples/grass.webp --size=1440x960 --output=result.png\n    texturize samples/gravel.png --iterations=200 --precision=1e-5\n    texturize samples/sand.tiff  --output=tmp/{source}-{octave}.webp\n    texturize samples/brick.jpg  --device=cpu\n\n\nFor details about the command-line options, see the tool itself:\n\n.. code-block:: bash\n\n    texturize --help\n\nHere are the command-line options currently available::\n\n    Usage:\n        texturize SOURCE... [--size=WxH] [--output=FILE] [--variations=V] [--seed=SEED]\n                            [--mode=MODE] [--octaves=O] [--threshold=H] [--iterations=I]\n                            [--device=DEVICE] [--precision=PRECISION] [--quiet] [--verbose]\n\n    Options:\n        SOURCE                  Path to source image to use as texture.\n        -s WxH, --size=WxH      Output resolution as WIDTHxHEIGHT. [default: 640x480]\n        -o FILE, --output=FILE  Filename for saving the result, includes format variables.\n                                [default: {source}_gen{variation}.png]\n        --variations=V          Number of images to generate at same time. [default: 1]\n        --seed=SEED             Configure the random number generation.\n        --mode=MODE             Either "patch" or "gram" to specify critics. [default: gram]\n        --octaves=O             Number of octaves to process. [default: 5]\n        --threshold=T           Quality for optimization, lower is better. [default: 1e-4]\n        --iterations=I          Maximum number of iterations each octave. [default: 99]\n        --device=DEVICE         Hardware to use, either "cpu" or "cuda".\n        --precision=PRECISION   Floating-point format to use, "float16" or "float32".\n        --quiet                 Suppress any messages going to stdout.\n        --verbose               Display more information on stdout.\n        -h, --help              Show this message.\n\n2. Installation\n===============\n\nThis repository uses submodules, so you\'ll need to clone it recursively to ensure\ndependencies are available:\n\n.. code-block:: bash\n\n    git clone --recursive https://github.com/photogeniq/neural-texturize.git\n\nThen, you can create a new virtual environment called ``myenv`` by installing\n`Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ and calling the following\ncommands, depending whether you want to run on CPU or GPU (via CUDA):\n\n.. code-block:: bash\n\n    cd neural-texturize\n\n    # a) Use this if you have an *Nvidia GPU only*.\n    conda env create -n myenv -f tasks/setup-cuda.yml\n\n    # b) Fallback if you just want to run on CPU.\n    conda env create -n myenv -f tasks/setup-cpu.yml\n\nOnce the virtual environment is created, you can activate it and finish the setup of\n``neural-texturize`` with these commands:\n\n.. code-block:: bash\n\n    conda activate myenv\n    poetry install\n\nFinally, you can check if everything worked by calling the script:\n\n.. code-block:: bash\n\n    texturize\n\nYou can use ``conda env remove -n myenv`` to delete the virtual environment once you\nare done.\n',
    'author': 'Alex J. Champandard',
    'author_email': '445208+alexjc@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/photogeniq/neural-texturize',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
