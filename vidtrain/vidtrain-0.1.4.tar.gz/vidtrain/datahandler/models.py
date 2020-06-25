import warnings
import glob
import gzip
import pickle
from time import strftime
from keras.layers import (Input, Dropout, ConvLSTM2D, Conv3D, Concatenate, BatchNormalization,
                          GlobalMaxPooling3D, GlobalMaxPooling2D, MaxPooling3D, TimeDistributed, Dense)
from keras.models import Model
from keras.callbacks import LearningRateScheduler, Callback, History
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from . import loss
from . import interface
from .data import FileVersioning


class NetworkTrainer(interface.NetworkTrainer):

    def __init__(self, model_factory=None, training_data=None, epochs=150):
        self.input_shape = None
        self.num_categories = None
        self.epochs = epochs
        self.training_data = training_data
        self.model_factory = model_factory
        self.model = None
        self.history = None
        self.scheduler = StepDecayScheduler()
        self.loss_plot = PlotLosses()
        self.file_versioning = FileVersioning()
        # ToDo: use TqdmCallback to add a gui progress bar

    def compile_model(self):
        assert self.model_factory is not None, 'Could not compile model. Please set model_factory attribute.'
        if self.input_shape is None or self.num_categories is None:
            assert self.training_data is not None, 'Could not determine input shape. Please set input_shape or training_data attributes.'
            self.input_shape = self.model_factory.calc_input_shape(self.training_data.data_shape)
            self.num_categories = self.model_factory.calc_num_categories(self.training_data.annotation_shape)
        self.model = self.model_factory.compile(input_shape=self.input_shape, num_categories=self.num_categories)

    def draw_model(self, file_name):
        assert self.model is not None, 'Please compile the model with compile_model() first.'
        from keras.utils.vis_utils import model_to_dot
        model_to_dot(self.model, dpi=72).write_svgz(file_name, prog=['dot', '-Nfontname=sans-serif'])

    def train(self):
        assert self.model is not None, 'Please compile the model with compile_model() first.'
        assert self.training_data is not None, 'Could not train without data. Please set training_data property.'
        lrate = LearningRateScheduler(self.scheduler.step_decay)
        callbacks = [lrate]
        if self.loss_plot.canvas is not None:
            callbacks.append(self.loss_plot)
        self.history = self.model.fit_generator(self.training_data.generator(),
                                                steps_per_epoch=self.training_data.steps_per_epoch(),
                                                epochs=self.epochs,
                                                callbacks=callbacks,
                                                validation_data=self.training_data.validation_generator(),
                                                validation_steps=self.training_data.validation_steps())

    def get_fig(self):
        if self.loss_plot.fig is None:
            self.loss_plot.create_fig()
        return self.loss_plot.fig

    def get_ax(self):
        if self.loss_plot.ax is None:
            self.loss_plot.create_fig()
        return self.loss_plot.ax

    def set_canvas(self, canvas):
        self.loss_plot.set_canvas(canvas)

    def copy(self):
        copy = NetworkTrainer(model_factory=self.model_factory, training_data=self.training_data, epochs=self.epochs)
        copy.loss_plot = self.loss_plot
        return copy

    def save(self, path_prefix, unique=True):
        path_prefix = self.file_versioning.get_name(base_path=path_prefix, unique=unique)
        params = {'input_shape': self.input_shape,
                  'num_categories': self.num_categories,
                  'factory_type': type(self.model_factory)}
        with gzip.open(path_prefix + '_params.pkl.gz', 'w') as f:
            pickle.dump(params, f)
        try:
            self.model_factory.save(path_prefix + '_model.pkl.gz')
            params['history'] = self.history.history
            with gzip.open(path_prefix + '_params.pkl.gz', 'w') as f:
                pickle.dump(params, f)
            self.model.save_weights(path_prefix + '_weights.h5')
        except AttributeError:
            pass
        return path_prefix

    def load(self, path_prefix):
        with gzip.open(path_prefix + '_params.pkl.gz', 'r') as f:
            params = pickle.load(f)
        self.input_shape = params['input_shape']
        self.num_categories = params['num_categories']
        self.model_factory = params['factory_type']()
        if 'history' in params.keys():
            self.history = History()
            self.history.history = params['history']
        try:
            self.model_factory.load(path_prefix + '_model.pkl.gz')
            self.compile_model()
            self.model.load_weights(path_prefix + '_weights.h5')
        except (AttributeError, FileNotFoundError):
            pass


