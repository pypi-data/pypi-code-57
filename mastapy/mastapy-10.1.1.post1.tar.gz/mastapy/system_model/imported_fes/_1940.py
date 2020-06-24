'''_1940.py

ImportedFEMultiNodeConnectorLink
'''


from mastapy.system_model.imported_fes import _1941
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_MULTI_NODE_CONNECTOR_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEMultiNodeConnectorLink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEMultiNodeConnectorLink',)


class ImportedFEMultiNodeConnectorLink(_1941.ImportedFEMultiNodeLink):
    '''ImportedFEMultiNodeConnectorLink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_MULTI_NODE_CONNECTOR_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEMultiNodeConnectorLink.TYPE'):
        super().__init__(instance_to_wrap)
