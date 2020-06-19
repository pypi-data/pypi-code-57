import pandas as pd
import numpy as np
import tensorflow as tf
# import matplotlib.pyplot as plt
# import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

pd.options.mode.chained_assignment = None


class QSAR_Datasets():
    def __init__(self):
        self.pos_uniprot, self.neg_uniport, self.sec_uniprot = self.get_label()
        self.all_secreted_data, self.all_secreted_data_np_padded = self.get_data()
        self.groundtruth = self.construct_groundtruth

    def get_label(self, gdrive_path="/content/drive/Shared drives/Juvena R&D/R&D/Machine Learning/Phase_1_QSAR/data/"):
        pos_uniprot = pd.read_csv(
            gdrive_path+"pos_uniprot.csv", index_col=0)['Uniprot']
        assert("Loaded 'pos_uniprot")
        neg_uniport = pd.read_csv(
            gdrive_path+"neg_uniprot.csv", index_col=0)['Uniprot']
        assert("Loaded 'neg_uniport")
        sec_uniprot = pd.read_csv(
            gdrive_path+"sec_uniprot.csv", index_col=0)['Uniprot']
        assert("Loaded 'sec_uniprot")
        return pos_uniprot, neg_uniport, sec_uniprot

    def get_data(self, gdrive_path="/content/drive/Shared drives/Juvena R&D/R&D/Machine Learning/Phase_1_QSAR/data/"):
        all_secreted_data = pd.read_csv(
            gdrive_path+"all_secreted_data_FM.csv", index_col=0)
        assert("Loaded 'all_secreted_data")
        all_secreted_data_np_padded = np.load(
            gdrive_path+"all_secreted_data_np_padded.npy", allow_pickle=True)
        assert("Loaded 'all_secreted_data_np_padded")
        return all_secreted_data, all_secreted_data_np_padded

    def construct_groundtruth(self):
        ground_truth_label = pd.Series(np.full(
            self.all_secreted_data.shape[0], 0), name='label', index=self.all_secreted_data.index)
        # This is the true positive for myopathy
        ground_truth_label[self.all_secreted_data['Uniprot'].isin(
            self.pos_uniprot)] = 1
        # This is the true negative for myopathy
        ground_truth_label[self.all_secreted_data['Uniprot'].isin(
            self.neg_uniport)] = 2
        assert("Loaded 'ground_truth_label")
        return ground_truth

    def add_poz(self):
        pass

    def add_neg(self):
        pass

    def remove_poz(self):
        pass

    def remove_neg(self):
        pass


def throw_na(df, perc=0.7, na_nine=False):
    """remove columns if na, which include true na and also old fashion na -9999,
     over certain percentage

    :param df: input pandas data.frame
    :type df: data frame
    :param perc: percentage of missing values, defaults to 0.7
    :type perc: float, optional
    :param na_nine: whether using old-fashion na -9999 in data, defaults to False
    :type na_nine: bool, optional
    :return: data frame without na
    :rtype: data frame
    """
    processed_df = None
    if na_nine:
        # if we are dealing with -9999
        for col in df:
            if ((df[col] == -9999).sum() / df.shape[0]) > 0.7:
                df.drop(col, axis=1, inplace=True)
        processed_df = df

    else:
        # gather index for more than a certain percentage NaN
        remove_idx = df.isna().sum()[
            (df.isna().sum() / df.shape[0]) > perc].index

        # drop these columns
        df.drop(remove_idx, axis=1)
        processed_df = df

    return processed_df


def throw_zero(df, perc=0.7):
    """Remove column if zero values over certain percentage

    :param df: input pandas data.frame
    :type df: data frame
    :param perc: percentage of missing values, defaults to 0.7
    :type perc: float, optional
    :return: processed data frame
    :rtype: data frame
    """
    for col in df:
        if ((df[col] == 0).sum() / df.shape[0]) > 0.7:
            print((df[col] == 0).sum())
            df.drop(col, axis=1, inplace=True)
    return df