class SequenceModelMixin(interface.SequenceModel):
    def __init__(self, config=None):
        self.conv3d_layers = 1
        self.convlstm2d_layers = 4
        self.kernels = 32
        self.optimizer = 'adam'
        self.dropout = 0
        self.relu_initializer = 'he_uniform'
        self.sigmoidal_initializer = 'glorot_uniform'
        self.recurrent_initializer = 'orthogonal'
        if config is not None:
            self.configure(config)

    def configure(self, config: interface.Config):
        for config in config.values():
            try:
                value = config.current_option if hasattr(config, 'current_option') else config.value
                setattr(self, config.name2var(), value)
            except AttributeError:
                warnings.warn('did not recognize config option: {}'.format(config.name))

    def _dense_conv_lstm(self, layers, connected_layers=(), conv3d=None, lstm=None) -> tuple:
        conv3d = conv3d or self.conv3d_layers
        lstm = lstm or self.convlstm2d_layers
        for _ in range(conv3d):
            (layers, connected_layers) = self._add_connected_layer(
                layers, connected_layers,
                layer_type='conv3d')
        for _ in range(lstm):
            (layers, connected_layers) = self._add_connected_layer(
                layers, connected_layers,
                layer_type='lstm')
        return (layers, connected_layers)

    def _add_connected_layer(self, layers, connected_layers, layer_type='conv3d') -> tuple:
        if layer_type == 'conv3d':
            temp_l = Conv3D(self.kernels,
                            kernel_size=(3, 3, 3),
                            activation='relu',
                            padding='same',
                            kernel_initializer=self.relu_initializer)(layers)
        else:
            temp_l = ConvLSTM2D(self.kernels,
                                kernel_size=(3, 3),
                                activation='tanh',
                                recurrent_activation='hard_sigmoid',
                                padding='same',
                                return_sequences=True,
                                kernel_initializer=self.sigmoidal_initializer,
                                recurrent_initializer=self.recurrent_initializer)(layers)
        if self.dropout > 0:
            temp_l = Dropout(self.dropout)(temp_l)
        temp_l = BatchNormalization()(temp_l)
        connected_layers += (temp_l,)
        if len(connected_layers) > 1:
            layers = Concatenate()(list(connected_layers))
        else:
            layers = connected_layers[0]
        return (layers, connected_layers)

    def save(self, path):
        with gzip.open(path, 'w') as f:
            pickle.dump(self.__dict__, f)

    def load(self, path):
        with gzip.open(path, 'r') as f:
            loaded = pickle.load(f)
        assert isinstance(loaded, dict), 'file must contain a dict. Got" {}'.format(type(loaded))
        self.__dict__ = loaded


class SequenceSegmentationModel(SequenceModelMixin):

    def calc_input_shape(self, data_shape: tuple) -> tuple:
        '''calculate input shape from data shape'''
        return (None, None, None) + data_shape[3:]

    def calc_num_categories(self, annotation_shape: tuple) -> int:
        '''calculate num_categories from annotation shape'''
        return annotation_shape[3]

    def compile(self, input_shape=(None, None, None, 1), data_shape=None, num_categories=1) -> Model:
        '''assemble and compile the model.

        input shape is either given directly or calculated from data shape
        '''
        if data_shape is not None:
            input_shape = self.calc_input_shape(data_shape)
        i = Input(input_shape)
        layers = i
        layers, connected_layers = self._dense_conv_lstm(
            layers, conv3d=self.conv3d_layers - 1, lstm=self.convlstm2d_layers - 1)
        layers, _ = self._dense_conv_lstm(layers, connected_layers, conv3d=1, lstm=1)
        o = Conv3D(num_categories, kernel_size=(3, 3, 3), activation='sigmoid', padding='same')(layers)
        model = Model(inputs=i, outputs=o)
        model.compile(loss=loss.dice_loss, optimizer=self.optimizer)
        return model


