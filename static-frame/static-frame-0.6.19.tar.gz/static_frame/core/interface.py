'''
Tools for documenting the SF interface.
'''
import typing as tp
import inspect
from itertools import chain

import numpy as np

from static_frame.core.frame import Frame
from static_frame.core.bus import Bus

from static_frame.core.util import DT64_S
from static_frame.core.util import AnyCallable

from static_frame.core.container import ContainerBase
from static_frame.core.container import ContainerOperand

from static_frame.core.type_blocks import TypeBlocks
from static_frame.core.index_base import IndexBase

from static_frame.core.index_datetime import IndexDate
from static_frame.core.index_datetime import IndexYearMonth
from static_frame.core.index_datetime import IndexYear

from static_frame.core.index_hierarchy import IndexHierarchy
from static_frame.core.display import Display
from static_frame.core.frame import FrameAsType

from static_frame.core.node_iter import IterNodeDelegate

from static_frame.core.container import _UFUNC_BINARY_OPERATORS
from static_frame.core.container import _RIGHT_OPERATOR_MAP
from static_frame.core.container import _UFUNC_UNARY_OPERATORS

from static_frame.core.node_selector import TContainer
from static_frame.core.node_selector import Interface
from static_frame.core.node_selector import InterfaceSelectDuo
from static_frame.core.node_selector import InterfaceSelectTrio
from static_frame.core.node_selector import InterfaceAssignTrio
from static_frame.core.node_selector import InterfaceAssignQuartet

from static_frame.core.node_selector import InterfaceAsType
from static_frame.core.node_selector import InterfaceGetItem

from static_frame.core.node_dt import InterfaceDatetime
from static_frame.core.node_str import InterfaceString


#-------------------------------------------------------------------------------
# function inspection utilities

MAX_ARGS = 3

def _get_parameters(
        func: AnyCallable,
        is_getitem: bool = False,
        max_args: int = MAX_ARGS,
        ) -> str:
    # might need special handling for methods on built-ins
    try:
        sig = inspect.signature(func)
    except ValueError:
        # on Python 3.6, this error happens:
        # ValueError: no signature found for builtin <built-in function abs>
        return '[]' if is_getitem else '()'

    positional = []
    kwarg_only = ['*'] # preload
    var_positional = ''
    var_keyword = ''

    count = 0
    count_total = 0
    for p in sig.parameters.values():
        if count == 0 and p.name == 'self':
            continue # do not increment counts

        if count < max_args:
            if p.kind == p.KEYWORD_ONLY:
                kwarg_only.append(p.name)
            elif p.kind == p.VAR_POSITIONAL:
                var_positional = p.name
            elif p.kind == p.VAR_KEYWORD:
                var_keyword = p.name
            else:
                positional.append(p.name)
            count += 1
        count_total += 1

    suffix = '' if count >= count_total else f', {Display.ELLIPSIS}'

    # if truthy, update to a proper iterable
    if var_positional:
        var_positional = ('*' + var_positional,) #type: ignore
    if var_keyword:
        var_keyword = ('**' + var_keyword,)  #type: ignore

    if len(kwarg_only) > 1: # do not count the preload
        param_repr = ', '.join(chain(positional, kwarg_only, var_positional, var_keyword))
    else:
        param_repr = ', '.join(chain(positional, var_positional, var_keyword))

    if is_getitem:
        return f'[{param_repr}{suffix}]'
    return f'({param_repr}{suffix})'


