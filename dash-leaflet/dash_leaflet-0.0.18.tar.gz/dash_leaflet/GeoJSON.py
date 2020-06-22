# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GeoJSON(Component):
    """A GeoJSON component.
LayerGroup is a wrapper of LayerGroup in react-leaflet.
It takes similar properties to its react-leaflet counterpart.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): Attribution
- data (dict; optional): GeoJSON data
- attribution (string; optional): Attribution
- className (string; optional): A custom class name to assign to the image. Empty by default.
- id (string; optional): The ID used to identify this component in Dash callbacks
- style (dict; optional): The CSS style of the component (dynamic)
- defaultOptions (dict; optional): Interactivity to be applied across all features. defaultOptions has the following type: dict containing keys 'hoverStyle', 'zoomToBoundsOnClick', 'popupContent'.
Those keys have the following types:
  - hoverStyle (dict; optional)
  - zoomToBoundsOnClick (boolean; optional)
  - popupContent (string; optional)
- defaultStyle (dict; optional): Style to be applied across all features.
- featureOptions (dict; optional): Interactivity to be applied per feature (an id must be assigned to target a feature). featureOptions has the following type: dict containing keys 'id'.
Those keys have the following types:
  - id (optional)
- featureStyle (dict; optional): Style to be applied per feature (an id must be assigned to target a feature). featureStyle has the following type: dict containing keys 'id'.
Those keys have the following types:
  - id (dict; optional)
- featureId (string; default "id"): Which feature property to be used for matching as the feature id.
- n_clicks (number; default 0): Dash callback property. Number of times the marker has been clicked
- featureClick (dict; optional): Last feature clicked.
- featureHover (dict; optional): Last feature hover."""
    @_explicitize_args
    def __init__(self, children=None, data=Component.UNDEFINED, attribution=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, style=Component.UNDEFINED, defaultOptions=Component.UNDEFINED, defaultStyle=Component.UNDEFINED, featureOptions=Component.UNDEFINED, featureStyle=Component.UNDEFINED, featureId=Component.UNDEFINED, n_clicks=Component.UNDEFINED, featureClick=Component.UNDEFINED, featureHover=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'data', 'attribution', 'className', 'id', 'style', 'defaultOptions', 'defaultStyle', 'featureOptions', 'featureStyle', 'featureId', 'n_clicks', 'featureClick', 'featureHover']
        self._type = 'GeoJSON'
        self._namespace = 'dash_leaflet'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'data', 'attribution', 'className', 'id', 'style', 'defaultOptions', 'defaultStyle', 'featureOptions', 'featureStyle', 'featureId', 'n_clicks', 'featureClick', 'featureHover']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(GeoJSON, self).__init__(children=children, **args)