class SequenceClassificationModel(SequenceModelMixin):
    def __init__(self, config=None):
        self.reduction_layers = 3
        self.reduction_layers_step = 1
        self.grow_kernels = 1.0
        self.fully_connected = False
        super().__init__(config=config)

    def calc_input_shape(self, data_shape: tuple) -> tuple:
        '''calculate input shape from data shape'''
        return (data_shape[0], None, None) + data_shape[3:]

    def calc_num_categories(self, annotation_shape: tuple) -> int:
        '''calculate num_categories from annotation shape'''
        return annotation_shape[1]

    def compile(self, input_shape=(64, None, None, 1), data_shape=None, num_categories=6) -> Model:
        '''assemble and compile the model.

        input shape is either given directly or calculated from data shape
        '''
        if data_shape is not None:
            input_shape = self.calc_input_shape(data_shape)
        i = Input(input_shape)
        layers = i
        layers, connected_layers = self._dense_conv_lstm(layers)
        if not self.fully_connected:
            num_kernels = self.kernels * (self.conv3d_layers + self.convlstm2d_layers)
        else:
            num_kernels = self.kernels
        for _ in range(self.reduction_layers):
            (layers, connected_layers, num_kernels) = self._add_reduction_layer(
                layers,
                connected_layers,
                num_kernels)
        if self.dropout > 0:
            layers = Dropout(self.dropout)(layers)
        layers = BatchNormalization()(layers)
        if self.fully_connected:
            connected_layers += (layers,)
            c_l = ()
            for l in connected_layers:
                c_l += (TimeDistributed(GlobalMaxPooling2D())(l),)
            layers = Concatenate()(list(c_l))
        else:
            layers = TimeDistributed(GlobalMaxPooling2D())(layers)
        o = TimeDistributed(Dense(num_categories,
                                  activation='sigmoid',
                                  kernel_initializer=self.sigmoidal_initializer))(layers)
        model = Model(inputs=i, outputs=o)
        model.compile(loss=loss.dice_loss, optimizer=self.optimizer)
        return model

    def _add_reduction_layer(self, layers, connected_layers, num_kernels) -> tuple:
        layers = MaxPooling3D(pool_size=(1, 2, 2))(layers)
        num_kernels = int(num_kernels * self.grow_kernels)
        for _ in range(self.reduction_layers_step):
            if self.dropout > 0:
                layers = Dropout(self.dropout)(layers)
            layers = BatchNormalization()(layers)
            if self.fully_connected:
                connected_layers += (layers,)
            layers = Conv3D(num_kernels,
                            (3, 3, 3),
                            activation='relu',
                            padding='same',
                            kernel_initializer=self.relu_initializer)(layers)
        return (layers, connected_layers, num_kernels)


class StepDecayScheduler:
    def __init__(self, initial_lrate=0.002, drop=0.5, epochs_drop=8.0):
        self.initial_lrate = initial_lrate
        self.drop = drop
        self.epochs_drop = epochs_drop

    def step_decay(self, epoch) -> float:
        lrate = self.initial_lrate * np.power(self.drop,
                                              np.floor((1 + epoch) / self.epochs_drop))
        return lrate


