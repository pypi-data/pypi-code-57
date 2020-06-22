##
# Copyright 2020 Atos Spain SA. All rights reserved.
#
# This file is part of EASIER.AI.
#
# EASIER.AI is free software: you can redistribute it and/or modify it under the terms of GNU Affero General 
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# See DISCLAIMER file for the full disclaimer information and LICENSE file for full license information 
# in the project root.
##

import tensorflow as tf
from tensorflow.keras import callbacks
from tensorflow.keras import backend as K
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

# import pandas
import modin.pandas as pandas

import datetime as dt
import threading
import sys
import numpy as np
import os
import time as time_lib
import pydash as _

from minio import Minio

import common_functions.helpers as helpers
import common_functions.constants as constants
from common_functions.logger import Logger
import elasticsearchlib.elastic_queries as queries
from elasticsearchlib.elasticsearchlib import Elasticsearchlib
from elasticsearchlib import elastic_mappings

import warnings
warnings.filterwarnings("ignore")

class Trainer:

    def __init__(self, config_file_path=None, connection_params=None, classifier=False, eslib=None):
        """
            You should either pass a path to a config file in config_file_path, or the dictionary
            in connection_params with the endpoints, ports and passwords for elasticsearch and minio.
            Parameters
            ----------
            connection_params : dict containing
                minio_host : IP/hostname
                minio_port : port
                minio_access : minio access key
                minio_secret : minio secret key
                elasticsearch_host : IP/hostname
                elasticsearch_port : port   
                elasticsearch_username : username,
                elasticsearch_password : password
        """
        os.system("mkdir ./logs")
        os.system("mkdir ./storage")
        
        if config_file_path is None:
            self.initialize(connection_params, classifier=classifier)
        else:
            self.initialize_config(connection_params, config_file_path, classifier=classifier, eslib=eslib)

    def initialize_config(self, connection_params, config_file_path="./config.ini", eslib=None, classifier=False):
        self.logger = Logger('trainer', os.path.basename(__file__))
        helpers._logger = Logger('helpers', 'helpers.py')

        # Config
        helpers.config = helpers.read_config_file(config_file_path)
        self.config = helpers.config

        if connection_params["elasticsearch_host"]:
            elasticsearch_host = connection_params["elasticsearch_host"]
        else:
            elasticsearch_host = helpers.config['ELK']["elastic_host"] 
        if connection_params["elasticsearch_port"]:
            elasticsearch_port = connection_params["elasticsearch_port"]
        else:
            elasticsearch_port = helpers.config['ELK']["elastic_port"] 

        if connection_params["elasticsearch_password"]:
            elasticsearch_password = connection_params["elasticsearch_password"]
        else:
            elasticsearch_password = None
        if connection_params["elasticsearch_username"]:
            elasticsearch_username = connection_params["elasticsearch_username"]
        else:
            elasticsearch_username = None
            
        if connection_params["minio_host"]:
            minio_host = connection_params["minio_host"]
        else:
            minio_host = helpers.config['MINIO']["minio_host"]
        if connection_params["minio_port"]:
            minio_port = connection_params["minio_port"]
        else:
            minio_port = helpers.config['MINIO']["minio_port"]
        if connection_params["minio_access"]:
            minio_access = connection_params["minio_access"]
        else:
            minio_access = helpers.config['MINIO']["minio_access"]
        if connection_params["minio_secret"]:
            minio_secret = connection_params["minio_secret"]
        else:
            minio_secret = helpers.config['MINIO']["minio_secret"]

        timeout = os.getenv('TIMEOUT', 30)

        # MINIO
        try:
            helpers.minioClient = Minio(minio_host + ':' + minio_port, minio_access, minio_secret, secure=False)
        except Exception as e:
            self.logger.error('Error on connecting to MINIO. Exiting program...')
            sys.exit(1)

        # Elasticsearch
        if eslib is None:
            eslib = Elasticsearchlib(Logger('elasticsearchlib', 'elasticsearchlib.py'))
            if elasticsearch_password and elasticsearch_username:
                self.logger.debug("Secured elasticsearch connection")
                ok, _es = eslib.start_connection_secure(elasticsearch_host, elasticsearch_port, elasticsearch_username, elasticsearch_password)
            else:
                ok, _es = eslib.start_connection(elasticsearch_host, elasticsearch_port)
            if not ok:
                self.logger.error('Error on connecting to elasticsearch - check elasticsearch logs')
                sys.exit(1)
            # Create indices (if not available)
            index_models = os.getenv('TRAINING_RESULTS_ID', helpers.config['ELASTIC']['index_models'])
            ok = eslib.create_index(index_models, elastic_mappings.model_mapping)
            if not ok:
                self.logger.error('Error creating models mapping on elasticsearch - check elasticsearch logs')
                sys.exit(1)
        self.eslib = eslib

        # ML libraries parameters import
        self.algorithm = self.config['ML']['algorithm']
        if self.algorithm == constants.LSTM or self.algorithm == constants.PHASED_LSTM:
            self.inner_activation = 'tanh'
            self.ft_range = (-1 ,1)
        else:
            self.inner_activation = constants.RELU
            self.ft_range = (0,1)
            
        # Imported ML class
        if classifier:
            self.pred = helpers.importer(self.algorithm, inference_type=constants.CLASSIFIER, 
            lr=float(self.config['ML']['learning_rate']))
        else:
            self.pred = helpers.importer(self.algorithm, inference_type=constants.ESTIMATOR, 
                lr=float(self.config['ML']['learning_rate']))
        
        # General parameters
        self.data_type = self.config['INFERENCE']['data_type']

        if self.data_type == constants.TIMESERIES:
            self.num_previous_measures = int(self.config['INFERENCE']['num_previous_measures'])
            self.num_forecasts = int(self.config['INFERENCE']['num_forecasts'])
        else:
            self.num_previous_measures = 0
            self.num_forecasts = 1

        self.num_features_dataset = 0
        self.num_inference_features = 0
        self.classes = None

        self.scaler = None
        self.one_hot_encoder = None
        self.label_encoder = None

        self.epoch_external = int(self.config['ML']['epoch_external'])
        self.epoch_internal = int(self.config['ML']['epoch_internal'])
        self.batch_size = int(self.config['ML']['batch_size'])
        self.initial_validation_split = float(self.config['ML']['initial_validation_split'])
        self.validation_split_multiplayer = float(self.config['ML']['validation_split_multiplayer'])

        self.keras_callbacks = [
            callbacks.EarlyStopping(monitor=constants.VAL_LOSS, min_delta=0, patience=10, verbose=0, mode='auto', baseline=None), 
            callbacks.TensorBoard(log_dir="../logs/TensorBoard/{}".format(time_lib.time()), write_images=True)]

        self.model_train = None

        self.finished = True

        self._active_timer = None

        self.time_index = self.config['DATA']['time_index'].replace(" ", "")

        self.time_window_to = self.config['ML']['time_window_to']
        self.time_window_from = self.config['ML']['time_window_from']

        self.delta_max_std = self.config['ML']['delta_max_std']
        self.resample_time = self.config['ML']['resample_time']
        self.resample = self.config['ML']['resample']

        try:
            self.class_name = self.config['DATA']['class_name']
        except Exception as e:
            self.class_name = "class"

        self.training_ratio = self.config['ML']['training_ratio']
        self.batch_size_multiplier = self.config['ML']['batch_size_multiplier']

    def initialize(self, connection_params, classifier=False):
        elasticsearch_host = connection_params["elasticsearch_host"] 
        elasticsearch_port = connection_params["elasticsearch_port"]
        minio_host = connection_params["minio_host"]
        minio_port = connection_params["minio_port"]
        minio_access = connection_params["minio_access"]
        minio_secret = connection_params["minio_secret"]
        if connection_params["elasticsearch_password"]:
            elasticsearch_password = connection_params["elasticsearch_password"]
        else:
            elasticsearch_password = None
            
        if connection_params["elasticsearch_username"]:
            elasticsearch_username = connection_params["elasticsearch_username"]
        else: 
            elasticsearch_username = None
        try:
            index_models = connection_params["index_models"]
        except Exception as e:
            index_models = os.getenv('TRAINING_RESULTS_ID', "models-" + str(int(time_lib.time())))

        # Logger
        helpers._logger = Logger('helpers', 'helpers.py')
        self.logger = Logger('trainer', os.path.basename(__file__))

        # MINIO
        helpers.minioClient = Minio(minio_host + ':' + minio_port, minio_access, minio_secret, secure=False)

        # Elasticsearch library
        self.eslib = Elasticsearchlib(Logger('elasticsearchlib', 'elasticsearchlib.py'))
        if elasticsearch_password and elasticsearch_username:
            self.logger.debug("Secured elasticsearch connection")
            ok, _es = eslib.start_connection_secure(elasticsearch_host, elasticsearch_port, elasticsearch_username, elasticsearch_password)
        else:
            ok, _es = self.eslib.start_connection(elasticsearch_host, elasticsearch_port)

        if not ok:
            self.logger.error('Error on connecting to elasticsearch - check elasticsearch logs')
            sys.exit(1)

        # Create indices (if not available)        
        ok = self.eslib.create_index(index_models, elastic_mappings.model_mapping)
        if not ok:
            self.logger.error('Error creating models mapping on elasticsearch - check elasticsearch logs')
            sys.exit(1)

        # ML libraries parameters import
        self.algorithm = constants.DENSE
        if self.algorithm == constants.LSTM or self.algorithm == constants.PHASED_LSTM:
            self.inner_activation = 'tanh'
            self.ft_range = (-1 ,1)
        else:
            self.inner_activation = constants.RELU
            self.ft_range = (0,1)
            
        # Imported ML class
        if classifier:
            self.pred = helpers.importer(self.algorithm, inference_type=constants.CLASSIFIER, 
                lr=0.01)
        else:
            self.pred = helpers.importer(self.algorithm, inference_type=constants.ESTIMATOR, 
                lr=0.01)
                
        # General parameters
        self.data_type = "normal"

        if self.data_type == constants.TIMESERIES:
            self.num_previous_measures = 100
            self.num_forecasts = 4
        else:
            self.num_previous_measures = 0
            self.num_forecasts = 1

        self.num_features_dataset = 0
        self.num_inference_features = 0
        self.classes = None

        self.scaler = None
        self.one_hot_encoder = None
        self.label_encoder = None

        self.epoch_external = 1
        self.epoch_internal = 50
        self.batch_size = 200
        self.initial_validation_split = 0.1
        self.validation_split_multiplayer = 1.75
        self.batch_size_multiplier = 1.5
        self.training_ratio = 0.8

        self.keras_callbacks = [
            callbacks.EarlyStopping(monitor=constants.VAL_LOSS, min_delta=0, patience=10, verbose=0, mode='auto', baseline=None), 
            callbacks.TensorBoard(log_dir="../logs/TensorBoard/{}".format(time_lib.time()), write_images=True)]

        self.model_train = None

        self.finished = True

        self._active_timer = None

        self.time_index = "timestamp"

        self.time_window_to = "1w"
        self.time_window_from = "now"

        self.delta_max_std = 300
        self.resample_time = 300
        self.resample = "no"

        self.class_name = "class"

        self.initial_train = True
        self.time_window_to_initial = "2y"
        
    def set_algorithm(self, algorithm, learning_rate=0.01, classifier=False):
        # ML libraries parameters import
        self.algorithm = algorithm
        if self.algorithm == constants.LSTM or self.algorithm == constants.PHASED_LSTM:
            self.inner_activation = 'tanh'
            self.ft_range = (-1 ,1)
        else:
            self.inner_activation = constants.RELU
            self.ft_range = (0,1)
            
        # Imported ML class
        if classifier:
            self.pred = helpers.importer(self.algorithm, inference_type=constants.CLASSIFIER, 
                lr=float(learning_rate))
        else:
            self.pred = helpers.importer(self.algorithm, inference_type=constants.ESTIMATOR, 
                lr=float(learning_rate))

    def set_data_type(self, data_type, classifier=False):
        self.data_type = data_type

        if self.data_type == constants.TIMESERIES:
            self.num_previous_measures = 100
            self.num_forecasts = 4
        else:
            self.num_previous_measures = 0
            self.num_forecasts = 1

    def get_dataset_from_docs(self, result):
        """
            @param result: dict resulting from an elasticsearch query res['hits']['hits']
        """
        data_list = []
        for entry in result:
            data = pandas.DataFrame([entry['_source']]).apply(pandas.to_numeric, errors='ignore', 
                                    axis=0, raw=True)
            data_list.append(data)
            
        dataset = pandas.concat(data_list)
        return dataset
    
    def extract_data_from_elk(self, entity, index_data, time_window_to=None, data_size=np.inf, query_size=2000):
        """
        Extract data from elasticsearch using scroll API if necessary.

        Parameters
        ----------
        entity : Can be None to take all ids. id of the entity/id in the field 'id' to filter in index_data. 
        index_data : index to query data in elasticsearch
        time_window_to : if there is a timestamp field, this field corresponds to the limit date to get data back from.
        data_size : Max number of elements to extract. Defaults to infinite. 
        query_size : If data_size is bigger than query_size, this call will split the extraction in several queries. This parameter stands for the max number of elements to extract in each query to elasticsearch.
        """
        if data_size < query_size:
            query_size = data_size

        if time_window_to is None:
            time_window_to = self.time_window_to

        if entity is not None and entity != index_data:
            if self.time_index != '':
                extraction_start_time = time_lib.clock()
                ok, aux = self.eslib.get_data_history(index_data, entity,
                                                self.time_window_from + '-' + time_window_to + '/d',
                                                self.time_window_from + '/d')
                extraction_end_time = time_lib.clock() 

                if not ok:                                    
                    self.logger.error('Error on extracting data from elasticsearch for: ' + str(entity))    
                    df = pandas.DataFrame()
                
                preprocess_start_time = extraction_end_time
                if len(aux) > data_size:
                    aux = aux[:data_size]
                
                return pandas.DataFrame(aux).apply(pandas.to_numeric, errors='ignore', axis=0, raw=True), extraction_end_time-extraction_start_time, preprocess_start_time
            else:
                extraction_start_time = time_lib.clock()
                ok, aux = self.eslib.scrolled_query(queries.query_by_id(entity), index_data, query_size=query_size,
                 max_size=data_size) 
                extraction_end_time = time_lib.clock() 

                if not ok:                                    
                    self.logger.error('Error on getting all data from docs from elasticsearch for: ' + str(entity))    
                    return pandas.DataFrame()

                preprocess_start_time = extraction_end_time
                aux = _.collections.map_(aux, lambda x: x['_source'])
                if len(aux) > data_size:
                    aux = aux[:data_size]
                
                return pandas.DataFrame(aux).apply(pandas.to_numeric, errors='ignore', axis=0, raw=True), extraction_end_time-extraction_start_time, preprocess_start_time
        else:
            extraction_start_time = time_lib.clock()    
            ok, aux = self.eslib.scrolled_query(queries.QUERY_ALL, index_data, query_size=query_size, max_size=data_size) 
            extraction_end_time = time_lib.clock() 

            if not ok:                                    
                self.logger.error('Error on getting all data from docs from elasticsearch for: ' + str(entity))    
                return pandas.DataFrame()

            preprocess_start_time = extraction_end_time
            aux = _.collections.map_(aux, lambda x: x['_source'])
            if len(aux) > data_size:
                aux = aux[:data_size]
                
            return pandas.DataFrame(aux).apply(pandas.to_numeric, errors='ignore', axis=0, raw=True), extraction_end_time-extraction_start_time, preprocess_start_time

            # for ok, aux in self.eslib.scrolled_query_generator(queries.QUERY_ALL, index_data, query_size=self.batch_size): 
            #     if not ok:                                    
            #         self.logger.error('Error on getting all data from docs from elasticsearch for: ' + str(entity))    
            #         df = pandas.DataFrame()
            #         break                                          
                
            #     yield self.get_dataset_from_docs(aux)

            # return df

    def series_to_supervised(self, data, n_in=1, n_out=1, dropnan=True):
        """
            Convert series to supervised learning (source: 
            https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/)
        """

        n_vars = 1 if type(data) is list else data.shape[1]
        # n_vars = 1
        df = pandas.DataFrame(data)

        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(df.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
        # put it all together
        agg = pandas.concat(cols, axis=1)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
            agg.dropna(inplace=True)
        return agg

    def set_up_timeseries_data(self, df, dataset_features, inference_features=None, classifier=False):
        """
            Prepares dataframe as a timeseries to be trained selecting the columns from the features 
            configuration/parameters.
            If we have time series data, features to be inferenced are considered for training.
            We use a time index.
        """
        self.num_features_dataset = 0
        self.num_inference_features = 0
        
        features = []
        features_df = df.columns.tolist()
        
        for dataset_feature in dataset_features:
            if dataset_feature in features_df:
                features = _.concat(features, dataset_feature)
                self.num_features_dataset += 1
            else:
                self.logger.error("Feature '" + str(dataset_feature) + "' was not found in dataset features (" + str(features_df) + "). It will be ignored.")
        
        if self.num_features_dataset == 0:
            self.logger.error("You must specify at least one feature in 'input_features' parameter.")
            sys.exit(1)

        if not classifier:
            for inference_feature in inference_features:
                if inference_feature in features_df:
                    features = _.concat(features, inference_feature)
                    self.num_inference_features += 1
                else:
                    self.logger.error("Feature '" + str(inference_feature) + "' was not found in dataset features (" + str(features_df) + "). It will be ignored.")
            
            if self.num_inference_features == 0:
                self.logger.error("You must specify at least one feature in 'prediction_features' parameter.")
                sys.exit(1)

        features = _.concat(self.time_index, features)

        df = df[features]
        
        # In modin, next operations throw an error in index is not set
        df = df.set_index(self.time_index)
        
        # mean delta time between measures in seconds
        t = pandas.to_datetime(df.index)
        delta_df = t.to_series().diff().dt.total_seconds()
        delta_df_max = float(delta_df.max())
        delta_df_min = float(delta_df.min())
        if delta_df_max - delta_df_min > float(self.delta_max_std):
            delta_df = int(np.abs(delta_df.mean()))
            delta = self.resample_time
            if delta is not None and delta != '':
                delta = int(delta)
            else:
                delta = delta_df
            self.logger.info("\tFound asynchronous data. Delta between measures: " + str(delta))
        else:
            delta = int(delta_df_min)
            self.logger.info("\tSynchronous data. Delta between measures: " + str(delta))

        df[self.time_index] = t
        
        try:
            # Remove duplicates
            df_resample = df.drop_duplicates(subset=self.time_index)
            df_resample = df_resample.set_index(self.time_index)

            # Resample time series to computed delta time, filling missing values with previous value.
            # We generate, this way, a synchronous time series
            if self.resample == 'yes':
                df_resample = df_resample.resample(str(delta)+'S').pad()
                df_resample.dropna(inplace=True)
            
            df = df_resample
        except Exception as e:
            self.logger.error("Error while trying to resample: " + str(e))
            return df

        return df

    def set_up_data(self, df, dataset_features, inference_features=None, classifier=False):
        """
            Prepares dataframe to be trained selecting the columns from the features 
            configuration/parameters.
            If we dont have time series data, features to be inferenced are only used as labels.
            We dont use a time index.
            If reset is False, then the number of features is always reset before computations.
        """
        self.num_features_dataset = 0
        self.num_inference_features = 0

        features = []
        features_df = df.columns.tolist()
        for dataset_feature in dataset_features:
            if dataset_feature in features_df:
                features = _.concat(features, dataset_feature)
                self.num_features_dataset += 1
            else:
                self.logger.error("Feature '" + str(dataset_feature) + "' was not found in dataset features (" + str(features_df) + "). It will be ignored.")
            
        if self.num_features_dataset == 0:
            self.logger.error("You must specify at least one feature in 'input_features' parameter.")
            sys.exit(1)

        if not classifier:
            for inference_feature in inference_features:
                if inference_feature in features_df:
                    features = _.concat(features, inference_feature)
                    self.num_inference_features += 1
                    self.num_features_dataset += 1
                else:
                    self.logger.error("Feature '" + str(dataset_feature) + "' was not found in dataset features (" + str(features_df) + "). It will be ignored.")
                
            if self.num_inference_features == 0:
                self.logger.error("You must specify at least one feature in 'inference_features' parameter.")
                sys.exit(1)

        df = df.loc[:, features]

        return df

    def get_out_classes(self, df, class_name=None):
        """
            Extracts classes from data frame, returning the dataframe without the column of classes 
            and a list with the classes. 
        """
        if class_name is None:
            class_name = self.class_name

        if class_name == '':
            self.logger.error(
                "You must specify the name of the field to be used as class in 'class_name' configuration parameter.")
            sys.exit(1)

        if class_name not in df.columns.to_list():
            self.logger.error(
                "'class_name' configuration parameter must be an existing field in the database.")
            sys.exit(1)

        self.classes = df[class_name].to_list()
        df = df.drop(self.class_name, axis=1)

        return df, self.classes

    def encode_classes(self, classes=None, label_encoder=None, dtype='int32'):
        """
            Uses a label encoder to encode a list of classes into numbers. Then transforms the array
            into a matrix of 1s and 0s. If any of parameters classes and label_encoder is provided,
            it/they is/are not stored as class' instance attributes. 
        """
        if classes is None:
            y = self.classes
        else:
            y = classes

        if label_encoder is None:
            if self.label_encoder is None:
                self.label_encoder = LabelEncoder()
                y = self.label_encoder.fit_transform(y)
            else:
                if self.label_encoder.classes_:
                    y = self.label_encoder.transform(y)
                else:
                    y = self.label_encoder.fit_transform(y)
            return to_categorical(y), self.label_encoder
        else:
            y = label_encoder.transform(y)   

            return to_categorical(y, dtype=dtype), label_encoder

    def one_hot_encode_categorical_cata(self, dataframe_global, one_hot_encoder=None):
        """
            Reads dataframe and selects the columns that are not numbers. 
            Those columns are removed and put into a one_hot_encoder to convert them to numbers. 
            They are put back to the dataframe.
        """
        non_numeric = dataframe_global.select_dtypes(include='object')
        if not non_numeric.empty:
            self.num_features_dataset -= non_numeric.shape[1]

            if one_hot_encoder is None:
                one_hot_encoder = OneHotEncoder(handle_unknown='ignore')
                non_numeric_encoded = one_hot_encoder.fit_transform(non_numeric.values).toarray()
            else:
                non_numeric_encoded = one_hot_encoder.transform(non_numeric.values).toarray()

            self.num_features_dataset += non_numeric_encoded.shape[1]
            
            dataframe_global = dataframe_global.select_dtypes(exclude='object')
            dataframe_global = dataframe_global.join(pandas.DataFrame(non_numeric_encoded))
        else:
            self.logger.debug("\tNo categorical data found")

        return dataframe_global, one_hot_encoder

    def scale_split_data(self, dataframe_global, classifier=False, classes=None, scaler = None, ft_range = None):
        """
            Reads dataframe and scales data according to the configuration.
            Once scaled, data is splited into training and testing and returned.
        """
        if classifier and classes is None:
            classes = self.classes

        if scaler is not None:
            self.scaler = scaler
        
        if ft_range is not None:
            self.ft_range = ft_range

        if classifier:
            self.num_inference_features = 0
            self.num_forecasts = 0

        if self.data_type == constants.TIMESERIES:
            scaled = dataframe_global.values.reshape(dataframe_global.values.shape[0],
                                                    self.num_features_dataset + self.num_inference_features)
            self.scaler, scaled = helpers.scale_dataset(self.scaler, scaled, 0, self.ft_range)
            # Make time series a supervised problem
            data_id = self.series_to_supervised(scaled, self.num_previous_measures, self.num_forecasts)

            # Removing unnecessary features (input features) from labels columns
            cols_to_remove = []
            for j in range(
                    data_id.shape[1],
                    self.num_previous_measures * (self.num_features_dataset + self.num_inference_features),
                    -(self.num_features_dataset + self.num_inference_features)):
                for l in range(self.num_features_dataset):
                    cols_to_remove.append(j - l - 1)

            # Removing unnecessary features (prediction features) from dataset (input features) columns
            for j in range(self.num_features_dataset, data_id.shape[1], self.num_features_dataset + self.num_inference_features):
                for l in range(j, j + self.num_inference_features):
                    cols_to_remove.append(l)

            data_id.drop(data_id.columns[cols_to_remove], axis=1, inplace=True)
            data_id = data_id.values

            split = int(len(data_id) * float(self.training_ratio))

            train = data_id[:split, :]  # First part of the array for testing
            test = data_id[split:, :]  # Last for validating

            # split into input and outputs
            x_train = train[:, :self.num_previous_measures * self.num_features_dataset]                    
            x_test= test[:, :self.num_previous_measures * self.num_features_dataset]
                    
            if not classifier:
                y_train = train[:, self.num_previous_measures * self.num_features_dataset:]
                y_test = test[:, self.num_previous_measures * self.num_features_dataset:]
            else:
                y_train = classes[:split]
                y_test = classes[split:]

            # reshape input to be 3D [samples, timesteps, features]
            x_train = x_train.reshape(
                (x_train.shape[0], int(x_train.shape[1] / self.num_features_dataset),
                self.num_features_dataset))
            x_test = x_test.reshape(
                (x_test.shape[0], int(x_test.shape[1] / self.num_features_dataset),
                self.num_features_dataset))
        else:
            # Shuffle data when not timeseries
            dataframe_shuffled = dataframe_global.sample(frac=1).reset_index(drop=True)

            scaled = dataframe_shuffled.values.reshape(dataframe_shuffled.values.shape[0],
                                                    self.num_features_dataset + self.num_inference_features)
            self.scaler, scaled = helpers.scale_dataset(self.scaler, scaled, 0, self.ft_range)

            data_id = scaled
            
            split = int(len(data_id) * float(self.training_ratio))

            train = data_id[:split, :]  # First part of the array for testing
            test = data_id[split:, :]  # Last for validating

            # split into input and outputs
            x_train, y_train = train[:, :self.num_features_dataset], None                            
            x_test, y_test = test[:, :self.num_features_dataset], None
            
            if not classifier:
                y_train = train[:, self.num_features_dataset:]
                y_test = test[:, self.num_features_dataset:]
            else:
                y_train = classes[:split]
                y_test = classes[split:]


        self.logger.info("\tTraining samples: " + str(x_train.shape[0]) + "\t Test samples: " + str(x_test.shape[0]))

        return scaled, x_train, y_train, x_test, y_test

    def train_model(self, x_train, y_train=None, x_test=None, y_test=None, classifier=False, keras_callbacks=None, balance=False, model = None):
        """
            Trains a model with the data passed as parameters.
            If x_train is a generator, remember to pass y_train as None (it also defaults to None).
        """
        if model is not None:
            self.model_train = model

        if self.model_train is None:
            if classifier:
                self.model_train = self.pred.get_model(
                    helpers.get_data_shape(self.data_type, self.num_features_dataset, 
                                    self.num_previous_measures, self.algorithm), 
                    len(self.le.classes_), # output shape
                    inner_activation=self.inner_activation)
            else:
                self.model_train = self.pred.get_model(
                    helpers.get_data_shape(self.data_type, self.num_features_dataset,
                                        self.num_previous_measures, self.algorithm),
                    self.num_forecasts * self.num_inference_features, # output shape depends on number of features inferenced
                    inner_activation=self.inner_activation)
            previous_id = None

        self.logger.info("Training shape: " + str(helpers.get_data_shape(self.data_type, self.num_features_dataset,
                                    self.num_previous_measures, self.algorithm)))
        
        num_epochs = self.epoch_external
        batch = self.batch_size
        val_split = self.initial_validation_split

        if balance:
            from imblearn.tensorflow import balanced_batch_generator

            x_train = balanced_batch_generator(x_train, y_train)
            y_train = None

            if x_test is not None:
                x_test = balanced_batch_generator(x_test, y_test)
                y_test = None

                history = self.model_train.fit_generator(x_train,
                                epochs=self.epoch_internal,
                                validation_data=x_test,
                                callbacks=keras_callbacks,
                                verbose=1)
            else:
                history = self.model_train.fit_generator(x_train,
                                epochs=self.epoch_internal,
                                validation_split=val_split,
                                callbacks=keras_callbacks,
                                verbose=1)
        else:
            for i in range(num_epochs):  
                if x_test is not None:
                    history = self.model_train.fit(x_train, y_train,
                                            epochs=self.epoch_internal,
                                            batch_size=batch,
                                            validation_data=(x_test,y_test),
                                            callbacks=keras_callbacks,
                                            verbose=1)

                else:          
                    history = self.model_train.fit(x_train, y_train,
                                            epochs=self.epoch_internal,
                                            batch_size=batch,
                                            validation_split=val_split,
                                            callbacks=keras_callbacks,
                                            verbose=1)

            # self.logger.debug(history)
            val_split = val_split * self.validation_split_multiplayer
            if batch is not None and batch < x_train.shape[0] / 2:
                batch = int(batch * float(self.batch_size_multiplier))
        
        return self.model_train, history

    def evaluate_model(self, x_test, y_test=None):
        """
            Evaluate the model with test data.
            Remember to pass y_test as None if x_test is a generator (it also defaults to None).
        """    
        scores = self.model_train.evaluate(x_test, y_test, verbose=1)

        return scores

# --------------------- Ready functions ----------------------

def to_categorical(y, num_classes=None, dtype='float32'):
    """Converts a class vector (integers) to binary class matrix.

    E.g. for use with categorical_crossentropy.

    # Arguments
        y: class vector to be converted into a matrix
            (integers from 0 to num_classes).
        num_classes: total number of classes.
        dtype: The data type expected by the input, as a string
            (`float32`, `float64`, `int32`...)

    # Returns
        A binary matrix representation of the input. The classes axis
        is placed last.
    """
    y = np.array(y, dtype='int')
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=dtype)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical

