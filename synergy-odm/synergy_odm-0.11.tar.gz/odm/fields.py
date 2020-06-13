__author__ = 'Bohdan Mushkevych'

import re
import decimal
import datetime

from odm.errors import ValidationError
DEFAULT_DT_FORMAT = '%Y-%m-%d %H:%M:%S'


class BaseField:
    """A base class for fields in a Synergy ODM document. Instances of this class
    may be added to subclasses of `Document` to define a document's schema. """

    # Creation counter keeps track of Fields declaration order in the Document
    # Each time a Field instance is created the counter should be increased
    creation_counter = 0

    def __init__(self, name:str=None, default=None, choices=None, verbose_name:str=None, null:bool=False):
        """
        :param name: (optional) name of the field in the JSON document
            if not set, variable name will be taken as the name
            i.e. `a = Field() -> a.name == 'a'`
        :param default: (optional) The default value for this field if no value
            has been set (or if the value has been unset).  It can be a
            callable.
        :param choices: (optional) The valid choices
        :param verbose_name: (optional) The human readable, verbose name for the field.
        :param null: (optional) Is the field value can be null. If no and there is a default value
            then the default value is set
        """
        self.name = name
        self._default = default
        self.choices = choices
        self.verbose_name = verbose_name
        self.null = null
        self.creation_counter = BaseField.creation_counter + 1
        BaseField.creation_counter += 1

    @property
    def default(self):
        if self._default is None:
            return None

        value = self._default
        if callable(value):
            value = value()
        return value

    def initialized(self, instance):
        if instance is None:
            # Document class being used rather than a document object. Guessing True
            return True
        return instance._data.get(self.name) is not None

    def __get__(self, instance, owner):
        """ Descriptor for retrieving a value from a field in a document. """
        if instance is None:
            # Document class being used rather than a document object
            return self

        # retrieve value from a BaseDocument instance if available
        value = instance._data.get(self.name)
        if value is not None or self.null:
            return value

        # value is None at this point
        if self.default is not None:
            value = self.default
            self.validate(value)
            instance._data[self.name] = value
        return value

    def __set__(self, instance, value):
        """ Descriptor for assigning a value to a field in a document. """
        if value is not None:
            self.validate(value)
            instance._data[self.name] = value
        elif self.null:
            # value is None and self.null is True
            # skip validation; force setting value to None
            instance._data[self.name] = value
        elif self.default is not None:
            # value is None and self.null is False and self.default is not None
            value = self.default
            self.validate(value)
            instance._data[self.name] = value
        else:
            # value is None and self.null is False and self.default is None
            # let the self.validate take care of reporting the exception
            self.validate(value)
            instance._data[self.name] = value

    def __delete__(self, instance):
        if self.name in instance._data:
            del instance._data[self.name]

    def __set_name__(self, owner, name):
        if hasattr(self, 'name') and self.name is not None:
            # field was initialized with a custom name
            pass
        else:
            self.name = name

    def raise_error(self, message='', errors=None, name=None):
        """Raises a ValidationError. """
        raise ValidationError(message, errors=errors, field_name=name if name else self.name)

    def from_json(self, value):
        """Convert a JSON-variable to a Python type. """
        return value

    def to_json(self, value):
        """Convert a Python type to a JSON-friendly type. """
        return self.from_json(value)

    def validate(self, value):
        """Performs validation of the value.
        :param value: value to validate
        :raise ValidationError if the value is invalid"""

        # check choices
        if self.choices:
            if isinstance(self.choices[0], (list, tuple)):
                option_keys = [k for k, v in self.choices]
                if value not in option_keys:
                    msg = f'Value {value} is not listed among valid choices {option_keys}'
                    self.raise_error(msg)
            elif value not in self.choices:
                msg = f'Value {value} is not listed among valid choices {self.choices}'
                self.raise_error(msg)


class NestedDocumentField(BaseField):
    """ Field wraps a stand-alone Document """

    def __init__(self, nested_klass, **kwargs):
        """
        :param nested_klass: BaseDocument-derived class
        :param kwargs: standard set of arguments from the BaseField
        """
        self.nested_klass = nested_klass
        kwargs.setdefault('default', lambda: nested_klass())
        super(NestedDocumentField, self).__init__(**kwargs)

    def validate(self, value):
        """Make sure that value is of the right type """
        if not isinstance(value, self.nested_klass):
            self.raise_error('NestedClass is of the wrong type: {0} vs expected {1}'
                             .format(value.__class__.__name__, self.nested_klass.__name__))
        super(NestedDocumentField, self).validate(value)


