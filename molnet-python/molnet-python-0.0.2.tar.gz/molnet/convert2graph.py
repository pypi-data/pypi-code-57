import molnet
from pathlib import Path
import torch
from torch_geometric.data import Data
from torch_geometric.data import InMemoryDataset
from torch_geometric.data import Batch

import numpy as np
from rdkit import Chem
"""
This script is modified from https://github.com/deepchem/deepchem/blob/master/deepchem/feat/graph_features.py
"""

# def keep_largest_fragment(sml):
#     """
#     Function that returns the SMILES sequence of the largest fragment for a input
#     SMILES sequence.
#     :param str sml: A SMILES sequence.
#     :return: The canonical SMILES sequence of the largest fragment.
#     :rtype: str
#     """
#     mol_frags = Chem.GetMolFrags(Chem.MolFromSmiles(sml), asMols=True)
#     largest_mol = None
#     largest_mol_size = 0
#     for mol in mol_frags:
#         size = mol.GetNumAtoms()
#         if size > largest_mol_size:
#             largest_mol = mol
#             largest_mol_size = size
#     return Chem.MolToSmiles(largest_mol)
#
#
# def remove_salt(sml, remover):
#     """
#     Function that strips salts from a SMILES. :param str sml: A SMILES sequence.
#     :param SaltRemover remover: RDKit's SaltRemover object.
#     :return: The canonical SMILES sequence without salts. If any error on processing, return None instead.
#     :rtype: Union[str, NoneType]
#     """
#     try:
#         sml = Chem.MolToSmiles(remover.StripMol(Chem.MolFromSmiles(sml),
#                                dontRemoveEverything=True))
#         if "." in sml:
#             sml = keep_largest_fragment(sml)
#     except:
#         sml = None
#     return sml


# def one_of_k_encoding(x, allowable_set):
#     if x not in allowable_set:
#         raise Exception("input {0} not in allowable set{1}:".format(x, allowable_set))
#     return [x == s for s in allowable_set]


def one_of_k_encoding_unk(x, allowable_set):
    """Maps inputs not in the allowable set to the last element."""
    if x not in allowable_set:
        x = allowable_set[-1]
    return [x == s for s in allowable_set]


def safe_index(lst, e):
    """Gets the index of e in l, providing an index of len(l) if not found"""
    try:
        return lst.index(e)
    except:
        return len(lst)


def calc_gasteiger_charges(mol_or_atom, iter=12):
    if isinstance(mol_or_atom, Chem.Atom):
        atom = mol_or_atom
    else:
        assert isinstance(mol_or_atom, Chem.Mol)
        atom = mol_or_atom.GetAtomWithIdx(0)
    try:
        mol_or_atom.GetProp('_GasteigerCharge')
    except KeyError:
        mol = atom.GetOwningMol()

        Chem.rdPartialCharges.ComputeGasteigerCharges(mol, nIter=iter, throwOnParamFailure=False)


def atom_features(atom, explicit_H=False, use_chirality=True, gasteiger_charges_iter=12):
    results = one_of_k_encoding_unk(atom.GetSymbol(),
                                    ['B', 'C', 'N', 'O', 'F', 'Si', 'P', 'S', 'Cl', 'Br', 'I', 'other']) + \
              one_of_k_encoding_unk(atom.GetDegree(), [0, 1, 2, 3, 4, 5, 6, 'others']) + \
              [atom.GetFormalCharge(), atom.GetNumRadicalElectrons()] + \
              one_of_k_encoding_unk(atom.GetHybridization(), [
                  Chem.rdchem.HybridizationType.SP, Chem.rdchem.HybridizationType.SP2,
                  Chem.rdchem.HybridizationType.SP3, Chem.rdchem.HybridizationType.SP3D,
                  Chem.rdchem.HybridizationType.SP3D2, 'other']) + [atom.GetIsAromatic()]
    # In case of explicit hydrogen(QM8, QM9), avoid calling `GetTotalNumHs`
    if not explicit_H:
        results = results + one_of_k_encoding_unk(atom.GetTotalNumHs(),
                                                  [0, 1, 2, 3, 4])
    if use_chirality:
        try:
            results += one_of_k_encoding_unk(atom.GetProp('_CIPCode'), ['R', 'S']) + [
                atom.HasProp('_ChiralityPossible')]
        except:
            results += [False, False] + [atom.HasProp('_ChiralityPossible')]
    calc_gasteiger_charges(atom)
    results += [float(atom.GetProp('_GasteigerCharge')), float(atom.GetProp('_GasteigerHCharge'))]
    return np.array(results)


