import numpy as np
import os
import datetime

import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.layers import LeakyReLU, ReLU, ELU
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.schedules import ExponentialDecay, InverseTimeDecay

from sklearn.preprocessing import StandardScaler

from . import scale


class RegressionANN(object):
    """
    Use tensorflow.keras to build an artifical neural network for regression
    """

    def __init__(self):
        pass

    def fit(self, X, y, input_dim, noutput, epochs,
            validation_data=None, outdir='./', outname='best.h5',
            scaleX=True, scaleY=True, verbose=0, batch_size=None,
            activation='relu',
            input_units=128,
            units=[128, 128, 128, 128, 128],
            learning_rate=0.001,
            lr_schedule=False,
            use_alr=False,
            alr_monitor='val_loss',
            alr_factor=0.1,
            alr_patience=5,
            alr_verbose=0,
            alr_min_lr=1e-4,
            use_es=False,
            es_monitor='val_loss',
            es_patience=10,
            es_verbose=0,
            kernel_initializer='glorot_uniform',
            use_tfboard=False,
            tfboard_logdir='logs/fit',
            tfboard_tag=None,
            tfboard_histogram_freq=0
            ):
        """
        input_dim: {int}. dimension of input layer
        noutput: {int}. number of outputs in final layer
        validation_data: (X_test, y_test)
        activation {str}: activation function to use for all layers
            (apart from last)
        input_units {int}: number of units in input layer
        units {list of ints}: number of units in each hidden layer.
            length of list is number of hidden layers
        use_alr {bool} default False.
            alr == adaptive learning rate
            if True then uses ReduceLROnPlateau
        alr_monitor {str, 'val_loss'}
        alr_factor {float, 0.1}
        alr_patience {int, 5}
        alr_verbose {int, 0 (or 1)}
        alr_min_lr {float, 1e-4}
        use_es {bool, False}
            es == early stopping
            if True then use EarlyStopping
        es_monitor{str, 'val_loss'}
        es_patience{int, 10}
        es_verbose{int, 0 (or 1)}
        kernel_initializer {str} default 'glorot_uniform'
        use_tfboard {bool: False} If true then enable TensorBoard logging
        tfboard_logdir {str: 'logs/fit'} path to log directory for TensorBoard
            callback.
        tfboard_tag {str: None}: identifier tag for TensorBoard sub directory
            If None then will use time stamp
        tfboard_histogram_freq {int: 0} histogram_freq in TensorBoard
        """
        self.outdir = outdir
        self.learning_rate = learning_rate
        self.use_alr = use_alr
        self.alr_monitor = alr_monitor
        self.alr_factor = alr_factor
        self.alr_patience = alr_patience
        self.alr_verbose = alr_verbose
        self.alr_min_lr = alr_min_lr
        self.use_es = use_es
        self.es_monitor = es_monitor
        self.es_patience = es_patience
        self.es_verbose = es_verbose
        self.kernel_initializer = kernel_initializer
        self.bestfile = os.path.join(self.outdir, outname)
        self.use_tfboard = use_tfboard
        self.tfboard_logdir = tfboard_logdir
        self.tfboard_histogram_freq = tfboard_histogram_freq

        if validation_data:
            X_test, y_test = validation_data

        self.scaleX = scaleX
        self.scaleY = scaleY
        if self.scaleX:
            X = X.copy()
            self.X_scalers = scale.make_scalers(X)
            X = scale.apply_scaler(X, self.X_scalers)
            if validation_data:
                X_test = scale.apply_scaler(X_test, self.X_scalers)
            self.save_X_scalers(os.path.join(self.outdir, "X_scalers"))
        if self.scaleY:
            y = y.copy()
            self.Y_scalers = scale.make_scalers(y)
            y = scale.apply_scaler(y, self.Y_scalers)
            if validation_data:
                y_test = scale.apply_scaler(y_test, self.Y_scalers)
            self.save_Y_scalers(os.path.join(self.outdir, "Y_scalers"))

        if validation_data:
            validation_data = (X_test, y_test)

        # Initialising the ANN
        self.model = Sequential()

        # Adding the input layer and the first hidden layer
        # self.model.add(Dense(128, kernel_regularizer=regularizers.l2(0.001), activation = 'relu', input_dim = input_dim))
        self.model.add(
            Dense(
                input_units,
                activation=activation,
                kernel_initializer=self.kernel_initializer,
                input_dim=input_dim
            )
        )
        # self.model.add(Dropout(0.2))

        for i in range(len(units)):
            self.model.add(
                Dense(units=units[i],
                      activation=activation,
                      kernel_initializer=self.kernel_initializer
                      ))

        # Adding the second hidden layer
        # self.model.add(Dense(units = 128, kernel_regularizer=regularizers.l2(0.001), activation = 'relu'))
        # self.model.add(Dense(units = 128, activation = 'relu'))
        # self.model.add(Dropout(0.2))

        # Adding the third hidden layer
        # self.model.add(Dense(units = 128, kernel_regularizer=regularizers.l2(0.001), activation = 'relu'))
        # self.model.add(Dense(units = 128, activation = 'relu'))
        # self.model.add(Dropout(0.2))

        # self.model.add(Dense(units = 128, kernel_regularizer=regularizers.l2(0.001), activation = 'relu'))
        # self.model.add(Dense(units = 128, activation = 'relu'))
        # self.model.add(Dropout(0.2))

        # self.model.add(Dense(units = 128, kernel_regularizer=regularizers.l2(0.001), activation = 'relu'))
        # self.model.add(Dense(units = 128, activation = 'relu'))
        # self.model.add(Dropout(0.2))

        # self.model.add(Dense(units = 128, kernel_regularizer=regularizers.l2(0.001), activation = 'relu'))
        # self.model.add(Dense(units = 128, activation = 'relu'))
        # self.model.add(Dropout(0.2))

        # Adding the output layer

        self.model.add(Dense(units=noutput))

        if lr_schedule:
            STEPS_PER_EPOCH = 1
            lr = InverseTimeDecay(
                0.001,
                decay_steps=STEPS_PER_EPOCH*500,
                decay_rate=1,
                staircase=False)
            # initial_learning_rate = 0.1
            # lr = ExponentialDecay(
            #     initial_learning_rate,
            #     decay_steps=100000,
            #     decay_rate=0.96,
            #     staircase=True)
        else:
            lr = self.learning_rate
        self.optimizer = Adam(learning_rate=lr)

        # Compiling the ANN
        self.model.compile(optimizer=self.optimizer,
                           loss='mean_squared_error', metrics=['mse'])

        if verbose:
            print(self.model.summary(), flush=True)

        callbacks = [ModelCheckpoint(
            f'{self.bestfile}', save_best_only=True, monitor='loss')]

        if self.use_tfboard:
            if tfboard_tag:
                self.tfboard_tag = tfboard_tag
            else:
                self.tfboard_tag = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            log_dir = os.path.join(self.tfboard_logdir, self.tfboard_tag)
            tensorboard_callback = TensorBoard(
                log_dir=log_dir, histogram_freq=self.tfboard_histogram_freq)
            callbacks.append(tensorboard_callback)

        if self.use_alr:
            reduce_lr = ReduceLROnPlateau(
                monitor=self.alr_monitor,
                factor=self.alr_factor,
                patience=self.alr_patience,
                min_lr=self.alr_min_lr,
                verbose=self.alr_verbose)
            callbacks.append(reduce_lr)

        if self.use_es:
            es = EarlyStopping(
                monitor=self.es_monitor,
                patience=self.es_patience,
                verbose=self.es_verbose
            )
            callbacks.append(es)

        # Fitting the ANN to the Training set
        history = self.model.fit(
            X,
            y,
            epochs=epochs,
            verbose=verbose,
            validation_data=validation_data,
            batch_size=batch_size,
            callbacks=callbacks
        )

        return history

    def load_model(self, file):
        self.model = load_model(file)

    def save_X_scalers(self, filename):
        np.save(filename, self.X_scalers)

    def save_Y_scalers(self, filename):
        np.save(filename, self.Y_scalers)

    def load_X_scalers(self, filename, allow_pickle=True):
        self.X_scalers = np.load(filename, allow_pickle=allow_pickle)

    def load_Y_scalers(self, filename, allow_pickle=True):
        self.Y_scalers = np.load(filename, allow_pickle=allow_pickle)

    def predict(self, X):
        if self.scaleX:
            X = scale.apply_scaler(X, self.X_scalers)

        y = self.model.predict(X)

        if self.scaleY:
            y = scale.apply_inverse_scaler(y, self.Y_scalers)

        return y
