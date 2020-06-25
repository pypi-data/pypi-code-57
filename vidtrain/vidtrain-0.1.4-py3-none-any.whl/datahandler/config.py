import pickle
import gzip
import collections
from . import interface


def create_config_item(name, value, **kw):
    '''Factory method for config items.'''
    if type(value) == str:
        return StringConfigItem(name=name, value=value, **kw)
    elif type(value) == int:
        if 'options' in kw.keys():
            return OptionConfigItem(name=name, value=value, **kw)
        else:
            return IntConfigItem(name=name, value=value, **kw)
    elif type(value) == float:
        return FloatConfigItem(name=name, value=value, **kw)
    elif type(value) == dict:
        return Config(panel_name=name, **value)
    elif isinstance(value(interface.Config, interface.ConfigItem)):
        return value
    else:
        raise ValueError('Value must be str, int, float, ConfigItem, dict or Config. Got {}'.format(type(value)))


def _empty_callback(val=None):
    pass


class Config(interface.Config):
    def __init__(self, *args, panel_name=None, **kw):
        self.panel_name = panel_name
        collections.UserDict.__init__(self, *args, **kw)

    def new_item(self, name, value, **kw):
        self.data[name] = create_config_item(name, value, **kw)

    def update(self, d):
        for name, value in d.items():
            if isinstance(value, dict):
                self.data[name] = create_config_item(name, **value)
            else:
                self.data[name] = create_config_item(name, value)

    def save(self, path):
        with gzip.open(path, 'w') as f:
            pickle.dump(self.data, f)

    def load(self, path):
        with gzip.open(path, 'r') as f:
            loaded = pickle.load(f)
        assert isinstance(loaded, dict), 'file must contain a dict. Got" {}'.format(type(loaded))
        self.data = loaded


class ConfigItemMixin:
    DEFAULT_GUI_EL = 'entry'

    def __init__(self, name: str, value, gui_element_type='entry', on_change=_empty_callback):
        self.name = name
        self._value = self.convert_val(value)
        self.default_value = value
        self.gui_element_type = gui_element_type
        self.on_change = on_change

    @property
    def value(self):
        '''Any: Value of the configuration item'''
        return self._value

    @value.setter
    def value(self, val):
        val = self.convert_val(val)
        change = val != self._value
        self._value = val
        if change:
            self.on_change(val)

    @property
    def default_value(self):
        '''Any: Default value of the configuration item'''
        return self._default_value

    @default_value.setter
    def default_value(self, val):
        self._default_value = self.convert_val(val)

    @property
    def gui_element_type(self):
        '''The gui element that should be used by the user to set the config item'''
        return self._gui_element_type

    @gui_element_type.setter
    def gui_element_type(self, element_type):
        if element_type not in self.GUI_ELEMENT_TYPES:
            element_type = self.DEFAULT_GUI_EL
        self._gui_element_type = element_type

    @property
    def on_change(self):
        '''Callable: A callback that is executed when the value changes'''
        return self._on_change

    @on_change.setter
    def on_change(self, callback):
        self._on_change = callback

    def is_valid(self, val):
        try:
            test = self.convert_val(val)
            return test is not None
        except Exception:
            return False

    def reset(self):
        '''Reset value to default_value.'''
        self.value = self.default_value

    def name2var(self) -> str:
        '''convert the name to a variable name'''
        return self.name.lower().replace(' ', '_')


class StringConfigItem(ConfigItemMixin, interface.ConfigItem):

    def convert_val(self, val):
        '''Ensure that val is a string (convert it if necessary).'''
        return str(val)


class OptionConfigItem(ConfigItemMixin, interface.OptionConfigItem):
    '''Configuration item that allows selecting one or more predefined options'''
    GUI_ELEMENT_TYPES = ['spinbox', 'radio', 'checkbox']
    DEFAULT_GUI_EL = 'spinbox'

    def __init__(self, name, value, options, gui_element_type='spinbox', on_change=_empty_callback):
        self.on_options_change = _empty_callback
        self.options = options
        ConfigItemMixin.__init__(self, name=name, value=value,
                                 gui_element_type=gui_element_type, on_change=on_change)

    @property
    def options(self):
        '''list of options'''
        return self._options

    @options.setter
    def options(self, option_list):
        assert isinstance(option_list, list)
        self._options = option_list
        if hasattr(self, '_value'):
            self.value = self.value  # ensure that value is still valid
        self.on_options_change()

    @property
    def current_option(self):
        return self.options[self.value]

    @current_option.setter
    def current_option(self, option):
        self.value = self.options.index(option)

    @property
    def to(self):
        return len(self.options) - 1

    @property
    def from_(self):
        return 0

    @property
    def on_options_change(self):
        return self._on_options_change

    @on_options_change.setter
    def on_options_change(self, callback):
        self._on_options_change = callback

    def toggle(self):
        if self.value == self.to:
            self.value = 0
        else:
            self.value += 1

    def convert_val(self, val):
        '''Ensure that val is a valid index of options.'''
        val = int(val)
        if val > self.to:
            val = self.to
        if val < self.from_:
            val = self.from_
        return val


class FloatConfigItem(ConfigItemMixin, interface.NumericConfigItem):
    DEFAULT_GUI_EL = 'slider'

    def __init__(self, name, value, gui_element_type='slider', on_change=_empty_callback, increment=0.1, from_=0, to=10):
        self._increment = increment
        self.from_ = from_
        self.to = to
        super().__init__(name=name, value=value,
                         gui_element_type=gui_element_type, on_change=on_change)

    @property
    def increment(self):
        '''increment'''
        return self._increment

    @increment.setter
    def increment(self, inc):
        '''increment'''
        self._increment = float(inc)
        self.value = self.value

    @property
    def from_(self):
        '''min value'''
        return self._from

    @from_.setter
    def from_(self, from_):
        '''min value'''
        self._from = self.check(from_)

    @property
    def to(self):
        '''max value'''
        return self._to

    @to.setter
    def to(self, to):
        '''max value'''
        self._to = self.check(to)

    def round(self, val):
        '''Ensure that val is a multiple of "increment".'''
        if hasattr(self, '_increment'):
            val = round(float(val) / self.increment) * self.increment
        return val

    def check(self, val):
        '''Ensure that val is a float (convert it if necessary).'''
        return float(self.round(val))

    def convert_val(self, val):
        '''Ensure that val is a float and a multiple of "increment" (convert it if necessary).'''
        val = self.check(val)
        if val > self.to:
            val = self.to
        if val < self.from_:
            val = self.from_
        return val


class IntConfigItem(FloatConfigItem):
    def __init__(self, name, value, gui_element_type='slider', on_change=_empty_callback, increment=1, from_=0, to=100):
        FloatConfigItem.__init__(self, name=name, value=value,
                                 gui_element_type=gui_element_type, on_change=on_change,
                                 increment=increment, from_=from_, to=to)

    @property
    def increment(self):
        '''increment'''
        return self._increment

    @increment.setter
    def increment(self, inc):
        '''increment'''
        self._increment = int(inc)
        self.value = self.value

    def check(self, val):
        '''Ensure that val is an int (convert it if necessary).'''
        return int(self.round(val))
