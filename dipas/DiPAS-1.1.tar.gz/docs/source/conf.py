# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
from pkg_resources import get_distribution
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


# -- Project information -----------------------------------------------------

project = 'DiPAS'
copyright = '2020, Dominik Vilsmeier'
author = 'Dominik Vilsmeier'

# The full version, including alpha/beta/rc tags
release = get_distribution(project.lower()).version
version = '.'.join(release.split('.')[:2])


# -- General configuration ---------------------------------------------------

master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['nbsphinx', 'sphinx.ext.autodoc', 'sphinx.ext.napoleon']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

autodoc_mock_imports = ['numpy', 'pandas', 'pint', 'scipy', 'scipy.constants', 'scipy.linalg', 'scipy.special', 'scipy.stats', 'torch']
sys.modules.update({name: MagicMock() for name in autodoc_mock_imports})
sys.modules['torch'].nn.Module = object


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'nature'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


def run_apidoc(_):
    from sphinx.ext import apidoc
    import os
    import sys

    # sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    source_dir = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(source_dir, 'api')
    module_path = os.path.join(source_dir, '..', '..', project.lower())
    apidoc.main(['-e', '-o', output_path, module_path, '--force'])

    with open(os.path.join(source_dir, 'api', 'modules.rst')) as fh:
        content = fh.read()
    content = content.replace('dipas', 'DiPAS API', 1)
    content = content.replace('=====', '=========', 1)
    with open(os.path.join(source_dir, 'api', 'modules.rst'), 'w') as fh:
        fh.write(content)


def setup(app):
    app.connect('builder-inited', run_apidoc)
