#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2020, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
'''

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Bokeh imports
from ..core.enums import TextureRepetition
from ..core.has_props import abstract
from ..core.properties import Enum, String
from ..model import Model

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'CanvasTexture',
    'ImageURLTexture',
    'Texture',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

@abstract
class Texture(Model):
    ''' Base class for ``Texture`` models that represent fill patterns.

    '''
    repetition = Enum(TextureRepetition, default="repeat", help="""

    """)

class CanvasTexture(Texture):
    '''

    '''
    code = String(help="""
    A snippet of JavaScript code to execute in the browser.

    """)

class ImageURLTexture(Texture):
    '''

    '''
    url = String(help="""

    """)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