def plot_history(history, show=True, save=False):
    import matplotlib.pyplot as plt
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))

    plt.figure()
    plt.plot(epochs, acc, 'bo', label='Training accuracy')
    plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend()
    if save:
        plt.savefig("acc.png")

    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training Loss')
    plt.plot(epochs, val_loss, 'b', label='Validation Loss')
    plt.title('Training and validation loss')
    plt.legend()

    if save:
        plt.savefig("loss.png")

    if show:
        plt.show()


def easier_train(trainer, entities, index_data=None, inference_type=constants.ESTIMATOR):
    """
        EASIER platform ready-training.
    """
    trainer.finished = False
    # Reset timer
    if isinstance(trainer._active_timer, threading.Timer):
        trainer._active_timer.cancel()

    if index_data is None:
        index_data = trainer.config['ELASTIC']['index_data']
    
    num_entities_trained = 0
    for entity in entities:
        trainer.num_features_dataset = 0
        trainer.num_inference_features = 0
        
        # KERAS + TENSORFLOW
        K.clear_session()
        with tf.Graph().as_default():
            # Load model or create a new one
            object_dict = helpers.load_model_file(trainer.eslib, entity, inference_type=inference_type)
            trainer.pred = object_dict.get(constants.PREDICTOR)
            if trainer.config['INFERENCE']['retrain'].lower() == 'true':
                trainer.model_train = object_dict.get(constants.MODEL_EXTENSION)
                trainer.scaler = object_dict.get(constants.SCALER_EXTENSION)
                trainer.one_hot_encoder = object_dict.get(constants.ONEHOTENCODER_EXTENSION)
                previous_id = object_dict.get(constants._ID)
            else:
                trainer.model_train = None
                trainer.scaler = None
                trainer.one_hot_encoder = None
                previous_id = None

            time_window_to = trainer.config['ML']['time_window_to']

            if trainer.model_train is None and trainer.config['ML_INITIAL']['initial_train'].lower() == 'true':
                # --------------- Initial training activation ---------------------
                time_window_to = trainer.config['ML_INITIAL']['time_window_to_initial']
                # -----------------------------------------------------------------

            # -------------------------------------- Data extraction --------------------------------------            
            max_entries = trainer.config['ELASTIC']['max_entries']
            
            if max_entries == 'all':
                df, extraction_time, preprocess_start_time = trainer.extract_data_from_elk(entity, index_data, time_window_to)
            else:
                df, extraction_time, preprocess_start_time = trainer.extract_data_from_elk(entity, index_data, time_window_to, data_size=int(max_entries))

            trainer.logger.info("elapsed_extraction_time: " + str(extraction_time))

            if df.empty: continue

            trainer.logger.debug("- Preprocessing data to train: " + entity)
            # Train only entities with more than minimum samples in config
            if df.shape[0] < int(trainer.config['ML']['minimum_samples']):
                trainer.logger.info(
                    'Cannot train model (' + entity + ') - Not enough samples [' + str(
                        df.shape[0]) + ']' + ". Please check configuration (minimum_samples).\n")
                continue  
            # ----------------------------------------------------------------------------------------------
            
            preprocess_start_time = time_lib.clock()
            # -------------------------------------- Data & Features preparation --------------------------------------
            if inference_type==constants.CLASSIFIER:
                inference_features = None
            else:
                inference_features = str(os.getenv("PREDICTION_FEATURES", trainer.config['DATA']['inference_features'])).replace(' ', '').split(',')
                
            dataset_features = str(os.getenv("INPUT_FEATURES", trainer.config['DATA']['dataset_features'])).replace(' ', '').split(',')
            
            if trainer.config['INFERENCE']['data_type'] == constants.TIMESERIES and trainer.config['DATA']['time_index'] != '':
                df = trainer.set_up_timeseries_data(df, dataset_features=dataset_features, inference_features=inference_features)
            else:
                if trainer.config['INFERENCE']['data_type'] == constants.TIMESERIES:
                    trainer.logger.error(
                        "If your data is a timeseries type, you must specify the timestamp column name in parameter time_index")
                    sys.exit(1)
                df = trainer.set_up_data(df, dataset_features=dataset_features, inference_features=inference_features)

            if trainer.config['ML']['training_size'] != 'all':
                # Train only on the last N parameters (defined in config.ini)
                dataframe_global = df.tail(int(trainer.config['ML']['training_size']))
            else:
                dataframe_global = df
            
            if dataframe_global.size == 0:
                trainer.logger.info("--- No data for training " + entity + ". Found " + str(len(
                dataframe_global)) + " observations.\n Please check configuration (minimum_samples > num_previous_measures).\n")
                continue
            # ----------------------------------------------------------------------------------------------
            
            trainer.logger.info("\tFeatures available: " + str(dataframe_global.columns.unique().tolist()))

            # ------------------ Categorical data encoding -------------------
            dataframe_global, trainer.one_hot_encoder = trainer.one_hot_encode_categorical_cata(dataframe_global, trainer.one_hot_encoder)
            # ----------------------------------------------------------------------------------------------
            
            # ------------------ Data scaling and train-test split ------------------
            scaled, x_train, y_train, x_test, y_test = trainer.scale_split_data(dataframe_global)
            # ----------------------------------------------------------------------------------------------
            preprocess_end_time = time_lib.clock()
            trainer.logger.info("elapsed_preprocess_time: " + str(preprocess_end_time - preprocess_start_time))

            # ------------------ Training ------------------
            trainer.keras_callbacks[1] = callbacks.TensorBoard(log_dir="../logs/TensorBoard/Estimation/" + 
                str(entity) + "/{}".format(dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')), write_images=True, write_graph=True)
            
            start_time = time_lib.clock()
            model_train, history = trainer.train_model(x_train, y_train, x_test=x_test, y_test=y_test, 
                    classifier=False, keras_callbacks=trainer.keras_callbacks, balance=False)
            end_time = time_lib.clock()
            trainer.logger.info("elapsed_trainning_time: " + str(end_time - start_time))

            scores = trainer.evaluate_model(x_test, y_test)
            trainer.logger.debug("\tEvaluation " + trainer.model_train.metrics_names[0] + " = " + str(float(scores[0])))
            trainer.logger.debug("\tEvaluation " + trainer.model_train.metrics_names[1] + " = " + str(float(scores[1])))
            
            # ----------------------------------------------------------------------------------------------

            # ------------------ Model metadata ------------------
            metadata = {}  # Loss and accuracy
            metadata[trainer.model_train.metrics_names[0]] = float(scores[0])
            metadata[trainer.model_train.metrics_names[1]] = float(scores[1])
            
            metadata['elapsed_extraction_time'] = extraction_time
            metadata['elapsed_preprocess_time'] = preprocess_end_time - preprocess_start_time
            metadata['elapsed_trainning_time'] = end_time - start_time
                        
            metadata['test'] = {
                'size': x_test.shape[0],
                #'first': x_test[0],
                #'last': x_test[x_test.shape[0]-1]
            }

            metadata['train'] = {
                'size': x_train.shape[0],
                #'first': x_train[0],
                #'last': x_train[x_train.shape[0]-1]
            }

            files_dict = {}
            files_dict[constants.MODEL_EXTENSION] = trainer.model_train
            files_dict[constants.SCALER_EXTENSION] = trainer.scaler
            if trainer.one_hot_encoder is not None:
                files_dict[constants.ONEHOTENCODER_EXTENSION] = trainer.one_hot_encoder
            # ----------------------------------------------------------------------------------------------

            trainer.logger.debug("- Finished Training: " + entity + "\n")
            num_entities_trained += 1
            
            if tf.__version__.split(".")[0] == '2':
                helpers.save_model(trainer.eslib, entity, metadata, files_dict, _id=previous_id, save_tflite=True, calibration_data=x_train, save_tpu=True)

        # Saving the model for tflite requires being outside a graph in TF1.x version
        if tf.__version__.split(".")[0] == '1':
            helpers.save_model(trainer.eslib, entity, metadata, files_dict, _id=previous_id, save_tflite=True, calibration_data=x_train, save_tpu=True)

    trainer.finished = True
    trainer.logger.debug("--- Finished training a total of " + str(num_entities_trained) + " models")

# --------------------- Experimental functions ----------------------

def transfer_model(pre_trained_model, last_layer=1, units_last_layer=512, activation_last_layer='relu', 
                   drop_out_rate=0.2, output_shape=1, output_activation='sigmoid', lr = 0.0001,
                   loss_fn = 'categorical_crossentropy', metrics = ["acc"]):
    """
    **Experimental feature**
    """
    from tensorflow.keras import layers
    from tensorflow.keras import Model
    from tensorflow.keras.optimizers import RMSprop

    i = 0
    for layer in pre_trained_model.layers:
        if i == last_layer:
            last_layer = layer
            break
        layer.trainable = False
        i = i + 1

    # pre_trained_model.summary()
    # TODO iterate in for loop as get_layer receives the layer name
    last_layer = pre_trained_model.get_layer(last_layer)
    # print('last layer output shape: ', last_layer.output_shape)
    last_output = last_layer.output

    # Flatten the output layer to 1 dimension
    x = layers.Flatten()(last_output)
    # Add new Dense layer to activate features
    x = layers.Dense(units_last_layer, activation=activation_last_layer)(x)
    # Add regularization -- pre_trained_model is usually very big
    x = layers.Dropout(drop_out_rate)(x)                  
    # Output layer
    x = layers.Dense(output_shape, activation=output_activation)(x)           

    model = Model(pre_trained_model.input, x) 

    model.compile(optimizer = RMSprop(lr=lr), 
                loss = loss_fn, # mean_squared_error, binary_crossentropy
                metrics = metrics)
    return model

def build_model(hp):
    """
    **Experimental feature**
    """
    from tensorflow import keras
    from tensorflow.keras import layers

    inputs = keras.Input(shape=(784,))
    x = layers.Dense(
        units=hp.Int('units', min_value=32, max_value=512, step=32),
        activation='relu')(inputs)
    outputs = layers.Dense(10, activation='softmax')(x)
    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice('learning_rate',
                      values=[1e-2, 1e-3, 1e-4])),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])
    return model

def hyperparameter_tunning(build_model, dataset, val_dataset):
    """
    **Experimental feature**
    Requisite: installing kerastuner with: "pip install -U keras-tuner" (https://keras-team.github.io/keras-tuner/)
    @param build_model: function that returns a compiled model, it receives as input a HyperModel "hp" parameter.
    """
    import kerastuner
 
    tuner = kerastuner.tuners.Hyperband(
            build_model,
            objective='val_loss',
            max_epochs=100,
            max_trials=200,
            executions_per_trial=2,
            directory='../storage')

    tuner.search(dataset, validation_data=val_dataset)
    
    tuner.results_summary()

    return tuner.get_best_models(num_models=1)