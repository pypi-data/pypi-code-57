#!/usr/bin/python
"""
Name: Rio Atmadja
Date: 11 May 2020
Description: Generic Classifier class
"""
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, roc_curve, confusion_matrix
from sklearn.model_selection import cross_val_score

# Aliases
from typing import List, Dict
from pandas.core.series import Series
from pandas.core.frame import DataFrame
from numpy import ndarray
from ml_engines.utils.constants import DEFAULT_CLF
from ml_engines.utils.ml_tools import get_random_features, train_test, as_character
np.random.seed(10000)

class Classify_ML(object):
    """
    This class is Generic helper classfiersn class
    """

    def __init__(self, clf, clf_name: str, feature_matrix: DataFrame, response_vector: Series, **param_args):
        """
        Once instaniated, this class will fit and split the training and testing data
        :clf: given the classfier
        :clf_name: given the classfier name
        :feature_matrix: given the independent variables
        :response_vector: given the dependent variable
        :param_args: given arbitrary arguments of kwargs optional parameters
        """

        # intantiates arguments
        self.param_args: Dict = param_args
        self.feature_matrix: DataFrame = feature_matrix
        self.response_vector: Series = response_vector
        self.clf = None
        self.feature_names_combinations: List[str] = []
        self.auto_accuracy: List[Dict] = []
        self.df = None
        self.clf_name = clf_name

        if not clf and not clf_name and not feature_matrix and not response_vector:
            raise AttributeError("ERROR: clf, clf_name, feature_matrix, response_vector are required.")

        if clf_name not in DEFAULT_CLF:
            raise ValueError(f"ERROR: available classfier for now {DEFAULT_CLF}")

        # split training and testing data here
        training_testing: Dict = train_test(feature_matrix=self.feature_matrix, response_vector=self.response_vector)

        self.X_train = training_testing.get("X_train")
        self.X_test = training_testing.get("X_test")
        self.y_train = training_testing.get("y_train")
        self.y_test = training_testing.get("y_test")

        self.clf = clf.fit(self.X_train, self.y_train)
        self.clf_original = clf

    def get_clf_name(self) -> str:
        """
        This function will return the classifier name
        :return: a string of classifier name
        """
        return self.clf_name

    def get_prediction_class(self) -> ndarray:
        """
        This function will return the prediction class from the given classfier
        :return: numpy array of the prediction class
        """
        return self.clf.predict(self.X_test)

    def get_predict_probability(self) -> ndarray:
        """
        This function will return all the prediction probabilites
        :return: numpy array of the prediction probabilities
        """
        return self.clf.predict_proba(self.X_test)

    def get_roc_auc_score(self, k_fold: int = np.random.randint(10, 15)) -> float:
        """
        This function calculate the roc_auc score, using cross validations technique.
        With a random kfolds from 10 to 15
        :k_fold: an optional k_fold parameter with an initial value of 10 - 15 k_fold
        :return: a roc_auc score in decimal points
        """
        if not self.is_binary():
            raise TypeError("True values must be in binary formats ")
        return cross_val_score(self.clf,
                               self.X_train,
                               self.y_train, cv=k_fold,
                               scoring="roc_auc").mean()  # Random K-folds 10-15

    def get_prediction_accuracy(self) -> float:
        """
        This function will return the prediction accuracy in decimal points
        :return the prediction accuracy in decimal points
        """
        return accuracy_score(self.get_prediction_class(), self.y_test)

    def get_null_accuracy(self) -> float:
        """
        This function will return the null accuracy from the true value vector
        :y_test: given the true value vector
        :return: the null accuracy from response vector
        """
        if self.param_args.get('binary_clf'):
            return max(self.y_test.mean(), 1 - self.y_test.mean())

        return float(self.y_test.value_counts().head(1) / len(self.y_test))

    def get_roc_curve(self) -> tuple:
        """
        This function will compute the ROC curve
        :return: a tuple that contains True postive, False postive rates and Thresholds
        """

        if not self.is_binary():
            raise TypeError("True values must be in binary formats ")

        fpr, tpr, threshold = roc_curve(self.y_test, self.get_predict_probability()[:, 1])
        return (fpr, tpr, threshold)

    def get_auto_accuracy(self, iteration: int = 1000) -> DataFrame:
        """
        This function will attempt to automatically tune feature matrix and find the best accuracy
        :iteration: an optional parameter with default iteration of 1000
        :return: pandas dataframe
        """

        feature_names: List[str] = self.param_args.get('feature_names')
        for i in range(iteration):
            self.feature_names_combinations.append(get_random_features(feature_enginering=self.param_args.get('feature_enginering') ,
                                                                       feature_names=feature_names))

        for feature in self.unique_feature_names():
            training_testing: Dict = train_test(feature_matrix=self.feature_matrix,
                                                response_vector=self.response_vector)

            X_train = training_testing.get("X_train")
            X_test = training_testing.get("X_test")
            y_train = training_testing.get("y_train")
            y_test = training_testing.get("y_test")

            y_pred_class = self.clf_original.fit(X_train, y_train).predict(X_test)
            results: Dict = self.calculate_cm(cm=confusion_matrix(y_test, y_pred_class), is_cm=True)
            results['features'] = feature
            self.auto_accuracy.append(results)

        self.df = pd.DataFrame.from_dict(self.auto_accuracy)
        return self.df

    def unique_feature_names(self) -> List[List]:
        """
        This function will return unique feature names
        :return: a list of list of unique feature names
        """
        if not self.feature_names_combinations:
            return []

        combination_feature_names: List[str] = sorted(set(list(filter(lambda column_name:
                                                                      column_name if len(column_name) else None,
                                                                      map(lambda features: ','.join(sorted(features)),
                                                                          self.feature_names_combinations)
                                                                      )
                                                               )
                                                          )
                                                      )

        return list(map(lambda feature: feature.split(','), combination_feature_names))

    def is_binary(self) -> bool:
        """
        Helpler function to check, if the true values contains binary response
        :return: a boolean value
        """
        return [0, 1] == sorted(pd.unique(self.y_test.tolist()).tolist())

    def calculate_cm(self, cm: ndarray = None, is_cm: bool = False) -> Dict:
        """

        This function will calculate the following confusion matrix attributes:
        - True Positive
        - True Negative
        - False Positive
        - False Negative
        - Sensitivity
        - Specificity
        - Accuracy
        - Error Rate
        - False Positive Rate
        :cm: an optional confusion matrix parameter, default is None
        :is_cm: an optional flag, set to True. If confusion matrix is provided
        :return: a dictionary of confusion matrix attributes
        """

        if not is_cm:
            cm = confusion_matrix(self.y_test, self.get_prediction_class())
        tp = cm[1][1]
        tn = cm[0][0]
        fp = cm[0][1]
        fn = cm[1][0]

        total: int = tp + tn + fp + fn
        actual_no: int = tn + fp
        actual_yes: int = fn + fp

        return {
            "accuracy": (tp + tn) / total,
            "error_rate": (fp + fn) / total,
            "sensitivity": tp / float(actual_yes),
            "specificity": tn / float(actual_no),
            "false_positve_rate": fp / float(actual_no)
        }