def _get_signatures(
        name: str,
        func: AnyCallable,
        *,
        is_getitem: bool = False,
        delegate_func: tp.Optional[AnyCallable] = None,
        delegate_name: str = '',
        max_args: int = MAX_ARGS,
        ) -> tp.Tuple[str, str]:

    if delegate_func:
        delegate = _get_parameters(delegate_func, max_args=max_args)
        if delegate_name:
            # prefix with name
            delegate = f'.{delegate_name}{delegate}'
            delegate_no_args = f'.{delegate_name}()'
        else:
            delegate_no_args = '()'
    else:
        delegate = ''
        delegate_no_args = ''

    signature = f'{name}{_get_parameters(func, is_getitem, max_args=max_args)}{delegate}'

    if is_getitem:
        signature_no_args = f'{name}[]{delegate_no_args}'
    else:
        signature_no_args = f'{name}(){delegate_no_args}'

    return signature, signature_no_args


#-------------------------------------------------------------------------------
class Features:
    '''
    Core utilities neede by both Interface and InterfaceSummary
    '''

    DOC_CHARS = 80

    GETITEM = '__getitem__'

    EXCLUDE_PRIVATE = {
        '__class__',
        '__class_getitem__',
        '__annotations__',
        '__doc__',
        '__delattr__',
        '__dir__',
        '__dict__',
        '__format__',
        '__getattribute__',
        '__hash__',
        '__init_sbclass__',
        '__lshift__',
        '__module__',
        '__init_subclass__',
        '__new__',
        '__setattr__',
        '__setstate__',
        '__setitem__',
        '__slots__',
        '__slotnames__',
        '__subclasshook__',
        '__weakref__',
        '__reduce__',
        '__reduce_ex__',
        '__sizeof__',
        }

    DICT_LIKE = {
        'get',
        'keys',
        'values',
        'items',
        '__contains__',
        '__iter__',
        '__reversed__'
        }

    DISPLAY = {
        'display',
        'display_tall',
        'display_wide',
        '__repr__',
        '__str__',
        'interface',
        }


    @classmethod
    def scrub_doc(cls, doc: tp.Optional[str]) -> str:
        if not doc:
            return ''
        doc = doc.replace('`', '')
        doc = doc.replace(':py:meth:', '')
        doc = doc.replace(':obj:', '')
        doc = doc.replace('static_frame.', '')

        # split and join removes contiguous whitespace
        msg = ' '.join(doc.split())
        if len(msg) <= cls.DOC_CHARS:
            return msg
        return msg[:cls.DOC_CHARS].strip() + Display.ELLIPSIS


#-------------------------------------------------------------------------------
class InterfaceGroup:
    Attribute = 'Attribute'
    Constructor = 'Constructor'
    DictLike = 'Dictionary-Like'
    Display = 'Display'
    Exporter = 'Exporter'
    Iterator = 'Iterator'
    Method = 'Method'
    OperatorBinary = 'Operator Binary'
    OperatorUnary = 'Operator Unary'
    Selector = 'Selector'
    Assignment = 'Assignment'
    AccessorString = 'Accessor String'
    AccessorDatetime = 'Accessor Datetime'


