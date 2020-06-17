"""
:synopsis: Global datasets available
.. moduleauthor:: Naval Bhandari <naval@neuro-ai.co.uk>
"""

from ..core import Dataset

CIFAR10 = Dataset("cifar10_train", 40000, 50000, 60000)
""":CIFAR10: CIFAR10 dataset. Contains training/validation/test subsets of data. Accessed using 
`CIFAR10.train/val/test` properties. Can also get direct subset using slices. """