def bond_features(bond, use_chirality=True):
    bt = bond.GetBondType()
    bond_feats = [
        bt == Chem.rdchem.BondType.SINGLE, bt == Chem.rdchem.BondType.DOUBLE,
        bt == Chem.rdchem.BondType.TRIPLE, bt == Chem.rdchem.BondType.AROMATIC,
        bond.GetIsConjugated(),
        bond.IsInRing()
    ]
    if use_chirality:
        bond_feats = bond_feats + one_of_k_encoding_unk(
            str(bond.GetStereo()),
            ["STEREONONE", "STEREOANY", "STEREOZ", "STEREOE"])
    return np.array(bond_feats)


def num_atom_features():
    # Return length of feature vector using a very simple molecule.
    m = Chem.MolFromSmiles('CC')
    alist = m.GetAtoms()
    a = alist[0]
    return len(atom_features(a))


def num_bond_features():
    # Return length of feature vector using a very simple molecule.
    simple_mol = Chem.MolFromSmiles('CC')
    Chem.SanitizeMol(simple_mol)
    return len(bond_features(simple_mol.GetBonds()[0]))


def mol_to_pyG_data(mol, explicit_H=False, use_chirality=True, gasteiger_charges_iter=12):
    calc_gasteiger_charges(mol)
    # atoms
    atom_features_list = []
    for atom in mol.GetAtoms():
        atom_feature = atom_features(atom, explicit_H=explicit_H, use_chirality=use_chirality)
        atom_features_list.append(atom_feature)
    x = torch.tensor(np.array(atom_features_list))
    # bonds, we will force molecules have at least 2 atoms
    edges_list = []
    edge_features_list = []
    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()
        edge_feature = bond_features(bond, use_chirality=use_chirality)
        edges_list.append((i, j))
        edge_features_list.append(edge_feature)
        edges_list.append((j, i))
        edge_features_list.append(edge_feature)

    # data.edge_index: Graph connectivity in COO format with shape [2, num_edges]
    edge_index = torch.tensor(np.array(edges_list).T, dtype=torch.long)

    # data.edge_attr: Edge feature matrix with shape [num_edges, num_edge_features]
    edge_attr = torch.tensor(np.array(edge_features_list),
                             dtype=torch.long)
    data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
    return data


class MoleculeNetGraphDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None, dataset='ESOL'):
        assert dataset in molnet.molnet_config.keys() or dataset == 'custom'
        self.dataset = dataset
        self.raw_data = None
        # self.remove_salt = remove_salt
        super(MoleculeNetGraphDataset, self).__init__(root, transform, pre_transform, pre_filter)
        self.data, self.slices = torch.load(self.processed_paths[0])


    @property
    def raw_file_names(self):
        relpath = molnet.molnet_config[self.dataset].relative_path
        files = molnet.molnet_config[self.dataset].files
        return [Path(relpath) / f for f in files]

    @property
    def processed_dir(self):
        return Path(self.root) / 'processed' / molnet.molnet_config[self.dataset].relative_path

    @property
    def processed_file_names(self):
        return [f"{self.dataset}.pt"]

    def download(self):
        mol_dataset = molnet.molnet_config[self.dataset].load_fn(self.raw_dir)
        if molnet.molnet_config[self.dataset].task_type == 'classification':
            mol_dataset.calc_weight_classification()
        else:
            mol_dataset.cal_weight_basic()
        self.raw_data = mol_dataset

    def process(self):
        if self.raw_data is None:
            self.download()
        data_list = [mol_to_pyG_data(mol) for mol in self.raw_data.mols]
        labels, weights = self.raw_data.y, self.raw_data.w
        assert len(data_list) == len(labels) == len(weights)
        for idx, data in enumerate(data_list):
            data.y = torch.tensor(labels[idx])
            data.w = torch.tensor(weights[idx])
        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])


class CustomMoleculeDataset(InMemoryDataset):
    def __init__(self, root, mols, y, w=None, transform=None, pre_transform=None, pre_filter=None, name='custom'):
        self.raw_data = molnet.load_functions.MolDataset(mols, y)
        self.name = name
        if w is not None:
            self.raw_data.w = w
        else:
            self.raw_data.cal_weight_basic()
        super(CustomMoleculeDataset, self).__init__(root, transform, pre_transform, pre_filter)
        (Path(self.processed_dir)/'pre_filter.pt').unlink()
        (Path(self.processed_dir) / 'pre_transform.pt').unlink()
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        Path(self.raw_dir).mkdir(parents=True, exist_ok=True)
        file_name_list = list(Path(self.raw_dir).iterdir())
        # assert len(file_name_list) == 1     # currently assume we have a
        # # single raw file
        return file_name_list
    @property
    def processed_file_names(self):
        return [f'{self.name}_{len(self.raw_data)}.pt']

    def download(self):
        print('Dummy download function invoked')

    def process(self):
        data_list = [mol_to_pyG_data(mol) for mol in self.raw_data.mols]
        labels, weights = self.raw_data.y, self.raw_data.w
        assert len(data_list) == len(labels) == len(weights)
        for idx, data in enumerate(data_list):
            data.y = torch.tensor(labels[idx])
            data.w = torch.tensor(weights[idx])
        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])

