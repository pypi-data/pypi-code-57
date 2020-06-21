import pandas as pd
import numpy as np
from pathlib import Path
from rdkit import RDLogger
from rdkit import Chem
import tqdm
import cloudpickle

from molnet.molnet_config import molnet_config
from molnet.download import download

lg = RDLogger.logger()
lg.setLevel(RDLogger.CRITICAL)


class MolDataset:
    def __init__(self, mols, y):
        """
        Numpy molecule dataset
        :param mols: N molecules
        :param y: N * num_tasks matrix
        """
        self.mols = np.asarray(mols)
        self.y = np.asarray(y)
        if len(self.y.shape) == 1:
            self.y = np.expand_dims(self.y, axis=1)  # make this shape (N, 1)
        assert len(self.y.shape) == 2
        self.w = None
        self._filter(based_on=self.mols, what=None)
        assert len(self.mols) == len(self.y)

    def __len__(self):
        return len(self.mols)

    def __repr__(self):
        return f'<MolDataset: {len(self)} molecules.>'

    def _filter(self, based_on, what):
        mask = (based_on != what)
        self.mols = self.mols[mask]
        self.y = self.y[mask]
        if self.w:
            self.w = self.w[mask]

    def calc_weight_classification(self):
        mask = np.isnan(self.y)
        assert np.all(np.unique(self.y[~mask]) == np.array([0,1]))
        self.w = np.ones_like(self.y, dtype=float)
        # target value is nan, then corresponding weight is 0
        self.w[mask] = 0
        for col in range(self.y.shape[1]):
            y, w = self.y[:, col], self.w[:, col]
            pos_mask = ~mask[:,col] & (y == 1)
            neg_mask = ~mask[:,col] & (y == 0)
            pos_num = pos_mask.sum()
            neg_num = neg_mask.sum()
            # negative weight is 1
            pos_w = neg_num / pos_num
            self.w[pos_mask, col] = pos_w
            self.w[neg_mask, col] = 1

    def cal_weight_basic(self):
        mask = np.isnan(self.y)
        self.w = np.ones_like(self.y, dtype=float)
        # target value is nan, then corresponding weight is 0
        self.w[mask] = 0

    def randomize(self):
        index = np.random.permutation(len(self.mols))
        self.mols = self.mols[index]
        self.y = self.y[index]
        if self.w:
            self.w = self.w[index]

    def subset(self, idx):
        mols = self.mols[idx]
        y = self.y[idx]
        return MolDataset(mols, y)

    @staticmethod
    def merge(dataset_lst):
        mols = np.concatenate([d.mols for d in dataset_lst], axis=0)
        y = np.concatenate([d.y for d in dataset_lst], axis=0)
        return MolDataset(mols, y)


def load_QM7(datadir, save=False):
    prefix = Path(datadir) / molnet_config['QM7'].relative_path
    download('QM7', datadir)
    cache_file = prefix / ('QM7' + '.bin')
    if cache_file.is_file():
        dataset = cloudpickle.load(open(cache_file, 'rb'))
        return dataset
    df = pd.read_csv(prefix / molnet_config['QM7'].files[0])
    mols = np.array([Chem.MolFromSmiles(i) for i in tqdm.tqdm(df['smiles'])])
    dataset = MolDataset(mols, df['u0_atom'].to_numpy())
    if save:
        cloudpickle.dump(dataset, open(cache_file, 'wb'))
    return dataset


# def load_QM7b(datadir, save=False):
#     prefix = Path(datadir) / molnet_config['QM7b'].relative_path
#     download('QM7b', datadir)
#     cache_file = prefix / ('QM7b' + '.bin')
#     if cache_file.is_file():
#         dataset = cloudpickle.load(open(cache_file, 'rb'))
#         return dataset
#     df = pd.read_csv(prefix / molnet_config['QM7b'].files[0])
#     mols = np.array([Chem.MolFromSmiles(i) for i in tqdm.tqdm(df['smiles'])])
#     dataset = MolDataset(mols, df['u0_atom'].to_numpy())
#     if save:
#         cloudpickle.dump(dataset, open(cache_file, 'wb'))
#     return dataset


def load_QM8(datadir, save=False):
    prefix = Path(datadir) / molnet_config['QM8'].relative_path
    download('QM8', datadir)
    cache_file = prefix / ('QM8' + '.bin')
    if cache_file.is_file():
        dataset = cloudpickle.load(open(cache_file, 'rb'))
        return dataset
    df = pd.read_csv(prefix / molnet_config['QM8'].files[0])
    # mols = df[molnet_config['QM8'].smiles_col].to_numpy()
    suppl = Chem.SDMolSupplier(str(prefix / molnet_config['QM8'].files[1]))
    mols = np.array([m for m in tqdm.tqdm(suppl)])
    y = df[molnet_config['QM8'].tasks_lst].to_numpy()
    dataset = MolDataset(mols, y)
    if save:
        cloudpickle.dump(dataset, open(cache_file, 'wb'))
    return dataset


def load_QM9(datadir, save=False):
    prefix = Path(datadir) / molnet_config['QM9'].relative_path
    download('QM9', datadir)
    cache_file = prefix / ('QM9' + '.bin')
    if cache_file.is_file():
        dataset = cloudpickle.load(open(cache_file, 'rb'))
        return dataset
    df = pd.read_csv(prefix / molnet_config['QM9'].files[0])
    # mols = df[molnet_config['QM8'].smiles_col].to_numpy()
    suppl = Chem.SDMolSupplier(str(prefix / molnet_config['QM9'].files[1]))
    mols = np.array([m for m in tqdm.tqdm(suppl)])
    y = df[molnet_config['QM9'].tasks_lst].to_numpy()
    dataset = MolDataset(mols, y)
    if save:
        cloudpickle.dump(dataset, open(cache_file, 'wb'))
    return dataset


def load_single_csv(name):
    def loadfn(datadir, save=False):
        prefix = Path(datadir) / molnet_config[name].relative_path
        download(name, datadir)
        cache_file = prefix / (name + '.bin')
        if cache_file.is_file():
            dataset = cloudpickle.load(open(cache_file, 'rb'))
            return dataset
        df = pd.read_csv(prefix / molnet_config[name].files[0])
        mols = np.array([Chem.MolFromSmiles(smi) for smi in tqdm.tqdm(df[molnet_config[name].smiles_col])])
        y = df[molnet_config[name].tasks_lst].to_numpy()
        dataset = MolDataset(mols, y)
        if save:
            cloudpickle.dump(dataset, open(cache_file, 'wb'))
        return dataset
    return loadfn


load_ESOL = load_single_csv('ESOL')
load_FreeSolv = load_single_csv('FreeSolv')
load_Lipophilicity = load_single_csv('Lipophilicity')
load_PCBA = load_single_csv('PCBA')
load_MUV = load_single_csv('MUV')
load_HIV = load_single_csv('HIV')
load_BACE = load_single_csv('BACE')
load_BBBP = load_single_csv('BBBP')
load_Tox21 = load_single_csv('Tox21')
load_ToxCast = load_single_csv('ToxCast')
load_SIDER = load_single_csv('SIDER')
load_ClinTox = load_single_csv('ClinTox')

if __name__ == '__main__':
    print(load_QM9('../'))
