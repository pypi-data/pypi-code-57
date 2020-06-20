# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Pianoroll(Component):
    """A Pianoroll component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- width (number; optional): A label that will be printed when this component is rendered.
- height (number; optional)
- stave_spacing (number; optional)
- scale (number; default 1)
- bar_offset (number; default 0)
- stave_list (list; optional): A Array containing object to hold bars as [[bar1],[bar2] etc..].
Bars containing staves as {clef:'string', name:'string', 'notes':[array or nested array of notenames], colors:[array that matches notes-array]}"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, stave_spacing=Component.UNDEFINED, scale=Component.UNDEFINED, bar_offset=Component.UNDEFINED, stave_list=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'width', 'height', 'stave_spacing', 'scale', 'bar_offset', 'stave_list']
        self._type = 'Pianoroll'
        self._namespace = 'score_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'width', 'height', 'stave_spacing', 'scale', 'bar_offset', 'stave_list']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Pianoroll, self).__init__(**args)
