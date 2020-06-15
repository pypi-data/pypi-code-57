# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algovis', 'algovis.sorting']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'algovis',
    'version': '0.1.3',
    'description': 'Python library for visualising algorithms',
    'long_description': '![Alogvis]( /algovis_img.PNG?raw=true)\n\nAlgovis is a library with which you can learn how to code data structures and algorithms in Python\n\nIt will have most of the prominent sorting, searching and graph algorithms with visualisations.\n\nCurrently the library has\n\n# Sorting\n\n- Bubble Sort\n\n# Getting Started\n\nI would highly suggest making a virtual environment as this library is still in beta\n\nFor making a virtual environment, we can use virtualenv\n\n```python\n# installing virtualenv\n\n$pip3 install virtualenv\n\n# making a test folder\n\n$mkdir test\n\n# make it the current directory\n\n$ cd test\n\n# making a virtual env (you can replace envname with whatever name you like)\n\n$virtualenv - p python3 envname\n\n# activating it\n\n$ source envname / bin / activate\n\n# installing algovis\n\n$ pip3 install algovis\n```\n\nYou can only access algovis inside this virtual environment. To leave this virtualenv, type\n\n```python\n$deactivate\n```\n\n# Using this library\n\nI have designed the library this way so that supporting making changes to it is easy\n\n```python\n# Using bubblesort in algovis\n\n# import the sorting module from library\n\nfrom algovis import sorting\n\n# importing random library to fill it the list with random integers\n\nimport random\n\n# Making a list of 50 random integers in range of 0 to 100\n\nmy_list = [random.randint(0, 100) for i in range(50)]\n\n# Making a bubble sort class object\n# It only accepts lists, raises an exception otherwise\n\nbs_object = sorting.BubbleSort(my_list)\n\n# bs_object is now an object of the bubblesort class\n# The class has 3 functions\n\n# .sort() with 2 optional parameters reverse and steps, both boolean\n# reverse sorts the list in descending order and steps shows every iteration\n# of the bubble sort algotithm\n\n# default of reverse if False\n# default of steps is False\n# return type: Dictionary\n\ndesc_sort = bs_object.sort(reverse=True, steps=True)\n\n# .evaluate() with 2 optional parameters reverse and iterations\n# .evaluate() returns a dictionary giving a dictionary of minimum,\n# maximum and average time to sort the list in seconds\n\n# reverse option sorts it in descending order\n# default is False\n\n# iterations is the number of times you want to run the algo\n# default is 1\n\neval_algo0 = bs_object.evaluate(iterations=100)\n\neval_algo1 = bs_object.evaluate(reverse=True, iterations=500)\n\n# .visualize() makes the visualization of the list you gave getting sorted\n# in ascending order\n# it has one option, reverse which is a boolean\n\nvis_algo = bs_object.visualize(reverse=True)\n\n```\n\n    [Last updated on 16th June 2020]\n',
    'author': 'hotshot07',
    'author_email': 'aroram@tcd.ie',
    'maintainer': 'hotshot07',
    'maintainer_email': 'aroram@tcd.ie',
    'url': 'https://github.com/hotshot07/algovis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
