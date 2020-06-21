from pathlib import Path
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit import Chem
import numpy as np
import cloudpickle


def generate_scaffold(smiles, include_chirality=False):
    """Compute the Bemis-Murcko scaffold for a SMILES string."""
    if isinstance(smiles, Chem.Mol):
        mol = smiles
    else:
        mol = Chem.MolFromSmiles(smiles)
    scaffold = MurckoScaffold.MurckoScaffoldSmiles(mol=mol, includeChirality=include_chirality)
    return scaffold


class Splitter(object):
    def __init__(self, save_to=None):
        self.save_to = save_to

    def save_split(self, name, obj_lst):
        if self.save_to is not None:
            p = Path(self.save_to)
            cloudpickle.dump(obj_lst, open(p/name, 'wb'))
            return p/name
        return None

    def load_split(self, name):
        if self.save_to is None:
            return None
        p = Path(self.save_to)
        if not (p/name).is_file():
            return None
        print(f'Loading splits from cached file: {p/name}')
        obj = cloudpickle.load(open(p/name, 'rb'))
        return obj

    def k_fold_split(self, dataset, k, seed=None):
        """
        Do k fold cv split
        :param dataset: whole dataset
        :param k: k fold
        :param seed: random seed
        :return: a list of subsets
        """
        cache = self.load_split('KFold.split')
        if cache is not None:
            return cache
        cv_datasets = []
        # rem_dataset is remaining portion of dataset
        rem_dataset = dataset
        for fold in range(k):
            # for example, k=5, a) select 1*1/(5-0)=1/5, remain 4/5; b) select 4/5*1/(5-1)=1/5, remain 3/5 ...
            frac_fold = 1. / (k - fold)
            fold_inds, rem_inds, _ = self.split(rem_dataset, frac_train=frac_fold,
                                                frac_valid=1-frac_fold, frac_test=0, seed=seed)
            cv_dataset = rem_dataset.subset(fold_inds)
            cv_datasets.append(cv_dataset)
            rem_dataset = rem_dataset.subset(rem_inds)
            self.save_split('KFold.split', cv_datasets)
        return cv_datasets

    def train_valid_test_split(self, dataset, frac_train=.8, frac_valid=.1, frac_test=.1, seed=None):
        """
        do train valid test split
        :param dataset:
        :param frac_train:
        :param frac_valid:
        :param frac_test:
        :param seed:
        :return:
        """
        cache = self.load_split('train_valid_test.split')
        if cache is not None:
            return cache
        train_inds, valid_inds, test_inds = self.split(dataset, frac_train=frac_train,
                                                       frac_test=frac_test, frac_valid=frac_valid, seed=seed)
        train_dataset = dataset.subset(train_inds)
        if len(valid_inds) != 0:
            valid_dataset = dataset.subset(valid_inds)
        else:
            valid_dataset = None
        if len(test_inds) != 0:
            test_dataset = dataset.subset(test_inds)
        else:
            test_dataset = None
        self.save_split('train_valid_test.split', (train_dataset, valid_dataset, test_dataset))
        return train_dataset, valid_dataset, test_dataset

    def train_test_split(self, dataset, frac_train=.8, seed=None):
        """
        Simple wraper of train_valid_test_split function
        :param dataset:
        :param frac_train:
        :param seed:
        :return:
        """
        cache = self.load_split('train_test.split')
        if cache is not None:
            return cache
        train_dataset, _, test_dataset = self.train_valid_test_split(dataset, frac_train=frac_train,
                                                                     frac_test=1 - frac_train, frac_valid=0,
                                                                     seed=seed)
        self.save_split('train_test.split', (train_dataset, test_dataset))
        return train_dataset, test_dataset

    def split(self, dataset, frac_train, frac_valid, frac_test, seed):
        raise NotImplementedError


class RandomSplitter(Splitter):
    """
    Class for random split molecules
    """
    def split(self, dataset, frac_train=.8, frac_valid=.1, frac_test=.1, seed=None):
        np.testing.assert_almost_equal(frac_train + frac_valid + frac_test, 1.)
        rng = np.random.RandomState(seed)
        perm = rng.permutation(len(dataset))
        train_cutoff = int(len(dataset) * frac_train)
        valid_cutoff = int(len(dataset) * (frac_train + frac_valid))
        return perm[:train_cutoff], perm[train_cutoff:valid_cutoff], perm[valid_cutoff:]


class ScaffoldSplitter(Splitter):
    """
    Class for doing data splits based on the scaffold of small molecules.
    """

    def split(self, dataset, frac_train=.8, frac_valid=.1, frac_test=.1, seed=None):
        """
        Do scaffold split
        :param dataset:
        :param frac_train:
        :param frac_valid:
        :param frac_test:
        :param seed: seed is useless here for scaffold split is not random
        :return:
        """
        np.testing.assert_almost_equal(frac_train + frac_valid + frac_test, 1.)
        if seed is not None:
            print("Scaffold split is not a random procedure, so seed is useless here")
        scaffolds = {}
        for ind, smiles in enumerate(dataset.mols):
            scaffold = generate_scaffold(smiles)
            if scaffold not in scaffolds:
                scaffolds[scaffold] = [ind]
            else:
                scaffolds[scaffold].append(ind)
        # Sort from largest to smallest scaffold sets
        scaffolds = {key: sorted(value) for key, value in scaffolds.items()}
        # TODO: Why here is sorted? this will produce same train, valid and test set on every time!
        scaffold_sets = [scaffold_set for (scaffold, scaffold_set) in
                         sorted(scaffolds.items(), key=lambda x: (len(x[1]), x[1][0]), reverse=True)]
        train_cutoff = frac_train * len(dataset)
        valid_cutoff = (frac_train + frac_valid) * len(dataset)
        train_inds, valid_inds, test_inds = [], [], []
        for scaffold_set in scaffold_sets:
            if len(train_inds) + len(scaffold_set) > train_cutoff:
                if len(train_inds) + len(valid_inds) + len(scaffold_set) > valid_cutoff:
                    test_inds += scaffold_set
                else:
                    valid_inds += scaffold_set
            else:
                train_inds += scaffold_set
        return train_inds, valid_inds, test_inds
