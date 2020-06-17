# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['samplics',
 'samplics.estimation',
 'samplics.sae',
 'samplics.sampling',
 'samplics.utils',
 'samplics.weighting']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1.3,<4.0.0',
 'numpy>=1.15,<2.0',
 'pandas>=1.0,<2.0',
 'scipy>=1.4,<2.0',
 'statsmodels>=0.10,<0.11']

setup_kwargs = {
    'name': 'samplics',
    'version': '0.2.3',
    'description': 'Select, weight and analyze complex sample data',
    'long_description': '==========\n*SAMPLICS*\n==========\n.. image:: https://travis-ci.com/survey-methods/samplics.svg?token=WwRayqkQBt1W4ihyTzvw&branch=master\n  :target: https://travis-ci.com/survey-methods/samplics\n\n.. image:: https://codecov.io/gh/survey-methods/samplics/branch/master/graph/badge.svg?token=7C0LBB5N8Y\n  :target: https://codecov.io/gh/survey-methods/samplics     \n\n.. image:: https://readthedocs.org/projects/samplics/badge/?version=latest\n  :target: https://samplics.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\n*samplics* is a python package for selecting, weighting and analyzing sample obtained from complex sampling design.\n\n\nInstallation\n------------\n``pip install samplics``\n\nif both Python 2.x and python 3.x are installed on your computer, you may have to use: ``pip3 install samplics``\n\nDependencies\n------------\nPython versions 3.6.x or newer and the following packages:\n\n* `numpy <https://numpy.org/>`_\n* `pandas <https://pandas.pydata.org/>`_\n* `scpy <https://www.scipy.org/>`_\n* `statsmodels <https://www.statsmodels.org/stable/index.h.tml>`_\n\nUsage\n------\n\nTo select a sample of primary sampling units using PPS method,\nwe can use a code similar to:\n\n.. code:: python\n\n    import samplics\n    from samplics.sampling import SampleSelection\n\n    psu_frame = pd.read_csv("psu_frame.csv")\n    psu_sample_size = {"East":3, "West": 2, "North": 2, "South": 3}\n    pps_design = SampleSelection(method="pps-sys", stratification=True, with_replacement=False)\n    frame["psu_prob"] = pps_design.inclusion_probs(\n        psu_frame["cluster"],\n        psu_sample_size,\n        psu_frame["region"],\n        psu_frame["number_households_census"]\n        )\n\nTo adjust the design sample weight for nonresponse,\nwe can use a code similar to:\n\n.. code:: python\n\n    import samplics\n    from samplics.weighting import SampleWeight\n\n    status_mapping = {\n        "in": "ineligible", "rr": "respondent", "nr": "non-respondent", "uk":"unknown"\n        }\n\n    full_sample["nr_weight"] = SampleWeight().adjust(\n        samp_weight=full_sample["design_weight"],\n        adjust_class=full_sample["region"],\n        resp_status=full_sample["response_status"],\n        resp_dict=status_mapping\n        )\n\n.. code:: python\n\n    import samplics\n    from samplics.estimation import TaylorEstimation, ReplicateEstimator\n\n    zinc_mean_str = TaylorEstimator("mean").estimate(\n        y=nhanes2f["zinc"],\n        samp_weight=nhanes2f["finalwgt"],\n        stratum=nhanes2f["stratid"],\n        psu=nhanes2f["psuid"],\n        remove_nan=True\n    )\n\n    ratio_wgt_hgt = ReplicateEstimator("brr", "ratio").estimate(\n        y=nhanes2brr["weight"],\n        samp_weight=nhanes2brr["finalwgt"],\n        x=nhanes2brr["height"],\n        rep_weights=nhanes2brr.loc[:, "brr_1":"brr_32"],\n        remove_nan = True\n    )\n\n\nContributing\n------------\nTBD\n\nLicense\n-------\n`MIT <https://github.com/survey-methods/samplics/blob/master/license.txt>`_\n\nProject status\n--------------\nThis is a beta version. At this stage, this project is not recommended to be\nused for production or any project that the user depend on.\n\n\n\n\n',
    'author': 'Mamadou S Diallo',
    'author_email': 'msdiallo@quantifyafrica.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://samplics.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
