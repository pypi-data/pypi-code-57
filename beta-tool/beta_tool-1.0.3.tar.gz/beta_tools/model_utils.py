#!/usr/bin/env python
# coding: utf-8

# @Author: dehong
# @Date: 2020-05-27
# @Time: 16:52
# @Name: model_utils
import bisect
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import logging
import traceback
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import numpy as np


def delete_feature(data, features):
    """
    删除特征
    :param data:
    :param features:
    :return:
    """
    try:
        for feature in features:
            del data[feature]
    except Exception:
        print('删除特征错误:::%s', feature)
    return data


def feature_str(data, features):
    """
    特征转 str
    :param data:
    :param features:
    :return:
    """
    try:
        for feature in features:
            data[feature] = data[feature].astype('str')
    except Exception:
        print('特征转 str错误:::%s', feature)
    return data


def encoder_train(data, features, model_save_path='/socrates_data/model_file/', path=None):
    """
    类别特征 encoder 编码
    :param model_save_path:
    :param data:
    :param features:
    :param path:
    :return:
    """
    lab = LabelEncoder()
    for feature in features:
        lab.fit(data[feature])
        data[feature] = lab.transform(data[feature])
        tmp_path = model_save_path + path + '_' + feature + '.pkl'
        try:
            joblib.dump(lab, tmp_path)
            logging.info('保存特征模型文件:%s', tmp_path)
        except Exception:
            logging.info(traceback.format_exc())
            logging.info('保存特征模型文件错误:%s', tmp_path)
    return data


def encoder_prediction(data, features, model_save_path='/socrates_data/model_file/',  path=None):
    """
    类别特征 encoder 编码
    :param model_save_path:
    :param data:
    :param features:
    :param path:
    :return:
    """
    lab = LabelEncoder()
    for feature in features:
        try:
            tmp_path = model_save_path + path + '_' + feature + '.pkl'
            lab = joblib.load(tmp_path)
            logging.info('加载特征模型文件:%s', tmp_path)

            data[feature] = data[feature].map(lambda x: 'other' if x not in lab.classes_ else x)
            lab_classes = lab.classes_.tolist()
            bisect.insort_left(lab_classes, 'other')
            lab.classes_ = lab_classes

            data[feature] = lab.transform(data[feature])
        except Exception:
            logging.info(traceback.format_exc())
            logging.info('加载特征模型文件错误:%s', tmp_path)
    return data


def label_encoder(data, prediction_id, model_type, categorical_feature):
    data.app_version.fillna(data.app_version.mode()[0], inplace=True)
    data.device_mode.fillna(data.device_mode.mode()[0], inplace=True)
    data.country_id.fillna(data.country_id.mode()[0], inplace=True)
    data.campaign_id.fillna('normal', inplace=True)
    data.material_id.fillna('normal', inplace=True)
    data.campaign_country.fillna('normal', inplace=True)
    data.campaign_name.fillna('normal', inplace=True)
    data.campaign_type.fillna('normal', inplace=True)

    if model_type == 'train':
        data = encoder_train(data, categorical_feature, prediction_id)
    elif model_type == 'predict':
        data = encoder_prediction(data, categorical_feature, prediction_id)

    return data


def regression_model_evalution_campaign(test_X, test_Y, model):
    campaign_ids = test_X.campaign_id.value_counts()
    f = 0
    t = 0
    for index, value in campaign_ids.iteritems():
        if value > 50:
            x = test_X[test_X.campaign_id == index]
            y = test_Y[x.index]
            y_ = model.predict(x)
            len(y_)
            real = y.sum() / len(y)
            pred = y_.sum() / len(y_)
            result = abs(pred - real) / real
            if result > 0.05:
                f = f + 1
                logging.info('False: %d', f)
            else:
                t = t + 1
                logging.info('True: %d', t)


def classifier_gbdt(train_X, train_Y, test_X, threshold=0.5):
    X_train, X_eval, y_train, y_eval = train_test_split(train_X, train_Y, test_size=0.2, random_state=0)
    model = GradientBoostingClassifier(n_estimators=100, max_depth=2)
    model.fit(X_train, y_train)

    y_eval_pred = model.predict_proba(X_eval)[:, 1]
    y_eval_pred = pd.Series(y_eval_pred).map(lambda x: 1 if x >= threshold else 0)

    y_pred = model.predict_proba(test_X)[:, 1]
    y_pred = pd.Series(y_pred).map(lambda x: 1 if x >= threshold else 0)

    logging.info(model.score(X_train, y_train))
    logging.info(model.score(X_eval, y_eval))
    logging.info('confusion_matrix:\n %s', confusion_matrix(y_eval, y_eval_pred))
    logging.info('classification_report:\n %s', classification_report(y_eval, y_eval_pred))
    feature_importance = pd.Series(model.feature_importances_, name='feature_importance',
                                   index=train_X.columns).sort_values(ascending=False)
    feature_importance = feature_importance / feature_importance.sum()
    logging.info(feature_importance)

    return model, y_pred


def get_grouped_data(input_data, feature, target_col, bins, cuts=0):
    has_null = pd.isnull(input_data[feature]).sum() > 0
    if has_null == 1:
        data_null = input_data[pd.isnull(input_data[feature])]
        input_data = input_data[~pd.isnull(input_data[feature])]
        input_data.reset_index(inplace=True, drop=True)

    is_train = 0
    if cuts == 0:
        is_train = 1
        prev_cut = min(input_data[feature]) - 1
        cuts = [prev_cut]
        reduced_cuts = 0
        for i in range(1, bins + 1):
            next_cut = np.percentile(input_data[feature], i * 100 / bins)
            if next_cut != prev_cut:
                cuts.append(next_cut)
            else:
                reduced_cuts = reduced_cuts + 1
            prev_cut = next_cut
        cut_series = pd.cut(input_data[feature], cuts)
    else:
        cut_series = pd.cut(input_data[feature], cuts)

    grouped = input_data.groupby([cut_series], as_index=True).agg(
        {target_col: [np.size, np.mean], feature: [np.mean]})
    grouped.columns = ['_'.join(cols).strip() for cols in grouped.columns.values]
    grouped[grouped.index.name] = grouped.index
    grouped.reset_index(inplace=True, drop=True)
    grouped = grouped[[feature] + list(grouped.columns[0:3])]
    grouped = grouped.rename(index=str, columns={target_col + '_size': 'Samples_in_bin'})
    grouped = grouped.reset_index(drop=True)
    corrected_bin_name = '[' + str(min(input_data[feature])) + ', ' + str(grouped.loc[0, feature]).split(',')[1]
    grouped[feature] = grouped[feature].astype('category')
    grouped[feature] = grouped[feature].cat.add_categories(corrected_bin_name)
    grouped.loc[0, feature] = corrected_bin_name

    if has_null == 1:
        grouped_null = grouped.loc[0:0, :].copy()
        grouped_null[feature] = grouped_null[feature].astype('category')
        grouped_null[feature] = grouped_null[feature].cat.add_categories('Nulls')
        grouped_null.loc[0, feature] = 'Nulls'
        grouped_null.loc[0, 'Samples_in_bin'] = len(data_null)
        grouped_null.loc[0, target_col + '_mean'] = data_null[target_col].mean()
        grouped_null.loc[0, feature + '_mean'] = np.nan
        grouped[feature] = grouped[feature].astype('str')
        grouped = pd.concat([grouped_null, grouped], axis=0)
        grouped.reset_index(inplace=True, drop=True)

    grouped[feature] = grouped[feature].astype('str').astype('category')
    if is_train == 1:
        return (cuts, grouped)
    else:
        return (grouped)
