import setuptools

from sri.common import config
from sri.common import entrypoints

setuptools.setup(
    name = config.PACKAGE_NAME,

    version = config.VERSION,

    description = 'Graph and PSL based TA1 primitive for D3M',
    long_description = 'Graph and PSL based TA1 primitive for D3M',
    keywords = 'd3m_primitive',

    maintainer_email = config.EMAIL,
    maintainer = config.MAINTAINER,

    # The project's main homepage.
    url = config.REPOSITORY,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Programming Language :: Python :: 3.6',
    ],

    # packages = setuptools.find_packages(exclude = ['contrib', 'docs', 'tests']),
    packages = [
        'sri',
        'sri.autoflow',
        'sri.baseline',
        'sri.common',
        'sri.pipelines',
        'sri.psl',
        'sri.psl.cli',
        'sri.interpretml',
        'sri.d3mglue',
    ],

    include_package_data = True,
    package_data = {
        'sri.psl.cli': [
            'psl-cli-2.3.0-SNAPSHOT-b5698f08.jar',
            'general_relational_template.data',
            'general_relational_template.psl',
            'vertex_classification_template.data',
            'vertex_classification_template.psl',
        ]
    },

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = [
        # Base
        'd3m', 'psutil',

        # Already provided by d3m (let d3m manage the exact versions):
        # 'numpy', 'pandas', 'scikit-learn',
    ],

    python_requires = '>=3.6',

    entry_points = entrypoints.get_entrypoints_definition()
)
