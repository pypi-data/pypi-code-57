"""# Function relator mixin"""

from .function_mixin import FunctionMixin

from sqlalchemy import Column, Integer, PickleType
from sqlalchemy.inspection import inspect
from sqlalchemy_mutable import MutableListType, MutableDictType

class FunctionRelator():
    """
    Base for database models with relationships to Function models. It 
    provides automatic conversion of functions to Function models when 
    setting attributes.

    Examples
    --------
    In the setup, we create a SQLAlchemy session, define a Parent model 
    subclassing `FunctionRelator`, and a Function model subclassing 
    `FunctionMixin`.

    ```python
    from sqlalchemy_function import FunctionMixin, FunctionRelator

    # standard session creation
    from sqlalchemy import create_engine, Column, ForeignKey, Integer
    from sqlalchemy.orm import relationship, sessionmaker, scoped_session
    from sqlalchemy.ext.declarative import declarative_base

    engine = create_engine('sqlite:///:memory:')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    Base = declarative_base()

    # subclass `FunctionRelator` for models with a relationship to Function models
    class Parent(FunctionRelator, Base):
    \    __tablename__ = 'parent'
    \    id = Column(Integer, primary_key=True)
    \    functions = relationship('Function', backref='parent')

    # subclass `FunctionMixin` to define a Function model
    class Function(FunctionMixin, Base):
    \    __tablename__ = 'function'
    \    id = Column(Integer, primary_key=True)
    \    parent_id = Column(Integer, ForeignKey('parent.id'))

    Base.metadata.create_all(engine)
    ```

    We can now set the `functions` attribute to a callable as follows.

    ```python
    def foo(*args, **kwargs):
    \    print('My args are', args)
    \    print('My kwargs are', kwargs)
    \    return 'return value'
    
    parent = Parent()
    parent.functions = foo
    # equivalent to:
    # parent.functions = [foo]
    # parent.functions = Function(foo)
    # parent.functions = [Function(foo)]
    parent.functions
    ```

    Out:

    ```
    [<__main__.Function object at 0x7f4e5a49c160>]
    ```
    """

    # FunctionRelator overrides the __setattr__ method to check for Function 
    # model relationships. These attributes need to be set through the super() 
    # method, and are considered 'exempt'.
    _exempt_attrs_fr = ['_func_rel_indicator', '_func_rel_attrs']

    def __new__(cls, *args, **kwargs):
        """
        Set class function relationship indicators and attributes.

        Attributes
        ----------
        _func_rel_indicator : dict
            Maps attribute names to boolean indicator that the attribute 
            subclasses `FunctionMixin`.

        _func_rel_attrs : dict
            Maps Function model attribute names to `(class, use_list)` tuple. 
            `class` is the Function model class. `use_list` indicates that the 
            Function model attribute is a list.
        """
        if not hasattr(cls, '_func_rel_indicator'):
            cls._func_rel_indicator = {}
            cls._func_rel_attrs = {}
        try:
            return super().__new__(cls, *args, **kwargs)
        except:
            return super().__new__(cls)

    def __setattr__(self, name, value):
        """Set attribute

        Before setting an attribute, determine if it the attribute is a 
        relationship to a Function model. If so, convert the value from a 
        function(s) to a Function model(s).
        """
        if name in self._exempt_attrs_fr:
            return super().__setattr__(name, value)
        is_func_rel = self._func_rel_indicator.get(name)
        if is_func_rel is None:
            is_func_rel = self._set_func_rel(name)
        if is_func_rel:
            model_class, use_list = self._func_rel_attrs[name]
            if use_list:
                value = self._to_function_models(value, model_class)
            else:
                value = self._to_function_model(value, model_class)
        super().__setattr__(name, value)

    @classmethod
    def _set_func_rel(cls, name):
        """
        Set the function relationship status for a previously unseen 
        attribute.

        Parameters
        ----------
        name : str
            Name of the previously unseen attribute.

        Returns
        -------
        is_func_rel : bool
            Indicates that the named attribute is a relationship to a Function 
            model.
        """
        mapper = inspect(cls).mapper
        rel = [r for r in mapper.relationships if r.key == name]
        if not (rel and FunctionMixin in rel[0].mapper.class_.__mro__):
            is_func_rel = False
        else:
            rel = rel[0]
            cls._func_rel_attrs[name] = (rel.mapper.class_, rel.uselist)
            is_func_rel = True
        cls._func_rel_indicator[name] = is_func_rel
        return is_func_rel
    
    def _to_function_models(self, funcs, model_class):
        """
        Convert a list of functions to Function models.
        
        Parameters
        ----------
        func : list of callables
            List of callables (functions) to convert

        model_class : class
            Class of the Function model to which the functions will be 
            converted.
        """
        if not isinstance(funcs, list):
            funcs = [funcs]
        models = [self._to_function_model(f, model_class) for f in funcs]
        return [m for m in models if m is not None]
    
    def _to_function_model(self, func, model_class):
        """Convert a single function to a Function model."""
        if isinstance(func, model_class):
            return func
        if callable(func):
            return model_class(func)
        if func is None:
            return None
        raise ValueError(
            'Function relationships requre Function models or callables'
        )