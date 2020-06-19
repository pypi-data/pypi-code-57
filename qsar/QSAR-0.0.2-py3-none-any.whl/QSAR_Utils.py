from . import QSAR_Dataset

import pandas as pd
import numpy as np
import pickle


def get_stats_file(file_path: str) -> object:
    """Read in statistics learnt during training from local file

    :param file_path: path points to the file location
    :type file_path: str
    :return: stat data frame
    :rtype: object
    """
    stats = pd.read_csv(file_path)
    stats.index = stats[stats.columns[0]]
    stats.drop(stats.columns[0], axis=1)
    return stats


def get_scaler(file_path: str) -> object:
    """Read in scaler
    This function retrieves a min-max scaler object which has been fit on original data

    :param file_path: path points to the file location
    :type file_path: str
    :return: scaler
    :rtype: object
    """
    with open(file_path, 'rb') as input:
        # get minmax scaler
        return pickle.load(input)


def process_ed_csv(data_ed):
    """
    This function takes the evolutionary distance dataframe and processes it
    It fills Nan values with zeros, and removes outliers
    Finally, it scales it and gives the result

    :param data_ed: pandas dataframe for evolutionary distance file
    :return: pandas dataframe for float type, integer type data, and uniprots
    """
    stats_ed = get_stats_file('data/stats/stats_ed.csv')

    # extract uniprot and drop unnecessary names
    uniprot_ed = data_ed["Uniprot"]
    # Dropping name columns
    data_ed = data_ed.drop(data_ed.columns[:3], axis=1)

    # Remove infinity and outliers
    data_ed = QSAR_Dataset.remove_inf_fillna(data_ed, stats=stats_ed)
    data_ed = QSAR_Dataset.remove_outliers(data_ed, stats=stats_ed)

    # Breaking up by datatype to save memory
    ed_flt_columns = pd.read_csv('data/stats/data_ed_flt_columns.csv')
    ed_int_columns = pd.read_csv('data/stats/data_ed_int_columns.csv')
    data_ed_int = data_ed[ed_int_columns.Columns]
    data_ed_flt = data_ed[ed_flt_columns.Columns]

    # Scaling
    scaler_ed_flt = get_scaler('data/stats/scaler_ed_flt.pkl')
    scaler_ed_int = get_scaler('data/stats/scaler_ed_int.pkl')

    data_ed_flt = QSAR_Dataset.minmax(data_ed_flt, scaler=scaler_ed_flt,
                                      dtype='float32')
    data_ed_int = QSAR_Dataset.minmax(data_ed_int, scaler=scaler_ed_int,
                                      dtype='int32')

    return data_ed_flt, data_ed_int, uniprot_ed


def process_phy_csv(data_phy):
    """process biochemical features csv file
    It removes nan values, removes outliers and scales the data
    :param data_phy: dataframe for the bio chemical feature file
    :type data_phy: dataframe
    :return: [description] Pandas dataframe for float type, integer type and 
        uniprots
    :rtype: [type] dataframe, dataframe, series
    """
    uniprot_phy = data_phy['Uniprot']

    # Picking important columns
    columns_phy = pd.read_csv('data/stats/columns_phy.csv')
    data_phy = data_phy[columns_phy['Columns']]

    # processing nans and outliers
    stats_phy = get_stats_file('data/stats/stats_phy.csv')
    data_phy = QSAR_Dataset.remove_inf_fillna(data_phy, stats=stats_phy,
                                              na_nine=True)
    data_phy = QSAR_Dataset.remove_outliers(data_phy, stats=stats_phy)

    columns_phy_flt = pd.read_csv('data/stats/columns_phy_flt.csv')
    columns_phy_int = pd.read_csv('data/stats/columns_phy_int.csv')

    # separating dtypes to save memory
    data_phy_flt = data_phy[columns_phy_flt.Columns]
    data_phy_int = data_phy[columns_phy_int.Columns]

    # scaling
    scaler_phy_flt = get_scaler('data/stats/scaler_phy_flt.pkl')
    scaler_phy_int = get_scaler('data/stats/scaler_phy_int.pkl')
    data_phy_flt = QSAR_Dataset.minmax(data_phy_flt, scaler=scaler_phy_flt,
                                       dtype='float32')
    data_phy_int = QSAR_Dataset.minmax(data_phy_int, scaler=scaler_phy_int,
                                       dtype='int32')

    return data_phy_flt, data_phy_int, uniprot_phy