class ListField(BaseField):
    """ Field represents standard Python collection `list` """

    def __init__(self, **kwargs):
        kwargs.setdefault('default', lambda: [])
        super(ListField, self).__init__(**kwargs)

    def validate(self, value):
        """Make sure that the inspected value is of type `list` or `tuple` """
        if not isinstance(value, (list, tuple)):
            self.raise_error(f'Only lists and tuples may be used in the ListField vs provided {type(value).__name__}')
        super(ListField, self).validate(value)


class DictField(BaseField):
    """A dictionary field that wraps a standard Python dictionary. This is
    similar to an embedded document, but the structure is not defined. """

    def __init__(self, **kwargs):
        kwargs.setdefault('default', lambda: {})
        super(DictField, self).__init__(**kwargs)

    def validate(self, value):
        """Make sure that the inspected value is of type `dict` """
        if not isinstance(value, dict):
            self.raise_error(f'Only Python dict may be used in the DictField vs provided {type(value).__name__}')
        super(DictField, self).validate(value)


class StringField(BaseField):
    """A unicode string field. """

    def __init__(self, regex=None, min_length=None, max_length=None, **kwargs):
        self.regex = re.compile(regex) if regex else None
        self.min_length, self.max_length = min_length, max_length
        super(StringField, self).__init__(**kwargs)

    def __set__(self, instance, value):
        value = self.from_json(value)
        super(StringField, self).__set__(instance, value)

    def from_json(self, value):
        if value is None:
            # NoneType values are not jsonified by BaseDocument
            return value

        if isinstance(value, str):
            return value
        elif not isinstance(value, (bytes, str)):
            return str(value)
        else:
            try:
                value = value.decode('utf-8')
            except:
                pass
            return value

    def validate(self, value):
        if not isinstance(value, (bytes, str)):
            self.raise_error(f'Only string types may be used in the StringField vs provided {type(value).__name__}')

        if self.max_length is not None and len(value) > self.max_length:
            self.raise_error('StringField value {0} length {1} is longer than max_length {2}'
                             .format(value, len(value), self.max_length))

        if self.min_length is not None and len(value) < self.min_length:
            self.raise_error('StringField value {0} length {1} is shorter than min_length {2}'
                             .format(value, len(value), self.min_length))

        if self.regex is not None and self.regex.match(value) is None:
            self.raise_error(f'StringField value "{value}" did not match validation regex "{self.regex}"')

        super(StringField, self).validate(value)


class IntegerField(BaseField):
    """ An integer field. """

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(IntegerField, self).__init__(**kwargs)

    def __set__(self, instance, value):
        value = self.from_json(value)
        super(IntegerField, self).__set__(instance, value)

    def from_json(self, value):
        if value is None:
            # NoneType values are not jsonified by BaseDocument
            return value

        if isinstance(value, int):
            return value
        try:
            value = int(value)
        except ValueError:
            pass
        return value

    def validate(self, value):
        try:
            value = int(value)
        except:
            self.raise_error(f'Could not parse {value} into an Integer')

        if self.min_value is not None and value < self.min_value:
            self.raise_error(f'IntegerField value {value} is lower than min value {self.min_value}')

        if self.max_value is not None and value > self.max_value:
            self.raise_error(f'IntegerField value {value} is larger than max value {self.max_value}')

        super(IntegerField, self).validate(value)


class DecimalField(BaseField):
    """A fixed-point decimal number field. """

    def __init__(self, min_value=None, max_value=None, force_string=False,
                 precision=2, rounding=decimal.ROUND_HALF_UP, **kwargs):
        """
        :param min_value: Validation rule for the minimum acceptable value.
        :param max_value: Validation rule for the maximum acceptable value.
        :param force_string: Store as a string.
        :param precision: Number of decimal places to store.
        :param rounding: The rounding rule from the python decimal library:

            - decimal.ROUND_CEILING (towards Infinity)
            - decimal.ROUND_DOWN (towards zero)
            - decimal.ROUND_FLOOR (towards -Infinity)
            - decimal.ROUND_HALF_DOWN (to nearest with ties going towards zero)
            - decimal.ROUND_HALF_EVEN (to nearest with ties going to nearest even integer)
            - decimal.ROUND_HALF_UP (to nearest with ties going away from zero)
            - decimal.ROUND_UP (away from zero)
            - decimal.ROUND_05UP (away from zero if last digit after rounding towards zero would have been 0 or 5;
                                  otherwise towards zero)

            Defaults to: ``decimal.ROUND_HALF_UP``

        """
        self.force_string = force_string
        self.precision = precision
        self.rounding = rounding
        self.min_value = self.from_json(min_value)
        self.max_value = self.from_json(max_value)

        super(DecimalField, self).__init__(**kwargs)

    def __get__(self, instance, owner):
        value = super(DecimalField, self).__get__(instance, owner)
        if value is self:
            return value
        return self.to_json(value)

    def __set__(self, instance, value):
        value = self.from_json(value)
        super(DecimalField, self).__set__(instance, value)

    def from_json(self, value):
        if value is None:
            # NoneType values are not jsonified by BaseDocument
            return value

        if isinstance(value, decimal.Decimal):
            return value
        try:
            value = decimal.Decimal(str(value))
        except decimal.InvalidOperation:
            return value
        return value.quantize(decimal.Decimal('.{0}'.format('0' * self.precision)), rounding=self.rounding)

    def to_json(self, value):
        if value is None:
            # NoneType values are not jsonified by BaseDocument
            return value

        if self.force_string:
            return str(value)
        else:
            return float(self.from_json(value))

    def validate(self, value):
        if not isinstance(value, decimal.Decimal):
            if not isinstance(value, (bytes, str)):
                value = str(value)
            try:
                value = decimal.Decimal(value)
            except Exception:
                self.raise_error(f'Could not parse {value} into a Decimal')

        if self.min_value is not None and value < self.min_value:
            self.raise_error(f'DecimalField value {value} is lower than min value {self.min_value}')

        if self.max_value is not None and value > self.max_value:
            self.raise_error(f'DecimalField value {value} is larger than max value {self.max_value}')

        # super.validate() checks if the value is among the list of allowed choices
        # most likely, it will be the list of floats and integers
        # as the Decimal does not support automatic comparison with the float, we will cast it
        super(DecimalField, self).validate(float(value))


