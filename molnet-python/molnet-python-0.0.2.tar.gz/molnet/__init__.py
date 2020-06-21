from molnet.molnet_config import molnet_config
# from molnet.load_functions import MolDataset, load_QM7, load_QM7b, load_QM8, load_QM9, load_ESOL, load_FreeSolv, \
#     load_Lipophilicity, load_PCBA, load_MUV, load_HIV, load_BACE, load_BBBP, load_Tox21, load_ToxCast, \
#     load_SIDER, load_ClinTox
import molnet.load_functions
from molnet.splitter import ScaffoldSplitter, RandomSplitter
# from molnet.convert2graph import
from pathlib import Path


molnet_list = list(molnet_config.keys())

for name in molnet_list:
    fn = getattr(load_functions, f'load_{name}')
    molnet_config[name].add_load_fn(fn)


def load(name, datadir, save_whole_dataset=False, save_split=False, split=None, seed=None):
    """

    :param name: Dataset name
    :param datadir: where to store downloaded and extracted and saved data
    :param save_whole_dataset: save pickled dataset, with extracted molecules and target
    :param save_split: save splitting results
    :param split:
    :param seed:
    :return:
    """
    if split is None:
        split = (0.8, 0.1, 0.1)
        split_method = 'train_valid_test_split'
    elif isinstance(split, (list, tuple)):
        assert len(split) == 3
        split_method = 'train_valid_test_split'
    elif isinstance(split, float):
        split_method = 'train_test_split'
    elif isinstance(split, int):
        split_method = 'k_fold_split'
    else:
        raise TypeError('Argument `split` should be None, list/tuple, int or float')
    assert split_method is not None
    # first check argument, then load data, make error fast
    whole_dataset = molnet_config[name].load_fn(datadir, save=save_whole_dataset)
    if save_split:
        save_split = Path(datadir) / molnet_config[name].relative_path
    else:
        save_split = None
    if molnet_config[name].split == 'random':
        spl = RandomSplitter(save_to=save_split)
    elif molnet_config[name].split == 'scaffold':
        spl = ScaffoldSplitter(save_to=save_split)
    else:
        # TODO: stratidied splitter (normally random split is enough)
        assert molnet_config[name].split == 'stratified'
        spl = RandomSplitter(save_to=save_split)

    split_fn = getattr(spl, split_method)
    if split_method == 'train_valid_test_split':
        train_dataset, valid_dataset, test_dataset = split_fn(whole_dataset, *split, seed=seed)
        if molnet_config[name].task_type == 'classification':
            train_dataset.calc_weight_classification()
        else:
            train_dataset.cal_weight_basic()
        if valid_dataset is not None:
            valid_dataset.cal_weight_basic()
        if test_dataset is not None:
            test_dataset.cal_weight_basic()
        res = (train_dataset, valid_dataset, test_dataset)

    elif split_method == 'train_test_split':
        train_dataset, test_dataset = split_fn(whole_dataset, frac_train=split, seed=seed)
        if molnet_config[name].task_type == 'classification':
            train_dataset.calc_weight_classification()
        else:
            train_dataset.cal_weight_basic()
        if test_dataset is not None:
            test_dataset.cal_weight_basic()
        res = (train_dataset, test_dataset)
    else:
        assert split_method == 'k_fold_split'
        res = split_fn(whole_dataset, k=split, seed=seed)
        for fold in res:
            if molnet_config[name].task_type == 'classification':
                fold.calc_weight_classification()
            else:
                fold.cal_weight_basic()
    return res

