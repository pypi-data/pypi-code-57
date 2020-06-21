from rdkit.Chem import SaltRemover
from rdkit.Chem import Descriptors
import hashlib
from rdkit import Chem
import os


class Config:
    def __init__(self, url, hash, smiles_col, tasks_lst, task_type, relative_path, files, split, metric):
        self.url = url
        self.hash = hash
        self.smiles_col = smiles_col
        self.tasks_lst = tasks_lst
        self.task_type = task_type
        self.relative_path = relative_path
        # extracted file list
        self.files = files
        # directly downloaded file name
        self.fname = url.rsplit('/', 1)[-1]
        self.split = split
        self.metric = metric

        self.load_fn = None

    def add_load_fn(self, fn):
        self.load_fn = fn


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    # this returns a string
    return hash_md5.hexdigest()


"""
Functions that can be used to preprocess SMILES sequnces in the form used in the publication.
This file is modified from https://github.com/jrwnter/cddd/blob/master/cddd/preprocessing.py
So that the training data are same. Please refer to this repo and their paper for further information.

Modified: minor RDKit function calls, docstring types.
"""

REMOVER = SaltRemover.SaltRemover()
ORGANIC_ATOM_SET = {5, 6, 7, 8, 9, 14, 15, 16, 17, 35, 53}
#                   B, C, N, O, F, Si, P,  S,  Cl, Br, I

# def canonical_smile(sml):
#     """
#     Helper Function that returns the RDKit canonical SMILES for a input SMILES sequnce
#     :param str sml: A SMILES sequence.
#     :return: A canonical SMILES sequence.
#     :rtype: str
#     """
#     # modified here to first transform `sml` to a `Mol` instance.
#     return Chem.MolToSmiles(Chem.MolFromSmiles(sml), canonical=True)





# def organic_filter(sml):
#     """
#     Function that filters for organic molecules.
#     :param str sml: A SMILES sequence.
#     :return: If `sml` can be interpreted by RDKit and is organic.
#     :rtype: bool
#     """
#     try:
#         m = Chem.MolFromSmiles(sml)
#         atom_num_list = [atom.GetAtomicNum() for atom in m.GetAtoms()]
#         is_organic = (set(atom_num_list) <= ORGANIC_ATOM_SET)
#         if is_organic:
#             return True
#         else:
#             return False
#     except:
#         return False


# def filter_smiles(sml):
#     """
#     Return the canonical SMILES sequence when fulfilled rules:
#         - -5 < LogP < 7
#         - 12 < mol_weight < 600
#         - 3 < num_heavy_atoms < 50
#         - is organic (in `ORGANIC_ATOM_SET`)
#     Return None Any input SMILES violate the rules will make this
#     :param str sml: A SMILES sequence.
#     :return: A canonical SMILES sequence or None.
#     :rtype: Union[str, NoneType]
#     """
#     try:
#         m = Chem.MolFromSmiles(sml)
#         logp = Descriptors.MolLogP(m)
#         mol_weight = Descriptors.MolWt(m)
#         num_heavy_atoms = Descriptors.HeavyAtomCount(m)
#         atom_num_list = [atom.GetAtomicNum() for atom in m.GetAtoms()]
#         is_organic = set(atom_num_list) <= ORGANIC_ATOM_SET
#         if ((logp > -5) & (logp < 7) &
#                 (mol_weight > 12) & (mol_weight < 600) &
#                 (num_heavy_atoms > 3) & (num_heavy_atoms < 50) &
#                 is_organic):
#             return Chem.MolToSmiles(m)
#         else:
#             return None
#     except:
#         return None


# def preprocess_smiles(sml):
#     """
#     Function that preprocesses a SMILES string such that it is in the same format as
#     the translation model was trained on. It removes salts from the
#     SMILES sequnce. If the sequnce correspond to an inorganic molecule or cannot be
#     interpreted by RDKit, None is returned.
#     :param str sml: A SMILES sequence.
#     :return: A canonical SMILES sequence or None.
#     :rtype: Union[str, NoneType]
#     """
#     new_sml = remove_salt(sml, REMOVER)
#     # new_sml = filter_smiles(new_sml)
#     return new_sml

