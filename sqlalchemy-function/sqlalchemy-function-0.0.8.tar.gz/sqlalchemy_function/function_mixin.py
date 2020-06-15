"""# Function mixin"""

from sqlalchemy import Column, Integer, PickleType
from sqlalchemy.inspection import inspect
from sqlalchemy_mutable import MutableListType, MutableDictType


class FunctionMixin():
    """
    A mixin for 'Function models'. When called, a Function model executes its 
    function, passing in its arguments and keyword arguments.

    Parameters
    ----------
    func : callable or None, default=None
        The function which the Function model will execute when called.

    \*args, \*\*kwargs :
        Arguments and keyword arguments which the Function model will pass 
        into its `func` when called. The `FunctionMixin` constructor will not
        override arguments and keyword arguments if they have already been
        set.

    Attributes
    ----------
    func : callable sqlalchemy.PickleType
        Set from the `func` parameter.

    args : sqlalchemy_mutable.MutableListType
        Set from the `*args` parameter.

    kwargs : sqlalchemy_mutable.MutableDictType
        Set from the `**kwargs` parameter.

    Examples
    --------
    In the setup, we create a SQLAlchemy session and a Function model  
    subclassing `FunctionMixin`.

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

    # subclass `FunctionMixin` to define a Function model
    class Function(FunctionMixin, Base):
    \    __tablename__ = 'function'
    \    id = Column(Integer, primary_key=True)

    Base.metadata.create_all(engine)
    ```

    We can now store and later call functions as follows.

    ```python
    def foo(*args, **kwargs):
    \    print('My args are', args)
    \    print('My kwargs are', kwargs)
    \    return 'return value'

    func = Function(foo, 'hello world', goodbye='moon')
    func()
    ```

    Out:

    ```
    My args are ('hello world',)
    My kwargs are {'goodbye': 'moon'}
    'return value'
    ```
    """
    func = Column(PickleType)
    args = Column(MutableListType)
    kwargs = Column(MutableDictType)

    def __init__(self, func, *args, **kwargs):
        self.func = func
        # note that args or kwargs may have already been set
        self.args = self.args or list(args)
        self.kwargs = self.kwargs or kwargs
        super().__init__()

    def set(self, func, *args, **kwargs):
        """
        Set the function, arguments, and keyword arguments.

        Parameters
        ----------
        func : callable or None, default=None
            The function which the Function model will execute when called.

        \*args, \*\*kwargs :
            Arguments and keyword arguments which the Function model will pass 
            into its `func` when called.

        Returns
        -------
        self : sqlalchemy_function.FunctionMixin
        """
        self.func, self.args, self.kwargs = func, list(args), kwargs
        return self
    
    def __call__(self):
        """
        Call `self.func`, passing in `*self.args, **self.kwargs`.

        **Note.** If the arguments or keyword arguments contain database 
        models, they will be 'unshelled' when they are passed into the 
        function. See <https://dsbowen.github.io/sqlalchemy-mutable/> for more
        detail.

        Returns
        -------
        output : 
            Output of `self.func`.
        """
        if self.func is None:
            return
        return self.func(*self.args.unshell(), **self.kwargs.unshell())