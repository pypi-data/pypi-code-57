#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2020, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Install some functions for the bokeh theme to make use of.


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
from bokeh.resources import Resources
from bokeh.settings import settings

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'get_sphinx_resources',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

def get_sphinx_resources(include_bokehjs_api=False):
    docs_cdn = settings.docs_cdn()

    # if BOKEH_DOCS_CDN is unset just use default CDN resources
    if docs_cdn is None:
        resources = Resources(mode="cdn")
    else:
        # "BOKEH_DOCS_CDN=local" is used for building and displaying the docs locally
        if docs_cdn == "local":
            resources = Resources(mode="server", root_url="/en/latest/")

        # "BOKEH_DOCS_CDN=test:newthing" is used for building and deploying test docs to
        # a one-off location "en/newthing" on the docs site
        elif docs_cdn.startswith("test:"):
            resources = Resources(
                mode="server", root_url="/en/%s/" % docs_cdn.split(":")[1])

        # Otherwise assume it is a dev/rc/full release version and use CDN for it
        else:
            resources = Resources(mode="cdn", version=docs_cdn)
    if include_bokehjs_api:
        resources.js_components.append("bokeh-api")
    return resources

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
