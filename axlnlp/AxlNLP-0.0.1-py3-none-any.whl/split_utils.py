import os
from am import get_logger
from sklearn.model_selection import KFold
import numpy as np
logger = get_logger(__name__)


class SplitUtils:
    

    def _split_data(self):
        if self._n_folds:
            return self.__n_fold_splits()
        else:
            raise NotImplementedError("No Alternative to creating cv splits currently exist..")


    def __n_fold_splits(self):

        pkl_splits_file = f"datasets/{self.name}/splits.pkl"
        logger.info(f"Will create cross validation splits for {self.name}. Save to {pkl_splits_file}")

        #splits
        if os.path.exists(pkl_splits_file):
            logger.info(f"Loading premade splits from {pkl_splits_file}")
            split_ids = u.load_pickle_data(pkl_splits_file)

            if len(split_ids) != n_folds:
                logger.warning("Nr of folds in loaded premade splits do not match given number of splits. Will use nr premade splits.")
        else:
            split_ids = self.__cv_split_data()
            u.pickle_data(split_ids, pkl_splits_file)

        return split_ids


    def __cv_split_data(self):
        logger.info(f"Splitting Data into {self.n_folds} folds ... ")
        kf = KFold(n_splits=self.n_folds, random_state=666, shuffle=True)
        split_idxes = kf.split(np.zeros(len(self)))

        # the shuffle from KFold is not good enough as it randomly
        # picks test samples from the set but does not shuffle the set..
        # to ensure nice shuffle, we just shuffle 'em again!
        splits = []
        for (i,train, dev) in enumerate(split_idxes):
            np.random.shuffle(train)
            np.random.shuffle(dev)
            splits = (i, train, dev)

        return splits