import tensorflow as tf

from tensorflow.keras import Input

from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, UpSampling1D, \
    Dropout, Dense, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.initializers import glorot_uniform, VarianceScaling
from tensorflow.keras.regularizers import l1

from tensorflow.keras.callbacks import ModelCheckpoint

from . import QSAR_Loss

tf.random.set_seed(0)


class QSAR_Autoencoder:
    """A convolutional auto-encoder implement."""
    def __init__(self, conv_dim, activation='leaky_relu',
                initialization='he_normal', lr=0.001, momentum=0.07):
        """create convolutional autoencoder model.

        :param conv_dim: conv dimension
        :type conv_dim: int
        :param activation: activation function, defaults to \
            'leaky_relu
        :type activation: str, optional
        :return: convolutional auto-encoder model
        :rtype: model
        """
        self.conv_dim = conv_dim
        self.activation = activation
        self.initialization = initialization
        self.optimizer = SGD(lr, momentum)
        self.conv_ae_model, self.conv_ae_encoder = self.create_model(
            self.conv_dim, self.activation, self.initialization)

    # with tf.device('gpu:0'):

    def create_model(self, conv_dim, activation_flag, initialization):
        """create convolutionary autoencoder model.

        :param conv_dim: list of conv dimensions, e.g. [20480, 300, 150, 100, \
            100, 80, 60, 15]
        :type conv_dim: int
        :param activation: activation function, defaults to \
            'leaky_relu'
        :type activation: str, optional
        :return: convolutional auto-encoder models: conv_ae_model, conv_ae_encoder
        :rtype: model
        """
        # returns autoencoder and encoder
        # layer_depth = len(layer_dim) - 1
        conv_depth = len(conv_dim) - 1
        filter_size = 3

        if str(activation_flag) == 'leaky_relu':
            activation = tf.keras.layers.LeakyReLU(alpha=0.3)
        # input vector
        input_vec = Input(shape=(conv_dim[0], 1))
        x = input_vec

        for i in range(conv_depth - 1):
            x = Conv1D(conv_dim[i + 1], filter_size, activation=activation,
                       padding='same',
                       kernel_initializer=initialization)(x)
            x = MaxPooling1D(2, 2, padding='valid')(x)

        # hidden layer
        encoded = Conv1D(conv_dim[-1], 1, activation='tanh', padding='same',
                         kernel_initializer=initialization)(x)
        x = encoded

        # To loss function
        y = Flatten()(encoded)
        enc_out = tf.keras.layers.Lambda(
            lambda z: tf.math.l2_normalize(z,
                                           axis=1), name='enc_out')(y)

        # decoder
        # internal layers in decoder
        for i in range(conv_depth, 1, -1):
            x = Conv1D(conv_dim[i], filter_size, activation=activation,
                       padding='same',
                       kernel_initializer=initialization)(x)

            x = UpSampling1D(2)(x)

            # output vector
        decoded = Conv1D(1, 1, strides=1, activation='sigmoid', padding='same',
                         name='decoded',
                         kernel_initializer=initialization)(x)

        conv_ae_model = Model(inputs=input_vec, outputs=[decoded, enc_out],
                              name='autoencoder')
        conv_ae_model.compile(optimizer=self.optimizer,
                              loss={'decoded': 'binary_crossentropy',
                                    'enc_out': QSAR_Loss.triplet_semihard_loss},
                              loss_weights={'decoded': 1.0, 'enc_out': 1.0})

        conv_ae_encoder = Model(inputs=input_vec, outputs=encoded,
                                name='encoder')
        return conv_ae_model, conv_ae_encoder

class QSAR_Classifier():
    """A convolutional auto-encoder implement.

    FM: Why some layers have dropout after, some don't? More dropout made 
        results worse
    """

    def __init__(self, input_shape=4800, 
                 activation_list=['leaky_relu', 'leaky_relu', 'leaky_relu',
                                  'leaky_relu', 'relu', 'relu'],
                 nn_layer_dim_list=[4800, 1000, 1000, 800, 200, 50],
                 lr=0.001, momentum=0.7):
        """QSAR Classifier Model construction.

        :param input_shape: Input layer dimension, defaults to 4800.
        :type input_shape: intput layer dimension, defaults to 4800.
        :type input_shape: int
        :param nn_layer_dim_list: List of layer dimensions excluding the output 
            layer,
            defaults to [4800, 1000, 1000, 800, 200, 50]
        :type nn_layer_dim_list: list, optional
        """
        self.input_shape = input_shape
        self.input_placeholder = Input(shape=(self.input_shape))
        self.activation_list = activation_list
        self.nn_layer_dim_list = nn_layer_dim_list
        self.optimizer = SGD(lr=lr, momentum=momentum)
        self.classifier = self.create_classifier(
            self.input_placeholder, self.activation_list, self.nn_layer_dim_list, self.optimizer)

    def create_classifier(self, model_input, activation_list, nn_layer_dim_list, optimizer):
        """Function that create a classifier basing on the structure
        information.

        :param model_input: model input place holder.
        :type model_input: TF.Input()
        :param nn_layer_dim_list: List of layer dimensions excluding the output 
            layer,
            defaults to [4800, 1000, 1000, 800, 200, 50]
        :type nn_layer_dim_list: list, optional
        :return: QSAR classification model
        :rtype: model
        """
        
        temp_model = model_input

        for layer, activation in zip(nn_layer_dim_list, activation_list):
            if activation == 'leaky_relu':
                activation = tf.keras.layers.LeakyReLU(alpha=0.3)
            temp_model = Dense(layer,
                               activation=activation,
                               kernel_initializer='he_normal')(temp_model)
            # temp_model = Dropout(0.1)(temp_model)

        # output layer
        model_output = Dense(1, activation='sigmoid',
                             kernel_initializer='he_normal')(temp_model)

        
        temp_model = Model(model_input, model_output)
        temp_model.compile(optimizer=optimizer, loss='binary_crossentropy')
        return temp_model