def remove_inf_fillna(df, stats=None, na_nine=False, train=False, median=False):
    """ removes infinities, replaces with max and min value, and fill Na with stats

    :param df: input pandas data.frame
    :type df: data frame
    :param stats: statistics container have min, max and median of each column,
        defaults to None
    :type stats: data frames
    :param na_nine: whether na is old fashion -9999, defaults to False
    :type na_nine: bool, optional
    :param train: whether is training dataset, defaults to False
    :type train: bool, optional
    :param median: whether fill na with median, defaults to False
    :type median: bool, optional
    :return: processed data frame + stats calculated from training dataset (max,
        min and median)
    :rtype: data frames
    """

    max_val_ = pd.Series(index=df.columns)
    min_val_ = pd.Series(index=df.columns)
    median_ = pd.Series(index=df.columns)
    for col in df:
        if train:
            max_val = df[col][df[col] < np.inf].max()
            min_val = df[col][df[col] > -np.inf].min()
            median = df[col].median()
            max_val_[col] = max_val
            min_val_[col] = min_val
            median_[col] = median

        else:
            max_val = stats['max_val'][col]
            min_val = stats['min_val'][col]
            median = stats['median'][col]
        df[col].replace(np.inf, max_val, inplace=True)
        df[col].replace(-np.inf, min_val, inplace=True)
        if na_nine or median:
            # if we are dealing with -9999
            df[col][df[col] == -9999] = median
            fill_value = median_
        else:
            fill_value = 0
    df.fillna(fill_value, inplace=True)

    if train:
        return df, max_val_, min_val_, median_
    else:
        return df


def remove_outliers(df, stats=None, cutoff_iqr=1.5, train=False):
    """remove outliers using 1.5 inter-quantile

    :param df: input data frame
    :type df: data frame
    :param stats: stats: statistics container have min, max and median of each
        column,, defaults to None
    :type stats: data frame, optional
    :param cutoff_iqr: outlier cutoff param, defaults to 1.5
    :type cutoff_iqr: float, optional
    :param train: whether it's training dataset, defaults to False
    :type train: bool, optional
    :return: processed data frame by removing outliers
    :rtype: [type]
    """
    # Replaces outliers with lower or upper cutoff
    q25_ = pd.Series(index=df.columns)
    q75_ = pd.Series(index=df.columns)
    for col_name in df:
        col = df[col_name]
        if train:
            # calculate interquartile range
            q25, q75 = np.percentile(col, 25), np.percentile(col, 75)
            q25_[col_name] = q25
            q75_[col_name] = q75
        else:
            q25 = stats['q25'][col_name]
            q75 = stats['q75'][col_name]
        iqr = q75 - q25
        # calculate the outlier cutoff
        cut_off = iqr * cutoff_iqr
        lower, upper = q25 - cut_off, q75 + cut_off
        # identify outliers
        col[col < lower] = lower
        col[col > upper] = upper
        df[col_name] = col
    if train:
        return df, q25_, q75_
    else:
        return df


def minmax(df, a=0, b=1, scaler=None, dtype='float32'):
    """min max normalization

    :param df: input data frame
    :type df: data frame
    :param a: low end of scaling range, defaults to 0
    :type a: int, optional
    :param b: high end of scaling range, defaults to 1
    :type b: int, optional
    :param scaler: other type of scaler, defaults to None
    :type scaler: class, optional
    :param dtype: data type, defaults to 'float32'
    :type dtype: str, optional
    :return: normalized data set
    :rtype: [type]
    """
    processed_dat = None
    if scaler is None:
        processed_dat = pd.DataFrame(MinMaxScaler((a, b)).fit_transform(df),
                                     df.columns, dtype=dtype)
    else:
        processed_dat = pd.DataFrame(scaler.transform(df), columns=df.columns,
                                     index=df.index, dtype=dtype)
    return processed_dat


def find_labels(s, cat):
    """ Function that takes in dictionary of categories and classifies rows of \
        series

    :param s: [description]
    :type s: [type]
    :param cat: dictionary of categories
    :type cat: dictionary
    :return: series
    :rtype: pd series
    """

    y = pd.Series(0, index=np.arange(s.shape[0]))
    s = s.str.split()
    for idx, val in enumerate(s):
        if val == val:
            for item in val:
                if item in cat:
                    y.iloc[idx] = item
        else:
            y.iloc[idx] = np.nan
    return pd.Series(y)