class PlotLosses(Callback):
    def __init__(self):
        Callback.__init__(self)
        self.fig = None
        self.ax = None
        self.canvas = None

    def create_fig(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def set_canvas(self, canvas):
        self.canvas = canvas
        self.canvas.update()
        self.ax.clear()
        self.ax.text(0.25, 0.5, 'starting training, please wait...')
        self.canvas.update()

    def on_train_begin(self, logs={}):
        self.i = 1
        self.x = []
        self.losses = []
        self.val_losses = []
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1
        self.ax.clear()
        self.ax.plot(self.x, self.losses, label="loss", figure=self.fig)
        self.ax.plot(self.x, self.val_losses, label="val_loss", figure=self.fig)
        self.ax.legend()
        plt.xlabel('epochs')
        plt.ylabel('loss')
        self.canvas.update()


class TrainingDataGenerator(interface.TrainingDataGenerator):
    '''generator for training data'''

    def __init__(self, x=None, y=None, batch_size=8, len_sequences=64, test_size=0.2):
        self.batch_size = batch_size
        self.len_sequences = len_sequences
        self.test_size = test_size
        self.random_state = 42
        self.x_train = self.x_test = self.y_train = self.y_test = None
        if x is not None:
            self.set_data(x, y)

    def set_data(self, x: list, y: list):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            x, y, test_size=self.test_size, random_state=self.random_state)

    @property
    def data_shape(self):
        '''shape of the data that is generated'''
        return (self.len_sequences,) + self.x_train[0].shape[1:]

    @property
    def annotation_shape(self):
        '''shape of the annotations that are generated'''
        return (self.len_sequences,) + self.y_train[0].shape[1:]

    def steps_per_epoch(self):
        '''number of steps per epoch (total number of datapoints/batch size'''
        return int(sum([x.shape[0] for x in self.x_train]) / self.len_sequences / self.batch_size)

    def generator(self, train=True, aug_shift=0):
        '''data generator that returns batches of data and annotations'''
        if train:
            x = self.x_train
            y = self.y_train
        else:
            x = self.x_test
            y = self.y_test
        indices = list(range(len(x)))
        np.random.shuffle(indices)
        sample_no = 0
        while True:
            stacks = []
            labels = []
            while len(stacks) < self.batch_size:
                stack = np.zeros((0,) + x[0].shape[1:])
                label = np.zeros((0,) + y[0].shape[1:])
                while stack.shape[0] < self.len_sequences:
                    if sample_no > len(indices) - 1:
                        np.random.shuffle(indices)
                        sample_no = 0
                    sample = x[indices[sample_no]]
                    missing_frames = self.len_sequences - stack.shape[0]
                    if sample.shape[0] <= missing_frames:
                        stack = np.vstack((stack, sample))
                        label = np.vstack((label, y[indices[sample_no]]))
                    else:
                        stack = np.vstack((stack, sample[:missing_frames, ]))
                        label = np.vstack((label, y[indices[sample_no]][:missing_frames, ]))
                    sample_no += 1
                if aug_shift > 0:
                    from scipy.ndimage import shift
                    dx = np.random.randint(-aug_shift, aug_shift)
                    dy = np.random.randint(-aug_shift, aug_shift)
                    stack = shift(stack, (0, dx, dy, 0), order=0, mode='nearest')
                # TODO: (prio 3) add augmentation for junction image size and framerate
                stacks.append(stack)
                labels.append(label)
            yield (np.array(stacks), np.array(labels))

    def validation_generator(self):
        '''data used exclusively for validation'''
        return self.generator(train=False)

    def validation_steps(self):
        '''number of steps per epoch (total number of datapoints/batch size'''
        return int(sum([x.shape[0] for x in self.x_test]) / self.len_sequences / self.batch_size)

    def save(self, path_prefix):
        np.savez_compressed(path_prefix + '_data.npz',
                            x_train=np.array(self.x_train), y_train=np.array(self.y_train),
                            x_test=np.array(self.x_test), y_test=np.array(self.y_test))
        params = {'batch_size': self.batch_size, 'len_sequences': self.len_sequences}
        with gzip.open(path_prefix + '_params.pkl.gz', 'w') as f:
            pickle.dump(params, f)

    def load(self, path_prefix):
        with np.load(path_prefix + '_data.npz') as data:
            self.x_train = list(data['x_train'])
            self.y_train = list(data['y_train'])
            self.x_test = list(data['x_test'])
            self.y_test = list(data['y_test'])
        with gzip.open(path_prefix + '_params.pkl.gz', 'r') as f:
            params = pickle.load(f)
        self.batch_size = params['batch_size']
        self.len_sequences = params['len_sequences']
