import abc
import collections


class Rotatable(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def rot(self):
        '''integer: stores the rotation in radians'''

    @property
    @abc.abstractmethod
    def flipped(self):
        '''boolean: stores the flipped state'''

    @abc.abstractmethod
    def rotate(self):
        '''rotate the rotatable object'''

    def flip(self):
        '''flip the rotatable object'''

    def update(self):
        '''update the respective GUI element'''


class Image(metaclass=abc.ABCMeta):
    '''create a matplotlib image'''

    @abc.abstractmethod
    def __init__(self, image, figsize: tuple, cmap='gray'):
        '''Arguments:
        image: numpy ndarray
        figsize: tuple (width, heigth) image size in inches
        '''

    @property
    @abc.abstractmethod
    def fig(self):
        '''matplotlib figure'''

    @property
    @abc.abstractmethod
    def ax(self):
        '''matplotlib axes'''

    @abc.abstractmethod
    def update(self, image):
        '''update the image with new data
        Arguments:
        image: numpy ndarray
        '''


class ZoomImage(Image):
    '''create a matplotlib image that can easily be zoomed'''

    @abc.abstractmethod
    def __init__(self, image, zoom=1, cmap='gray'):
        '''Arguments:
        image: numpy ndarray
        zoom: the zoom factor (optional)
        '''


class SaveLoad(metaclass=abc.ABCMeta):
    '''Base class for classes that can save and load data to/from files.'''

    @abc.abstractmethod
    def load(self, path):
        '''load data from file'''

    @abc.abstractmethod
    def save(self, path):
        '''save data to file'''


class IsEmpty(metaclass=abc.ABCMeta):
    '''Interface for classes that can be empty'''
    @abc.abstractmethod
    def empty(self) -> bool:
        '''return True if the class does not contain data, False otherwise'''


class Config(collections.UserDict, SaveLoad, metaclass=abc.ABCMeta):
    '''A Configuration must be an implementation of MutableSequence that accepts only ConfigItems or Config as elements'''

    @property
    def panel_name(self):
        '''string: Name of the configuration panel'''
        return self._panel_name

    @panel_name.setter
    def panel_name(self, name):
        assert isinstance(name, str) or name is None, 'panel_name must be str or None'
        self._panel_name = name

    @abc.abstractmethod
    def new_item(self, name, value, **kw):
        '''Create a new ConfigItem and add it to the Config sequence'''

    @abc.abstractmethod
    def update(self, d):
        '''parse a dict, create and add the respective ConfigItems'''

    def parse(self, val):
        if isinstance(val, (ConfigItem, Config)):
            return val
        else:
            raise ValueError('Config items must be Config or ConfigItem, got {}'.format(type(val)))

    def __setitem__(self, key, val):
        self.data[key] = self.parse(val)


class ConfigItem(metaclass=abc.ABCMeta):
    GUI_ELEMENT_TYPES = ['entry']

    @property
    def name(self):
        '''string: Name of the configuration item'''
        return self._name

    @name.setter
    def name(self, name):
        assert isinstance(name, str)
        self._name = name

    @property
    @abc.abstractmethod
    def value(self):
        '''Any: Value of the configuration item'''

    @property
    @abc.abstractmethod
    def default_value(self):
        '''Any: Default value of the configuration item'''

    @property
    @abc.abstractmethod
    def gui_element_type(self):
        '''The gui element that should be used by the user to set the config item'''

    @property
    @abc.abstractmethod
    def on_change(self):
        '''Callable: A callback that is executed when the value changes'''

    @abc.abstractmethod
    def convert_val(self, val):
        '''Ensure that val is valid for value and default_value.'''

    @abc.abstractmethod
    def is_valid(self, val):
        '''Check that val can be converted into a valid value by convert_val.'''

    @abc.abstractmethod
    def reset(self):
        '''Reset the value to default_value.'''

    @abc.abstractmethod
    def name2var(self) -> str:
        '''convert the name to a variable name'''


class NumericConfigItem(ConfigItem):
    GUI_ELEMENT_TYPES = ['slider', 'spinbox']
    @property
    @abc.abstractmethod
    def increment(self):
        '''increment'''

    @property
    @abc.abstractmethod
    def from_(self):
        '''min value'''

    @property
    @abc.abstractmethod
    def to(self):
        '''max value'''

    @abc.abstractmethod
    def check(self, val):
        '''Ensure that val is valid for from_ and to.'''


class StringConfigItem(ConfigItem):
    pass


class OptionConfigItem(ConfigItem):

    @property
    @abc.abstractmethod
    def options(self):
        '''list of options'''

    @property
    @abc.abstractmethod
    def current_option(self):
        '''the element in options that has the index value.

        the corresponding setter changes value to the index corresponding to its given argument'''

    @abc.abstractmethod
    def toggle(self):
        '''toggle through the options'''

    @property
    @abc.abstractmethod
    def from_(self):
        '''min value (always 0)'''

    @property
    @abc.abstractmethod
    def to(self):
        '''max value (len(options) - 1)'''

    @property
    @abc.abstractmethod
    def on_options_change(self):
        '''callback triggered when options change'''


class Stack(SaveLoad, IsEmpty):
    '''A data stack'''

    @property
    @abc.abstractmethod
    def num_slices(self):
        '''return: int: number of images in the stack'''


class ImageStack(Stack):

    @property
    @abc.abstractmethod
    def width(self):
        '''return: int: width of each image in pixels'''

    @property
    @abc.abstractmethod
    def height(self):
        '''return: int: height of each image in pixels'''

    @property
    @abc.abstractmethod
    def image_shape(self):
        '''return: tuple: shape of each image in pixels'''

    @property
    @abc.abstractmethod
    def num_channels(self):
        '''return: int: number of color channels of each image'''

    @abc.abstractmethod
    def median(self):
        '''return: 2D np.ndarray: median projection of the stack'''

    @abc.abstractmethod
    def mean(self):
        '''return: 2D np.ndarray: mean projection of the stack'''

    @abc.abstractmethod
    def std(self):
        '''return: 2D np.ndarray: standard deviation projection of the stack'''

    @abc.abstractmethod
    def max(self):
        '''return: 2D np.ndarray: maximum projection of the stack'''

    @abc.abstractmethod
    def copy_tile(self, pos, dim):
        '''copy a tile out of the stack.
        Arguments:
        tuple pos: x and y coordinates
        typle dim: wdth and height of the tile
        return: 4D np.ndarray: copy a part of the stack'''


class MultiImageStack(collections.UserDict, SaveLoad, IsEmpty):
    '''many image stacks stored as collections.UserDict'''

    @abc.abstractmethod
    def np_array(self):
        '''return np.array(self.data.values())'''

    @abc.abstractmethod
    def image_stacks(self, key=None):
        '''return a generator that yields ImageStacks. 
        if key is provided, an individual ImageStack is created from the data corresponding to that key.
        '''


class ImageStackClassification(Stack):
    '''Image stack classification'''

    @property
    @abc.abstractmethod
    def category_names(self):
        '''generator that returns category names.
        names are either generated on the fly or returned from a list stored the category_names.setter
        '''

    @property
    @abc.abstractmethod
    def num_categories(self):
        '''the number of categories'''


class MultiImageStackClassification(MultiImageStack):
    '''many image stack classifications stored as collections.UserDict'''

    def create_from_multi_image_stack(self, mis: MultiImageStack):
        '''calculate data according to the data shape of MultiImageStack'''


class FormatTrainingData():
    @abc.abstractmethod
    def __init__(self, slice_len, slice_padding):
        '''initialize with slice_len and slice padding arguments'''

    @abc.abstractmethod
    def apply(self, x, y):
        '''slice the numpy arrays in dict x and y into slices and concatenate the slices into a list
        x and y must have identical keys and the first dimension of the numpy arrays must match
        '''


class TrainingDataGenerator(SaveLoad):
    '''generator for training data'''

    @property
    @abc.abstractmethod
    def data_shape(self):
        '''shape of the data that is generated'''

    @property
    @abc.abstractmethod
    def annotation_shape(self):
        '''shape of the annotations that are generated'''

    @abc.abstractmethod
    def steps_per_epoch(self):
        '''number of steps per epoch (total number of datapoints/batch size'''

    @abc.abstractmethod
    def generator(self):
        '''data generator that returns batches of data and annotations'''

    @abc.abstractmethod
    def validation_generator(self):
        '''data used exclusively for validation'''

    @abc.abstractmethod
    def validation_steps(self):
        '''number of steps per epoch (total number of datapoints/batch size'''


class NetworkList(SaveLoad, IsEmpty):
    pass


class NetworkTrainer(SaveLoad):
    def __init__(self, model_factory=None, training_config=None):
        pass

    @abc.abstractmethod
    def compile_model(self):
        '''use model_factory to create and compile a keras model'''

    @abc.abstractmethod
    def draw_model(self, file_name):
        '''draw the model'''

    @abc.abstractmethod
    def train(self):
        '''train the model'''

    @abc.abstractmethod
    def get_fig(self):
        '''get the figure handle for the loss plot'''

    @abc.abstractmethod
    def get_ax(self):
        '''get the axis handle for the loss plot'''

    @abc.abstractmethod
    def set_canvas(self, canvas):
        '''set the canvas for the loss plot'''


class SequenceModel(SaveLoad):

    @abc.abstractmethod
    def configure(self, config: Config):
        '''apply configuration settings'''

    @abc.abstractmethod
    def calc_input_shape(self, data_shape: tuple) -> tuple:
        '''calculate input shape from data shape'''

    @abc.abstractmethod
    def calc_num_categories(self, annotation_shape: tuple) -> int:
        '''calculate num_categories from annotation shape'''

    @abc.abstractmethod
    def compile(self, input_shape, data_shape, output_classes):
        '''assemble and compile the model.

        input shape is either given directly or calculated from data shape
        '''


class PredictionFormatter():
    '''Format data so that it can be passed to SequenceModel.predict and reverse-format predictions'''
    @abc.abstractmethod
    def __init__(self, sequence_len=64, time_overlap=16):
        '''Arguments:
        sequence_len: int, total length of sequences
        time_overlap: int, number of frames that individual sequences should overlap
        '''

    @abc.abstractmethod
    def apply(self, data: MultiImageStack):
        '''Split all stacks in data into substacks of length sequence_len.

        Arguments:
        data: interface.MultiImageStack, data to be split

        Returns:
        numpy.ndarray split stacks
        '''

    @abc.abstractmethod
    def revert(self, data: MultiImageStack, y_pred):
        '''concatenate y_pred into stacks that match the shape of the stacks in data

        Arguments:
        data: MultiImageStack, original data used as template for predicted data
        y_pred: numpy.ndarray, prediction results

        Returns:
        MultiImageStackClassification
        '''


class WorkflowData(metaclass=abc.ABCMeta):
    '''Stores all workflow data as properties.'''

    @property
    @abc.abstractmethod
    def path(self):
        '''path where the data will be stored'''


class VidtrainDataLossException(Exception):
    pass
