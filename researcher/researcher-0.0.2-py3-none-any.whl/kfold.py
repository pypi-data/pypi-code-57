import numpy as np

from researcher.assist import *
from torch.utils.data import DataLoader

class KfoldIndexer():
    def __init__(self, folds, base_df):
        self.folds = folds
        self.base_df = base_df
        self.splits = np.array_split(range(len(base_df)), folds)
    
    def get_indices(self, fold):  
        return [idx for ary in self.splits[:fold] + self.splits[fold+1:] for idx in ary], self.splits[fold]

    def all_indices(self):  
        return [idx for ary in self.splits[:] for idx in ary]


class KFoldSplitter(KfoldIndexer):
    def __init__(self, folds, base_df, extract_train=lambda x: x, extract_val=lambda x: x):
        super().__init__(folds, base_df)

        self.extract_train = extract_train
        self.extract_val = extract_val

    def get_dataframe(self, indices, reduce_fn):
        subset = self.base_df.iloc[indices]
        subset.reset_index(drop=True, inplace=True)
        subset = reduce_fn(subset)

        return subset

class KFoldTorchSplit(KFoldSplitter):
    def __init__(self, folds, base_df, cols, batch_size, extract_train=lambda x:x, extract_val=lambda x:x):
        super().__init__(folds, base_df, extract_train=extract_train, extract_val=extract_val)
        
        self.cols = cols
        self.batch_size = batch_size

    def get_loader(self, indices, reduce_fn):
        df = self.get_dataframe(indices, reduce_fn)
        subset = df[self.cols].values
        subset = np.stack([np.stack(subset[i]) for i in range(subset.shape[0])])

        return DataLoader(subset, batch_size=self.batch_size), df

    def get_data(self, fold):
        if fold is None:
            train_indices = self.all_indices()
            train, train_df = self.get_loader(train_indices, self.extract_train)
            return train, None, train_df, None

        train_indices, val_indices = self.get_indices(fold)
        train, train_df = self.get_loader(train_indices, self.extract_train)
        val, val_df = self.get_loader(val_indices, self.extract_val)
        return train, val, train_df, val_df

class KFoldTFSplit(KFoldSplitter):
    def __init__(self, folds, base_df, x_cols, y_cols, extract_train=lambda x:x, extract_val=lambda x:x):
        super().__init__(folds, base_df, extract_train=extract_train, extract_val=extract_val)

        self.x_cols = x_cols
        self.y_cols = y_cols

    def get_xy(self, indices, reduce_fn, shuffle=False):
        subset = self.get_dataframe(indices, reduce_fn)

        if shuffle:
            subset = subset.sample(frac=1)

        X_subset = to_array(subset, self.x_cols)
        y_subset = to_array(subset, self.y_cols)

        return subset, X_subset, y_subset
    
    def get_data(self, fold, shuffle=False):
        train_indices, val_indices = self.get_indices(fold)
        train, X_train, y_train = self.get_xy(train_indices, self.extract_train, shuffle)

        val, X_val, y_val = self.get_xy(val_indices, self.extract_val, shuffle)

        return train, val, X_train, y_train, X_val, y_val

