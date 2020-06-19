#!/usr/bin/env python
from ml_engines.supervised.classfication import Classify_ML
from ml_engines.utils.ml_tools import get_dimensions
from sklearn.linear_model import LogisticRegression
from typing import List
from unittest import TestCase
import numpy as np
import pandas as pd
np.random.seed(1000)

# Test datasets
loan = pd.DataFrame( np.random.randint(0, 2, size=(1000, 3)), columns=['Maritial Status',  'Gender', 'Employemeent'])
loan['Income'] = np.random.randint(30000, 120000, size=(1000, 1))
loan['Age'] = np.random.randint(18, 75, size=(1000, 1))
loan['Educations'] = np.random.randint(0, 7, size=(1000, 1))
loan['Number of Pervious Loans'] = np.random.randint(1, 8, size=(1000, 1))
loan['Loan Status'] = np.random.randint(0, 2, size=(1000, 1))
loan.index = np.arange(1, len(loan) + 1)

feature_names: List[str] = loan.columns.tolist()
feature_matrix: List[str] = loan.columns.tolist()[0:-1]
clf = Classify_ML(clf=LogisticRegression(C=1e9), clf_name='logreg',
                  feature_matrix=loan[feature_matrix[0:2]],
                  response_vector=loan['Loan Status'],
                  binary_clf=True,
                  feature_enginering=True,
                  feature_names=feature_names)

class TestClassification(TestCase):

    def test_dataframe_test(self):
        """
        Initial tests
        :return:
        """
        dimension: tuple = get_dimensions(loan)
        return self.assertEqual((1000, 8), dimension)



