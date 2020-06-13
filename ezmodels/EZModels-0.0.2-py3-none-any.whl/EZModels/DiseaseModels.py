import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation
import math
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import tensorflow
import logging
import sys
import warnings
logging.getLogger('tensorflow').setLevel(logging.ERROR)

class DiseaseSpreadLSTM():
    def __init__(self, file_path, column_name, window_size=3, node_count1=50, node_count2=50, 
                 dropout1=0.50, dropout2=0.20, activation='linear', optimizer='adam', loss='mse', epochs=200):
        self.window_size = window_size
        self.dataset,\
        self.scaler,\
        self.scaled_dataset,\
        self.train_set,\
        self.test_set\
        = self.load_data_and_normalize(file_path, column_name)
        self.X_train,\
        self.y_train,\
        self.X_test,\
        self.y_test\
        = self.generate_train_test_shaped(self.train_set, self.test_set, window_size)
        self.model = self.create_ltsm_two_hidden_layers(node_count1, dropout1, node_count2, 
                                                       dropout2, activation, optimizer, loss)
        self.epochs = epochs
        self.trainPredict = None
        self.testPredict = None
        self.XPredict = None
        self.trainPredictShift = None
        self.testPredictShift = None
        self.trainScore = None
        self.testScore = None
        self.is_fitted = False
        self.been_predicted = False
        self.all_plots_possible = False
        self.multiple_preds = None
        
        
    def predict(self, num_days=1):
        if not self.is_fitted:
            self.fit_model()
            self.is_fitted = True
            
        predicitions = []
        for i in range(num_days):
            if not self.been_predicted:
                self.X_train,\
                self.X_test,\
                self.y_train,\
                self.y_test\
                = self.train_test_pred_loop(self.scaled_dataset, self.window_size)
                X, _ = DiseaseSpreadLSTM.create_dataset(self.scaled_dataset, self.window_size)
                X = np.reshape(X, (X.shape[0], X.shape[1], 1))
                
                self.trainPredict = self.model.predict(self.X_train, batch_size=1)
                self.model.reset_states()
                self.testPredict = self.model.predict(self.X_test, batch_size=1)
                self.model.reset_states()
                self.XPredict = self.model.predict(X, batch_size=1)
                
                # invert predictions
                self.trainPredict = self.scaler.inverse_transform(self.trainPredict)
                self.y_train = self.scaler.inverse_transform([self.y_train])
                self.testPredict = self.scaler.inverse_transform(self.testPredict)
                testY = self.scaler.inverse_transform([self.y_test])
                self.XPredict = self.scaler.inverse_transform(self.XPredict)

                # shift train predictions
                self.trainPredictShift = np.empty_like(self.scaled_dataset)
                self.trainPredictShift[:, :] = np.nan
                self.trainPredictShift[self.window_size:len(self.trainPredict)+self.window_size, :] = self.trainPredict

                # shift test predictions
                self.testPredictShift = np.empty_like(self.scaled_dataset)
                self.testPredictShift[:, :] = np.nan
                self.testPredictShift[len(self.trainPredict)+(self.window_size*2)+1:len(self.scaled_dataset)-1, :]\
                = self.testPredict
                
                self.multiple_preds = np.empty_like(self.scaled_dataset)
                self.multiple_preds[:, :] = np.nan
                self.multiple_preds = self.XPredict

                predicitions.append(int(self.XPredict[-1]))
                self.real_values = self.scaler.inverse_transform(self.scaled_dataset)
                self.update_data_for_preds(next_pred=predicitions[i])
                self.been_predicted = True
            else:
                X, _ = DiseaseSpreadLSTM.create_dataset(self.scaled_dataset, self.window_size)
                X = np.reshape(X, (X.shape[0], X.shape[1], 1))
                self.XPredict = self.model.predict(X, batch_size=1)
                self.XPredict = self.scaler.inverse_transform(self.XPredict)
                self.multiple_preds = np.empty_like(self.scaled_dataset)
                self.multiple_preds[:, :] = np.nan
                self.multiple_preds = self.XPredict                
                
                predicitions.append(self.XPredict[-1])
                self.update_data_for_preds(next_pred=predicitions[i])
                
        return predicitions
        
        
    def rmse(self):
        # calculate root mean squared error
        testY = self.scaler.inverse_transform([self.y_test])
        self.trainScore = math.sqrt(mean_squared_error(self.y_train[0], self.trainPredict[:,0]))
        self.testScore = math.sqrt(mean_squared_error(testY[0], self.testPredict[:,0]))
        return self.trainScore, self.testScore


    def plot(self, save=False, name='LSTM_PRED', title='', xlabel=None, ylabel=None, xlabel_fontsize=12, 
             ylabel_fontsize=14, title_fontsize=20, size=(12,7), legend=True, 
             l1_color='#62a6de', l1_label='Actual',
             l2_color='#90ed4a', l2_label='Training Set Prediction', 
             l3_color='#ed9264', l3_label='Testing Set Prediction',
             l4_color='#ed6464', l4_label='Predicition',             
             legend_size=12, show_xy_labels=True, view='standard'
            ):

        if not self.is_fitted:
            raise ForgotToFitException("You done goofed!", 
                        "You never fit your model or made a prediction! What am I supposed to plot!?")

        fig = plt.figure(figsize=size)
        ax = fig.add_subplot()

        if show_xy_labels:
            ax.set_title(title, fontsize=title_fontsize)
            plt.xlabel(xlabel, fontsize=xlabel_fontsize)
            plt.ylabel(ylabel, fontsize=ylabel_fontsize)
        else:
            plt.xticks([])
            plt.yticks([])
            
        if view == 'standard':
            p1 = plt.plot(self.real_values, l1_color, label=l1_label)
            p4 = plt.plot(self.multiple_preds, l4_color, label=l4_label)
        elif view == 'train_test':
            p1 = plt.plot(self.real_values, l1_color, label=l1_label)
            p2 = plt.plot(self.trainPredictShift, l2_color, label=l2_label)
            p3 = plt.plot(self.testPredictShift, l3_color, label=l3_label)
        elif view == 'all':
            p1 = plt.plot(self.real_values, l1_color, label=l1_label)
            p2 = plt.plot(self.trainPredictShift, l2_color, label=l2_label)
            p3 = plt.plot(self.testPredictShift, l3_color, label=l3_label)
            p4 = plt.plot(self.multiple_preds, l4_color, label=l4_label)
        else:
            warnings.warn('Incorrect view selected. Showing standard view by default.  Please choose\
            one of [standard, train_test, all].');
        
        if legend == True:
            plt.legend(loc=2, fontsize=legend_size)
        plt.show()

        if save:
            fig.savefig(name)
    
            
    def fit_model(self, X=None, y=None, epochs=None, batch_size=None, verbose=None):
        if X != None or y != None or epochs != None or batch_size != None:
            self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=verbose)
        else:
            self.model.fit(self.X_train, self.y_train, 
                           epochs=self.epochs, batch_size=len(self.X_train), verbose=0)


    def update_data_for_preds(self, next_pred):
        temp_d = list(self.dataset)
        temp_s = list(self.scaled_dataset)
        temp_d.append(next_pred)
        self.dataset = np.asarray(temp_d).astype('float32')
        self.dataset = np.asarray(self.dataset).reshape(-1, 1)
        self.scaled_dataset = self.scaler.fit_transform(self.dataset)

    
    @staticmethod
    def train_test_pred_loop(scaled_dataset, window_size):
        train_size = int(len(scaled_dataset) * 0.75)
        test_size = len(scaled_dataset) - train_size
        train, test = scaled_dataset[0:train_size,:], scaled_dataset[train_size:len(scaled_dataset),:]

        
        X_train, y_train = DiseaseSpreadLSTM.create_dataset(train, window_size)
        X_test, y_test = DiseaseSpreadLSTM.create_dataset(test, window_size)

        
        # reshape input to be [samples, time steps, features]
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        return X_train, X_test, y_train, y_test
    
    
    @staticmethod
    def load_data_and_normalize(file_path, column_name):
        df = pd.read_excel(file_path)
        dataset = df[[column_name]]
        dataset = dataset.values
        dataset = dataset.astype('float32')
        
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_dataset = scaler.fit_transform(dataset)
        
        # split into train and test sets
        train_size = int(len(scaled_dataset) * 0.75)
        test_size = len(scaled_dataset) - train_size
        train_set, test_set = scaled_dataset[0:train_size,:], scaled_dataset[train_size:len(scaled_dataset),:]
        return dataset, scaler, scaled_dataset, train_set, test_set
    
    
    @staticmethod
    def create_dataset(dataset, window_size=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-window_size-1):
            a = dataset[i:(i+window_size), 0]
            dataX.append(a)
            dataY.append(dataset[i + window_size, 0])
        return np.array(dataX), np.array(dataY)
    
    
    @staticmethod
    def generate_train_test_shaped(train_set, test_set, window_size):
        X_train, y_train = DiseaseSpreadLSTM.create_dataset(train_set, window_size)
        X_test, y_test = DiseaseSpreadLSTM.create_dataset(test_set, window_size)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        return X_train, y_train, X_test, y_test
    
    
    @staticmethod
    def create_ltsm_two_hidden_layers(node_count1, dropout1, node_count2, 
                                     dropout2, activation, optimizer, loss):
        model = Sequential()

        model.add(LSTM(node_count1, return_sequences=True))
        model.add(Dropout(dropout1))

        model.add(LSTM(node_count2))
        model.add(Dropout(dropout2))

        model.add(Dense(1))
        model.add(Activation(activation))

        model.compile(optimizer = optimizer, loss = loss)
        return model
    
    
class ForgotToFitException(Exception):
    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload # you could add more args
    def __str__(self):
        return str(self.message)