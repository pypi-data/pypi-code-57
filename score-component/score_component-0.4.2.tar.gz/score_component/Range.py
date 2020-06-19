# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Range(Component):
    """A Range component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- width (number; default 200)
- height (number; default 100)
- staffY (number; default 30)
- notes (list; optional)
- clefs (list; optional)
- colors (list; default [[]])
- annotations (list; optional)
- draw_lines (boolean; default True)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, staffY=Component.UNDEFINED, notes=Component.UNDEFINED, clefs=Component.UNDEFINED, colors=Component.UNDEFINED, annotations=Component.UNDEFINED, draw_lines=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'width', 'height', 'staffY', 'notes', 'clefs', 'colors', 'annotations', 'draw_lines']
        self._type = 'Range'
        self._namespace = 'score_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'width', 'height', 'staffY', 'notes', 'clefs', 'colors', 'annotations', 'draw_lines']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Range, self).__init__(**args)
