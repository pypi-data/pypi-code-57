import inspect, os

__execdir__ = os.path.basename(
    os.path.dirname(
        os.path.abspath(
            inspect.getfile(
                inspect.currentframe()
            )
        )
    )
)
__packagename__ = 'FSMakeROI'
__version__='v1.2'
__author__ = 'Siddhartha Dhiman'
__copyright__ = 'Copyright 2020, Siddhartha Dhiman'
__credits__ = [
    'Siddhartha Dhiman',
]
__maintainer__ = 'Siddhartha Dhiman'
__email__ = 'dhiman@musc.edu'
__url__ = 'https://github.com/TheJaeger/FSMakeROI'
__license__='MPL 2.0'
__description__ = ('A CLI tool to extract ROIs from Freesurfer '
                    'segmentation file')
                    
# Gets folder name where this file resides
__execdir__ = os.path.basename(
    os.path.dirname(
        os.path.abspath(
            inspect.getfile(
                inspect.currentframe()
                )
            )
        )
    )

# PyPi package requirements
REQUIRES = [
    'numpy',
    'pandas',
    'nibabel',
    'tqdm'
]

# Python version requirements
PYTHON_REQUIRES = ">=3.7"

# Package classifiers
CLASSIFIERS = [
    'Programming Language :: Python :: 3.7',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'Operating System :: OS Independent'
]