class BooleanField(BaseField):
    """A boolean field type. """

    def __init__(self, true_values=None, false_values=None, **kwargs):
        self.true_values = true_values if true_values else ['true', 'yes', '1']
        self.false_values = false_values if false_values else ['false', 'no', '0']
        super(BooleanField, self).__init__(**kwargs)

    def __set__(self, instance, value):
        value = self.from_json(value)
        super(BooleanField, self).__set__(instance, value)

    def from_json(self, value):
        if value is None:
            # NoneType values are not jsonified by BaseDocument
            return value

        if isinstance(value, bool):
            return value
        if not isinstance(value, (bytes, str)):
            # case numbers if needed to the string
            value = str(value)
        value = value.lower().strip()

        if value in self.true_values:
            return True
        elif value in self.false_values:
            return False
        else:
            raise ValueError(f'Could not parse {value} into a bool')

    def validate(self, value):
        if not isinstance(value, bool):
            self.raise_error(f'Only boolean type may be used in the BooleanField vs provided {type(value).__name__}')


class DateTimeField(BaseField):
    """ A datetime field. Features:
    - During runtime, value is stored in datetime format
    - If a string value is assigned to the field, then it is assumed to be in dt_format
      and converted to the datetime object
    - If an integer is assigned to the field, then it is considered to represent number of seconds since epoch
      in UTC and converted to the datetime object
    - During json serialization, value is converted to the string accordingly to dt_format. """

    def __init__(self, dt_format=DEFAULT_DT_FORMAT, **kwargs):
        self.dt_format = dt_format
        super(DateTimeField, self).__init__(**kwargs)

    def __set__(self, instance, value):
        value = self.from_json(value)
        super(DateTimeField, self).__set__(instance, value)

    def validate(self, value):
        new_value = self.to_json(value)
        if not isinstance(new_value, (bytes, str)):
            self.raise_error(f'Could not parse "{value}" into a date')

    def to_json(self, value):
        if value is None:
            # NoneType values are not jsonified by BaseDocument
            return value

        if callable(value):
            value = value()

        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.strftime(self.dt_format)
        raise ValueError(f'DateTimeField.to_json unknown datetime type: {type(value).__name__}')

    def from_json(self, value):
        if value is None:
            # NoneType values are not jsonified by BaseDocument
            return value

        if isinstance(value, (datetime.datetime, datetime.date)):
            return value
        if isinstance(value, (bytes, str)):
            return datetime.datetime.strptime(value, self.dt_format)
        if isinstance(value, (int, float)):
            return datetime.datetime.utcfromtimestamp(value)
        raise ValueError(f'DateTimeField.from_json expects data of string/int/float types vs {type(value).__name__}')


class ObjectIdField(BaseField):
    """A field wrapper around ObjectIds. """

    def __get__(self, instance, owner):
        value = super(ObjectIdField, self).__get__(instance, owner)
        if value is self:
            return value
        return self.from_json(value)

    def __set__(self, instance, value):
        value = self.from_json(value)
        super(ObjectIdField, self).__set__(instance, value)

    def from_json(self, value):
        if value is None:
            # NoneType values are not jsonified by BaseDocument
            return value

        if not isinstance(value, (bytes, str)):
            value = str(value)
        return value

    def validate(self, value):
        try:
            str(value)
        except:
            self.raise_error(f'Could not parse {value} into a unicode')