print('*' * 20)
#####

# EXPRESSION


def process_exp_csv(data_exp):
    """process gene expression csv file
    Takes in the gene expression csv. Removes nan values and outliers
    It also preprocesses the categorical datatypes
    :param data_exp: dataframe for gene expression
    :type data_exp: dataframe
    :return: dataframe for numerical, categorical and then Uniprot
    :rtype: dataframe, dataframe, series
    """
    uniprot_exp = data_exp['Uniprot']

    # Selecting columns
    columns_exp_num = pd.read_csv('data/stats/columns_num_exp.csv')
    data_num = data_exp[columns_exp_num['Columns']]

    # Removing nan and outliers
    stats_exp = get_stats_file('data/stats/stats_exp.csv')
    data_num = QSAR_Dataset.remove_inf_fillna(data_num, stats=stats_exp,
                                              median=True)
    data_num = QSAR_Dataset.remove_outliers(data_num, stats=stats_exp)

    # Scaling
    scaler_exp = get_scaler('data/stats/scaler_exp.pkl')
    data_num = QSAR_Dataset.minmax(data_num, scaler=scaler_exp)

    # Categorical variables
    columns_cat_exp = pd.read_csv('data/stats/columns_cat_exp.csv')
    columns_mixed_exp = pd.read_csv('data/stats/columns_mixed_exp.csv')
    data_exp_cat = data_exp[columns_cat_exp['Columns']]

    # processing mixed variables
    data_exp_mixed = data_exp[columns_mixed_exp['Columns']]
    data_exp_mixed = QSAR_Dataset.process_prog(data_exp_mixed)

    # one hot encoding
    data_exp_cat = pd.get_dummies(data_exp_cat, dtype='int32')
    data_exp_mixed = pd.get_dummies(data_exp_mixed, dtype='int32')

    data_cat = pd.concat([data_exp_cat, data_exp_mixed], axis=1)

    columns_cat_exp_final = pd.read_csv('data/stats/columns_exp_finalcat.csv')
    data_cat = QSAR_Dataset.fill_missing_one_hot(data_cat,
                                                 columns_cat_exp_final['Columns'])

    # Arranging order
    data_cat = data_cat[columns_cat_exp_final['Columns']].astype('int32')

    return data_num, data_cat, uniprot_exp


def process_bio_csv(data_bio):
    """[summary] Processes the cell-biology file
    It extracts the category column and processes it
    :param data_bio: [description] dataframe for the cell-biology file
    :type data_bio: [type] dataframe
    :return: [description] processed, one hot encoded categorical features
    :rtype: [type] dataframe
    """
    uniprot_bio = data_bio['Uniprot']

    # string operations
    data_bio = QSAR_Dataset.create_subcell_df(data_bio)
    data_bio = pd.get_dummies(data_bio)

    columns_bio = pd.read_csv('data/stats/columns_bio.csv')
    data_bio = QSAR_Dataset.fill_missing_one_hot(data_bio,
                                                 columns_bio['Columns'])

    # sort columns
    data_bio = data_bio[columns_bio.Columns].astype('int32')

    return data_bio, uniprot_bio


def find_rows_with_uniprots(path, find_uni):
    """This function picks out only certain Uniprots from a csv
    :param path: path to a csv
    :type path: string
    :param find_uni: A list of Uniprots that we want to find in the csv
    :type find_uni: list
    :return: dataframe that has only the uniprots that we have mentioned
    :rtype: dataframe
    """

    # Count the lines
    num_lines = sum(1 for l in open(path))

    # make indices
    idx = pd.Series(range(1, num_lines))

    # Extract uniprot column
    uniprot = pd.read_csv(path, usecols=['Uniprot'])

    # Skip other rows
    skip_rows = idx[~uniprot['Uniprot'].isin(find_uni)]

    return pd.read_csv(path, skiprows=skip_rows)