def process_prog(df):
    """
    Some features in the bio chemical features file need string processing
    This function takes these columns marked that contain information about prognostics
    It processes the string and makes it into categorical features
    :param df: input data frame for columns containing prognostic features
    :type df: data frame
    :return: [description] Dataframe of processed categorical types
    :rtype: [type] dataframe
    """
    prog = pd.DataFrame()
    for col in df:
        s = df[col].copy()
        s_split = s.str.split()
        # finding two words that should be one
        twowords = set()
        oneword = set()
        for idx, val in enumerate(s_split):
            if val == val:
                for j, item in enumerate(val):
                    if item.isalpha():
                        if val[j + 1].isalpha():
                            oneword.add(val[j] + val[j + 1])
                            twowords.add(val[j] + ' ' + val[j + 1])
        for word, words in zip(oneword, twowords):
            s.replace(words, word, inplace=True, regex=True)
        # finding independent categories
        # finding two words that should be one
        cat = set()
        for idx, val in enumerate(s.str.split()):
            if val == val:
                for item in val:
                    if item.isalpha():
                        cat.add(item)
        prog[col] = find_labels(s, cat)
        prog.index = df.index
    return prog


def fill_missing_one_hot(df, columns):
    """Adding missing columns with zero columns

    :param df: input data frame
    :type df: data frame
    :param columns: column names
    :type columns: list
    :return: data frame with zero columns added.
    :rtype: data frame
    """
    missing_columns = columns[~columns.isin(df.columns)]
    for col in missing_columns:
        df[str(col)] = np.zeros(df.shape[0])
    return df


def create_subcell_df(df):
    """Function that processing cell biology data file
    This function preprocesses the subcellular location feature from cell biology file

    :param df: input cell biology data frame
    :type df: data frame
    :return: sub-cellular location data frame
    :rtype: data frame
    """

    subcell_loc = df['Subcellular.location..CC.']

    # Removing unnecessary string
    subcell_loc = subcell_loc.str.replace('SUBCELLULAR LOCATION: ', '')
    # Removing stirng inside curly braces
    subcell_loc = subcell_loc.str.replace('\{([^}]+)\}', '')
    # subcell_loc = subcell_loc.str.replace('\(([^}]+)\)', '')
    subcell_loc

    category_map = {'nucleus': ['nucleus', 'nuclear', 'chromosome'],
                    'cytoplasm': ['cytoplasm', 'cytosol', 'cytoskeleton'],
                    'extracellular': ['extracellular', 'secreted'],
                    'mitochondria': ['mitochondria', 'mitochondrial',
                                     'mitochondrion'],
                    'cell membrane': ['cell membrane', 'cell  projection'],
                    'endoplasmic reticulum': ['endoplasmic reticulum',
                                              'sarcoplasmic', 'microsome'],
                    'golgi': ['golgi'],
                    'lysosome': ['lysosome'],
                    'peroxisome': ['peroxisome'],
                    'None': []}

    subcell_df = pd.DataFrame(columns=category_map.keys())

    for i, line in subcell_loc.items():
        # iterate over subcellular location cc column
        # Flag to see if at least one location is found
        found = False

        # check if nan
        if line != line:
            subcell_df.loc[i, 'None'] = 1
            continue
        line = line.lower()
        for key, value in category_map.items():
            for sub_string in value:
                if sub_string in line:
                    subcell_df.loc[i, key] = 1
                    found = True
                    break
            if key == 'None' and not found:
                subcell_df.loc[i, 'None'] = 1
                continue
    subcell_df.fillna(0, inplace=True)
    return subcell_df


def reshape(df, features='clean'):
    """This function reshapes the dataframe for input into the autoencoder.
    The padding is required because the autoencoder loses some features when 
        decoding.
    This is because the maxpooling will cut feature length in half, and when 
        there are odd numbers, it wil round up

    :param df: input data frame
    :type df: data frame
    :param features: whether the data frame is cleaned or raw, defaults to 'clean'
    :type features: str, optional
    :raises Exception: Only allow clean and raw as input
    :return: reshaped data frame that can fit into convolutional autoencoder.
    :rtype: data frame
    """

    if features == 'clean':
        # Reshaping array for convolutional autoencoder
        df = np.concatenate(
            [np.zeros((df.shape[0], 53)), df, np.zeros((df.shape[0], 54))], axis=1)
        df = df.reshape(df.shape[0], df.shape[1], 1)
        return df
    else:
        raise Exception('Invalid feature transformation request. Options: \
            "clean", "raw"')
