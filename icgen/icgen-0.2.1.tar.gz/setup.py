# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icgen']

package_data = \
{'': ['*'],
 'icgen': ['infos/*',
           'infos/cmaterdb/*',
           'infos/cycle_gan/*',
           'infos/emnist/*',
           'infos/eurosat/*',
           'infos/imagenet_resized/*',
           'infos/visual_domain_decathlon/*']}

install_requires = \
['PILLOW>=7.1.2,<8.0.0',
 'more_itertools>=8.4.0,<9.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'tensorflow>=2.2.0,<3.0.0',
 'tensorflow_datasets==2.1.0',
 'torch>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'icgen',
    'version': '0.2.1',
    'description': ' Image Classification Dataset Generator',
    'long_description': '# ICGen\n\n## Installation\n\n### The Package\n\n```\ngit clone https://github.com/automl/ICGen.git\npip install ICGen/\n```\n\n### Downloading the Datasets\n\nTo download datasets you can run\n\n```\npython -m icgen.download --data_path DATA_PATH --datasets D1 D2 D3\n```\n\nor directly download a complete group\n\n```\npython -m icgen.download --data_path DATA_PATH --dataset_group GROUP  # all, train, dev, test\n```\n\nFor a list of available datasets you can run\n\n```\npython -m icgen.dataset_names\n```\n\n\n## Usage\n\n### Sampling Tasks\n\n```python\nimport icgen\ndataset_generator = icgen.ICDatasetGenerator(\n  data_path="datasets",  # Replace with the data_path you downloaded the datasets to\n  min_resolution=16,\n  max_resolution=512,\n  max_log_res_deviation=1,  # Sample only 1 log resolution from the native one\n  min_classes=2,\n  max_classes=100,\n  min_examples_per_class=20,\n  max_examples_per_class=100_000,\n)\ndev_data, test_data, dataset_info = dataset_generator.get_dataset(dataset="cifar10", augment=True)\n```\n\nThe `augment` parameter controls whether the original dataset is modified.\n\nOptions only affect sampling with `augment=True` and the min max ranges do not filter datasets.\n\nThe data is left at the original resolution, so it can be resized once by the user.\n\nYou can also sample from a list of datasets\n\n```python\ntask = dataset_generator.get_dataset(datasets=["cifar100", "emnist/balanced"], augment=True)\n```\n\nWe provide some lists of available datasets\n\n```python\nimport icgen\nicgen.DATASETS_TRAIN\nicgen.DATASETS_VAL\nicgen.DATASETS_TEST\nicgen.DATASETS\n```\n\n### Reconstructing and Distributing Tasks\n\nIn distributed applications it may be necessary to sample datasets on one machine and then use them on another one.\nConversely, for reproducibility it may be necessary to store the exact dataset which was used.\nFor these cases icgen uses a dataset identifier which uniquely identifies datasets.\n\n\n## License\n\n[MIT](LICENSE)\n',
    'author': 'Danny Stoll',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/automl/ICGen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
