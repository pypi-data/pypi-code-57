import random
from collections import defaultdict

import numpy as np
import pandas as pd

from mdlp.discretization import MDLP
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.exceptions import NotFittedError
from sklearn.utils import check_X_y, check_array
from sklearn.utils.multiclass import unique_labels
from xcs import XCSAlgorithm
from xcs.scenarios import PreClassifiedData, UnclassifiedData

from skxcs.exceptions import NotTransformedError, NotPredictedError


def reward_function(actual, target):
    return float(actual == target)


class XcsClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self,
                 max_population_size=200,
                 learning_rate=.15,
                 accuracy_coefficient=.1,
                 error_threshold=.01,
                 accuracy_power=5,
                 discount_factor=0,
                 ga_threshold=35,
                 crossover_probability=.75,
                 mutation_probability=.03,
                 deletion_threshold=20,
                 fitness_threshold=.1,
                 subsumption_threshold=20,
                 wildcard_probability=.33,
                 initial_prediction=.00001,
                 initial_error=.00001,
                 initial_fitness=.00001,
                 exploration_probability=.5,
                 minimum_actions=None,
                 do_ga_subsumption=False,
                 do_action_set_subsumption=False,
                 random_state=0):

        """ Implementation of a init function for a classifier.

                Parameters
                ----------

                max_population_size : default: 200, range: [1, +inf)

                learning_rate : default: .15, range: (0, 1)

                accuracy_coefficient : default: .1, range: (0, 1]

                error_threshold : default: .01, range: [0, maximum reward]

                accuracy_power : default: 5, range: (0, +inf)

                discount_factor : default: .71, range: [0, 1)

                ga_threshold : default: 35, range: [0, +inf)

                crossover_probability : default: .75, range: [0, 1]

                mutation_probability : default: .03, range: [0, 1]

                deletion_threshold :default: 20, range: [0, +inf)

                fitness_threshold : default: .1, range: [0, 1]

                subsumption_threshold : default: 20, range: [0, +inf)

                wildcard_probability : default: .33, range: [0, 1]

                initial_prediction : default: .00001, range: [0, +inf)

                initial_error : default: .00001, range: (0, +inf)

                initial_fitness : default: .00001, range: (0, +inf)

                exploration_probability : default: .5, range: [0, 1]

                minimum_actions : default: None, range: [1, +inf)

                do_ga_subsumption : default: False, range: {True, False}

                do_action_set_subsumption : default: False, range: {True, False}
        """

        self.max_population_size = max_population_size
        self.learning_rate = learning_rate
        self.accuracy_coefficient = accuracy_coefficient
        self.error_threshold = error_threshold
        self.accuracy_power = accuracy_power
        self.discount_factor = discount_factor
        self.ga_threshold = ga_threshold
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.deletion_threshold = deletion_threshold
        self.fitness_threshold = fitness_threshold
        self.subsumption_threshold = subsumption_threshold
        self.wildcard_probability = wildcard_probability
        self.initial_prediction = initial_prediction
        self.initial_error = initial_error
        self.initial_fitness = initial_fitness
        self.exploration_probability = exploration_probability
        self.minimum_actions = minimum_actions
        self.do_ga_subsumption = do_ga_subsumption
        self.do_action_set_subsumption = do_action_set_subsumption
        self.random_state = random_state

    def _more_tags(self):
        return {
            'non_deterministic': True,
            'poor_score': True,
            'no_validation': True
                }

    def _is_col_binary(self, series):
        unique = sorted(series.unique())
        return unique == [0, 1] or unique == [1] or unique == [0]

    def _is_binary(self, X):
        if isinstance(X, pd.DataFrame):
            for index, series in X.iteritems():
                if not self._is_col_binary(series):
                    return False
        else:
            return np.array_equal(X, X.astype(bool))
        return True

    def fit(self, X, y, index=None, columns=None):

        """ Implementation of a fitting function for a classifier.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values. An array of int.

        index : array of index names

        columns : array of column names

        Returns
        -------
        self : object
            Returns self.
        """

        # Check that X and y have correct shape
        check_X_y(X, y, dtype=None)

        self.model_ = None
        self.classes_ = unique_labels(y)

        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(data=X, columns=columns, index=index)

        self.X_shape_1_ = X.shape[1]

        if not self._is_binary(X):
            X = self.transform_df(X, y=y)

        random.seed(self.random_state)
        algorithm = XCSAlgorithm()

        # For a detailed explanation of each parameter, please see the original
        # paper, "An Algorithmic Description of XCS", by Martin Butz and Stewart Wilson.
        algorithm.max_population_size = self.max_population_size
        algorithm.learning_rate = self.learning_rate
        algorithm.accuracy_coefficient = self.accuracy_coefficient
        algorithm.error_threshold = self.error_threshold
        algorithm.accuracy_power = self.accuracy_power
        algorithm.discount_factor = self.discount_factor
        algorithm.ga_threshold = self.ga_threshold
        algorithm.crossover_probability = self.crossover_probability
        algorithm.mutation_probability = self.mutation_probability
        algorithm.deletion_threshold = self.deletion_threshold
        algorithm.fitness_threshold = self.fitness_threshold
        algorithm.subsumption_threshold = self.subsumption_threshold
        algorithm.wildcard_probability = self.wildcard_probability
        algorithm.initial_prediction = self.initial_prediction
        algorithm.initial_error = self.initial_error
        algorithm.initial_fitness = self.initial_fitness
        algorithm.exploration_probability = self.exploration_probability
        algorithm.minimum_actions = self.minimum_actions
        algorithm.do_ga_subsumption = self.do_ga_subsumption
        algorithm.do_action_set_subsumption = self.do_action_set_subsumption

        self.training_scenario_ = PreClassifiedData(X.to_numpy(), y, reward_function=reward_function)
        self.model_ = algorithm.new_model(self.training_scenario_)
        self.model_.run(self.training_scenario_, learn=True)
        self.model_.algorithm.exploration_probability = 0
        # Return the classifier
        return self

    def predict(self, X):
        """ Implementation of a prediction for a classifier.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        index : array of index names

        columns : array of column names

        Returns
        -------
        y : ndarray, shape (n_samples,)

        """

        if not (hasattr(self, 'model_') and hasattr(self, 'classes_')):
            raise NotFittedError("This {}s instance is not fitted yet. "
                                 "Call 'fit' with appropriate arguments before using this estimator.".format(self))
        random.seed(self.random_state)

        check_array(X, dtype=None)

        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(data=X)

        if self.X_shape_1_ != X.shape[1]:
            raise ValueError("Number of features in fit and predict has to be same. Reshape your data."
                             "Note: Indexes with Nan values are dropped.")

        if self._is_binary(X):
            X = X
        else:
            X = self.transform_df(X)

        testing_scenario = UnclassifiedData(X.to_numpy(), possible_actions=self.training_scenario_.get_possible_actions())
        self.model_.run(testing_scenario, learn=False)

        y = np.array(testing_scenario.get_classifications())

        return y

    def _transform_numerical_data_mdlp(self, X, y=None, min_depth=1, min_split=1e-3):
        frames_list = []
        if y is not None:
            mldp_y, _ = pd.factorize(y)
            transformer = MDLP(min_depth=min_depth, min_split=min_split,
                               random_state=random.seed(self.random_state))
            X_disc = transformer.fit_transform(X, mldp_y)

        for number, column in enumerate(X.iteritems()):
            if y is not None:
                intervals = transformer.cat2intervals(X_disc, number)
                dict_of_dummy_columns: dict = {}
                for interval in set(intervals):
                    col_name = '{}_[{};{})'.format(column[0], round(interval[0], 2), round(interval[1], 2))
                    dict_of_dummy_columns[col_name] = interval

                self.num_col_dict_[column[0]] = dict_of_dummy_columns

            if not hasattr(self, 'num_col_dict_'):
                raise ValueError('Bad input data {}'.format(X))

            num_col_dict = self.num_col_dict_.get(column[0])

            if num_col_dict:
                df = pd.DataFrame(columns=num_col_dict.keys())

                for i, value in enumerate(column[1]):
                    dummy_col = []
                    for k, v in num_col_dict.items():
                        if v[0] <= value < v[1]:
                            dummy_col.append(1)
                        else:
                            dummy_col.append(0)
                    df.loc[i] = dummy_col

                frames_list.append(df)

        result = pd.concat(frames_list, axis=1, sort=False)
        return result

    def transform_df(self, X, y=None, min_depth=1, min_split=1e-3):
        """
        Transform data to binnary using one hot encoding and MDLP discretization algorithm and return
         transformed version.

        Parameters
        ----------
        X : DataFrame or ndarray of shape [n_samples, n_features]
            Training set.

        min_depth : int (default=1)
        Used in MLDP discretization, the minimum depth of the interval splitting.

        min_split : float (default=1e-3)
        Used in MLDP discretization, the minimum size to split a bin.

        y : array like, indicating transformation of training data and used in mldp discretazer, when transforming
              test data y must be None.

        Returns
        -------
        X_new : numpy array of shape [n_samples, n_features_new]
            Transformed array.
        """

        # select numerical and categorical values
        categorical_data = X.select_dtypes(include=[object])
        numerical_data = X.select_dtypes(exclude=[object])
        frames_list = []
        if not hasattr(self, 'num_col_dict_'):
            self.num_col_dict_ = {}

        # one hot encode
        if not categorical_data.empty:
            cat_frame = pd.get_dummies(categorical_data)
            cat_frame.reset_index(inplace=True, drop=True)
            frames_list.append(cat_frame)
        if not numerical_data.empty:
            num_frame = self._transform_numerical_data_mdlp(numerical_data, y=y, min_depth=min_depth, min_split=min_split)

            frames_list.append(num_frame)

        if frames_list:
            frames = pd.concat(frames_list, axis=1, sort=False)

            if y is not None:
                self.train_column_names_ = list(frames)
            else:
                if not hasattr(self, 'train_column_names_'):
                    raise NotTransformedError("This {}s instance has to transform TRAINING data first. "
                                              "Call 'transform_df' with appropriate arguments.".format(self))
                test_column_names = list(frames)
                for col_name in self.train_column_names_:
                    if col_name not in frames.columns:
                        frames[col_name] = 0

                for col_name in test_column_names:
                    if col_name not in self.train_column_names_:
                        frames = frames.drop(columns=col_name)

            return frames
        else:
            ValueError("'X' must not be empty.")

    def pretty_print_prediction(self, X):
        """ Implementation of a pretty print of prediction. Returns an original testing dataframe with appended
        prediction labeled 'y'.
        Instance of classifier has to predict and transform data first.

        Returns
        -------
        X : DataFrame, shape (n_features, n_samples)
        """

        y = self.predict(X)

        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(data=X)

        X['y'] = y

        return X

    def get_rules(self):
        """
        Method returning a list of binary rules formed by classifier. Condition is represented by a binary row
        representing row in initial, non binary data.  Classifier has to be fitted first.

        :return:
        List of strings representing rules in format:
        condition => action [fitness]
        Example:
        10101010110001 => 1 [81.7]
        """
        if not (hasattr(self, 'model_') and hasattr(self, 'classes_')):
            raise NotFittedError("This {}s instance is not fitted yet. "
                                 "Call 'fit' with appropriate arguments before calling 'get_rules'.".format(self))

        return ['{} => {} {} {}'.format(rule.condition, rule.action, '[%.5f]' % rule.fitness, rule.experience) for rule in self.model_]

    def get_condition_str(self, condition):
        var_names = list(
            set(
                col_name[:col_name.rfind('_')] for col_name in self.train_column_names_
            )
        )
        vars_dict = {}
        for v in var_names:
            vars_dict[v] = {1: [], 0: []}

        final_rule_list = []

        for num, bit in enumerate(list(condition)):
            col_name = self.train_column_names_[num]
            underscore_index = col_name.find('_')
            var = col_name[:underscore_index]
            value = col_name[underscore_index + 1:]
            if bit == 1 or bit ==0:
                v_dict = vars_dict[var]
                v_list = v_dict[bit]
                v_list.append('{}{}={}'.format(var, '!' if bit == 0 else '', value))

        for variable in vars_dict.values():
            if variable[1]:
                list_to_add = variable[1]
                final_rule_list += list_to_add
            elif variable[0]:
                list_to_add = variable[0]
                final_rule_list += list_to_add

        return ', '.join(final_rule_list)

    def get_pretty_rules(self):
        if not (hasattr(self, 'model_') and hasattr(self, 'classes_')):
            raise NotFittedError("This {}s instance is not fitted yet. "
                                 "Call 'fit' with appropriate arguments "
                                 "before calling 'get_rules'.".format(self))

        if not hasattr(self, 'train_column_names_'):
            raise NotTransformedError("This {}s instance has to transform "
                                      "TRAINING data first. "
                                      "Call 'transform_df' with appropriate arguments,"
                                      " before calling 'get_pretty_rules'".format(self))
        rules = []
        for rule in self.model_:
            con_str = self.get_condition_str(rule.condition)
            rules.append('{} => Class={}'.format(con_str, rule.action))

        return rules

    def get_full_rules(self):
        """
        Method returning a list of rules of type XCSClassifierRule. For more information read XCSClassifierRule
        documentation. Classifier has to be fitted first.
        :return:
        List of rules of type XCSClassifierRule.
        """
        if not (hasattr(self, 'model_') and hasattr(self, 'classes_')):
            raise NotFittedError("This {}s instance is not fitted yet. "
                                 "Call 'fit' with appropriate arguments before  calling 'get_full_rules'.".format(self))

        return [rule for rule in self.model_]

    def get_antlength(self):
        var_names = list(
            set(
                col_name[:col_name.rfind('_')]
                for col_name in self.train_column_names_
            )
        )
        num_of_rules = 0

        for rule in self.model_:
            rules = {}
            for v in var_names:
                rules[v] = []

            for num, bit in enumerate(list(rule.condition)):
                col_name = self.train_column_names_[num]
                var = col_name[:col_name.rfind('_')]
                if bit == 1 or bit == 0:
                    var_list = rules[var]
                    var_list.append(bit)

            for var_bits in rules.values():
                if 1 in var_bits:
                    num_of_rules += 1
                else:
                    for b in var_bits:
                        if b == 0:
                            num_of_rules += 1

        return num_of_rules/len(self.model_)
