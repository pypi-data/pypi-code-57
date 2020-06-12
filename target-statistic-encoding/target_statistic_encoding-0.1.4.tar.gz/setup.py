# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_statistic_encoding', 'target_statistic_encoding.stat_funcs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.23.0,<0.24.0', 'typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'target-statistic-encoding',
    'version': '0.1.4',
    'description': 'A lightweight library for encoding categorical features in your dataset with robust k-fold target statistics in training.',
    'long_description': '# target statistic encoding\n\n<div align="center">\n  <a href="https://badge.fury.io/py/target-statistic-encoding"><img src="https://badge.fury.io/py/target-statistic-encoding.svg" alt="PyPI version" height="18"></a>\n<a href="https://codecov.io/gh/CircArgs/target_statistic_encoding">\n  <img src="https://codecov.io/gh/CircArgs/target_statistic_encoding/branch/master/graph/badge.svg" />\n</a>\n \n<img alt="Build Status" src="https://github.com/CircArgs/target_statistic_encoding/workflows/test/badge.svg">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n<img alt="Language Python" src="https://img.shields.io/badge/language-Python-blue">\n</div>\n\n---\n\n# [Table of contents:](#table-of-contents)\n\n- [Install](#install)\n  - [from pypi](#from-pypi)\n  - [from source](#from-source)\n- [What?](#what)\n- [Why?](#why)\n- [Benefits of this implementation](#benefits-of-this-implementation)\n- [How?](#how)\n- [API](#api)\n  - [Instantiate](#instantiate)\n  - [fit](#fit)\n    - [prefer`.fit_transform` on your training set](#prefer-fit-transform--on-your-training-set)\n    - [use `.transform` on your **non-training** set](#use--transform--on-your---non-training---set)\n- [Custom target statistic functions](#custom-target-statistic-functions)\n  - [Given:](#given)\n  - [Implement your own:](#implement-your-own)\n\n# Install\n\n### from pypi\n\n`pip install target-statistic-encoding`\n\n### from source\n\n`python -m pip install git+https://github.com/CircArgs/target_statistic_encoding.git`\n\n# What?\n\nThere are many means to convert categorical features to numeric ones from one-hot to embeddings. Then there are target statistic methods. These methods take statistics based on the target feature.\n\n# Why?\n\nEven within this simple technique there is variation in implementations. Some implement a time-mimicking approach such as Catboost to gain robustness over target leakage. However, one issue with this approach is that while it introduces some variation to the encoding, for a some samples the statistic is possibly excessively biased. This small package takes a different approach for this reason. Instead, it uses stratified folds of the training set and aggregates target statistics on each fold independently.\n\n# Benefits of this implementation\n\n- stratified split target statistic helps prevent target leakage thus making your models more robust\n- credibility factor allows categories with low support to be ignored additionally making your models more robust\n- clean api\n- variety of target statistic functions in addition to allowing custom implemented ones\n- easy productionalization - everything is 100% serializable with pickle\n  ex.\n  ```python\n  #save for prod/test time environment\n  pd.to_pickle(cat2num, "cat2num_for_production.pkl")\n\n  #read into prod env\n  cat2num=pd.read_pickle("cat2num_for_production.pkl")\n  ...\n  model.predict(cat2num.transform(prod_data))\n  ```\n\n# How?\n\nThis is just a simple utility library that performs the following sample operation:\n[See this example notebook](examples/example.ipynb)\n\n_keep in mind this is simply an example. The example target is random here so no real signal is expected_\n![example usage](assets/example.png)\n\n# API\n\n## Instantiate\n\n```python\nInit signature:\nCat2Num(\n    cat_vars: List[str],\n    target_var: str,\n    stat_func: target_statistic_encoding.stat_funcs.stat_funcs._StatFunc = <function mean.<locals>.stat_func at 0x7fea58a85950>,\n)\nArgs:\n    cat_vars (List[str]): a list of strings representing the categorical features to be encoded\n    target_var (str): string of the name of the target feature in `data`\n    stat_func (optional Function(*args, **kwargs) -> Function({pd.Series, pd.DataFrameGroupBy}) -> {float, pd.Series})): function which returns a closure to aggregate statistics over target - default stat_funcs.mean()\n```\n\n## fit\n\n### prefer`.fit_transform` on your training set\n\n**_Note: running `.fit` followed by `.transform` on your training set is not equivalent to simply running `.fit_transform`. There wil be no differentiation amongst category statistics as they will all be mapped to the mean._**\n\n```python\ncat2num.fit_transform(\n    data: pandas.core.frame.DataFrame,\n    split: str = None,\n    n_splits: int = 5,\n    credibility: Union[float, int] = 0,\n    drop: bool = False,\n    suffix: str = \'_Cat2Num\',\n    inplace: bool = False,\n)\n\nArgs:\n    data (pd.DataFrame): pandas dataframe with categorical features to convert to numeric target statistic\n    split (str): name of a column to use in the data for folding the data.\n        - if this is use then n_splits is ignored\n    n_splits (int): number of splits to use for target statistic\n    credibility (float or int):\n        - if float must be in [0, 1] as % of fitting data considered credible to fit statistic to\n        - if int must be >=0 as number of records in fitting data level must exist within to be credible\n        - levels not above this threshold will be given the overall target mean\n    drop (bool): drop the original columns\n    suffix (str): a string to append to the end of an encoded column, default `\'_Cat2Num\'`\n    inplace (bool): whether the transformation should be done inplace or return the transformed data, default `False`\n\nReturns:\n    the passed dataframe with encoded columns added if inplace is `False` else `None`\n```\n\n```python\ncat2num.fit(\n    data: pandas.core.frame.DataFrame,\n    credibility: Union[float, int] = 0,\n)\n\nArgs:\n    data (pd.DataFrame): pandas dataframe with categorical features to fit numeric target statistic from\n    credibility (float or int):\n        - if float must be in [0, 1] as % of fitting data considered credible to fit statistic to\n        - if int must be >=0 as number of records in fitting data level must exist within to be credible\n        - levels not above this threshold will be given the overall target mean\n\nReturns:\n    fit Cat2Num instance\n```\n\n### use `.transform` on your **non-training** set\n\n```python\ncat2num.transform(\n    data: pandas.core.frame.DataFrame,\n    drop: bool = False,\n    suffix: str = \'_Cat2Num\',\n    inplace: bool = False,\n)\n\nArgs:\n    data (pd.DataFrame): pandas dataframe with categorical features to convert to numeric target statistic\n    drop (bool): drop the original columns\n    suffix (str): a string to append to the end of an encoded column, default `\'_Cat2Num\'`\n    inplace (bool): whether the transformation should be done inplace or return the transformed data, default `False`\n\nReturns:\n    the passed dataframe with encoded columns added if inplace is `False` else `None`\n```\n\n# Custom target statistic functions\n\nYou may optionally opt for a target statistic based on a statistic other than the mean although this is usually unwanted/unnecessary.\n\nSeveral are included and you can implement your own with a few considerations.\n\n### Given:\n\n- mean (`target_statistic_encoding.stat_funcs.Mean()`) - the default\n- median (`target_statistic_encoding.stat_funcs.Median()`)\n- std (`target_statistic_encoding.stat_funcs.Std()`)\n- var (`target_statistic_encoding.stat_funcs.Var()`)\n- quantile (`target_statistic_encoding.stat_funcs.Quantile(quantile=0.5)`)\n\n### Implement your own:\n\nYou may optionally implement your own target statistic function. It must be a callable that operates on the `pandas.core.groupby.DataFrameGroupby` type i.e. the result of a `pandas.DataFrame.groupby` e.g.: something akin to\n\n<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>target</th>    </tr>    <tr>      <th>X1</th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>a</th>      <td>0.287356</td>    </tr>    <tr>      <th>b</th>      <td>0.298795</td>    </tr>    <tr>      <th>c</th>      <td>0.336879</td>    </tr>    <tr>      <th>d</th>      <td>0.287037</td>    </tr>  </tbody></table>\n',
    'author': 'CircArgs',
    'author_email': 'quebecname@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CircArgs/target_statistic_encoding',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