class InterfaceRecord(tp.NamedTuple):

    cls_name: str
    group: str # should be InterfaceGroup
    signature: str
    doc: str
    reference: str = '' # a qualified name as a string for doc gen
    use_signature: bool = False
    is_attr: bool = False
    delegate_reference: str = ''
    delegate_is_attr: bool = False
    signature_no_args: str = ''

    @classmethod
    def gen_from_dict_like(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:
        if name == 'values':
            signature = signature_no_args = name
        else:
            signature, signature_no_args = _get_signatures(
                    name,
                    obj,
                    is_getitem=False,
                    max_args=max_args,
                    )
        yield cls(cls_name,
                InterfaceGroup.DictLike,
                signature,
                doc,
                reference,
                signature_no_args=signature_no_args
                )

    @classmethod
    def gen_from_display(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:
        if name != 'interface':
            # signature = f'{name}()'
            signature, signature_no_args = _get_signatures(
                    name,
                    obj,
                    is_getitem=False,
                    max_args=max_args,
                    )
            yield cls(cls_name,
                    InterfaceGroup.Display,
                    signature,
                    doc,
                    reference,
                    signature_no_args=signature_no_args
                    )
        else: # interface attr
            yield cls(cls_name,
                    InterfaceGroup.Display,
                    name,
                    doc,
                    use_signature=True,
                    signature_no_args=name
                    )

    @classmethod
    def gen_from_astype(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:
        # InterfaceAsType found on Frame, IndexHierarchy
        if isinstance(obj, InterfaceAsType):
            for field in obj.INTERFACE:

                delegate_obj = getattr(obj, field)
                delegate_reference = f'{obj.__class__.__name__}.{field}'

                if field == Features.GETITEM:
                    # the cls.getitem version returns a FrameAsType
                    signature, signature_no_args = _get_signatures(
                            name,
                            delegate_obj,
                            is_getitem=True,
                            delegate_func=FrameAsType.__call__,
                            max_args=max_args,
                            )
                else:
                    signature, signature_no_args = _get_signatures(
                            name,
                            delegate_obj,
                            is_getitem=False,
                            max_args=max_args,
                            )
                doc = Features.scrub_doc(getattr(InterfaceAsType, field).__doc__)
                yield cls(cls_name,
                        InterfaceGroup.Method,
                        signature,
                        doc,
                        reference,
                        use_signature=True,
                        is_attr=True,
                        delegate_reference=delegate_reference,
                        signature_no_args=signature_no_args
                        )
        else: # Series, Index, astype is just a method
            signature, signature_no_args = _get_signatures(name, obj, max_args=max_args)
            yield cls(cls_name,
                    InterfaceGroup.Method,
                    signature,
                    doc,
                    reference,
                    signature_no_args=signature_no_args
                    )


    @classmethod
    def gen_from_constructor(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:

        signature, signature_no_args = _get_signatures(
                name,
                obj,
                is_getitem=False,
                max_args=max_args,
                )
        yield cls(cls_name,
                InterfaceGroup.Constructor,
                signature,
                doc,
                reference,
                signature_no_args=signature_no_args
                )

    @classmethod
    def gen_from_exporter(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:

        signature, signature_no_args = _get_signatures(
                name,
                obj,
                is_getitem=False,
                max_args=max_args,
                )
        yield cls(cls_name,
                InterfaceGroup.Exporter,
                signature,
                doc,
                reference,
                signature_no_args=signature_no_args
                )

    @classmethod
    def gen_from_iterator(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:

        signature, signature_no_args = _get_signatures(
                name,
                obj.__call__, #type: ignore
                is_getitem=False,
                max_args=max_args,
                )

        yield cls(cls_name,
                InterfaceGroup.Iterator,
                signature,
                doc,
                reference,
                use_signature=True,
                is_attr=True, # doc as attr so sphinx does not add parens to sig
                signature_no_args=signature_no_args,
                )

        for field in IterNodeDelegate.INTERFACE: # apply, map, etc
            delegate_obj = getattr(IterNodeDelegate, field)
            delegate_reference = f'{IterNodeDelegate.__name__}.{field}'
            doc = Features.scrub_doc(delegate_obj.__doc__)

            signature, signature_no_args = _get_signatures(
                    name,
                    obj.__call__, #type: ignore
                    is_getitem=False,
                    delegate_func=delegate_obj,
                    delegate_name=field,
                    max_args=max_args,
                    )
            yield cls(cls_name,
                    InterfaceGroup.Iterator,
                    signature,
                    doc,
                    reference,
                    use_signature=True,
                    is_attr=True,
                    delegate_reference=delegate_reference,
                    signature_no_args=signature_no_args
                    )

    @classmethod
    def gen_from_accessor(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            cls_interface: tp.Type[Interface[TContainer]],
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:

        group = (InterfaceGroup.AccessorString
                if cls_interface is InterfaceString
                else InterfaceGroup.AccessorDatetime)

        for field in cls_interface.INTERFACE: # apply, map, etc
            delegate_obj = getattr(cls_interface, field)
            delegate_reference = f'{cls_interface.__name__}.{field}'
            doc = Features.scrub_doc(delegate_obj.__doc__)

            terminus_name = f'{name}.{field}'

            if isinstance(delegate_obj, property):
                # some date tools are properties
                yield InterfaceRecord(cls_name,
                        group,
                        terminus_name,
                        doc,
                        reference,
                        is_attr=True,
                        use_signature=True,
                        delegate_reference=delegate_reference,
                        delegate_is_attr=True,
                        signature_no_args=terminus_name
                        )
            else:
                signature, signature_no_args = _get_signatures(
                        terminus_name,
                        delegate_obj,
                        max_args=max_args,
                        )
                yield cls(cls_name,
                        group,
                        signature,
                        doc,
                        reference,
                        is_attr=True,
                        use_signature=True,
                        delegate_reference=delegate_reference,
                        signature_no_args=signature_no_args
                        )

    @classmethod
    def from_getitem(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:
        '''
        For root __getitem__ methods, as well as __getitem__ on InterfaceGetItem objects.
        '''
        if name != Features.GETITEM:
            target = obj.__getitem__ #type: ignore
        else:
            target = obj
            name = ''

        signature, signature_no_args = _get_signatures(
                name,
                target,
                is_getitem=True,
                max_args=max_args,
                )

        yield InterfaceRecord(cls_name,
                InterfaceGroup.Selector,
                signature,
                doc,
                reference,
                use_signature=True,
                is_attr=True,
                signature_no_args=signature_no_args
                )


    @classmethod
    def gen_from_selection(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            cls_interface: tp.Type[Interface[TContainer]],
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:

        for field in cls_interface.INTERFACE:
            # get from object, not class
            delegate_obj = getattr(obj, field)
            delegate_reference = f'{cls_interface.__name__}.{field}'
            doc = Features.scrub_doc(delegate_obj.__doc__)

            if field != Features.GETITEM:
                delegate_is_attr = True
                signature, signature_no_args = _get_signatures(
                        f'{name}.{field}', # make compound interface
                        delegate_obj.__getitem__,
                        is_getitem=True,
                        max_args=max_args,
                        )
            else: # is getitem
                delegate_is_attr = False
                signature, signature_no_args = _get_signatures(
                        name, # on the root, no change necessary
                        delegate_obj,
                        is_getitem=True,
                        max_args=max_args,
                        )

            yield InterfaceRecord(cls_name,
                    InterfaceGroup.Selector,
                    signature,
                    doc,
                    reference,
                    use_signature=True,
                    is_attr=True,
                    delegate_reference=delegate_reference,
                    delegate_is_attr=delegate_is_attr,
                    signature_no_args=signature_no_args
                    )


    @classmethod
    def gen_from_assignment(cls, *,
            cls_name: str,
            name: str,
            obj: tp.Union[InterfaceAssignTrio[TContainer],
                    InterfaceAssignQuartet[TContainer]],
            reference: str,
            doc: str,
            cls_interface: tp.Type[Interface[TContainer]],
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:

        for field in cls_interface.INTERFACE:

            # get from object, not class
            delegate_obj = getattr(obj, field)
            delegate_reference = f'{cls_interface.__name__}.{field}'
            delegate_doc = Features.scrub_doc(delegate_obj.__doc__)

            # will be either SeriesAssign or FrameAssign
            terminus_obj = obj.delegate.__call__
            terminus_reference = f'{obj.delegate.__name__}.__call__'
            terminus_doc = Features.scrub_doc(terminus_obj.__doc__)

            # use the delegate to get the root signature, as the root is just a property that returns an InterfaceAssignTrio or similar
            if field != Features.GETITEM:
                delegate_is_attr = True
                signature, signature_no_args = _get_signatures(
                        f'{name}.{field}', # make compound interface
                        delegate_obj.__getitem__,
                        is_getitem=True,
                        delegate_func=terminus_obj,
                        max_args=max_args,
                        )
            else: # is getitem
                delegate_is_attr = False
                signature, signature_no_args = _get_signatures(
                        name, # on the root, no change necessary
                        delegate_obj,
                        is_getitem=True,
                        delegate_func=terminus_obj,
                        max_args=max_args,
                        )

            yield InterfaceRecord(cls_name,
                    InterfaceGroup.Assignment,
                    signature,
                    terminus_doc,
                    reference,
                    use_signature=True,
                    is_attr=False,
                    delegate_reference=terminus_reference,
                    signature_no_args=signature_no_args
                    )

    @classmethod
    def gen_from_method(cls, *,
            cls_name: str,
            name: str,
            obj: AnyCallable,
            reference: str,
            doc: str,
            max_args: int,
            ) -> tp.Iterator['InterfaceRecord']:

        signature, signature_no_args = _get_signatures(name, obj, max_args=max_args)

        if name in _UFUNC_UNARY_OPERATORS:
            yield InterfaceRecord(cls_name,
                    InterfaceGroup.OperatorUnary,
                    signature,
                    doc,
                    reference,
                    signature_no_args=signature_no_args
                    )
        elif name in _UFUNC_BINARY_OPERATORS or name in _RIGHT_OPERATOR_MAP:
            yield InterfaceRecord(cls_name,
                    InterfaceGroup.OperatorBinary,
                    signature,
                    doc,
                    reference,
                    signature_no_args=signature_no_args
                    )
        else:
            yield InterfaceRecord(cls_name,
                    InterfaceGroup.Method,
                    signature,
                    doc,
                    reference,
                    signature_no_args=signature_no_args
                    )


#-------------------------------------------------------------------------------

class InterfaceSummary(Features):

    _CLS_TO_INSTANCE_CACHE: tp.Dict[tp.Type[ContainerBase], ContainerBase] = {}

    @classmethod
    def is_public(cls, field: str) -> bool:
        if field.startswith('_') and not field.startswith('__'):
            return False
        if field in cls.EXCLUDE_PRIVATE:
            return False
        return True


    @classmethod
    def get_instance(cls, target: tp.Type[ContainerBase]) -> ContainerBase:
        '''
        Get a sample instance from any ContainerBase; cache to only create one per life of process.
        '''
        if target not in cls._CLS_TO_INSTANCE_CACHE:
            if target is TypeBlocks:
                instance = target.from_blocks(np.array((0,))) #type: ignore
            elif target is Bus:
                f = Frame.from_elements((0,), name='frame')
                instance = target.from_frames((f,)) #type: ignore
            elif issubclass(target, IndexHierarchy):
                instance = target.from_labels(((0,0),))
            elif issubclass(target, (IndexYearMonth, IndexYear, IndexDate)):
                instance = target(np.array((0,), dtype=DT64_S))
            elif target in (ContainerOperand, ContainerBase, IndexBase):
                instance = target()
            elif issubclass(target, Frame):
                instance = target.from_elements((0,))
            else:
                instance = target((0,)) #type: ignore
            cls._CLS_TO_INSTANCE_CACHE[target] = instance
        return cls._CLS_TO_INSTANCE_CACHE[target]

    @classmethod
    def name_obj_iter(cls,
            target: tp.Type[ContainerBase],
            ) -> tp.Iterator[tp.Tuple[str, tp.Any, tp.Any]]:
        instance = cls.get_instance(target=target)

        for name_attr in dir(target.__class__): # get metaclass
            if name_attr == 'interface':
                # getting interface off of the class will recurse
                yield name_attr, None, ContainerBase.__class__.interface #type: ignore

        # force tehse to be ordered at the bottom
        selectors = ('__getitem__', 'iloc', 'loc')
        selectors_found = set()

        for name_attr in sorted(dir(target)):
            if name_attr == 'interface':
                continue # skip, provided by metaclass
            if not cls.is_public(name_attr):
                continue
            if name_attr in selectors:
                selectors_found.add(name_attr)
                continue
            yield name_attr, getattr(instance, name_attr), getattr(target, name_attr)


        for name_attr in selectors:
            if name_attr in selectors_found:
                yield name_attr, getattr(instance, name_attr), getattr(target, name_attr)


    #---------------------------------------------------------------------------
    @classmethod
    def interrogate(cls,
            target: tp.Type[ContainerBase],
            *,
            max_args: int = MAX_ARGS
            ) -> tp.Iterator[InterfaceRecord]:

        for name_attr, obj, obj_cls in cls.name_obj_iter(target):
            # properties resdie on the class
            doc = ''
            # reference = '' # reference attribute to use

            if isinstance(obj_cls, property):
                doc = cls.scrub_doc(obj_cls.__doc__)
            elif hasattr(obj, '__doc__'):
                doc = cls.scrub_doc(obj.__doc__)

            if hasattr(obj, '__name__'):
                name = obj.__name__
            else: # some attributes yield objects like arrays, Series, or Frame
                name = name_attr

            cls_name = target.__name__
            reference = f'{cls_name}.{name}'

            kwargs = dict(
                    cls_name=cls_name,
                    name=name,
                    obj=obj,
                    reference=reference,
                    doc=doc,
                    max_args=max_args,
                    )

            if name in cls.DICT_LIKE:
                yield from InterfaceRecord.gen_from_dict_like(**kwargs)
            elif name in cls.DISPLAY:
                yield from InterfaceRecord.gen_from_display(**kwargs)
            elif name == 'astype':
                yield from InterfaceRecord.gen_from_astype(**kwargs)
            elif name.startswith('from_') or name == '__init__':
                yield from InterfaceRecord.gen_from_constructor(**kwargs)
            elif name.startswith('to_'):
                yield from InterfaceRecord.gen_from_exporter(**kwargs)
            elif name.startswith('iter_'):
                yield from InterfaceRecord.gen_from_iterator(**kwargs)
            elif isinstance(obj, InterfaceGetItem) or name == cls.GETITEM:
                yield from InterfaceRecord.from_getitem(**kwargs)
            elif isinstance(obj, InterfaceString):
                yield from InterfaceRecord.gen_from_accessor(
                            cls_interface=InterfaceString,
                            **kwargs,
                            )
            elif isinstance(obj, InterfaceDatetime):
                yield from InterfaceRecord.gen_from_accessor(
                            cls_interface=InterfaceDatetime,
                            **kwargs,
                            )
            elif obj.__class__ in (InterfaceSelectDuo, InterfaceSelectTrio):
                yield from InterfaceRecord.gen_from_selection(
                        cls_interface=obj.__class__,
                        **kwargs)
            elif obj.__class__ in (InterfaceAssignTrio, InterfaceAssignQuartet):
                yield from InterfaceRecord.gen_from_assignment(
                        cls_interface=obj.__class__,
                        **kwargs)
            elif callable(obj): # general methods
                yield from InterfaceRecord.gen_from_method(**kwargs)
            else: # attributes
                yield InterfaceRecord(cls_name,
                        InterfaceGroup.Attribute,
                        name,
                        doc,
                        reference,
                        signature_no_args=name
                        )

    @classmethod
    def to_frame(cls,
            target: tp.Type[ContainerBase],
            *,
            minimized: bool = True,
            max_args: int = MAX_ARGS,
            ) -> Frame:
        '''
        Reduce to key fields.
        '''
        f = Frame.from_records(
                cls.interrogate(target, max_args=max_args),
                name=target.__name__
                )
        f = f.sort_values(('cls_name', 'group',))
        f = f.set_index('signature', drop=True)
        if minimized:
            return f[['cls_name', 'group', 'doc']] #type: ignore
        return f #type: ignore


